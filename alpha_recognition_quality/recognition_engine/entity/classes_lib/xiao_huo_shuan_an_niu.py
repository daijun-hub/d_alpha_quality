
from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity


class XiaoHuoShuanAnNiu(ClassifiedEntity):
    
    chinese_name = "消火栓按钮"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        self.chinese_name = "消火栓按钮"
        self.entity_base_type = EntityBaseType.FIRE_ALARM_DEVICE
