from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import Entity,ClassifiedEntity


# 合并且分类类型
class FangHuoFa150(ClassifiedEntity):
    
    chinese_name = "150°防火阀"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "150°防火阀"
        self.entity_base_type = EntityBaseType.HOUSEHOLD_APPLIANCE

