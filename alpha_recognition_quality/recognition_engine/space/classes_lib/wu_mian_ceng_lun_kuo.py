from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity


class WuMianCengLunKuo(Space):
    chinese_name = "屋面层轮廓"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "屋面层轮廓"
        self.space_base_type = SpaceBaseType.OUTDOOR_SUPPORT_SPACE
