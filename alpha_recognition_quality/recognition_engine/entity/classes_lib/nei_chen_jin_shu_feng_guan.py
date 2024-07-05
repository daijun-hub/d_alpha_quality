from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity


# 分类类型
class NeiChenJinShuFengGuan(ClassifiedEntity):
    
    chinese_name = "内衬金属风管"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "内衬金属风管"
        self.entity_base_type = EntityBaseType.KITCHEN_RESTROOM_OBJECT
