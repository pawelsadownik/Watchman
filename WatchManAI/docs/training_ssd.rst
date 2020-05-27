.. code-block:: python
    :number-lines:

    class SSD300Trainer(consts):
        Builds SSD300 topology (parametrized with consts) using GluonCV and MXNet.
        Pre-processes COCO dataset to make it suitable for feeding the network.
        Provides method to run training.

        Arguments:
            consts: Consts class instance with model parameters.
                Example attributes: consts.BATCH_SIZE, consts.LR_DECAY_EPOCH

        train(self):
            Runs SSD300 training.
