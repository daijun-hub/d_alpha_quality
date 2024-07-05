from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity
from ....config_manager.architecture.drawing_config import DrawingType


class GuoLang(Space):
    chinese_name = "过廊"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "过廊"
