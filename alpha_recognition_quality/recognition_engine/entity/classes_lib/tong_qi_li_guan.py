from ..base_type import EntityBaseType
from ..entity import Entity, ClassifiedEntity
from ...border_entity import BorderEntity
from typing import List


# 分类构建，引线标注
class TongQiLiGuan(ClassifiedEntity):
    
    chinese_name = "通气立管"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "通气立管"
        self.entity_base_type = EntityBaseType.PIPE
        self.lead_mark = entity_object.lead_mark

