from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity
from ..entity import PrimitiveEntity, ProcessedGBEStruct, ProcessedGBE


class DianXian(PrimitiveEntity):
    
    chinese_name = "电线"

    def __init__(self, processed_gbe: ProcessedGBE) -> None:
        PrimitiveEntity.__init__(self, processed_gbe)

        self.chinese_name = "电线"
        self.entity_base_type = EntityBaseType.WIRE
        self.start_end_point_list = [coord for coord in self.start_end_point_list if len(coord) == 4]
