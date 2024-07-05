from ...entity.base_type import EntityBaseType
from ..mark import Mark
from ...border_entity import BorderEntity
from ...entity.entity import Entity
from ...utils.utils_mark import *

class JianZhuPouMianBiaoZhu(Mark):

    chinese_name = "建筑剖面标注"

    def __init__(self, arch_section_anno_info: List) -> None:
        # 建筑剖面标注： 两条直线和一个文本
        line_entity_1, line_entity_2, text_entity = arch_section_anno_info
        line_1, line_1_id = line_entity_1
        line_2, line_2_id = line_entity_2
        text, text_id = text_entity
        bbox = [min(line_1[0], line_2[0], text[0], line_1[2], line_2[2], text[2]),
                min(line_1[1], line_2[1], text[1], line_1[3], line_2[3], text[3]),
                max(line_1[0], line_2[0], text[0], line_1[2], line_2[2], text[2]),
                max(line_1[1], line_2[1], text[1], line_1[3], line_2[3], text[3])]

        self.entity_base_type = EntityBaseType.OTHERS
        self.bounding_rectangle = BoundingRectangle(bbox)
        self.basic_entity_id_list = [line_1_id, line_2_id, text_id]

