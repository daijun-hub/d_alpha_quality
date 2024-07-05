from ..space import Space
from ..base_type import SpaceBaseType
from typing import List
from ...border_entity import BorderEntity


class XinBaoJian(Space):
    chinese_name = "信报间"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "信报间"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE       # 对象父类
