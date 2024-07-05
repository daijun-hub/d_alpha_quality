import cv2

from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity
from ....config_manager.architecture.drawing_config import DrawingType
from ...utils.utils_space import get_labeled_height_architecture, get_contour_perimeter, \
    get_space_related_nonbear_wall_list, get_space_related_door, get_space_related_entity_by_extend_entity_bbox


class DaTang(Space):
    chinese_name = "大堂"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "大堂"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE       # 对象父类
        # 标高数值属性
        self.labeled_height = get_labeled_height_architecture(self.contour.contour, border_entity)

        self.lobby_type = self.get_stair_room_type(border_entity)

        # 获取空间长度、宽度、周长
        # cv2.minAreaRect ==>（最小外接矩形的中心（x，y），（宽度，高度），旋转角度）
        # theta是由x轴逆时针转至W(宽)的角度，[-90,0)
        (cx, cy), (w, h), theta = cv2.minAreaRect(self.contour.contour)
        self.space_length = max(w, h)
        self.space_width = min(w, h)
        self.space_perimeter = get_contour_perimeter(self.contour.contour)

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

        # 获取关联窗
        window_list = ["普通窗", "凸窗", "转角窗"]
        self.related_window = []
        for window_name in window_list:
            self.related_window.extend(get_space_related_entity_by_extend_entity_bbox(self, border_entity, window_name))

        # 获取关联孔洞
        self.related_hole = get_space_related_entity_by_extend_entity_bbox(self, border_entity, "墙洞口")

        # 开敞属性
        self.open_type = self._judge_open_attr()

    def _judge_open_attr(self):
        open_type = "开敞"
        for window in self.related_window:
            if window.window_is_outside:
                open_type = "封闭"
                break
        return open_type
    def get_stair_room_type(self, border_entity):
        """大堂细分类型
        ① 图纸类型为住宅首层平面图或住宅二三层平面图或住宅非首层平面图，该属性值为住宅大堂
        ② 图纸类型为地下车库平面图，该属性值为地下车库大堂
        """
        if border_entity.drawing_type in [DrawingType.INDOOR_FIRST_FLOOR, DrawingType.SECOND_THIRD_FLOOR,
                                          DrawingType.INDOOR]:
            return "住宅大堂"
        elif border_entity.drawing_type in [DrawingType.UNDERGROUND]:
            return "地下车库大堂"


if __name__ == "__main__":
    a = Space(None, None, ["None", "None"], None)
    b = DaTang(a)
    print(b)
