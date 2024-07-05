from ..base_type import EntityBaseType
from ..entity import Entity, ClassifiedEntity
from ...border_entity import BorderEntity
from typing import List
from ..entity import Entity,ClassifiedEntity
from ...border_entity import BorderEntity


# 合并且分类类型
class LangYongBaoHuQi(ClassifiedEntity):
    
    chinese_name = "浪涌保护器"
    
    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "浪涌保护器"
        self.entity_base_type = EntityBaseType.ELECTRIC_DEVICE