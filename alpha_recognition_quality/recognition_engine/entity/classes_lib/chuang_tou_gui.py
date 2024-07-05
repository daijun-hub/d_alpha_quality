from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils import *


# 分类构件
class ChuangTouGui(ClassifiedEntity):
    chinese_name = "床头柜"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "床头柜"
        self.entity_base_type = EntityBaseType.OTHERS
