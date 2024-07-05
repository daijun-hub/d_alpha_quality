from ..space import Space
from ..base_type import SpaceBaseType
from typing import List
from ...border_entity import BorderEntity


# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加

class YuPeng(Space):
    chinese_name = "雨篷"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "雨篷"
        self.space_base_type = SpaceBaseType.OUTDOOR_SUPPORT_SPACE       # 对象父类


if __name__ == "__main__":
    a = Space(None, None, ["None", "None"], None)
    b = YuPeng(a)
    print(b)
