from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity


class PeiDianXiang(ClassifiedEntity):
    
    chinese_name = "配电箱"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "配电箱"
        self.entity_base_type = EntityBaseType.ELECTRIC_EQUIPMENT
        self.electric_distribution_box_number = entity_object.electric_distribution_box_number
