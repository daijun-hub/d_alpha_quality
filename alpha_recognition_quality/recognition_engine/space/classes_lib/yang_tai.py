from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity

from ....common.utils_draw_and_rule import get_balcony_type, get_balcony_width_depth
from ...utils.utils_space import get_space_related_entity
from ....config_manager.architecture.drawing_config import DrawingType as DrawingTypeArchi
from ....common.utils import expand_contour, get_contours_iou, get_contour_from_bbox
from ....common.utils2 import load_drawing_pkl


class YangTai(Space):
    chinese_name = "阳台"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "阳台"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE

        # 阳台细分类型, 封闭或开敞
        self.balcony_type = get_balcony_type(self.bbox.list, border_entity)
        # 阳台净宽度, 净进深
        self.balcony_width, self.balcony_depth = get_balcony_width_depth(self.contour.contour, border_entity)

        # 标准层图框表达的不仅仅是一层
        self.floor = border_entity.floor_num_list
        self.is_refuge_space = False
        self.is_close_space = True if self.balcony_type == '封闭阳台' else False

    def get_related_entities(self, border_entity):
        """
        获取相关的构件
        :param border_entity:
        :return:
        """
        # 阳台雨水立管
        entities_name = ['阳台雨水立管', '地漏']
        for entity_name in entities_name:
            self.related_entities_dict[entity_name] = get_space_related_entity(self, border_entity, entity_name)

        self._get_related_wall(border_entity)
        self._get_related_door(border_entity)
        self._get_related_window(border_entity)
        self._get_related_hole(border_entity)

        self.deng_ju_list = self.get_related_entity(border_entity, "灯具")
        self.pu_tong_deng_list = self.get_related_entity(border_entity, "普通灯")

    def _get_related_wall(self, border_entity):
        related_wall = []
        nobear_wall_list = border_entity.entity_object_dict.get('墙', [])
        balcony_cnt_ext = expand_contour(self.contour.contour, 10)
        for nobear_wall in nobear_wall_list:
            if get_contours_iou(balcony_cnt_ext, nobear_wall.contour.contour) > 0:
                related_wall.append(nobear_wall)

        self.related_wall = related_wall

    def _get_related_door(self, border_entity):
        related_door = []
        balcony_cnt_ext = expand_contour(self.contour.contour, 10)
        map_label = ["单开门", "双开门", "子母门", "门联窗", "推拉门"]
        for label in map_label:
            door_list = border_entity.entity_object_dict.get(label, [])
            for door in door_list:
                if get_contours_iou(balcony_cnt_ext, get_contour_from_bbox(door.bounding_rectangle.list)) > 0:
                    related_door.append(door)

        self.related_door = related_door

    def _get_related_window(self, border_entity):
        related_window = []
        balcony_cnt_ext = expand_contour(self.contour.contour, 10)
        map_label = ["普通窗", "凸窗", "转角窗"]
        for label in map_label:
            window_list = border_entity.entity_object_dict.get(label, [])
            for window in window_list:
                if get_contours_iou(balcony_cnt_ext, get_contour_from_bbox(window.bounding_rectangle.list)) > 0:
                    related_window.append(window)

        self.related_window = related_window

    def _get_related_hole(self, border_entity):
        related_hole = []
        hole_list = border_entity.entity_object_dict.get('墙洞口', [])
        balcony_cnt_ext = expand_contour(self.contour.contour, 10)
        for hole in hole_list:
            if get_contours_iou(balcony_cnt_ext, get_contour_from_bbox(hole.bounding_rectangle.list)) > 0:
                related_hole.append(hole)

        self.related_hole = related_hole

    def get_cross_border_attribs(self, border_entity, building_object):
        # 获取标高属性
        self._get_labeled_height(building_object)

    def _get_labeled_height(self, building_object):
        '''
        # 获取标高属性
        '''
        print("[Note] 获取户的楼层标高 ... ")
        # self.labeled_height
        for special_drawing_dict in building_object.special_drawing_list:
            section_border_dict = special_drawing_dict.get(DrawingTypeArchi.SECTION, None)
            elevation_border_dict = special_drawing_dict.get(DrawingTypeArchi.ELEVATION, None)
            side_elevation_border_dict = special_drawing_dict.get(DrawingTypeArchi.SIDE_ELEVATION, None)
            if section_border_dict is not None:
                section_file_id = section_border_dict.get("file_id", None)
            elif elevation_border_dict is not None:
                section_file_id = elevation_border_dict.get("file_id", None)
            elif side_elevation_border_dict is not None:
                section_file_id = side_elevation_border_dict.get("file_id", None)
            else:
                section_file_id = None
            if section_file_id is not None:
                section_border_entity = load_drawing_pkl(section_file_id)
                # 获取层高信息
                floor_r_height_dict = section_border_entity.special_info_dict.get("floor_r_height", None)
                print("floor_r_height_dict", floor_r_height_dict)
                if floor_r_height_dict is not None:
                    floor_num = None
                    for f in self.floor:
                        if f.isdigit():
                            floor_num = int(f)
                            break
                    print("[Note] floor num ", floor_num)
                    self.labeled_height = floor_r_height_dict[floor_num] if floor_num in floor_r_height_dict else 0.
                    self.labeled_height_file_id = section_border_entity.cad_border_id
                    self.labeled_height_pickle_id = section_file_id
            # print("labeled_height", self.labeled_height)

    def get_related_entity(self, border_entity, entity_name, min_iou=0.5):
        """
        根据构件名字获取构件列表
        Args:
            border_entity:
            entity_name:
            min_iou:

        Returns:

        """
        related_entity_list = []
        entity_list = border_entity.entity_object_dict.get(entity_name, [])
        for entity_obj in entity_list:
            bbox = entity_obj.bounding_rectangle.list
            cnt = get_contour_from_bbox(bbox)
            if get_contours_iou(expand_contour(self.contour.contour, 400 * border_entity.ratio[0]), cnt) > min_iou:
                related_entity_list.append(entity_obj)
        return related_entity_list

