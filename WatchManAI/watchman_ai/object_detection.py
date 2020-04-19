import argparse
from watchman_ai.models.ssd300.build_ssd300 import SSD300Builder


def parse_args():
    # TODO: Handle inference arguments
    parser = argparse.ArgumentParser(description='DL training arguments.')

    # TODO: add help messages for all arguments
    parser.add_argument('--model_name', type=str, required=True, dest='MODEL_NAME')
    parser.add_argument('--dataset_name', type=str, default='coco', dest='DATASET_NAME')
    parser.add_argument('--save_interval', type=int, default=10, dest='SAVE_INTERVAL')  # epoch interval
    parser.add_argument('--val_interval', type=int, default=4, dest='VAL_INTERVAL')  # epoch interval
    parser.add_argument('--log_interval', type=int, default=100, dest='LOG_INTERVAL')  # batch interval
    parser.add_argument('--epochs', type=int, default=200, dest='EPOCHS')
    parser.add_argument('--start_epoch', type=int, default=0, dest='START_EPOCH')
    parser.add_argument('--momentum', type=float, default=0.9, dest='MOMENTUM')
    parser.add_argument('--wd', type=float, default=0.0005, dest='WD')
    parser.add_argument('--lr', type=float, default=0.001, dest='LR')
    parser.add_argument('--lr_decay', type=float, default=0.1, dest='LR_DECAY')
    parser.add_argument('--lr_decay_epoch', type=str, default='120,160', dest='LR_DECAY_EPOCH')
    parser.add_argument('--data_path', type=str, default='~/.mxnet/datasets/', dest='DATA_PATH')
    parser.add_argument('--num_workers', type=int, default=4, dest='NUM_WORKERS')
    parser.add_argument('--batch_size', type=int, default=32, dest='BATCH_SIZE')
    parser.add_argument('--in_size', type=int, default=300, dest='IN_SIZE')
    parser.add_argument('--params_path', type=str, default='', dest='PARAMS_PATH')
    parser.add_argument('--resume_training', action='store_true', dest='RESUME_TRAINING')
    parser.add_argument('--classes', type=str, default='person,suitcase,handbag', dest='CLASSES')
    parser.add_argument('--use_gpu', action='store_true', dest='USE_GPU')
    parser.add_argument('--seed', type=int, default=233, dest='SEED')

    return parser.parse_args()

if __name__ == '__main__':
    # TODO: add validation for supported model_name's
    consts = parse_args()
    consts.SAVE_PREFIX = f'{consts.MODEL_NAME}'
    consts.VAL_METRIC_F_NAME = f'{consts.MODEL_NAME}_eval'
    consts.DATA_PATH += f'{consts.DATASET_NAME}/'
    consts.LOG_F_PATH = f'{consts.MODEL_NAME}_train.log'
    if consts.DATASET_NAME == 'coco':
        consts.TRAIN_DATA_NAME = 'instances_train2017'
        consts.VAL_DATA_NAME = 'instances_val2017'
    consts.CLASSES = consts.CLASSES.split(',')
    consts.LR_DECAY_EPOCH = consts.LR_DECAY_EPOCH.split(',')
    print(consts)

	ssd300 = SSD300Builder(consts)
	ssd300.train()

