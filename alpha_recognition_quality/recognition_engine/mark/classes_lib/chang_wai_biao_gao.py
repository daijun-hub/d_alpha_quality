from ...entity.base_type import EntityBaseType
from ..mark import Mark
from ...border_entity import BorderEntity
from ...entity.entity import Entity
from ...utils.utils_mark import *
from ....config_manager.architecture.drawing_config import DrawingType

class ChangWaiBiaoGao(Mark):

    chinese_name = "建筑外场地标高"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:

        self.bounding_rectangle = entity_object.bounding_rectangle
        self.entity_base_type = EntityBaseType.TEXT






