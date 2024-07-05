from ...entity.base_type import EntityBaseType
from ..mark import Mark
from ...border_entity import BorderEntity
from ...entity.entity import Entity
from ...utils.utils_mark import *

class JianZhuMianJi(Mark):

    chinese_name = "建筑面积"

    def __init__(self, arch_area_info: List) -> None:
        # wanchengmian: [line,bbox_temp, width, height]
        x1, y1, x2, y2, text, basic_entity_id = arch_area_info
        bbox = [x1, y1, x2, y2]
        self.entity_base_type = EntityBaseType.TEXT
        # self.start_end_point_list = [line[:2], line[2:]]
        self.bounding_rectangle = BoundingRectangle(bbox)
        self.basic_entity_id_list = [basic_entity_id]
