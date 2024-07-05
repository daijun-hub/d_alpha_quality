from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils import *
from ....common.utils2 import load_drawing_pkl
from shapely.geometry import LineString, Polygon, MultiLineString, Point
from ....config_manager.structure.drawing_config import DrawingType as drawing_type_structure


class JieGouQiangShen(ClassifiedEntity):
    chinese_name = "结构墙身"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        self.chinese_name = "结构墙身"
        self.name_number = get_qiangshen_number(entity_object, border_entity)  # 墙身编号
        self.wall_thickness = None  #
        self.horiz_distribute_bar_dia = []  # 水平分布筋直径
        self.horiz_distribute_bar_dist = []  # 水平分布筋距离
        self.vertical_distribute_bar_dia = []  # 垂直分布筋直径
        self.vertical_distribute_bar_dist = []  # 垂直分布筋距离

    def get_cross_border_attribs(self, border_entity, building_object):
        self._get_qiangshen_attribs(border_entity, building_object)  # 更新墙身的 水平分布筋直径，水平分布筋距离，垂直分布筋直径，垂直分布筋距离

    def _get_qiangshen_attribs(self, border_entity, building_object):
        ratio = border_entity.ratio
        extend_range = int(1000 * ratio[0])
        if self.name_number is None:
            print('Note: qiangshen name number not found !!')
        else:
            # 获取该图纸中的表格
            biaoge_list = border_entity.entity_object_dict['表格']
            all_text_info = border_entity.border_text_info[TextType.ALL]
            qsb_text_list = [text for text in all_text_info if re.search('墙身表', text.extend_message)]
            all_qh_text_list = [text for text in all_text_info if re.search('墙厚', text.extend_message)]
            all_qhnum_text_list = [text for text in all_text_info if re.search('[1-9]{2,3}', text.extend_message)]
            all_hori_bar_text_list = [text for text in all_text_info if re.search('水平.*筋', text.extend_message)]
            all_vert_bar_text_list = [text for text in all_text_info if re.search('[竖垂].*筋', text.extend_message)]
            all_bar_text_list = [text for text in all_text_info if re.search('%%132[0-9]@[0-9]', text.extend_message)]
            candidate_name_number_list = [text for text in all_text_info if self.name_number == text.extend_message]
            target_found = False
            for biaoge in biaoge_list:
                biaoge_bbox = biaoge.bounding_rectangle.list
                biaoge_ext_bbox = [biaoge_bbox[0] - extend_range, biaoge_bbox[1] - extend_range,
                                   biaoge_bbox[2] + extend_range, biaoge_bbox[3] + extend_range]
                text_list = [text for text in qsb_text_list if Iou_temp(biaoge_ext_bbox, text.bbox.list) > 0]
                if len(text_list) > 0:
                    print('Note: 在该图纸中找到墙身表')
                    # 找到该表格中所需要的文本
                    name_number_list = [text for text in candidate_name_number_list if Iou_temp(biaoge_ext_bbox, text.bbox.list) > 0]
                    if len(name_number_list) == 0:
                        continue
                    target_found = True
                    qh_text_list = [text for text in all_qh_text_list if Iou_temp(biaoge_ext_bbox, text.bbox.list) > 0]
                    hori_bar_text_list = [text for text in all_hori_bar_text_list if Iou_temp(biaoge_ext_bbox, text.bbox.list) > 0]
                    vert_bar_text_list = [text for text in all_vert_bar_text_list if Iou_temp(biaoge_ext_bbox, text.bbox.list) > 0]
                    name_number = name_number_list[0]
                    if len(qh_text_list) > 0:
                        qh_text = qh_text_list[0]
                        intersect_bbox = get_intersect_area_table(name_number.bbox.list, qh_text.bbox.list, biaoge_bbox)
                        if intersect_bbox is not None:
                            for qhnum_text in all_qhnum_text_list:
                                if Iou_temp(intersect_bbox, qhnum_text.bbox.list) > 0:
                                    self.wall_thickness = eval(qhnum_text.extend_message)
                                    print('---> wall thickness found: ', self.wall_thickness)
                                    break

                    if len(hori_bar_text_list) > 0:
                        hori_bar_text = hori_bar_text_list[0]
                        intersect_bbox_hori = get_intersect_area_table(name_number.bbox.list, hori_bar_text.bbox.list, biaoge_bbox)
                        if intersect_bbox_hori is not None:
                            for bar_text in all_bar_text_list:
                                if Iou_temp(intersect_bbox_hori, bar_text.bbox.list) > 0:
                                    self.horiz_distribute_bar_dia, self.horiz_distribute_bar_dist = \
                                        get_qiangshen_bar_info(bar_text)
                                    print('---> horiz_distribute_bar_dia found: ', self.horiz_distribute_bar_dia)
                                    print('---> horiz_distribute_bar_dist found: ', self.horiz_distribute_bar_dist)
                                    break

                    if len(vert_bar_text_list) > 0:
                        vert_bar_text = vert_bar_text_list[0]
                        intersect_bbox_vert = get_intersect_area_table(name_number.bbox.list, vert_bar_text.bbox.list,
                                                                       biaoge_bbox)
                        if intersect_bbox_vert is not None:
                            for bar_text in all_bar_text_list:
                                if Iou_temp(intersect_bbox_vert, bar_text.bbox.list) > 0:
                                    self.vertical_distribute_bar_dia, self.vertical_distribute_bar_dist = \
                                        get_qiangshen_bar_info(bar_text)
                                    print('---> vertical_distribute_bar_dia found: ', self.vertical_distribute_bar_dia)
                                    print('---> vertical_distribute_bar_dist found: ', self.vertical_distribute_bar_dist)
                                    break
            # 跨图获取属性
            if target_found is False:
                WALL_COLUMN_DETAILS_list = []
                for special_drawing_dict in building_object.special_drawing_list:
                    for drawing_type, info_dict in special_drawing_dict.items():
                        file_id = info_dict['file_id']
                        if drawing_type == drawing_type_structure.WALL_COLUMN_DETAILS:
                            WALL_COLUMN_DETAILS_list.append(file_id)
                for WALL_COLUMN_DETAILS_id in WALL_COLUMN_DETAILS_list:
                    border_entity_info = load_drawing_pkl(WALL_COLUMN_DETAILS_id)
                    ratio = border_entity_info.ratio
                    # 获取该图纸中的表格
                    biaoge_list = border_entity_info.entity_object_dict['表格']
                    all_text_info = border_entity_info.border_text_info[TextType.ALL]
                    qsb_text_list = [text for text in all_text_info if re.search('墙身表', text.extend_message)]
                    all_qh_text_list = [text for text in all_text_info if re.search('墙厚', text.extend_message)]
                    all_qhnum_text_list = [text for text in all_text_info if
                                           re.search('[1-9]{2,3}', text.extend_message)]
                    all_hori_bar_text_list = [text for text in all_text_info if re.search('水平.*筋', text.extend_message)]
                    all_vert_bar_text_list = [text for text in all_text_info if
                                              re.search('[竖垂].*筋', text.extend_message)]
                    all_bar_text_list = [text for text in all_text_info if
                                         re.search('%%132[0-9]@[0-9]', text.extend_message)]
                    candidate_name_number_list = [text for text in all_text_info if
                                                  self.name_number == text.extend_message]
                    for biaoge in biaoge_list:
                        biaoge_bbox = biaoge.bounding_rectangle.list
                        biaoge_ext_bbox = [biaoge_bbox[0] - extend_range, biaoge_bbox[1] - extend_range,
                                           biaoge_bbox[2] + extend_range, biaoge_bbox[3] + extend_range]
                        text_list = [text for text in qsb_text_list if Iou_temp(biaoge_ext_bbox, text.bbox.list) > 0]
                        if len(text_list) > 0:
                            print('Note: 在该图纸中找到墙身表')
                            # 找到该表格中所需要的文本
                            name_number_list = [text for text in candidate_name_number_list if
                                                Iou_temp(biaoge_ext_bbox, text.bbox.list) > 0]
                            if len(name_number_list) == 0:
                                continue
                            qh_text_list = [text for text in all_qh_text_list if
                                            Iou_temp(biaoge_ext_bbox, text.bbox.list) > 0]
                            hori_bar_text_list = [text for text in all_hori_bar_text_list if
                                                  Iou_temp(biaoge_ext_bbox, text.bbox.list) > 0]
                            vert_bar_text_list = [text for text in all_vert_bar_text_list if
                                                  Iou_temp(biaoge_ext_bbox, text.bbox.list) > 0]
                            name_number = name_number_list[0]
                            if len(qh_text_list) > 0:
                                qh_text = qh_text_list[0]
                                intersect_bbox = get_intersect_area_table(name_number.bbox.list, qh_text.bbox.list,
                                                                          biaoge_bbox)
                                if intersect_bbox is not None:
                                    for qhnum_text in all_qhnum_text_list:
                                        if Iou_temp(intersect_bbox, qhnum_text.bbox.list) > 0:
                                            self.wall_thickness = eval(qhnum_text.extend_message)
                                            print('---> wall thickness found: ', self.wall_thickness)
                                            break

                            if len(hori_bar_text_list) > 0:
                                hori_bar_text = hori_bar_text_list[0]
                                intersect_bbox_hori = get_intersect_area_table(name_number.bbox.list,
                                                                               hori_bar_text.bbox.list, biaoge_bbox)
                                if intersect_bbox_hori is not None:
                                    for bar_text in all_bar_text_list:
                                        if Iou_temp(intersect_bbox_hori, bar_text.bbox.list) > 0:
                                            self.horiz_distribute_bar_dia, self.horiz_distribute_bar_dist = \
                                                get_qiangshen_bar_info(bar_text)
                                            print('---> horiz_distribute_bar_dia found: ',
                                                  self.horiz_distribute_bar_dia)
                                            print('---> horiz_distribute_bar_dist found: ',
                                                  self.horiz_distribute_bar_dist)
                                            break

                            if len(vert_bar_text_list) > 0:
                                vert_bar_text = vert_bar_text_list[0]
                                intersect_bbox_vert = get_intersect_area_table(name_number.bbox.list,
                                                                               vert_bar_text.bbox.list,
                                                                               biaoge_bbox)
                                if intersect_bbox_vert is not None:
                                    for bar_text in all_bar_text_list:
                                        if Iou_temp(intersect_bbox_vert, bar_text.bbox.list) > 0:
                                            self.vertical_distribute_bar_dia, self.vertical_distribute_bar_dist = \
                                                get_qiangshen_bar_info(bar_text)
                                            print('---> vertical_distribute_bar_dia found: ',
                                                  self.vertical_distribute_bar_dia)
                                            print('---> vertical_distribute_bar_dist found: ',
                                                  self.vertical_distribute_bar_dist)
                                            break
















