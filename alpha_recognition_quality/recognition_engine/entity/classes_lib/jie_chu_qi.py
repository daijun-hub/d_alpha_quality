from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity


# 分类构件
class JieChuQi(ClassifiedEntity):
    
    chinese_name = "接触器"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "接触器"
        self.entity_base_type = EntityBaseType.ELECTRIC_DEVICE