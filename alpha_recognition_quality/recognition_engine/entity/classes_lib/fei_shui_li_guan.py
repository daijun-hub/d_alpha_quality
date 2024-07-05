from ..base_type import EntityBaseType
from ..entity import Entity, ClassifiedEntity
from ...border_entity import BorderEntity
from typing import List
from ....common.utils import get_position, get_absolute_position


# 分类构建，引线标注
class FeiShuiLiGuan(ClassifiedEntity):
    
    chinese_name = "废水立管"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "废水立管"
        self.entity_base_type = EntityBaseType.PIPE
        self.lead_mark = entity_object.lead_mark

    def get_position(self, border_entity):
        """
        立管所在卫生间的位置
        Args:
            border_entity:

        Returns:

        """
        self.position = get_position(self, border_entity)

    def get_absolute_position(self, border_entity):
        """
        获取绝对位置
        Args:
            border_entity:

        Returns:

        """
        bbox = self.bounding_rectangle
        center = (round((bbox[2] + bbox[0]) / 2), round((bbox[3] + bbox[1]) / 2))
        self.absolute_position = get_absolute_position(center, border_entity)
