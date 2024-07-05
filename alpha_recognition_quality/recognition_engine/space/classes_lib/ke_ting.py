from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity


class KeTing(Space):
    chinese_name = "客厅"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "客厅"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE