from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity


class WuZhangAiCheWei(ClassifiedEntity):
    
    chinese_name = "无障碍车位"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "无障碍车位"
        self.entity_base_type = EntityBaseType.PARKING