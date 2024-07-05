from ..mark import Mark
from ...entity.entity import ProcessedGBEStruct
from typing import List
from ....common.utils_draw_and_rule import extend_margin_by_side, get_bbox_from_line
from ...base.bounding_rectangle import BoundingRectangle
from ...utils.utils_objectification_common import *

class DiXiaCheKuCheDaoXian(Mark):
    """
    对于标记类，需要实现__init__和create_object_list方法。
    """
    chinese_name = "地下车库车道线"

    def __init__(self, p_gbes: ProcessedGBEStruct, line: List) -> None:
        Mark.copy(self, p_gbes)
        self.start_end_point_list = [line]
        line_bbox = extend_margin_by_side_object(get_bbox_from_line(line), 3, 'long')
        self.bounding_rectangle = BoundingRectangle(line_bbox)
