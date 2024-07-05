from ..base_type import EntityBaseType
from ..entity import Entity
from ..entity import ClassifiedEntity
from ...border_entity import BorderEntity


# 分类类型
class JianChaJing(ClassifiedEntity):
    
    chinese_name = "检查井"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "检查井"
        self.entity_base_type = EntityBaseType.PIPE_ACCESSORY
