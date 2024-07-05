from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity


# 分类类型
class RanQiReShuiQi(ClassifiedEntity):
    chinese_name = "燃气热水器"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "燃气热水器"
        self.entity_base_type = EntityBaseType.KITCHEN_RESTROOM_OBJECT