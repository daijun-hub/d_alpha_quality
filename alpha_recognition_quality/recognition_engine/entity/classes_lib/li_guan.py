from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ....common.utils import get_entity_owned_space


class LiGuan(ClassifiedEntity):
    chinese_name = "立管"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "立管"
        self.entity_base_type = EntityBaseType.PIPE

    def get_owned_space(self, border_entity):
        """
        所属空间
        Returns:

        """
        self.owned_space = get_entity_owned_space(self, border_entity)
