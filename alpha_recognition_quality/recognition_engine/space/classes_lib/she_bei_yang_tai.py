from ..space import Space
from ..base_type import SpaceBaseType
from typing import List
from ...border_entity import BorderEntity
from ....common.utils import get_space_owned_space
from ...utils.utils_space import *


class SheBeiYangTai(Space):
    chinese_name = "设备阳台"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "设备阳台"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE     
        self.is_refuge_space = False
        self.is_close_space = False

        # self.area # 轮廓面积
        self.floor = border_entity.floor_num_list[0] if border_entity.floor_num_list else None
        self.related_wall = []
        self.related_window = []
        self.related_door = []
        self.related_hole = []

    def get_related_entities(self, border_entity):
        self._get_related_wall_list(border_entity)
        self._get_related_window_list(border_entity)
        self._get_related_door_list(border_entity)
        self._get_related_hole_list(border_entity)

    def _get_related_wall_list(self, border_entity):
        self.related_wall = get_space_related_entity(self, border_entity, "墙",
                                                          ext_len = wall_thickness_CAD * border_entity.ratio[0]//3)

    def _get_related_window_list(self, border_entity):
        self.related_window = get_space_related_entity(self, border_entity, "其他窗",
                                                            ext_len = wall_thickness_CAD * border_entity.ratio[0]//3)

    def _get_related_door_list(self, border_entity):
        self.related_door = get_space_related_entity(self, border_entity, "其他门",
                                                          ext_len = wall_thickness_CAD * border_entity.ratio[0]//3)
        self.related_door += get_space_related_entity(self, border_entity, "管井门",
                                                     ext_len=wall_thickness_CAD * border_entity.ratio[0] // 3)

    def _get_related_hole_list(self, border_entity):
        self.related_hole = get_space_related_entity(self, border_entity, "墙洞口",
                                                          ext_len = wall_thickness_CAD * border_entity.ratio[0]//3)

