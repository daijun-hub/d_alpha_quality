import cv2
from ..space import Space
from ..base_type import SpaceBaseType
from typing import List
from ...border_entity import BorderEntity


# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加

class PaiYanJing(Space):
    chinese_name = "排烟井"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "排烟井"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE       # 对象父类

        self.floor = border_entity.floor_num_list[0] if border_entity.floor_num_list else None
        self.is_close_space = True
        (cx, cy), (w, h), theta = cv2.minAreaRect(self.contour.contour)
        self.space_length = max(w, h)
        self.space_width = min(w, h)


if __name__ == "__main__":
    a = Space(None, None, ["None", "None"], None)
    b = PaiYanJing(a)
    print(b)
