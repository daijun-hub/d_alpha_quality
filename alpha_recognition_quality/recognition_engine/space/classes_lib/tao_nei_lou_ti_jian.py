from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity
from ...utils import get_stair_type


class TaoNeiLouTiJian(Space):
    chinese_name = "套内楼梯间"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "套内楼梯间"
        # self.stair_room_type = get_stair_type(space_object.contour.contour, border_entity)
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE
