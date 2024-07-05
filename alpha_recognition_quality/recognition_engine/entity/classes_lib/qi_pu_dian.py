from ...border_entity import BorderEntity
from ..entity import CombinedEntity, Entity
from ...base.bounding_rectangle import BoundingRectangle


class QiPuDian(CombinedEntity):
    def __init__(self, layer_name: str, bounding_rectangle: BoundingRectangle, border_entity: BorderEntity) -> None:
        CombinedEntity.__init__(self, layer_name, bounding_rectangle)
        self.chinese_name = "起铺点"
        self.direction = None
