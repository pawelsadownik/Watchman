import mxnet as mx
from mxnet import autograd, gluon, nd
from gluoncv.data import COCODetection
from gluoncv.data.batchify import Tuple, Stack, Pad
from gluoncv.data.transforms.presets.ssd import SSDDefaultTrainTransform, SSDDefaultValTransform


def get_coco_data_holders(consts):
    train_data = _get_coco_train_data(consts)
    val_data = _get_coco_val_data(consts)

    return train_data, val_data


def _get_coco_train_data(consts):
    train_data = COCODetection(root=consts.DATA_PATH, splits=consts.TRAIN_DATA_NAME)

    return train_data


def _get_coco_val_data(consts):
    val_data = COCODetection(root=consts.DATA_PATH, splits=consts.VAL_DATA_NAME, skip_empty=False)

    return val_data


def get_coco_data_loaders(net, train_data, val_data, consts, ctx):
    in_size = consts.IN_SIZE
    bs = consts.BATCH_SIZE
    n_workers = consts.NUM_WORKERS

    with autograd.train_mode():
        fake_in_size = 1
        channels = 3
        _, _, anchors = net(nd.zeros((fake_in_size, channels, in_size, in_size), ctx))
    anchors = anchors.as_in_context(mx.cpu())

    img_train_s = Stack()
    class_targets = Stack()
    box_targets = Stack()
    train_batchify_fn = Tuple(img_train_s, class_targets, box_targets)
    train_data_transformed = train_data.transform(SSDDefaultTrainTransform(in_size, in_size, anchors))
    train_data_loader = gluon.data.DataLoader(train_data_transformed,
                                              batch_size=bs,
                                              shuffle=True,
                                              batchify_fn=train_batchify_fn,
                                              last_batch='rollover',
                                              num_workers=n_workers)

    img_val_s = Stack()
    padding = Pad(pad_val=-1)
    val_batchify_fn = Tuple(img_val_s, padding)
    val_data_transformed = val_data.transform(SSDDefaultValTransform(in_size, in_size))
    val_data_loader = gluon.data.DataLoader(val_data_transformed,
                                            batch_size=bs,
                                            shuffle=False,
                                            batchify_fn=val_batchify_fn,
                                            last_batch='keep',
                                            num_workers=n_workers)

    return train_data_loader, val_data_loader
