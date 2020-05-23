import mxnet as mx
from mxnet.gluon import utils
from gluoncv.utils.metrics.coco_detection import COCODetectionMetric


def get_coco_validation_metric(val_data, consts):
    val_metric = COCODetectionMetric(val_data,
                                     consts.VAL_METRIC_F_NAME,
                                     cleanup=True,
                                     data_shape=(consts.IN_SIZE, consts.IN_SIZE))
    return val_metric


def validate_topology_coco(net, val_data_loader, ctx, eval_metric):
    eval_metric.reset()
    net.set_nms(nms_thresh=0.45, nms_topk=400)
    mx.nd.waitall()
    net.hybrydize()

    for batch in val_data_loader:
        data = utils.split_and_load(batch[0], ctx_list=ctx, even_split=False)
        label = utils.split_and_load(batch[1], ctx_list=ctx, even_split=False)

        det_bboxes, det_ids, det_scores = [], [], []
        gt_bboxes, gt_ids, gt_difficults = [], [], []

        for x, y in zip(data, label):
            ids, scores, bboxes = net(x)
            det_ids.append(ids)
            det_scores.append(scores)
            det_bboxes.append(bboxes.clip(0, batch[0].shape[2]))
            gt_ids.append(y.slice_axis(axis=-1, begin=4, end=5))
            gt_bboxes.append(y.slice_axis(axis=-1, begin=0, end=4))
            gt_difficults.append(y.slice_axis(axis=-1, begin=5, end=6) if y.shape[-1] > 5 else None)

        eval_metric.update(det_bboxes, det_ids, det_scores, gt_bboxes, gt_ids, gt_difficults)

    return eval_metric.get()
