from ..base_type import EntityBaseType
from ..entity import Entity,ClassifiedEntity
from ...border_entity import BorderEntity


# 合并且分类类型
# evacuation_signs
class ShuSanZhiShiBiaoZhi(ClassifiedEntity):
    
    chinese_name = "疏散指示标志"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "疏散指示标志"
        self.entity_base_type = EntityBaseType.ILLUMINATION_DEVICE


