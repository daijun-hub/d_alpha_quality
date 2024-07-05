from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity


# 分类类型
class FangHuoJuanLianKongZhiQi(ClassifiedEntity):
    
    chinese_name = "防火卷帘控制器"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "防火卷帘控制器"
        self.entity_base_type = EntityBaseType.ELECTRIC_DEVICE