from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity
from ...utils import *


# 分类类型
class WuZhangAiPoDao(ClassifiedEntity):

    chinese_name = "无障碍坡道"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "无障碍坡道"
        self.entity_base_type = EntityBaseType.BASE
