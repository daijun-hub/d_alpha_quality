from ..base_type import EntityBaseType
from ..entity import CombinedEntity, Entity
from ...base.bounding_rectangle import BoundingRectangle
from ...border_entity import BorderEntity


# 合并构件
class ZhuZi(CombinedEntity):
    
    chinese_name = "柱子"

    def __init__(self, layer_name: str, bounding_rectangle: BoundingRectangle, border_entity: BorderEntity) -> None:
        CombinedEntity.__init__(self, layer_name, bounding_rectangle)

        self.chinese_name = "柱子"
        self.entity_base_type = EntityBaseType.PILLAR
