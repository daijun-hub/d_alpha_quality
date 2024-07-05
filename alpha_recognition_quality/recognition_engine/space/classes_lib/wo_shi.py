from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity

from ...utils.utils_space import get_room_type

KEYWORD_TYPE_DICT = {"主卧": "主卧", "次卧": "次卧", "起居": "卧室兼起居室"}


class WoShi(Space):
    chinese_name = "卧室"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "卧室"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE

        # 卧室细分类型
        self.bedroom_type = get_room_type(self.contour.contour, border_entity, KEYWORD_TYPE_DICT)
