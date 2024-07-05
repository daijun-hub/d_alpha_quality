from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity
from ...utils import get_stair_type
from ...utils.utils_space import *


class ChangKaiLouTiJian(Space):
    chinese_name = "敞开楼梯间"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "敞开楼梯间"
        self.stair_room_type = get_stair_type(space_object.contour.contour, border_entity)
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE

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
        related_window = []
        window_type_list = ['普通窗', '凸窗', '转角窗']
        for window_type in window_type_list:
            window_list = get_space_related_entity(self, border_entity, window_type,
                                                   ext_len=wall_thickness_CAD * border_entity.ratio[0] // 3)
            for window in window_list:
                related_window.append(window)

        self.related_window = related_window

    def _get_related_door_list(self, border_entity):
        related_door = []
        door_type_list = ['单开门', '双开门', '子母门', '门联窗', '推拉门']
        for door_type in door_type_list:
            door_list = get_space_related_entity(self, border_entity, door_type,
                                                 ext_len=wall_thickness_CAD * border_entity.ratio[0] // 3)
            for door in door_list:
                related_door.append(door)

        self.related_door = related_door

    def _get_related_hole_list(self, border_entity):
        self.related_hole = get_space_related_entity(self, border_entity, "墙洞口",
                                                          ext_len = wall_thickness_CAD * border_entity.ratio[0]//3)
