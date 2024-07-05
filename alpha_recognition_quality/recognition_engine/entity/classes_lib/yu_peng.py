from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity
from ...utils import *


# 分类类型
class YuPeng(ClassifiedEntity):

    chinese_name = "雨蓬"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "雨蓬"
        self.entity_base_type = EntityBaseType.BASE
        # 位置
        self.position = self.bounding_rectangle
        # 雨蓬结构下缘标高
        self.canopy_bottom_label_heigh = get_space_label_height(self.bounding_rectangle.list, border_entity)
        # 雨蓬轮廓
        self.contour = get_contour_from_bbox(self.bounding_rectangle.list)
        # 出挑距离
        self.overhang_distance = None

