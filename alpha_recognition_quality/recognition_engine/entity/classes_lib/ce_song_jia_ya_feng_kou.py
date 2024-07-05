from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity


class CeSongJiaYaFengKou(ClassifiedEntity):
    
    chinese_name = "侧送加压风口"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "侧送加压风口"
        self.entity_base_type = EntityBaseType.PIPE_ACCESSORY