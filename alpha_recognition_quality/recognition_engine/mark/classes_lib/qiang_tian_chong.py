from ...entity.base_type import EntityBaseType
from ..mark import Mark
from ...base.bounding_rectangle import BoundingRectangle
from ...border_entity import BorderEntity
from typing import List


class QiangTianChong(Mark):

    chinese_name = "墙填充"

    def __init__(self, layer_name: str, hatch_info: List) -> None:

        if layer_name == 'solid_wall_line':
            self.wall_type = '剪力墙'
        else:
            self.wall_type = '砌块墙'

        self.bounding_rectangle = BoundingRectangle(hatch_info[0])
        self.entity_base_type = EntityBaseType.HATCH
        self.start_end_point_list = hatch_info[1]
