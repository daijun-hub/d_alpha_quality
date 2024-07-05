from ...entity.base_type import EntityBaseType
from ..mark import Mark
from ...border_entity import BorderEntity
from ...entity.entity import Entity
from ...utils.utils_mark import *
import sys

class JianZhuSuoYinBiaoZhu(Mark):

    chinese_name = "建筑索引标注"

    def __init__(self, arch_index_info: List) -> None:
        # 建筑剖面标注： 两条直线和一个文本
        arch_index_bbox = [sys.maxsize, sys.maxsize, -sys.maxsize, -sys.maxsize]
        basic_entity_id_list = []
        for entity in arch_index_info:
            # print("entity", entity[0])
            arch_index_bbox[0] = min(arch_index_bbox[0], entity[0][0], entity[0][2])
            arch_index_bbox[1] = min(arch_index_bbox[1], entity[0][1], entity[0][3])
            arch_index_bbox[2] = max(arch_index_bbox[2], entity[0][0], entity[0][2])
            arch_index_bbox[3] = max(arch_index_bbox[3], entity[0][1], entity[0][3])
            basic_entity_id_list.append(entity[1])

        self.entity_base_type = EntityBaseType.OTHERS
        self.bounding_rectangle = BoundingRectangle(arch_index_bbox)
        self.basic_entity_id_list = basic_entity_id_list

