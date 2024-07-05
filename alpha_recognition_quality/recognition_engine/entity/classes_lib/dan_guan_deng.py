from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity


# 分类构件
class DanGuanDeng(ClassifiedEntity):
    
    chinese_name = "单管灯"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "单管灯"
        self.entity_base_type = EntityBaseType.ILLUMINATION_DEVICE
