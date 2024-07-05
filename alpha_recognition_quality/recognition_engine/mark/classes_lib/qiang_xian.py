from ...entity.base_type import EntityBaseType
from ..mark import Mark
from ...base.bounding_rectangle import BoundingRectangle
from ...border_entity import BorderEntity
from typing import List
from ...utils.utils_entity import extend_margin_by_side # utils_engity和utils_objectification_common都有这个函数
from ...utils.utils_objectification_common import *
from ....common.utils import *


class QiangXian(Mark):
    """
    对于标记类，需要实现__init__和create_object_list方法。
    """
    chinese_name = "墙线"
    def __init__(self, layer_name: str, line: List) -> None:

        self.entity_base_type = EntityBaseType.LINE
        self.start_end_point_list = [line]
        line_bbox = extend_margin_by_side_object(get_bbox_from_line(line), 3, 'long')
        self.bounding_rectangle = BoundingRectangle(line_bbox)

