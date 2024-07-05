import cv2
from ...common.utils import get_contours_iou

class Contour(object):
    """基础轮廓类"""
    def __init__(self,
                 opencv_contour,
                 ratio):
        self.contour = opencv_contour
        self.area = self._get_area(ratio)

    def _get_area(self, ratio):
        area = cv2.contourArea(self.contour, oriented=False)
        area = area / ratio[0] / ratio[1] / 10**6
        return area
    
    @property
    def bounding_rectangle(self):
        x, y, w, h = cv2.boundingRect(self.contour)
        return [x, y, x + w, y + h]
    
    def get_iou(self, other_contour: 'Contour'):
        return get_contours_iou(self.contour, other_contour.contour)
