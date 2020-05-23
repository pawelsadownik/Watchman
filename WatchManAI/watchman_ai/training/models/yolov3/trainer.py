import warnings
import mxnet as mx
import gluoncv.utils as gutils
from gluoncv.model_zoo import yolo3_darknet53_coco
from watchman_ai.training.models.common import _serializers, _validators
from watchman_ai.training.models.yolov3 import _trainers, _data_loaders
from watchman_ai.training.tools import logger


class YoloV3Trainer:

    def __init__(self, consts):
        gutils.random.seed(consts.SEED)
        # distributed training is not supported - we can only use GPU with id=0
        self.ctx = [mx.gpu(0)] if consts.USE_GPU else [mx.cpu()]
        self.net = yolo3_darknet53_coco(pretrained_base=True)
        self.async_net = self.net

        if consts.RESUME_TRAINING:
            _serializers.load_params(self.net, self.async_net, consts.PARAMS_PATH)
        else:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')
                self.net.initialize()
                self.async_net.initialize()

        train_data, val_data = _data_loaders.get_coco_data_holders(consts)
        self.num_samples = len(train_data)
        self.train_data_loader, self.val_data_loader = _data_loaders.get_coco_data_loaders(self.async_net,
                                                                                           train_data,
                                                                                           val_data,
                                                                                           consts)
        self.eval_metric = _validators.get_coco_validation_metric(val_data, consts)
        self.logger = logger.get_logger(consts.LOG_F_NAME)
        self.consts = consts

    def train(self):
        _trainers.train(self.net,
                        self.train_data_loader,
                        self.val_data_loader,
                        self.eval_metric,
                        self.ctx,
                        self.num_samples,
                        self.consts,
                        self.logger)