from ...entity.base_type import EntityBaseType
from ..mark import Mark
from ...border_entity import BorderEntity
from ...entity.entity import Entity
from typing import List
from ...base.bounding_rectangle import BoundingRectangle
from ....common.utils_draw_and_rule import *
from ...utils.utils_objectification_common import *


class DiShangDaoLuXian(Mark):

    chinese_name = "地上道路线"

    def __init__(self, entity_object: Entity, line: List) -> None:
        self.entity_base_type = EntityBaseType.LINE
        self.start_end_point_list = [line]
        line_bbox = extend_margin_by_side_object(get_bbox_from_line(line), 3, 'long')
        self.bounding_rectangle = BoundingRectangle(line_bbox)