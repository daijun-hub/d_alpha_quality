import cv2

from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity
from ....config_manager.architecture.drawing_config import DrawingType
from ...utils.utils_space import get_labeled_height_architecture, get_contour_perimeter, \
    get_space_related_nonbear_wall_list, get_space_related_door, get_space_related_entity_by_extend_entity_bbox


class YanHuiDaTing(Space):
    chinese_name = "宴会大厅"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "宴会大厅"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE

    def get_related_entities(self, border_entity):
        """
        获取相关的构件
        :param border_entity:
        :return:
        """
        # 获取关联墙体
        self.related_wall = get_space_related_nonbear_wall_list(self, border_entity)

        # 获取关联门
        self.related_door = get_space_related_door(self, border_entity)