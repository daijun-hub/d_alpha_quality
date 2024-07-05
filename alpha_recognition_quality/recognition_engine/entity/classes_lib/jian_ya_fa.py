from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity


class JianYaFa(ClassifiedEntity):
    
    chinese_name = "减压阀"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "减压阀"
        self.entity_base_type = EntityBaseType.PIPE_ACCESSORY
        self.lead_mark = entity_object.lead_mark