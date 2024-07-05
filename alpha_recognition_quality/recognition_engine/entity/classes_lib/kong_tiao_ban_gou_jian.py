from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity


# 分类类型
class KongTiaoBanGouJian(ClassifiedEntity):

    chinese_name = "空调板构件"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "空调板构件"
        self.entity_base_type = EntityBaseType.BASE
        # 图集做法
        self.atlas_detail = None