import cv2
from PIL import Image
from watchman_ai.stream.connection.broadcast import Broadcaster


class Video:
    """
    Represents video source (ip camera, local camera or video file) and provides
    function which allows to gather consecutive video frames.
    """
    def __init__(self, source, fps_limit, cmp_server_addr):
        """
        Creates Video handle, based on video source.

        :param source: id for video source, could be ip address, local camera id or video file name
        :param fps_limit: maximum number of frames per second which should be processed
        :param cmp_server_addr: ip address of server on which frames will be processed

        :type source: str
        :type fps_limit: int
        :type cmp_server_addr: str
        """
        self.source = source
        self.fps_limit = fps_limit  # TODO: should be removed? already used in Streamer
        self.capture = cv2.VideoCapture(self.source)
        self.broadcaster = Broadcaster(cmp_server_addr)

    def get_frame_info(self):
        """
        Returns image, information whether alarm occurs and alarm type.
        Optionally (alarm occurs), draws bounding boxes on image.

        :return: processed image (with bounding boxes if alarm occurs), information whether alarm occurs and alarm type
                 (alarm type is empty if alarm doesn't occur)
        :rtype: tuple(PIL.Image, bool, str)
        """
        ret, img = self.capture.read()
        if ret:
            # bboxes, flag = self.broadcaster.classify_img(img)  # Uncomment this line if you want to test broadcaster
            # if flag:
            #     self._draw_bounding_boxes(img, bboxes, flag)
            img = Image.fromarray(img)
        else:
            img = None  # TODO: change to exception
        return img, False, ''  # TODO: return real flag and error

    def _draw_bounding_boxes(self, img, bboxes, flag):
        for bbox in bboxes:
            x1, y1, x2, y2 = bbox
            cv2.rectangle(img, (x1, y1), (x2, y2), color=flag, thickness=2)

    def __del__(self):
        self.capture.release()
