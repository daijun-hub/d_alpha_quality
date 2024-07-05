from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import Entity,ClassifiedEntity


# 合并且分类类型
class ZhanShiPaiFengJi(ClassifiedEntity):
    
    chinese_name = "战时排风机"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "战时排风机"
        self.entity_base_type = EntityBaseType.HOUSEHOLD_APPLIANCE

