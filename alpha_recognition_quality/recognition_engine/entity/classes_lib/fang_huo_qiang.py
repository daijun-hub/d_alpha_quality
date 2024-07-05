from ...base.bounding_rectangle import BoundingRectangle
from ..base_type import EntityBaseType
from ..entity import Entity, CombinedEntity
from ...border_entity import BorderEntity
from ...utils.utils_objectification_common import *

class FangHuoQiang(CombinedEntity):
    
    chinese_name = "防火墙"

    def __init__(self, layer_name: str, bounding_rectangle: BoundingRectangle, border_entity: BorderEntity) -> None:
        line = bounding_rectangle.list
        print("line: ", line)
        line_bbox = extend_margin_by_side_object(line, 3, 'long')
        print("line_bbox: ", line_bbox)
        bounding_rectangle = BoundingRectangle(line_bbox)
        CombinedEntity.__init__(self, layer_name, bounding_rectangle)
        self.chinese_name = "防火墙"
        self.entity_base_type = EntityBaseType.STRUCTURE_WALL