from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ....common.utils_draw_and_rule import door_nearby_text
from ...utils import *


class ZiMuMen(ClassifiedEntity):
    chinese_name = "子母门"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        text_cls = door_nearby_text(entity_object.bounding_rectangle.list, border_entity)

        self.chinese_name = "子母门"
        self.entity_base_type = EntityBaseType.DOOR
        # 宽度
        self.door_wall_width = door_width_entity(entity_object.bounding_rectangle.list, border_entity, text_cls)
        # 高度
        self.door_height = door_height_entity(entity_object.bounding_rectangle.list, border_entity, text_cls)
        # 门用途
        self.door_usage, self.door_orientation = door_usage_entity(entity_object.bounding_rectangle.list, border_entity)
        # 门开向空间
        self.door_towards_direction = door_towards_direction_entity(entity_object.bounding_rectangle.list,
                                                                    border_entity)
        # 门扇
        self.door_leaf_number = door_leaf_number_entity(entity_object.bounding_rectangle.list, border_entity)
        # 门消防联动控制
        self.door_fire_linked_control = door_xiaofang_control(entity_object.bounding_rectangle.list, border_entity)
        # 门开启区域
        self.door_open_region_contour = get_door_open_region_contour(entity_object.bounding_rectangle.list,
                                                                     border_entity)
        # 洞口面积
        self.door_open_area = self.door_height * self.door_wall_width if self.door_height and self.door_wall_width else None
        # 门基线
        self.door_base_line = get_door_base_line_entity(entity_object.bounding_rectangle.list, border_entity)
        # 门朝向线
        self.door_direction_line = get_door_direction_line_entity(entity_object.bounding_rectangle.list, border_entity)
        # 是否为外门
        self.is_outer_evacuating_door = judge_evacuating_door(entity_object.bounding_rectangle.list, border_entity)
        # 开启范围
        self.door_angle = door_angle_entity(entity_object.bounding_rectangle.list, border_entity)
        # 编号
        map_label = "(LM|M)\d{1,2}"
        self.door_number = get_entity_label_number(entity_object.bounding_rectangle.list, border_entity,
                                                   extend_margin=1800, map_label=map_label)
        self.is_ping_kai_men = True
        self.open_mode = '平开门'

        # 新属性名称
        # 门开启方向：与中线垂直，且朝向弧线方的法线
        self.door_open_direction = get_door_open_direction_entity(self.door_direction_line, self.door_base_line)
        # 门位置：门中线的两个端点坐标，以门baseline代表
        self.position = get_door_base_line_entity(entity_object.bounding_rectangle.list, border_entity)
        # 门轴位置
        self.door_shaft_position = get_door_axis_entity(self, border_entity)
        # 门开启状态
        self.is_normally_open_door = get_door_open_status_entity(self, border_entity)
        # 是否是管井门
        self.is_GuanJingMen = judge_door_is_guanjing_door(self, border_entity)
        # 是否为户门
        self.is_HuMen = True if self.door_usage == "户门" else False
        # 宽度
        self.width = self.door_wall_width
        # 高度
        self.height = self.door_height
        # 洞口面积
        self.hole_area = self.door_open_area
        # 防火等级
        self.door_fire_resistance_level = door_fm_entity(entity_object.bounding_rectangle.list, border_entity, text_cls)
        # 是否为外门
        self.is_outer_door = self.is_outer_evacuating_door
