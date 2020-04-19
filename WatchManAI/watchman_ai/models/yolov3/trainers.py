import time
import mxnet as mx
from mxnet import gluon, autograd
from gluoncv.utils import LRScheduler, LRSequential
from watchman_ai.models.yolov3.validators import validate_yolov3_coco
from watchman_ai.models.yolov3.serializers import save_params


def train(net, train_data_loader, val_data_loader, eval_metric, ctx, consts, logger):
    net.collect_params().reset_ctx(ctx)
    warmup_epoch = 0
    lr_decay_epoch = [int(i) for i in consts.LR_DECAY_EPOCH]
    lr_decay_epoch = [e - warmup_epoch for e in lr_decay_epoch]
    n_batches = consts.NUM_SAMPLES // consts.BATCH_SIZE
    lr_scheduler = LRSequential([LRScheduler('linear', base_lr=0, target_lr=consts.LR,
                                             nepochs=1, iters_per_epoch=n_batches),
                                 LRScheduler(consts.LR_MODE, base_lr=consts.LR, nepochs=consts.EPOCHS - warmup_epoch,
                                             iters_per_epoch=n_batches, step_epoch=lr_decay_epoch,
                                             step_factor=consts.LR_DECAY, power=2),])
    params = {'wd': consts.WD, 'momentum': consts.MOMENTUM, 'lr_scheduler': lr_scheduler}
    net_optimizer = gluon.Trainer(net.collect_params(), 'sgd', params, kvstore='local', update_on_kvstore=None)

    sigmoid_ce = gluon.loss.SigmoidBinaryCrossEntropyLoss(from_sigmoid=False)
    l1_loss = gluon.loss.L1Loss()

    obj_metrics = mx.metric.Loss('ObjLoss')
    center_metrics = mx.metric.Loss('BoxCenterLoss')
    scale_metrics = mx.metric.Loss('BoxScaleLoss')
    cls_metrics = mx.metric.Loss('ClassLoss')

    logger.info(consts)
    logger.info(f'Start training from [Epoch {consts.START_EPOCH}]')
    best_mean_avg_prec = [0]

    for epoch in range(consts.START_EPOCH, consts.EPOCHS):
        tic = time.time()
        btic = time.time()
        mx.nd.waitall()
        net.hybridize()

        for i, batch in enumerate(train_data_loader):
            data = gluon.utils.split_and_load(batch[0], ctx_list=ctx)
            fixed_targets = [gluon.utils.split_and_load(batch[it], ctx_list=ctx, batch_axis=0) for it in range(1, 6)]
            gt_boxes = gluon.utils.split_and_load(batch[6], ctx_list=ctx, batch_axis=0)
            sum_losses, obj_losses, center_losses, scale_losses, cls_losses = [], [], [], [], []

            with autograd.record():
                for ix, x in enumerate(data):
                    obj_loss, center_loss, scale_loss, cls_loss = net(x, gt_boxes[ix],
                                                                      *[ft[ix] for ft in fixed_targets])
                    sum_losses.append(obj_loss + center_loss + scale_loss + cls_loss)
                    obj_losses.append(obj_loss)
                    center_losses.append(center_loss)
                    scale_losses.append(scale_loss)
                    cls_losses.append(cls_loss)

                    autograd.backward(sum_losses)

            net_optimizer.step(consts.BATCH_SIZE)

            obj_metrics.update(0, obj_losses)
            center_metrics.update(0, center_losses)
            scale_metrics.update(0, scale_losses)
            cls_metrics.update(0, cls_losses)

            if not (i + 1) % consts.LOG_INTERVAL:
                obj_name, obj_loss = obj_metrics.get()
                center_name, center_loss = center_metrics.get()
                scale_name, scale_loss = scale_metrics.get()
                cls_name, cls_loss = cls_metrics.get()
                t_now = time.time()
                speed = consts.BATCH_SIZE / (t_now - btic)
                logger.info(f'[Epoch {epoch}][Batch {i}], Speed: {speed:.3f} samples/sec, '
                            f'{obj_name}={obj_loss:.3f}, {center_name}={center_loss:.3f}, '
                            f'{scale_name}={scale_loss}, {cls_name}={cls_loss}')

            btic = time.time()

        obj_name, obj_loss = obj_metrics.get()
        center_name, center_loss = center_metrics.get()
        scale_name, scale_loss = scale_metrics.get()
        cls_name, cls_loss = cls_metrics.get()
        epoch_time = time.time() - tic
        logger.info(f'[Epoch {epoch}], epoch time: {epoch_time:.3f}, '
                    f'{obj_name}={obj_loss:.3f}, {center_name}={center_loss:.3f}, '
                    f'{scale_name}={scale_loss}, {cls_name}={cls_loss}')

        if not epoch % consts.VAL_INTERVAL or not epoch % consts.SAVE_INTERVAL:
            mean_avg_prec_name, mean_avg_prec = validate_yolov3_coco(net, val_data_loader, ctx, eval_metric)
            val_msg = '\n'.join([f'{k}={v}' for k, v in zip(mean_avg_prec_name, mean_avg_prec)])
            logger.info(f'[Epoch {epoch}] validation: \n{val_msg}')
            curr_mean_avg_prec = float(mean_avg_prec[-1])
        else:
            curr_mean_avg_prec = 0

        save_params(net, best_mean_avg_prec, curr_mean_avg_prec, epoch, consts.SAVE_INTERVAL, consts.SAVE_PREFIX)
