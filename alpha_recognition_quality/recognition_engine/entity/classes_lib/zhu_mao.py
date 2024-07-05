from ..base_type import EntityBaseType
from ..entity import CombinedEntity
from ...base.bounding_rectangle import BoundingRectangle
from ...border_entity import BorderEntity


class ZhuMao(CombinedEntity):
    
    chinese_name = "柱帽"

    def __init__(self, layer_name: str, bounding_rectangle: BoundingRectangle, border_entity: BorderEntity) -> None:
        CombinedEntity.__init__(self, layer_name, bounding_rectangle)

        self.chinese_name = "柱帽"
        self.entity_base_type = EntityBaseType.PILLAR