from ..space import Space
from ..base_type import SpaceBaseType
from typing import List
from ...border_entity import BorderEntity
from ....common.utils import get_space_owned_space
import cv2.cv2 as cv2
from ...utils.utils_space import *


class TaoNeiShuiGuanJing(Space):
    chinese_name = "套内水管井"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "套内水管井"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE       # 对象父类
        self.get_owned_space(border_entity)
        self.get_size(border_entity)
        self.get_center()

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


    # def get_position(self):
    #     """
    #     与轮廓相同
    #     Returns:
    #
    #     """

    def get_size(self, border_entity):
        """
        获取大小, 长度、宽度
        Returns: [length, width]

        """
        ratio = border_entity.ratio
        length_width = (abs(self.bbox[2] - self.bbox[0])/ratio[0],
                        abs(self.bbox[3] - self.bbox[1])/ratio[0])
        self.size = [round(max(length_width)), round(min(length_width))]

    def get_owned_space(self, border_entity):
        """
        所属空间
        Returns:

        """
        owned_space = get_space_owned_space_v2(self, border_entity, 0.9)
        space_name = []
        for i in owned_space:
            if i.chinese_name in ['卫生间','厨房']:
                space_name.append(i.chinese_name)
        self.owned_space = space_name

    def get_center(self):
        """
        获取质心
        Returns:

        """
        cnt = self.contour.contour
        M = cv2.moments(cnt)
        center_x = int(M["m10"] / M["m00"])
        center_y = int(M["m01"] / M['m00'])
        self.center = [center_x, center_y]


if __name__ == "__main__":
    a = Space(None, None, ["None", "None"], None)
    b = TaoNeiShuiGuanJing(a)
    print(b)