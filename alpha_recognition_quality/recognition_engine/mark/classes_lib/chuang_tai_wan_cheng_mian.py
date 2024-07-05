from ..mark import Mark
from ...entity.entity import ProcessedGBEStruct
from typing import List
from ...base.bounding_rectangle import BoundingRectangle
from ...entity.base_type import EntityBaseType
from ..mark import Mark
from ...space.space import Space
from ...border_entity import BorderEntity
from ...entity.entity import Entity


class ChuangTaiWanChengMian(Mark):
    """
    对于标记类，需要实现__init__和create_object_list方法。
    """

    chinese_name = "窗台完成面"

    def __init__(self, wanchengmian: List) -> None:
        # wanchengmian: [line, bbox_temp]
        line, bbox = wanchengmian[0], wanchengmian[1]
        self.entity_base_type = EntityBaseType.LINE
        self.start_end_point_list = [line]
        self.bounding_rectangle = BoundingRectangle(bbox)
