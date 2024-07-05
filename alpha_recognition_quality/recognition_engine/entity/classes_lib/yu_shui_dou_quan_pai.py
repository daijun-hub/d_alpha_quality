from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity


# 合并且分类构件
class YuShuiDouQuanPai(ClassifiedEntity):
    
    chinese_name = "雨水斗全排"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        
        self.chinese_name = "雨水斗全排"
        self.entity_base_type = EntityBaseType.PIPE_ACCESSORY