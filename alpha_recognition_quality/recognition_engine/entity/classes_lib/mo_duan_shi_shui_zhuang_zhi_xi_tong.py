from ..base_type import EntityBaseType
from ..entity import Entity, ClassifiedEntity
from ...border_entity import BorderEntity
from typing import List


# 合并且分类且标注类构件

class MoDuanShiShuiZhuangZhi_XiTong(ClassifiedEntity):
    
    chinese_name = "末端试水装置-系统"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "末端试水装置-系统"
        self.entity_base_type = EntityBaseType.PIPE_ACCESSORY
        self.lead_mark = entity_object.lead_mark
