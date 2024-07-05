from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity


class RanQiBiGuaLu(ClassifiedEntity):
    
    chinese_name = "燃气壁挂炉"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "燃气壁挂炉"
        self.entity_base_type = EntityBaseType.LAMP
