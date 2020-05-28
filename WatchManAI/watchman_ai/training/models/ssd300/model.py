import warnings
import mxnet as mx
import gluoncv.utils as gutils
from mxnet.gluon.nn import BatchNorm
from gluoncv.model_zoo import ssd_300_vgg16_atrous_coco
from watchman_ai.training.models.common import serializers, validators
from watchman_ai.training.models.ssd300 import data_loaders, trainers
from watchman_ai.training.tools import logger


class SSD300Trainer:
    """
    Builds SSD300 topology (parametrized with consts) using GluonCV and MXNet.
    Pre-processes COCO dataset to make it suitable for feeding the network.
    Provides method to run training.

    .. note: model has pre-trained base (VGG-16)
    .. seealso: https://arxiv.org/abs/1512.02325
    """

    def __init__(self, consts):
        """
        Creates SSD300 topology instance for chosen device, loads weights (conditionally),
        prepares validator and data loader, set ups logger.

        :param consts: object with model parameters as it's attributes
        :type consts: Consts

        .. note: resources directory provides json like configuration
        """
        gutils.random.seed(consts.SEED)
        # distributed training is not supported - we can only use GPU with id=0
        self.ctx = [mx.gpu(0)] if consts.USE_GPU else [mx.cpu()]
        self.net = ssd_300_vgg16_atrous_coco(pretrained_base=True, norm_layer=BatchNorm)
        self.async_net = self.net  # asynchronous net is used for data loading

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
                                                                                          consts,
                                                                                          self.ctx[0])
        self.eval_metric = validators.get_coco_validation_metric(val_data, consts)
        self.logger = logger.get_logger(consts.LOG_F_NAME)
        self.consts = consts

    def train(self):
        """
        Runs SSD300 training.

        .. note: finishes after requested number of epochs (provided in consts.EPOCHS)
        """
        trainers.train_ssd300_coco(self.net,
                                   self.train_data_loader,
                                   self.val_data_loader,
                                   self.eval_metric,
                                   self.ctx,
                                   self.consts,
                                   self.logger)