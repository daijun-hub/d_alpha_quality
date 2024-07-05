from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity


class BianYaQi(ClassifiedEntity):
    
    chinese_name = "变压器"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        self.chinese_name = "变压器"
        self.entity_base_type = EntityBaseType.ELECTRIC_DEVICE
