from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils import *
from ....common.utils2 import load_drawing_pkl
from shapely.geometry import LineString, Polygon, MultiLineString, Point
from ....config_manager.structure.drawing_config import DrawingType as drawing_type_structure


class JieGouBan(ClassifiedEntity):
    chinese_name = "结构板"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        self.chinese_name = "结构板"

        # 相关属性
        self.slab_number = entity_object.slab_number
        self.slab_thickness = entity_object.slab_thickness
        self.bottom_x_reinforceing_bar_dia = entity_object.bottom_x_reinforceing_bar_dia
        self.bottom_x_reinforceing_bar_dis = entity_object.bottom_x_reinforceing_bar_dis

        self.bottom_y_reinforceing_bar_dia = entity_object.bottom_y_reinforceing_bar_dia
        self.bottom_y_reinforceing_bar_dis = entity_object.bottom_y_reinforceing_bar_dis

        self.top_x_reinforceing_bar_dia = entity_object.top_x_reinforceing_bar_dia
        self.top_x_reinforceing_bar_dis = entity_object.top_x_reinforceing_bar_dis

        self.top_y_reinforceing_bar_dia = entity_object.top_y_reinforceing_bar_dia
        self.top_y_reinforceing_bar_dis = entity_object.top_y_reinforceing_bar_dis

        self.top_bear_reinforceing_dia = entity_object.top_bear_reinforceing_dia
        self.top_bear_reinforceing_dis = entity_object.top_bear_reinforceing_dis

    # # 跨图框属性获取
    # def get_cross_border_attribs(self, border_entity, building_object):
    #     self._get_attribs(building_object, border_entity)
