import re

from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils import *
from ....config_manager.architecture.drawing_config import DrawingType as drawing_type_architecture
from ....common.utils2 import load_drawing_pkl


class QiangDongKou(ClassifiedEntity):
    chinese_name = "墙洞口"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        self.chinese_name = "墙洞口"
        self.entity_base_type = EntityBaseType.HOLE
        # 构件轮廓
        self.contour = self.get_contour(border_entity)
        # 定义构件在户空间相对于户中心和入户门的土建连线中点为极轴逆时针的夹脚
        self.angle_against_apartment = None
        # 到户中心的距离
        self.dist_to_apartment_centroid = None
        # 定义构件在所属空间相对于所在空间中心和门的土建连线中点为极轴逆时针的夹脚
        self.angle_against_room = None
        # 到所属空间中心的距离
        self.dist_to_room_centroid = None
        # 通过引线标注来判断类别 KPBQ
        self.hole_type = self.judge_hole_type(border_entity)
        # 跨图框属性
        self.floor_distance = None
        self.wall_distance = None
        # 构件位置(即为构件中心线与墙线的交点), 关联墙
        self.position, self.related_wall = self.get_position(border_entity)
        # 构件所在楼层
        self.floor = self.get_floor(border_entity)
        # 构件长度,构件高度
        self.length, self.height = self.get_length_and_height(border_entity)
        # 中心距地高度
        self.height_above_ground = self.get_height_above_ground(border_entity)
        # 洞口面积
        self.hole_area = self.get_hole_area(border_entity)

    def get_contour(self, border_entity):
        contour = None
        contour = get_contour_from_bbox(remove_margin(self.bounding_rectangle.list))
        return contour

    def get_cross_border_attribs(self, border_entity, building_object):
        # 通过设计说明图来找到预留孔洞距所依墙边距离数值
        # self._get_wall_distance(building_object)
        # 预留孔洞中心”距本层楼板距离”数值
        self._get_floor_distance(building_object)

    def _get_floor_distance(self, building_object):
        text_mark_list = []
        text_louban_list = []
        text_wall_list = []
        text_num_list = []
        for special_drawing_dict in building_object.special_drawing_list:
            for drawing_type, info_dict in special_drawing_dict.items():
                file_id = info_dict['file_id']
                if drawing_type == drawing_type_architecture.BUILDING_DESIGN:
                    bd_border_entity = load_drawing_pkl(file_id)
                    ratio = bd_border_entity.ratio
                    text_all = bd_border_entity.border_text_info[TextType.ALL]
                    for text in text_all:
                        if re.search(''.join(self.lead_mark), text.extend_message):
                            text_mark_list.append(text)
                        if re.search(".*本层楼板", text.extend_message):
                            text_louban_list.append(text)
                        if re.search(".*墙边", text.extend_message):
                            text_wall_list.append(text)
                        if re.search("^[0-9]\d*$", text.extend_message):
                            text_num_list.append(text)
                    for text_mark in text_mark_list:
                        for text_louban in text_louban_list:
                            if Iou_temp([text_mark.bbox.list[0], text_mark.bbox.list[1],
                                         text_mark.bbox.list[2] + 8000 * ratio[0], text_mark.bbox.list[3]],
                                        text_louban.bbox.list):
                                for text_num in text_num_list:
                                    if Iou_temp([text_louban.bbox.list[0], text_louban.bbox.list[1],
                                                 text_louban.bbox.list[2] + 2300 * ratio[0], text_louban.bbox.list[3]],
                                                text_num.bbox.list):
                                        self.floor_distance = text_num
                                        self.floor_cad_id = bd_border_entity.cad_border_id
                                        self.floor_pickle_id = file_id
                                        break
                            if self.floor_distance != None:
                                break
                        for text_wall in text_wall_list:
                            if Iou_temp([text_mark.bbox.list[0], text_mark.bbox.list[1],
                                         text_mark.bbox.list[2] + 8000 * ratio[0], text_mark.bbox.list[3]],
                                        text_wall.bbox.list):
                                for text_num in text_num_list:
                                    if Iou_temp([text_wall.bbox.list[0], text_wall.bbox.list[1],
                                                 text_wall.bbox.list[2] + 2300 * ratio[0], text_wall.bbox.list[3]],
                                                text_num.bbox.list):
                                        self.wall_distance = text_num
                                        self.floor_cad_id = bd_border_entity.cad_border_id
                                        self.floor_pickle_id = file_id
                                        break
                                if self.wall_distance != None:
                                    break

    # def _get_wall_distance(self, building_object):
    #     text_mark = []
    #     for drawing_type, info_dict in building_object.special_drawing_dict.items():
    #         file_id = info_dict['file_id']
    #         if drawing_type == drawing_type_architecture.BUILDING_DESIGN:
    #             bd_border_entity = load_drawing_pkl(file_id)
    #             text_all = bd_border_entity.border_text_info[TextType.ALL]
    #             for text in text_all:
    #                 if re.search(self.lead_mark, text.extend_message):
    #                     text_mark.append(text)

    def judge_hole_type(self, border_entity):
        hole_type = None
        bbox = self.bounding_rectangle.list
        # 获取引线
        anno_line_list = border_entity.special_info_dict['annotation_info_list']
        for line_l, text_l, main_end_point in anno_line_list:
            main_line = line_l[0]
            branch_list = line_l[1:]
            if hole_type != None:
                break
            if Iou_temp(extend_margin(main_line), bbox):
                for text in text_l:
                    if re.search('K', text):
                        hole_type = 'K'
                        break
                    elif re.search('P', text):
                        hole_type = 'P'
                        break
                    elif re.search('B', text):
                        hole_type = 'B'
                        break
                    elif re.search('Q', text):
                        hole_type = 'Q'
                        break
        return hole_type

    def get_position(self, border_entity):
        position = None
        related_wall = None
        wall_window_list = []
        for key, entity_list in border_entity.entity_combination_result.items():
            if re.search('wall|window|door|chuang', key):
                for entity in entity_list:
                    wall_window_list.append(entity[:4])
        for wall in wall_window_list:
            wall_contour = get_contour_from_bbox(wall)
            dong_contour = get_contour_from_bbox(self.bounding_rectangle.list)
            if get_contours_iou(wall_contour, dong_contour):
                related_wall = wall
                wall_poly = Polygon(wall_contour.squeeze())
                dong_poly = Polygon(dong_contour.squeeze())
                cross_point_list = get_cross_point_list_pre(wall_poly, dong_poly)
                if len(cross_point_list) == 1:
                    position = cross_point_list[0]
                    break
        if position is None:
            print("None")
        return position, related_wall

    def get_floor(self, border_entity):
        floor = border_entity.floor_num_list
        return floor

    def get_length_and_height(self, border_entity):
        length = None
        height = None
        annotation_list = border_entity.mark_object_dict['引注']
        for anno in annotation_list:
            anno_contour_extend = get_contour_from_bbox(extend_margin(anno.bounding_rectangle.list))
            if get_contours_iou(anno_contour_extend, self.contour):
                anno_text = ''.join(anno.labeled_text)
                if anno_text:
                    if re.search('宽', anno_text[0]):
                        length = re.findall(r'宽:?(\d*)mm', anno_text)
                    if re.search('高', anno_text[0]):
                        height = re.findall(r'高:?(\d*)mm', anno_text)
        return length, height

    def get_height_above_ground(self, border_entity):
        height_above_ground = None
        annotation_list = border_entity.mark_object_dict['引注']
        for anno in annotation_list:
            anno_contour_extend = get_contour_from_bbox(extend_margin(anno.bounding_rectangle.list))
            if get_contours_iou(anno_contour_extend, self.contour):
                anno_text = ''.join(anno.labeled_text)
                if anno_text:
                    if re.search('距地', anno_text):
                        height_above_ground = re.findall(r'距地:?(\d*)mm', anno_text)
        return height_above_ground

    def get_hole_area(self, border_entity):
        hole_area = None
        annotation_list = border_entity.mark_object_dict['引注']
        for anno in annotation_list:
            anno_contour_extend = get_contour_from_bbox(extend_margin(anno.bounding_rectangle.list))
            if get_contours_iou(anno_contour_extend, self.contour):
                anno_text = ''.join(anno.labeled_text)
                if anno_text:
                    if re.search('半径', anno_text):
                        radius = int(''.join(re.findall(r'半径:?(\d*)mm', anno_text)))
                        hole_area = format(3.14*(radius*radius), '.2f')
        return hole_area
