import cv2
from ..space import Space
from ..base_type import SpaceBaseType
from typing import List
from ...border_entity import BorderEntity
from ...utils import get_space_related_nonbear_wall_list, get_space_related_door, \
    get_space_related_entity_by_extend_entity_bbox, get_contour_perimeter


# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加

class GongQuSheBeiPingTai(Space):
    chinese_name = "公区设备平台"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "公区设备平台"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE

        # 获取楼层
        floor_list = border_entity.floor_num_list
        self.floor = floor_list[0] if len(floor_list) > 0 else None

        #获取空间长度、宽度、周长
        # cv2.minAreaRect ==>（最小外接矩形的中心（x，y），（宽度，高度），旋转角度）
        # theta是由x轴逆时针转至W(宽)的角度，[-90,0)
        (cx, cy), (w, h), theta = cv2.minAreaRect(self.contour.contour)
        self.space_length = max(w, h)
        self.space_width = min(w, h)
        self.space_perimeter = get_contour_perimeter(self.contour.contour)

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
