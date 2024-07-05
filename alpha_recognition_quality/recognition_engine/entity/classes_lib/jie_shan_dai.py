from ..base_type import EntityBaseType
from ..entity import PrimitiveEntity, ProcessedGBEStruct, ProcessedGBE
from ...border_entity import BorderEntity


class JieShanDai(PrimitiveEntity):
    
    chinese_name = "接闪带"

    def __init__(self, processed_gbe: ProcessedGBE) -> None:
        PrimitiveEntity.__init__(self, processed_gbe)
        self.chinese_name = "接闪带"
        self.entity_base_type = EntityBaseType.OTHERS
        self.start_end_point_list = [coord for coord in self.start_end_point_list if len(coord) == 4]
