from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity


class XiaoFangDengGaoChangDi(Space):
    chinese_name = "消防登高场地"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "消防登高场地"
        self.space_base_type = SpaceBaseType.PIELD_AREA

