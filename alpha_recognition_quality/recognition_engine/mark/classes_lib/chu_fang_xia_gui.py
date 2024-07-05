from ..mark import Mark
from ...entity.entity import ProcessedGBEStruct
from ...base.bounding_rectangle import BoundingRectangle
from ...entity.base_type import EntityBaseType
from ...utils.utils_objectification_common import *
from ....common.utils import *


class ChuFangXiaGui(Mark):
    """
    对于标记类，需要实现__init__和create_object_list方法。
    """
    chinese_name = "厨房下柜"

    def __init__(self, line) -> None:
        self.start_end_point_list = [line]
        line_bbox = extend_margin_by_side_object(get_bbox_from_line(line), 3, 'long')
        self.bounding_rectangle = BoundingRectangle(line_bbox)
        self.entity_base_type = EntityBaseType.LINE
