from ..base_type import EntityBaseType
from ..entity import Entity,ClassifiedEntity
from ...border_entity import BorderEntity
from ...utils import *


# 合并且分类类型
class LiMianChuang(ClassifiedEntity):
    
    chinese_name = "立面窗"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        ratio = border_entity.ratio
        bbox = self.bounding_rectangle.list
        self.chinese_name = "立面窗"
        self.entity_base_type = EntityBaseType.WINDOW
        self.window_fan_shape_area = entity_object.window_fan_shape_area
        self.window_area = (bbox[3] - bbox[1]) * (bbox[2] - bbox[0]) / ratio[0] / ratio[1] / 1000000
        self.window_number = entity_object.window_number
        self.window_divide, self.window_attribute, self.window_open_num = get_window_attribute_entity(self.bounding_rectangle.list, border_entity)
        self.inside_windows = get_inside_window(self.bounding_rectangle.list, border_entity)
        # self.window_number = window_numbering(entity_object.bounding_rectangle.list, border_entity, window_kind='普通窗')
