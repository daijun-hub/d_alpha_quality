from ..base_type import EntityBaseType
from ..entity import CombinedEntity
from ...base.bounding_rectangle import BoundingRectangle
from ...border_entity import BorderEntity
from ....common.utils import *
from ...utils.utils_objectification_common import *


class ShiXinQiang(CombinedEntity):
    
    chinese_name = "实心墙"

    def __init__(self, layer_name: str, bounding_rectangle, border_entity: BorderEntity) -> None:
        A = bounding_rectangle
        line_bbox = extend_margin_by_side_object(get_bbox_from_line(bounding_rectangle[:4]), 3, 'long')
        bounding_rectangle = BoundingRectangle(line_bbox)

        CombinedEntity.__init__(self, layer_name, bounding_rectangle)

        self.chinese_name = "实心墙"
        self.entity_base_type = EntityBaseType.STRUCTURE_WALL
        self.start_end_point = A 
