import cv2
from ..space import Space
from ..base_type import SpaceBaseType
from typing import List
from ...border_entity import BorderEntity


# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加

class FengJing(Space):
    chinese_name = "风井"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "风井"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE
        self.is_close_space = True

        # 获取楼层
        floor_list = border_entity.floor_num_list
        self.floor = floor_list[0] if len(floor_list) > 0 else None

        #获取空间长度、宽度
        # cv2.minAreaRect ==>（最小外接矩形的中心（x，y），（宽度，高度），旋转角度）
        # theta是由x轴逆时针转至W(宽)的角度，[-90,0)
        (cx, cy), (w, h), theta = cv2.minAreaRect(self.contour.contour)
        self.space_length = max(w, h)
        self.space_width = min(w, h)