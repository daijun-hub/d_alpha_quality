from ..space import Space
from typing import List
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity
from ....config_manager.architecture.drawing_config import DrawingType as DrawingTypeArchi
from ....common.utils import expand_contour, get_contours_iou, get_contour_from_bbox


class PeiDianJian(Space):
    chinese_name = "配电间"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "配电间"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE
        self.floor = self._get_floor(border_entity)
        self.is_close_space = True

    def _get_floor(self, border_entity):
        drawing_type = border_entity.drawing_type
        if drawing_type == DrawingTypeArchi.UNDERGROUND:
            return '地下层'
        elif drawing_type == DrawingTypeArchi.INDOOR_FIRST_FLOOR:
            return '一层'

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
        distribution_room_cnt_ext = expand_contour(self.contour.contour, 10)
        for nobear_wall in nobear_wall_list:
            if get_contours_iou(distribution_room_cnt_ext, nobear_wall.contour.contour) > 0:
                related_wall.append(nobear_wall)

        self.related_wall = related_wall

    def _get_related_door(self, border_entity):
        related_door = []
        distribution_room_cnt_ext = expand_contour(self.contour.contour, 10)
        map_label = ["单开门", "双开门", "子母门", "门联窗", "推拉门"]
        for label in map_label:
            door_list = border_entity.entity_object_dict.get(label, [])
            for door in door_list:
                if get_contours_iou(distribution_room_cnt_ext, get_contour_from_bbox(door.bounding_rectangle.list)) > 0:
                    related_door.append(door)

        self.related_door = related_door

    def _get_related_hole(self, border_entity):
        related_hole = []
        hole_list = border_entity.entity_object_dict.get('墙洞口', [])
        distribution_room_cnt_ext = expand_contour(self.contour.contour, 10)
        for hole in hole_list:
            if get_contours_iou(distribution_room_cnt_ext, get_contour_from_bbox(hole.bounding_rectangle.list)) > 0:
                related_hole.append(hole)

        self.related_hole = related_hole
