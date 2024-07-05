from ..space import Space
from ..base_type import SpaceBaseType
from typing import List
from ...border_entity import BorderEntity
from ...utils import get_space_related_nonbear_wall_list, get_space_related_door, \
    get_space_related_entity_by_extend_entity_bbox

# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加

class NuanJing(Space):
    chinese_name = "暖井"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "暖井"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE

        # 获取楼层
        floor_list = border_entity.floor_num_list
        self.floor = floor_list[0] if len(floor_list) > 0 else None

    def get_related_entities(self, border_entity):
        """
        获取相关的构件
        :param border_entity:
        :return:
        """
        # 获取关联墙体
        self.related_wall = get_space_related_nonbear_wall_list(self, border_entity)

        # 获取关联门
        self.related_door = get_space_related_door(self, border_entity)

        # 获取关联窗
        window_list = ["普通窗", "凸窗", "转角窗"]
        self.related_window = []
        for window_name in window_list:
            self.related_window.extend(get_space_related_entity_by_extend_entity_bbox(self, border_entity, window_name))

        # 获取关联孔洞
        self.related_hole = get_space_related_entity_by_extend_entity_bbox(self, border_entity, "墙洞口")