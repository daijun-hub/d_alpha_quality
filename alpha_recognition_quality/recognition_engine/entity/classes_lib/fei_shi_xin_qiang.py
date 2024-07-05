from ..base_type import EntityBaseType
from ..entity import CombinedEntity
from ...base.bounding_rectangle import BoundingRectangle
from ...border_entity import BorderEntity


class FeiShiXinQiang(CombinedEntity):
    
    chinese_name = "非实心墙"

    def __init__(self, layer_name: str, bounding_rectangle: BoundingRectangle, border_entity: BorderEntity) -> None:
        bounding_rectangle = BoundingRectangle(bounding_rectangle[:4])
        CombinedEntity.__init__(self, layer_name, bounding_rectangle)

        self.chinese_name = "非实心墙"
        self.entity_base_type = EntityBaseType.STRUCTURE_WALL
