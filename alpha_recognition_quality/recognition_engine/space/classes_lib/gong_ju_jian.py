from ..space import Space
from ..base_type import SpaceBaseType
from typing import List
from ...border_entity import BorderEntity


# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加

class GongJuJian(Space):
    chinese_name = "工具间"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "工具间"