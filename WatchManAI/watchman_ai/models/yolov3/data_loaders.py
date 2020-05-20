from mxnet import gluon
from gluoncv.data import COCODetection
from gluoncv.data.batchify import Tuple, Stack, Pad
from gluoncv.data.transforms.presets.yolo import YOLO3DefaultTrainTransform, YOLO3DefaultValTransform


def get_coco_data_holders(consts):
    train_data = _get_coco_train_data(consts)
    val_data = _get_coco_val_data(consts)
    consts.NUM_SAMPLES = len(train_data)
    return train_data, val_data


def _get_coco_train_data(consts):
    train_data = COCODetection(root=consts.DATA_PATH, splits=consts.TRAIN_DATA_NAME, use_crowd=False)
    return train_data


def _get_coco_val_data(consts):
    val_data = COCODetection(root=consts.DATA_PATH, splits=consts.VAL_DATA_NAME, skip_empty=False)
    return val_data


def get_coco_data_loaders(net, train_data, val_data, in_size, bs, n_workers):
    train_batchify_fn = Tuple(*([Stack() for _ in range(6)] + [Pad(pad_val=-1) for _ in range(1)]))
    train_data_transformed = train_data.transform(YOLO3DefaultTrainTransform(in_size, in_size, net, mixup=False))
    train_data_loader = gluon.data.DataLoader(train_data_transformed,
                                              batch_size=bs,
                                              shuffle=True,
                                              batchify_fn=train_batchify_fn,
                                              last_batch='rollover',
                                              num_workers=n_workers)

    val_batchify_fn = Tuple(Stack(), Pad(pad_val=-1))
    val_data_transformed = val_data.transform(YOLO3DefaultValTransform(in_size, in_size))
    val_data_loader = gluon.data.DataLoader(val_data_transformed,
                                            batch_size=bs,
                                            shuffle=False,
                                            batchify_fn=val_batchify_fn,
                                            last_batch='keep',
                                            num_workers=n_workers)

    return train_data_loader, val_data_loader