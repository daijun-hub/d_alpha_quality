from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils.utils_entity import *


class TuiLaMen(ClassifiedEntity):
    
    chinese_name = "推拉门"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        text_cls = door_nearby_text(entity_object.bounding_rectangle.list, border_entity)

        self.chinese_name = "推拉门"
        self.door_usage, _ = door_usage_entity(entity_object.bounding_rectangle.list, border_entity)
        self.entity_base_type = EntityBaseType.DOOR
        # 门基线&门中线
        self.door_base_line = get_door_base_line_entity(entity_object.bounding_rectangle.list, border_entity)
        self.door_direction_line = get_door_direction_line_entity(entity_object.bounding_rectangle.list, border_entity)

        # 编号
        # map_label = "(TLM|M)[ ]?[甲乙丙]?\d{1,2}"
        map_label = "(LM|M|FM|MC|TLM|MD)[]?[甲乙丙]?(\d{1,2})?"
        self.door_number = get_door_label_number(entity_object.bounding_rectangle.list, border_entity,
                                                 extend_margin=1800, map_label=map_label)
        # self.door_number = get_entity_label_number(entity_object.bounding_rectangle.list, border_entity, extend_margin=1800, map_label=map_label)
        self.is_tui_la_men = True
        self.open_mode = '推拉门'

        # 新属性
        # 宽度
        self.width = door_width_entity(entity_object.bounding_rectangle.list, border_entity, text_cls)
        # 高度
        self.height = door_height_entity(entity_object.bounding_rectangle.list, border_entity, text_cls)
        # 洞口面积
        self.hole_area = self.door_height * self.door_wall_width if self.door_height and self.door_wall_width else None
