import warnings
import mxnet as mx
import gluoncv.utils as gutils
from mxnet.gluon.nn import BatchNorm
from gluoncv.model_zoo import yolo3_darknet53_coco
from watchman_ai.models.common import serializers
from watchman_ai.models.yolov3 import data_loaders, trainers
from watchman_ai.models.common import validators
from watchman_ai.tools.logger import get_logger


class YoloV3Builder:

    supported_datasets = ['coco']

    def __init__(self, consts):
        dataset_name_cleaned = consts.DATASET_NAME.strip().lower()
        if dataset_name_cleaned not in YoloV3Builder.supported_datasets:
            pass  # TODO: prepare custom exception to raise

        gutils.random.seed(consts.SEED)
        # distributed training is not supported - we can only use GPU with id=0
        self.ctx = [mx.gpu(0)] if consts.USE_GPU else [mx.cpu()]
        self.net = yolo3_darknet53_coco(pretrained_base=True)
        self.async_net = self.net

        if consts.RESUME_TRAINING:
            serializers.load_params(self.net, self.async_net, consts.PARAMS_PATH)
        else:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')
                self.net.initialize()
                self.async_net.initialize()

        train_data, val_data = data_loaders.get_coco_data_holders(consts)
        self.train_data_loader, self.val_data_loader = data_loaders.get_coco_data_loaders(self.async_net,
                                                                                          train_data,
                                                                                          val_data,
                                                                                          consts.IN_SIZE,
                                                                                          consts.BATCH_SIZE,
                                                                                          consts.NUM_WORKERS)
        self.eval_metric = validators.get_coco_validation_metric(val_data, consts)
        self.logger = get_logger(consts)
        self.consts = consts

    def train(self):
        trainers.train(self.net,
                       self.train_data_loader,
                       self.val_data_loader,
                       self.eval_metric,
                       self.ctx,
                       self.consts,
                       self.logger)