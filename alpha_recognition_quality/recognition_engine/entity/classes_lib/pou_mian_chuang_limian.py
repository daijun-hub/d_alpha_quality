from ..base_type import EntityBaseType
from ..entity import CombinedEntity, Entity
from ...base.bounding_rectangle import BoundingRectangle
from ...border_entity import BorderEntity


class PouMianChuangLiMian(CombinedEntity):
    
    chinese_name = "剖面窗"

    def __init__(self, layer_name: str, bounding_rectangle: BoundingRectangle, border_entity: BorderEntity) -> None:
        CombinedEntity.__init__(self, layer_name, bounding_rectangle)

        self.chinese_name = "剖面窗"
        self.entity_base_type = EntityBaseType.WINDOW


