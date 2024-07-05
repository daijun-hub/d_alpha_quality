from ..space import Space
from typing import List
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity
from ...utils.utils_space import fetch_building_width_length


# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加
class PingMianTuJianZhuLunKuo(Space):
    chinese_name = "平面图建筑轮廓"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.building_length, self.building_width = fetch_building_width_length(self.bbox.list, border_entity)
        self.chinese_name = "平面图建筑轮廓"
