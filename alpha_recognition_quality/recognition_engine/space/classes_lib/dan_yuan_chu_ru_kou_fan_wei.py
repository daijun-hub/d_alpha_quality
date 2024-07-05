from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity
from ....config_manager.architecture.drawing_config import DrawingType


class DanYuanChuRuKouFanWei(Space):
    chinese_name = "单元出入口范围"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "单元出入口范围"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE


if __name__ == "__main__":
    pass
