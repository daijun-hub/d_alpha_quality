from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity
from ...utils import get_stair_type


class LouTiJianXiuXiPingTai(Space):
    chinese_name = "楼梯间休息平台"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "楼梯间休息平台"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE
