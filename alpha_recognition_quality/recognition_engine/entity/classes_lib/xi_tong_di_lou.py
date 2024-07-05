from ..base_type import EntityBaseType
from ..entity import Entity, ClassifiedEntity
from ...border_entity import BorderEntity


# 合并且分类类型构件
class XiTongDiLou(ClassifiedEntity):
    
    chinese_name = "系统地漏"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        
        self.chinese_name = "系统地漏"
        self.entity_base_type = EntityBaseType.OTHERS
