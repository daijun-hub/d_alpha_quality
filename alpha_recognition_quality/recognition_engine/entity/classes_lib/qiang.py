import re

from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils import *


# 图元类构件
class Qiang(ClassifiedEntity):
    chinese_name = "墙"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        self.chinese_name = "墙"

        self.wall_center_line = entity_object.wall_center_line
        self.wall_thickness = entity_object.wall_thickness

        # 通过引线标注判断是否隔音
        self.sound_proof = self.judge_sound_proof(border_entity)

    def judge_sound_proof(self, border_entity: BorderEntity) -> bool:
        bbox = self.bounding_rectangle.list
        # 获取引线
        anno_line_list = border_entity.special_info_dict['annotation_info_list']

        for line_l, text_l, main_end_point in anno_line_list:
            branch_line = line_l[0]
            target_text_list = [t for t in text_l if re.search('隔声|隔音', t)]
            if len(target_text_list) == 0:
                continue
            iou = Iou_temp(extend_margin(branch_line, 10), extend_margin(bbox, 10))
            if iou > 0.01:
                return True

        return False
