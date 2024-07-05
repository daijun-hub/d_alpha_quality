from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity


class PuTongDeng(ClassifiedEntity):
    
    chinese_name = "普通灯"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "普通灯"
        self.entity_base_type = EntityBaseType.ILLUMINATION_DEVICE
