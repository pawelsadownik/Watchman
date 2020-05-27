import cv2
import mxnet as mx
import numpy as np
from gluoncv.model_zoo import ssd_300_vgg16_atrous_coco


class Detector:

    def __init__(self, gpu_execution=False):
        self._ctx = mx.gpu(0) if gpu_execution else mx.cpu()
        self._net = ssd_300_vgg16_atrous_coco(pretrained=True, ctx=self._ctx)
        self._person_id, self._suitcase_id = self._get_class_filters()

    def get_predictions(self, frames, threshold=0.65):
        # TODO: for now we assume that frames is one-element list
        frame = frames[0]
        tensor, frame = self._transform_frame(frame)
        class_IDs, scores, bounding_boxes = self._net(tensor)
        return self._clean_predictions(class_IDs, scores, bounding_boxes, threshold)

    def _get_class_filters(self):
        person_id = self._net.classes.index('person')
        suitcase_id = self._net.classes.index('suitcase')
        return person_id, suitcase_id

    def _transform_frame(self,
                         frame,
                         short_side=300,
                         mean=(0.485, 0.456, 0.406),
                         std=(0.229, 0.224, 0.225)):
        x, y, _ = frame.shape
        min_ = min(x, y)
        if min_ > short_side:
            factor = min_ / short_side
            new_x = int(x / factor)
            new_y = int(y / factor)
            frame = cv2.resize(frame, dsize=(new_x, new_y))
        tensor = mx.nd.array(frame, ctx=self._ctx)
        tensor = mx.nd.image.to_tensor(tensor)
        tensor = mx.nd.image.normalize(tensor, mean=mean, std=std)
        return tensor, frame

    def _clean_predictions(self,
                           class_IDs,
                           scores,
                           bounding_boxes,
                           threshold):
        class_IDs = class_IDs.asnumpy()  # asnumpy() works as synchronization point
        scores = scores.asnumpy()
        bounding_boxes = bounding_boxes.asnumpy()

        mask_above_thresh = scores > threshold
        mask_correct_class = np.logical_or(class_IDs == self._person_id, class_IDs == self._suitcase_id)
        mask = np.logical_and(mask_above_thresh, mask_correct_class)
        mask_bbox = np.repeat(mask, 4, axis=1)

        valid_cls_ids = class_IDs[mask]
        valid_scores = scores[mask]
        valid_boxes = bounding_boxes[mask_bbox]

        return valid_cls_ids, valid_scores, valid_boxes
