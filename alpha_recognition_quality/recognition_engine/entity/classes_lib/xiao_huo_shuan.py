import re

from ....common import Iou_temp
from ..base_type import EntityBaseType
from ..entity import Entity, ClassifiedEntity
from ...border_entity import BorderEntity


# 合并且分类类型构件
class XiaoHuoShuan(ClassifiedEntity):
    chinese_name = "消火栓"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "消火栓"
        self.entity_base_type = EntityBaseType.FIRE_ALARM_DEVICE

    def get_embedding_thickness(self, border_entity):
        """
        得到嵌入墙体厚度
        Args:
            border_entity:

        Returns:

        """
        self.embedding_thickness = get_embedding_thickness(self, border_entity)

    def get_related_entities(self, border_entity):
        """

        Args:
            border_entity:

        Returns:

        """
        # 更新跨对象属性
        self.get_embedding_thickness(border_entity)


def get_embedding_thickness(entity_object, border_entity):
    """
    嵌入墙体厚度
    """
    max_iou = 0
    bbox = entity_object.bounding_rectangle
    for k, v in border_entity.entity_object_dict.items():
        if re.match('.*墙$', k) is None:
            continue
        for i in v:
            wall_bbox = i.bounding_rectangle
            iou = Iou_temp(bbox, wall_bbox)
            if iou > max_iou:
                max_iou = iou
        if max_iou >= 0.1:
            break
    if max_iou > 0.9:
        return 200
    if max_iou < 0.1:
        return 0
    return 100
