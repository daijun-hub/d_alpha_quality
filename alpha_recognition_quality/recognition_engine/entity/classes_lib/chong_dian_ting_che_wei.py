from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity


class ChongDianTingCheWei(ClassifiedEntity):
    
    chinese_name = "充电停车位"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "充电停车位"
        self.entity_base_type = EntityBaseType.PARKING