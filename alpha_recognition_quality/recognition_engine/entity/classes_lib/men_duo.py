from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity, ProcessedGBE
from ...border_entity import BorderEntity
from ...utils import *


class MenDuo(ClassifiedEntity):
    
    chinese_name = "门垛"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "门垛"
        self.entity_base_type = EntityBaseType.DOOR
