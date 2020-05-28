import argparse
import os
import sys
from watchman_ai.stream.connection.stream import Streamer


WATCHMAN_AI_ROOT_PATH = os.environ.get('WATCHMAN_AI_ROOT_PATH', '~/watchman/WatchManAI')
if not os.path.exists(WATCHMAN_AI_ROOT_PATH):
    print('You need to set up correct WATCHMAN_AI_ROOT_PATH!', file=sys.stderr)
    sys.exit(-999)
sys.path.insert(0, WATCHMAN_AI_ROOT_PATH)


def parse_args():
    parser = argparse.ArgumentParser(description='Processed video streamer program.')

    parser.add_argument('--video_source', type=str, required=True, dest='SOURCE',
                        help='Source of the video to be processed. Could be one of [file, ip camera].')
    parser.add_argument('--notification_addr', type=str, required=True, dest='NOTIF_ADDR',
                        help='End point on which alarm should be sent.')
    parser.add_argument('--info', type=str, dest='INFO', required=True,
                        help='Information about video source info. For camera it could be location.')
    parser.add_argument('--cmp_server_addr', type=str, default='', dest='SERVER_ADDR',
                        help='Address to computation server.')  # TODO: add default server address
    parser.add_argument('--local_camera', action='store_true', dest='LOCAL_CAMERA',
                        help='Whether source came from local camera or not.')
    parser.add_argument('--fps_limit', type=int, default=10, dest='FPS_LIMIT',
                        help='Maximum number of processed frames per second.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    source = int(args.SOURCE) if args.LOCAL_CAMERA else args.SOURCE
    stream = Streamer(source, args.INFO, args.NOTIF_ADDR, args.FPS_LIMIT, args.SERVER_ADDR)
    stream.run()  # TODO: find way to graceful server kill
