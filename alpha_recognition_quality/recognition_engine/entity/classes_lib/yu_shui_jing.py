from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity


class YuShuiJing(ClassifiedEntity):
    
    chinese_name = "雨水井"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "雨水井"
        self.entity_base_type = EntityBaseType.PIPE_ACCESSORY
