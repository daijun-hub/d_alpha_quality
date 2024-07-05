from ...entity.base_type import EntityBaseType
from ..mark import Mark
from ...base.bounding_rectangle import BoundingRectangle
from ...border_entity import BorderEntity
from typing import List


class YongDiHongXian(Mark):

    chinese_name = "用地红线"

    def __init__(self, layer_name: str, red_line_info: List) -> None:

        self.bounding_rectangle = BoundingRectangle(red_line_info[0])
        self.entity_base_type = EntityBaseType.LINE
        self.start_end_point_list = red_line_info[1]
