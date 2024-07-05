from ..space import Space
from typing import List
from ....common.utils_draw_and_rule import get_accessible_ramp_shape, get_accessible_ramp_type
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity


class WuZhangAiPoDao(Space):
    chinese_name = "无障碍坡道"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "无障碍坡道"
        self.space_base_type = SpaceBaseType.OUTDOOR_SUPPORT_SPACE
        self.gradient = None
        self.shape = get_accessible_ramp_shape(self.bbox.list, border_entity)  
        self.accessible_ramp_type = get_accessible_ramp_type(self.bbox.list, border_entity)


if __name__ == "__main__":
    pass
