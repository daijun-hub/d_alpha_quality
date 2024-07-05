from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import Entity, ClassifiedEntity
from ....common.utils import get_entity_owned_space, get_contours_iou, get_position


# 合并且分类类型构件
class DiLou(ClassifiedEntity):
    chinese_name = "地漏"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "地漏"
        self.entity_base_type = EntityBaseType.OTHERS

    def get_position(self, border_entity):
        """
        相对阳台左上角2侧墙体距离
        Args:
            border_entity:

        Returns:

        """
        self.position = get_position(self, border_entity, ['阳台'])
