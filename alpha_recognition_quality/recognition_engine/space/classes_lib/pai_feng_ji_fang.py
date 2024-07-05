from ..space import Space
from ..base_type import SpaceBaseType
from typing import List
from ...border_entity import BorderEntity
from ....common.utils import expand_contour, get_contours_iou, get_contour_from_bbox


class PaiFengJiFang(Space):
    chinese_name = "排风机房"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "排风机房"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE
        self.floor = '地下层'
        self.is_close_space = True

    def get_related_entities(self, border_entity):
        """
        获取相关的构件
        :param border_entity:
        :return:
        """
        self._get_related_wall(border_entity)
        self._get_related_door(border_entity)
        self._get_related_hole(border_entity)

    def _get_related_wall(self, border_entity):
        related_wall = []
        nobear_wall_list = border_entity.entity_object_dict.get('墙', [])
        ventilation_room_cnt_ext = expand_contour(self.contour.contour, 10)
        for nobear_wall in nobear_wall_list:
            if get_contours_iou(ventilation_room_cnt_ext, nobear_wall.contour.contour) > 0:
                related_wall.append(nobear_wall)

        self.related_wall = related_wall

    def _get_related_door(self, border_entity):
        related_door = []
        ventilation_room_cnt_ext = expand_contour(self.contour.contour, 10)
        map_label = ["单开门", "双开门", "子母门", "门联窗", "推拉门"]
        for label in map_label:
            door_list = border_entity.entity_object_dict.get(label, [])
            for door in door_list:
                if get_contours_iou(ventilation_room_cnt_ext, get_contour_from_bbox(door.bounding_rectangle.list)) > 0:
                    related_door.append(door)

        self.related_door = related_door

    def _get_related_hole(self, border_entity):
        related_hole = []
        hole_list = border_entity.entity_object_dict.get('墙洞口', [])
        ventilation_room_cnt_ext = expand_contour(self.contour.contour, 10)
        for hole in hole_list:
            if get_contours_iou(ventilation_room_cnt_ext, get_contour_from_bbox(hole.bounding_rectangle.list)) > 0:
                related_hole.append(hole)

        self.related_hole = related_hole
