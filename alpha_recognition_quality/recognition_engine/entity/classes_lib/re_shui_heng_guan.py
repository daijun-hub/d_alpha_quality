from ..base_type import EntityBaseType
from ..entity import PrimitiveEntity, ProcessedGBEStruct, ProcessedGBE
from ...border_entity import BorderEntity
from typing import List


# 图元类构件
class ReShuiHengGuan(PrimitiveEntity):
    
    chinese_name = "热水横管"

    def __init__(self, processed_gbe: ProcessedGBE) -> None:
        PrimitiveEntity.__init__(self, processed_gbe)
        self.chinese_name = "热水横管"

        self.entity_base_type = EntityBaseType.PIPE
        self.start_end_point_list = [coord for coord in self.start_end_point_list if len(coord) == 4]
