import cv2
from PIL import Image
from watchman_ai.stream.connection.broadcast import Broadcaster


class Video:

    def __init__(self, source, fps_limit, cmp_server_addr):
        self.source = source
        self.fps_limit = fps_limit
        self.capture = cv2.VideoCapture(self.source)
        self.broadcaster = Broadcaster(cmp_server_addr)

    def get_frame_info(self):
        ret, img = self.capture.read()
        if ret:
            # classification = self.broadcaster.classify_img(img)  # Uncomment this line if you want to test broadcaster
            img = Image.fromarray(img)
        else:
            img = None  # TODO: change to exception
        return img, ''  # TODO: return real flag

    def __del__(self):
        self.capture.release()
