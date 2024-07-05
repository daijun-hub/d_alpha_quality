from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ....common.utils_draw_and_rule import get_stair_width_long


class ZhiPaoLouTi(ClassifiedEntity):
    
    chinese_name = "直跑楼梯"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        self.chinese_name = "直跑楼梯"
        self.entity_base_type = EntityBaseType.STAIR
        # self.stair_long = get_stair_width_long(entity_object.bounding_rectangle.list, border_entity, need_type="long")
        # self.stair_width = get_stair_width_long(entity_object.bounding_rectangle.list, border_entity, need_type="width")