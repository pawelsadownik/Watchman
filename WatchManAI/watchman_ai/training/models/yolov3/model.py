import warnings
import mxnet as mx
import gluoncv.utils as gutils
from gluoncv.model_zoo import yolo3_darknet53_coco
from watchman_ai.training.models.common import serializers, validators
from watchman_ai.training.models.yolov3 import trainers, data_loaders
from watchman_ai.training.tools import logger


class YOLOv3Trainer:
    """
    Builds YOLOv3 topology (parametrized with consts) using GluonCV and MXNet.
    Pre-processes COCO dataset to make it suitable for feeding the network.
    Provides method to run training.

    .. note: model has pre-trained base (DarkNet-53)
    .. seealso: https://arxiv.org/abs/1506.02640
    """

    def __init__(self, consts):
        """
        Creates YoloV3 topology instance for chosen device, loads weights (conditionally),
        prepares validator and data loader, set ups logger.

        :param consts: object with model parameters as it's attributes
        :type consts: Consts

        .. note: resources directory provides json like configuration
        """
        gutils.random.seed(consts.SEED)
        # distributed training is not supported - we can only use GPU with id=0
        self.ctx = [mx.gpu(0)] if consts.USE_GPU else [mx.cpu()]
        self.net = yolo3_darknet53_coco(pretrained_base=True)
        self.async_net = self.net  # asynchronous net is used for data loading

        if consts.RESUME_TRAINING:
            serializers.load_params(self.net, self.async_net, consts.PARAMS_PATH)
        else:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')
                self.net.initialize()
                self.async_net.initialize()

        train_data, val_data = data_loaders.get_coco_data_holders(consts)
        self.num_samples = len(train_data)
        self.train_data_loader, self.val_data_loader = data_loaders.get_coco_data_loaders(self.async_net,
                                                                                          train_data,
                                                                                          val_data,
                                                                                          consts)
        self.eval_metric = validators.get_coco_validation_metric(val_data, consts)
        self.logger = logger.get_logger(consts.LOG_F_NAME)
        self.consts = consts

    def train(self):
        """
        Runs YOLOv3 training.

        .. note: finishes after requested number of epochs (provided in consts.EPOCHS)
        """
        trainers.train(self.net,
                       self.train_data_loader,
                       self.val_data_loader,
                       self.eval_metric,
                       self.ctx,
                       self.num_samples,
                       self.consts,
                       self.logger)