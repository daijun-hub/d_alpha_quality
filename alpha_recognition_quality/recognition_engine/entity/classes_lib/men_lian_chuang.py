from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils.utils_entity import *


# 分类构件
class MenLianChuang(ClassifiedEntity):
    
    chinese_name = "门联窗"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "门联窗"
        self.entity_base_type = EntityBaseType.DOOR_WITH_WINDOW
        self.window_is_outside = judge_outside_window_entity(entity_object.bounding_rectangle.list, border_entity)
        self.is_outer_evacuating_door = judge_evacuating_door(entity_object.bounding_rectangle.list, border_entity)
        self.door_base_line = get_door_base_line_entity(entity_object.bounding_rectangle.list, border_entity)
        self.door_direction_line = get_door_direction_line_entity(entity_object.bounding_rectangle.list, border_entity)

        # 1022 新增属性
        # 是否是凸窗
        self.is_bay_window = False
        # 宽度
        self.width = window_width_height_entity(entity_object.bounding_rectangle.list,
                                                border_entity,
                                                window_kind='门联窗')[0]
        # 高度
        self.height = window_width_height_entity(entity_object.bounding_rectangle.list,
                                                border_entity,
                                                window_kind='门联窗')[1]
        # 窗面积
        self.window_open_area = self.window_width * self.window_height if self.window_width and self.window_height else None  # 窗面积
        # 位置
        self.position = get_window_position_entity(self, border_entity)
        # 开启方式:平面图不易获取，跨图获取
        self.open_way = None
        # 防火等级
        self.window_fire_resistance_level = get_window_fire_resistance_level_entity(
            entity_object.bounding_rectangle.list, border_entity)
        # 是否内窗
        self.is_inner_window = not self.window_is_outside
        # 是否自动排烟窗
        self.is_automatic_smoke_exhaust_window = judge_automatic_smoke_exhaust_window_entity(
            entity_object.bounding_rectangle.list, border_entity)
        # 编号
        map_label = "(LM|M|FM|MC|TLM|MD)[]?[甲乙丙]?(\d{1,2})?"
        self.door_number = get_door_label_number(entity_object.bounding_rectangle.list, border_entity,
                                                 extend_margin=1800, map_label=map_label)