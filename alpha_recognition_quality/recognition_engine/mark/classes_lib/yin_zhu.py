from ..mark import Mark
from ...border_entity import BorderEntity
from ...base.bounding_rectangle import BoundingRectangle
from ...entity.base_type import EntityBaseType
import cv2
import numpy as np


class YinZhu(Mark):
    """
    对于标记类，需要实现__init__和create_object_list方法。
    """

    chinese_name = "引注"

    def __init__(self, annotation_info, border_entity: BorderEntity) -> None:
        line_l, text_l, m_point = annotation_info
        self.bounding_rectangle = BoundingRectangle(self.get_bbox(line_l))
        self.labeled_text = text_l  # 引注文本是一个列表
        self.annotation_line_list = line_l  # 引线列表
        self.annotation_start_point = m_point  # 引注起点
        self.entity_base_type = EntityBaseType.TEXT

    def get_bbox(self, line_list):
        x_min_list = [line[0] for line in line_list]
        y_min_list = [line[1] for line in line_list]
        x_max_list = [line[2] for line in line_list]
        y_max_list = [line[3] for line in line_list]
        x_list = x_min_list + x_max_list
        y_list = y_min_list + y_max_list
        xmin, ymin, xmax, ymax = 0, 0, 0, 0
        if len(x_list) > 0:
            xmin = min(x_list)
            xmax = max(x_list)

        if len(y_list) > 0:
            ymin = min(y_list)
            ymax = max(y_list)

        return [xmin, ymin, xmax, ymax]
