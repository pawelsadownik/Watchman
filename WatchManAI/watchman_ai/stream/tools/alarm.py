import requests


def raise_alarm(end_point, cam_info, flag, timestamp):
    data = {
        'flag': flag,
        'Timestamp': timestamp,
        'CameraInfo': cam_info
    }
    answer = requests.post(url=end_point, json=data)
    if answer.status_code != requests.codes.ok:
        print('Something went wrong - alarm was not raised.')