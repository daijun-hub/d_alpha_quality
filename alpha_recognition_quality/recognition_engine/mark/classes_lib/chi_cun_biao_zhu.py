from ...entity.base_type import EntityBaseType
from ..mark import Mark
from ...border_entity import BorderEntity
from ...entity.entity import Entity
from ...utils.utils_mark import *

class ChiCunBiaoZhu(Mark):

    chinese_name = "尺寸标注"

    def __init__(self, anno_size_info: List) -> None:
        # [[x1,y1,x2,y2, text], entity_id]
        anno_size_info, basic_entity_id = anno_size_info
        self.entity_base_type = EntityBaseType.OTHERS
        # self.start_end_point_list = [line[:2], line[2:]]
        self.bounding_rectangle = BoundingRectangle(anno_size_info[:4])
        self.basic_entity_id_list = [basic_entity_id]
        self.extend_message = anno_size_info[4]