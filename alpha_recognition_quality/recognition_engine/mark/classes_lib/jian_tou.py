from ..mark import Mark
from ...entity.entity import ProcessedGBEStruct
from typing import List
from ...base.bounding_rectangle import BoundingRectangle
from ...entity.base_type import EntityBaseType


class JianTou(Mark):
    """
    对于标记类，需要实现__init__和create_object_list方法。
    """

    chinese_name = "箭头"

    def __init__(self, arrow_info: List) -> None:
        # arrow_info: [angle, l_list, arrow_bbox]
        angle, l_list, arrow_bbox = arrow_info
        self.bounding_rectangle = BoundingRectangle(arrow_bbox)
        self.arrow_direction = angle
        self.start_end_point_list = l_list
        self.entity_base_type = EntityBaseType.PATTERN
