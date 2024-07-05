from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity


# 合并且分类构件
class FaMen(ClassifiedEntity):
    
    chinese_name = "阀门"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        
        self.chinese_name = "阀门"
        self.entity_base_type = EntityBaseType.PIPE_ACCESSORY