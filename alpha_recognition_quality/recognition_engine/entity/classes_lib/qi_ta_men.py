from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils.utils_entity import *


class QiTaMen(ClassifiedEntity):
    
    chinese_name = "其他门"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "其他门"
        self.entity_base_type = EntityBaseType.DOOR
        self.door_base_line = get_door_base_line_entity(entity_object.bounding_rectangle.list, border_entity)
        self.door_direction_line = get_door_direction_line_entity(entity_object.bounding_rectangle.list, border_entity)
