from ..base_type import EntityBaseType
from ..entity import Entity, ClassifiedEntity
from ...border_entity import BorderEntity
from typing import List
from ....common.utils import get_entity_owned_space, get_position


# 分类构建，引线标注
class WuShuiLiGuan(ClassifiedEntity):
    chinese_name = "污水立管"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "污水立管"
        self.entity_base_type = EntityBaseType.PIPE
        self.lead_mark = entity_object.lead_mark

    def get_position(self, border_entity):
        """
        污水立管相对所载最小空间的位置
        Args:
            border_entity:

        Returns:

        """
        self.position = get_position(self, border_entity, ['卫生间'])
