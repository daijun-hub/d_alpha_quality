from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity

from ....common.utils_draw_and_rule import get_balcony_type


class KaiChangYangTai(Space):
    chinese_name = "开敞阳台"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "开敞阳台"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE

        # 阳台细分类型
        self.balcony_type = '开敞阳台'
