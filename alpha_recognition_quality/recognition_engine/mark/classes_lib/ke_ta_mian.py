from ...entity.base_type import EntityBaseType
from ..mark import Mark
from ...border_entity import BorderEntity
from ...entity.entity import Entity
from ...utils.utils_mark import *

class KeTaMian(Mark):

    chinese_name = "可踏面"

    def __init__(self, ketamian_info: List) -> None:
        # wanchengmian: [line,bbox_temp, width, height]
        line, bbox, ktm_width, ktm_height = ketamian_info
        self.entity_base_type = EntityBaseType.LINE
        self.start_end_point_list = [line[:2], line[2:]]
        self.bounding_rectangle = BoundingRectangle(bbox)
        # 可踏面高度
        self.ktm_height = ktm_height
        # 可踏面宽度
        self.ktm_width = ktm_width

