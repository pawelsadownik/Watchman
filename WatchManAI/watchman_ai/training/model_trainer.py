import argparse
import json
import os
from watchman_ai.training.models.ssd300.trainer import SSD300Trainer
from watchman_ai.training.models.yolov3.trainer import YoloV3Trainer


WATCHMAN_AI_ROOT_PATH = os.environ.get('WATCHMAN_AI_ROOT_PATH', '~/watchman/WatchManAI')


class Consts:
    def __init__(self, **kwargs):
        for key, val in kwargs:
            setattr(self, key, val)


def parse_args():
    parser = argparse.ArgumentParser(description='DL training program.')

    parser.add_argument('--model', type='str', required=True, dest='MODEL',
                        help='Model to execute, one of: [ssd300, yolov3]')
    parser.add_argument('--resume_training', action='store_true', dest='RESUME_TRAINING',
                        help='Whether to start training for checkpoint or not.')
    parser.add_argument('--params_path', type=str, default='', dest='PARAMS_PATH',
                        help='Path where checkpoint is stored.')
    parser.add_argument('--start_epoch', type=int, default=0, dest='START_EPOCH',
                        help='Epoch after which checkpoint was stored.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    model = args.MODEL
    model_param_f_name = f'{model}_params.json'
    model_param_f_path = os.path.join(WATCHMAN_AI_ROOT_PATH,
                                      'watchman_ai', 'training', 'resources',
                                      model_param_f_name)

    with open(model_param_f_path, 'r') as json_file:
        params = json.load(json_file)
    consts = Consts(**params)

    if model == 'ssd300':
        trainer = SSD300Trainer(consts)
    else:
        trainer = YoloV3Trainer(consts)
    trainer.train()
