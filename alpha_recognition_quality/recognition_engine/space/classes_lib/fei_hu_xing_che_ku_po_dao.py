from ..space import Space
from typing import List
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity


# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加

class FeiHuXingCheKuPoDao(Space):
    chinese_name = "非弧形车库坡道"  # 中台名称为 车库坡道

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "非弧形车库坡道"  # 中台名称为 车库坡道
        self.space_base_type = SpaceBaseType.OUTDOOR_SUPPORT_SPACE


if __name__ == "__main__":
    pass