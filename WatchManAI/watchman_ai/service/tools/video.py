import cv2
import sys
from watchman_ai.service.detection.ssd300 import Detector


class Executor:

    valid_source_types = ['file', 'stream']

    def __init__(self, source, source_type='file', gpu_execution=False):
        # TODO: setup logger
        if source_type not in Executor.valid_source_types:
            # TODO: print some message
            sys.exit(-789)

        # TODO: for now we assume that source type always be a file
        self.capture = cv2.VideoCapture(source)
        if not self.capture.isOpened():
            # TODO: print some message
            sys.exit(-790)

        self.detector = Detector(gpu_execution)

    def run_loop(self):
        while (self.capture.isOpened()):
            ret, frame = self.capture.read()
            # if ret:
                # class_IDs, scores, boundig_boxes = self.detector.get_predictions([frame])
            pass

    def __del__(self):
        self.capture.release()
        cv2.destroyAllWindows()  # TODO: should be removed?
