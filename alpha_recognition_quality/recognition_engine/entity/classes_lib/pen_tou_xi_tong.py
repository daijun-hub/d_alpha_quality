from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity


# 合并且分类类型
class PenTouXiTong(ClassifiedEntity):
    
    chinese_name = "喷头-系统"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "喷头-系统"
        self.entity_base_type = EntityBaseType.SPRINKLER
