from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity
from ...utils import *


# 合并且分类构件
class DianTi(ClassifiedEntity):
    chinese_name = "电梯"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "电梯"
        self.entity_base_type = EntityBaseType.MECHANICAL_DEVICE
        # 电梯编号
        self.elevator_number = get_entity_label_number(self.bounding_rectangle.list, border_entity, extend_margin=1200,
                                                       map_label="DT")
        # 停靠楼层
        self.stop_floor = border_entity.floor_num_list
        # 用途（消防电梯、无障碍电梯）
        self.usage = get_entity_label_number(self.bounding_rectangle.list, border_entity,
                                             extend_margin=1200, map_label=["消防", "无障碍", "担架", "无机房"])

        # 是否为无障碍电梯
        self.is_wheelchair_accessible_elevator = False
        # 是否为消防电梯
        self.is_fire_elevator = False
        # 是否为担架电梯
        self.is_stretcher_elevator = False
        # 是否为无机房电梯
        self.is_mrl_elevator = False

        self._judge_elevator_usage()

        # 是否为贯通梯(前后开门)
        self.is_through = len(get_entity_nearby_entity(self.bounding_rectangle.list, border_entity, extend_margin=1800,
                                                       map_label="elevator_door")) > 1
        # 底坑深度， 利用标高相减
        self.pit_depth = get_elevator_bottom_depth(self.bounding_rectangle.list, border_entity, extend_margin=1800)

        # 顶层高度, 利用标高相减
        # 需跨图框，需要机房层信息
        # self.top_floor_height = None

    def _judge_elevator_usage(self):
        if self.usage:
            for usage in self.usage:
                if "无障碍" in usage:
                    self.is_wheelchair_accessible_elevator = True
                if "消防" in usage:
                    self.is_fire_elevator = True
                if "担架" in usage:
                    self.is_stretcher_elevator = True
                if "无机房" in usage:
                    self.is_mrl_elevator = True

