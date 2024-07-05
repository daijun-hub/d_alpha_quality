from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity

from ...utils import get_labeled_height_architecture


class ZongTuJianZhuLunKuo(Space):
    chinese_name = "总图建筑轮廓"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "总图建筑轮廓"
        self.space_base_type = SpaceBaseType.PIELD_AREA
        # 标高数值属性
        self.labeled_height = get_labeled_height_architecture(self.contour.contour, border_entity)
