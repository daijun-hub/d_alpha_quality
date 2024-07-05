from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity


class ShouDongBaoJingAnNiu(ClassifiedEntity):
    
    chinese_name = "手动报警按钮"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        self.chinese_name = "手动报警按钮"
        self.entity_base_type = EntityBaseType.FIRE_ALARM_DEVICE
