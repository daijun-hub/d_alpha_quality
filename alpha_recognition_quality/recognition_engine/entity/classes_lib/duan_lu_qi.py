from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils import get_breaker_pole, get_power_system, get_breaker_hu


class DuanLuQi(ClassifiedEntity):
    
    chinese_name = "断路器"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "断路器"
        self.entity_base_type = EntityBaseType.ELECTRIC_DEVICE
        self.pole = get_breaker_pole(self.bounding_rectangle.list, border_entity)  # 断路器极数
        self.power_supply_system = get_power_system(self.pole)                     # 电源制式
        self.belong_hu = get_breaker_hu(self.bounding_rectangle ,border_entity)
