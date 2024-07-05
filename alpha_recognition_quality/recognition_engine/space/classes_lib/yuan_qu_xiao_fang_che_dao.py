from ..space import Space
from ..base_type import SpaceBaseType
from typing import List
from ...border_entity import BorderEntity
from ...utils import get_car_entrance_type
from ....common.utils_draw_and_rule import get_podu, get_swerve_radius


# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加

class YuanQuXiaoFangCheDao(Space):
    chinese_name = "园区消防车道"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "园区消防车道"
        # self.gradient = get_podu(space_object.contour.contour, text_list)
        self.gradient = {}  # 超时，临时注释节省时间
        # self.turning_radius = get_swerve_radius(space_object.contour.contour, border_entity)
        self.turning_radius = {}  # 超时，临时注释节省时间
        # self.vehicle_passage_way_type = get_car_entrance_type(space_object.contour.contour, border_entity)
        self.vehicle_passage_way_type = '消防车行出入口'
        self.space_base_type = SpaceBaseType.PIELD_AREA


if __name__ == "__main__":
    a = Space(None, None, ["None", "None"], None)
    b = YuanQuXiaoFangCheDao(a)
    print(b)