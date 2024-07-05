from ..space import Space
from ..base_type import SpaceBaseType
from typing import List
from ...border_entity import BorderEntity
from ....common.utils_draw_and_rule import get_swerve_radius, get_podu


# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加

class YuanQuPuTongCheDao(Space):
    chinese_name = "园区普通车道"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "园区普通车道"
        # self.turning_radius = get_swerve_radius(space_object.contour.contour, border_entity)
        self.turning_radius = {}  # 超时，临时注释节省时间
        # self.gradient = get_podu(space_object.contour.contour, border_entity)
        self.gradient = {}  # 超时，临时注释节省时间
        self.space_base_type = SpaceBaseType.PIELD_AREA


if __name__ == "__main__":
    a = Space(None, None, ["None", "None"], None)
    b = YuanQuPuTongCheDao(a)
    print(b)
