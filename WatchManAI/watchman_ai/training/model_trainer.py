import argparse
import json
import os
import sys


"""
Runs requested model training.

:Example:
train SSD300 from scratch:
    python3 model_trainer.py --model=ssd300
train YOLOv3 from checkpoint:
    python3 model_trainer.py --model=yolov3 --resume_training
    --params_path='./path/to/param/weights.ckpt' --start_epoch=20'
"""


WATCHMAN_AI_ROOT_PATH = os.environ.get('WATCHMAN_AI_ROOT_PATH', '~/watchman/WatchManAI')
if not os.path.exists(WATCHMAN_AI_ROOT_PATH):
    print('You need to set up correct WATCHMAN_AI_ROOT_PATH!', file=sys.stderr)
    sys.exit(-999)
sys.path.insert(0, WATCHMAN_AI_ROOT_PATH)


class Consts:
    """
    Represents model parameters.
    """
    def __init__(self, named_args):
        for key, val in named_args.items():
            setattr(self, key, val)

    def __str__(self):
        attrs = vars(self)
        return '\n'.join([f'{key} = {val}' for key, val in attrs.items()])


def parse_args():
    parser = argparse.ArgumentParser(description='DL training program.')

    parser.add_argument('--model', type=str, required=True, dest='MODEL',
                        help='Model to execute, one of: [ssd300, yolov3].')
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
    consts = Consts(params)

    if model == 'ssd300':
        from watchman_ai.training.models.ssd300.model import SSD300Trainer
        trainer = SSD300Trainer(consts)
    else:
        from watchman_ai.training.models.yolov3.model import YOLOv3Trainer
        trainer = YOLOv3Trainer(consts)
    trainer.train()
