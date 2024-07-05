from ..mark import Mark
from ...entity.entity import ProcessedGBEStruct
from ...base.bounding_rectangle import BoundingRectangle
from typing import List
from ...entity.base_type import EntityBaseType


class PingMianLouTiTaBu(Mark):
    """
    对于标记类，需要实现__init__和create_object_list方法。
    """

    chinese_name = "平面楼梯踏步"

    def __init__(self, tabu_info: List) -> None:
        x1, y1, x2, y2, length, width = tabu_info
        self.bounding_rectangle = BoundingRectangle([x1, y1, x2, y2])
        self.step_width = width
        self.step_length = length
        self.entity_base_type = EntityBaseType.PATTERN
