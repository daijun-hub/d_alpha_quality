from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import Entity, ClassifiedEntity


# 合并且分类类型
class PeiDianXiangChuXianHuiLu(ClassifiedEntity):
    
    chinese_name = "配电箱出线回路"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "配电箱出线回路"
        self.entity_base_type = EntityBaseType.ELECTRIC_EQUIPMENT

        self.disconnector_type = entity_object.disconnector_type  # 断路器属性
        self.thermal_relay_type = entity_object.thermal_relay_type  # 热继电器属性
        self.electric_meter_type = entity_object.electric_meter_type  # 电表属性
        self.contactor_type = entity_object.contactor_type  # 接触器属性
        self.disconnector_parameter = entity_object.disconnector_parameter  # 断路器参数属性
        self.thermal_relay_parameter = entity_object.thermal_relay_parameter  # 热继电器参数属性
        self.circuit_phase_sequence = entity_object.circuit_phase_sequence  # 相序属性
        self.circuit_number = entity_object.circuit_number  # 回路编号属性
        self.wire_parameter = entity_object.wire_parameter  # 电缆规格属性
        self.circuit_usage = entity_object.circuit_usage  # 用途属性
        self.circuit_power = entity_object.circuit_power  # 功率属性
        self.electric_meter_parameter = entity_object.electric_meter_parameter  # 电表参数属性
        self.contactor_parameter = entity_object.contactor_parameter  # 接触器参数属性
