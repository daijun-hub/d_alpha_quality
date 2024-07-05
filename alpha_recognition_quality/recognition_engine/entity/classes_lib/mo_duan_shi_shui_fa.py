from ..base_type import EntityBaseType
from ..entity import Entity, ClassifiedEntity
from ...border_entity import BorderEntity
from typing import List
from ..entity import Entity,ClassifiedEntity
from ...border_entity import BorderEntity


# 合并且分类类型
class MoDuanShiShuiFa(ClassifiedEntity):
    
    chinese_name = "末端试水阀"
    
    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "末端试水阀"
        self.entity_base_type = EntityBaseType.OTHERS
        self.lead_mark = entity_object.lead_mark

