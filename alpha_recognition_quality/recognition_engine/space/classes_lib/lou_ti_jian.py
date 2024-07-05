from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity
from ...utils import get_stair_type
from ...utils.utils_space import *

class LouTiJian(Space):
    chinese_name = "楼梯间"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "楼梯间"
        self.stair_room_type = get_stair_type(space_object.contour.contour, border_entity)
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE

        self.floor = border_entity.floor_num_list[0] if border_entity.floor_num_list else None


        self.related_wall = []              # 关联墙列表
        self.related_window = []            # 关联窗列表
        self.related_door = []              # 关联门列表
        self.related_hole = []              # 关联孔洞
        self.bounding_axis_line = []        # 轴号列表
        self.bounding_axis_label = []       # 轴号对应轴网列表
        self.wall_point_list = 0             # 梯段方向 墙的两侧点list
        self.related_door_open_type = []    # 关联门内外开方式


    def get_related_entities(self, border_entity):
        self._get_related_wall_list(border_entity)
        self._get_related_window_list(border_entity)
        self._get_related_door_list(border_entity)
        self._get_related_hole_list(border_entity)
        self.get_bounding_axis_line_and_label(border_entity)
        self.get_wall_thickness(border_entity)
        self.related_door_open_type = self.get_door_open_type(border_entity)

    def _get_related_wall_list(self, border_entity):
        # self.related_wall = self.related_wall = get_space_related_nonbear_wall_list(self, border_entity)
        related_wall = []
        wall_type_list = ['承重墙', '非承重墙']
        for wall_type in wall_type_list:
            wall_list = get_space_related_entity(self, border_entity, wall_type,
                                                   ext_len=wall_thickness_CAD * border_entity.ratio[0] // 3)
            for wall in wall_list:
                related_wall.append(wall)

        self.related_wall = related_wall

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
        door_type_list = ['单开门', '双开门', '子母门', '门联窗']
        for door_type in door_type_list:
            door_list = get_space_related_entity(self, border_entity, door_type,
                                                 ext_len=wall_thickness_CAD * border_entity.ratio[0] // 3)
            for door in door_list:
                related_door.append(door)

        self.related_door = related_door

    def _get_related_hole_list(self, border_entity):
        self.related_hole = get_space_related_entity(self, border_entity, "墙洞口",
                                                     ext_len=wall_thickness_CAD * border_entity.ratio[0] // 3)

    def get_bounding_axis_line_and_label(self, border_entity):
        self.bounding_axis_line, self.bounding_axis_label = get_bounding_axis_line_and_label(self, border_entity)

    def get_wall_thickness(self, border_entity):
        self.wall_point_list = get_stair_room_wall_thickness(self, border_entity)

    def get_door_open_type(self, border_entity):
        door_open_type_list = []
        for door in self.related_door:
            door_bbox = door.bounding_rectangle.list
            door_cnt = get_contour_from_bbox(door_bbox)
            if get_contours_iou(self.contour.contour, door_cnt) > 0.7:
                door_open_type_list.append("内开")
            else:
                door_open_type_list.append("外开")
        return door_open_type_list
