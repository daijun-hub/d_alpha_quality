from ..space import Space
from ..base_type import SpaceBaseType
from typing import List
from ...border_entity import BorderEntity


# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加
from ...utils import judge_front_room_open


class FangYanLouTiQianShi(Space):
    chinese_name = "防烟楼梯前室"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "防烟楼梯前室"
        self.space_base_type = SpaceBaseType.OUTDOOR_SUPPORT_SPACE
        self.is_open_front_room = judge_front_room_open(space_object.contour.contour, border_entity)