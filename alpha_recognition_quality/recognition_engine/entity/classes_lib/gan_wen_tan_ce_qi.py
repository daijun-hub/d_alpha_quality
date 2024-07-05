from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity


# 分类构件
class GanWenTanCeQi(ClassifiedEntity):
    
    chinese_name = "感温探测器"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "感温探测器"
        self.entity_base_type = EntityBaseType.FIRE_ALARM_DEVICE