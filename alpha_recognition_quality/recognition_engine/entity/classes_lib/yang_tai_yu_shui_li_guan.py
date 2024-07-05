from ..base_type import EntityBaseType
from ..entity import Entity, ClassifiedEntity
from ...border_entity import BorderEntity
from ....common.utils import get_entity_owned_space, get_position


# 分类构建，引线标注
class YangTaiYuShuiLiGuan(ClassifiedEntity):
    chinese_name = "阳台雨水立管"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "阳台雨水立管"
        self.entity_base_type = EntityBaseType.PIPE
        self.lead_mark = entity_object.lead_mark

    def get_owned_space(self, border_entity):
        """
        所属空间
        Returns: 空间对象列表

        """
        self.owned_space = get_entity_owned_space(self, border_entity)

    def get_position(self, border_entity):
        """
        阳台雨水立管相对阳台左上角2侧墙体距离
        Args:
            border_entity:

        Returns:

        """
        self.position = get_position(self, border_entity, ['阳台'])
