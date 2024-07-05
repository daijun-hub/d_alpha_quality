from ...base.bounding_rectangle import BoundingRectangle
from ..base_type import EntityBaseType
from ..entity import Entity, CombinedEntity
from ...border_entity import BorderEntity


class TaiJie(CombinedEntity):
    
    chinese_name = "台阶"

    def __init__(self, layer_name: str, bounding_rectangle: BoundingRectangle, border_entity: BorderEntity) -> None:
        CombinedEntity.__init__(self, layer_name, bounding_rectangle)

        self.chinese_name = "台阶"
        self.entity_base_type = EntityBaseType.STAIR