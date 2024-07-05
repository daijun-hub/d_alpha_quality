from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity


# 合并且分类构件
class QiTaLouTi(ClassifiedEntity):
    
    chinese_name = "其他楼梯"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        
        self.chinese_name = "其他楼梯"
        self.entity_base_type = EntityBaseType.STAIR