import time
import mxnet as mx
from mxnet import autograd
from mxnet.gluon import Trainer, utils
from gluoncv.loss import SSDMultiBoxLoss
from watchman_ai.models.common import validators, serializers


def train_ssd300_coco(net, train_data_loader, val_data_loader, eval_metric, ctx, consts, logger):
    net.collect_params().reset_ctx(ctx)
    net_optimizer = Trainer(net.collect_params(),
                            optimizer='sgd',
                            optimizer_params={
                                'learning_rate': consts.LR,
                                'wd': consts.WD,
                                'momentum': consts.MOMENTUM
                            })

    lr_decay = float(consts.LR_DECAY)
    lr_steps = sorted([float(ls) for ls in consts.LR_DECAY_EPOCH if ls.strip()])

    mbox_loss = SSDMultiBoxLoss()
    ce_metric = mx.metric.Loss('CrossEntropy')
    smoothl1_metric = mx.metric.Loss('SmoothL1')

    best_mean_avg_prec = [0]
    logger.info(consts)
    logger.info(f'Starting from [Epoch {consts.START_EPOCH}]')

    for epoch in range(consts.START_EPOCH, consts.EPOCHS):
        while lr_steps and epoch >= lr_steps[0]:
            new_lr = net_optimizer.learning_rate * lr_decay
            lr_steps.pop(0)
            net_optimizer.set_learning_rate(new_lr)
            logger.info(f'[Epoch {epoch}] learning rate = {new_lr}')
        ce_metric.reset()
        smoothl1_metric.reset()
        epoch_tic = time.time()
        batch_tic = time.time()
        net.hybridize(static_alloc=True, static_shape=True)

        for i, batch in enumerate(train_data_loader):
            data = utils.split_and_load(batch[0], ctx_list=ctx)
            cls_targets = utils.split_and_load(batch[1], ctx_list=ctx)
            box_targets = utils.split_and_load(batch[2], ctx_list=ctx)

            with autograd.record():
                cls_predictions = []
                box_predictions = []

                for x in data:
                    cls_prediction, box_prediction, _ = net(x)
                    cls_predictions.append(cls_prediction)
                    box_predictions.append(box_prediction)

                sum_loss, cls_loss, box_loss = mbox_loss(cls_predictions, box_predictions, cls_targets, box_targets)
                autograd.backward(sum_loss)

            net_optimizer.step(1)

            ce_metric.update(0, [l * consts.BATCH_SIZE for l in cls_loss])
            smoothl1_metric.update(0, [l * consts.BATCH_SIZE for l in box_loss])

            if not (i + 1) % consts.LOG_INTERVAL:
                ce_name, ce_loss = ce_metric.get()
                sl1_name, sl1_loss = smoothl1_metric.get()
                t_now = time.time()
                speed = consts.BATCH_SIZE / (t_now - batch_tic)
                logger.info(f'[Epoch {epoch}][Batch {i}], Speed: {speed:.3f} samples/sec, '
                            f'{ce_name}={ce_loss:.3f}, {sl1_name}={sl1_loss:.3f}')

            batch_tic = time.time()

        ce_name, ce_loss = ce_metric.get()
        sl1_name, sl1_loss = smoothl1_metric.get()
        epoch_time = time.time() - epoch_tic
        logger.info(f'[Epoch {epoch}], epoch time: {epoch_time:.3f},'
                    f'{ce_name}={ce_loss:.3f}, {sl1_name}={sl1_loss:.3f}')

        if not epoch % consts.VAL_INTERVAL or not epoch % consts.SAVE_INTERVAL:
            mean_avg_prec_name, mean_avg_prec = validators.validate_topology_coco(net, val_data_loader, ctx, eval_metric)
            val_msg = '\n'.join([f'{k}={v}' for k, v in zip(mean_avg_prec_name, mean_avg_prec)])
            logger.info(f'[Epoch {epoch}] validation: \n{val_msg}')
            curr_mean_avg_prec = float(mean_avg_prec[-1])
        else:
            curr_mean_avg_prec = 0

        serializers.save_params(net, best_mean_avg_prec, curr_mean_avg_prec, epoch, consts.SAVE_INTERVAL, consts.SAVE_PREFIX)
