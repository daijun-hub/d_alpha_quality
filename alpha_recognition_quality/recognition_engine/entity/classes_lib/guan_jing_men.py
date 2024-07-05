from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils.utils_entity import *
from ....common.utils_draw_and_rule import door_nearby_text


class GuanJingMen(ClassifiedEntity):
    
    chinese_name = "管井门"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        text_cls = door_nearby_text(entity_object.bounding_rectangle.list, border_entity)

        self.chinese_name = "管井门"
        self.entity_base_type = EntityBaseType.DOOR
        self.door_fire_resistance_level = door_fm_entity(entity_object.bounding_rectangle.list, border_entity, text_cls)
        self.door_base_line = get_door_base_line_entity(entity_object.bounding_rectangle.list, border_entity)
        self.door_direction_line = get_door_direction_line_entity(entity_object.bounding_rectangle.list, border_entity)
