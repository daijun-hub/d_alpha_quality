# -*- coding: utf-8 -*-
import os
from collections import defaultdict
import json
from typing import Dict, List, Tuple, Union
from pathlib import Path
from PIL.Image import Image
from numpy import ndarray

from .base.bounding_vertex import BoundingVertex
from ..common.CONSTANTS import IMG_WITH_WALL_KEY
from ..common.image_manager import ImageManager
from .entity.text.text import TextEntity, TextEntityWithBoundVertex
from .base.bounding_rectangle import BoundingRectangle
from .base.contour import Contour
from .base.line import Line
from .entity.entity import GraphicBasicEntity, Entity
from .space.space import Space
from .mark.mark import Mark
from ..config_manager.architecture.drawing_config import DrawingType as DrawingTypeArch
from ..config_manager.electric.drawing_config import DrawingType as DrawingTypeElec
from ..config_manager.plumbing.drawing_config import DrawingType as DrawingTypePlum
from ..config_manager.hvac.drawing_config import DrawingType as DrawingTypeHvac
from ..config_manager.structure.drawing_config import DrawingType as DrawingTypeStruct
from ..common.utils import Iou_temp, extend_margin
from ..common.utils2 import get_building_floor_info, upload_drawing_pkl
from ..design_object.cad_base.cad_basic_entity_type import CADBasicEntityType
from ..analysis_engine.utils.utils_integration import build_room_graph_pre, get_household_list_pre


class BorderEntity(object):

    def __init__(self,
                 major,
                 drawing_type,
                 drawing_name: str,
                 floor_num_list: List[str],
                 space_name: str,
                 space_scale: float,
                 border_coord: List[float],
                 ext_margin: int,
                 ratio: Tuple[float],
                 subproject_name: str,
                 subproject_num_list: List[str],
                 entity_bbox_list: List[Entity],
                 entity_combination_result: Dict[str, List[BoundingRectangle]],
                 origin_border_entity_info: Dict[str, List[GraphicBasicEntity]],
                 room_info: List[Space],
                 border_text_info: Dict[str, List[TextEntity]],
                 border_text_info_with_bound_vertex: Dict[str, List[TextEntityWithBoundVertex]],
                 image_manager: ImageManager,
                 parking_bbox_coord,
                 entity_class_dict,
                 entity_score_dict,
                 wall_contour: List[Contour],
                 border_style_info,
                 door_base_coords: List[Line],
                 single_line_door_window_list: List[Line],
                 small_room_contours: List[Contour],
                 parking_contour_dict: Dict[tuple, ndarray],
                 axis_net_bbox_list: List,
                 axis_net_line_list: List,
                 axis_net_line_num_list: List[str],
                 axis_net_line_deg_list: List[int],
                 sheet_information: List,
                 subdrawing_list: List,
                 special_info_dict: Dict,
                 cad_border_id: str,
                 layout_name: str,
                 no_bear_wall_bbox_cnt_list: List[Contour],
                 bear_wall_bbox_cnt_list: List[Contour],
                 entity_bbox_contour_dict,
                 ):
        self.major = major  # 专业
        self.drawing_type = drawing_type  # 图纸类型
        self.drawing_name = drawing_name  # 图框名称
        self.floor_num_list = floor_num_list  # 楼层列表
        self.space_name = space_name  # 所在空间名，layout_name同义
        self.space_scale = space_scale  # CAD->现实长度单位转换比例
        self.border_coord = border_coord  # CAD的图框坐标
        self.ext_margin = ext_margin  # 图框的外扩bbox
        self.ratio = ratio  # CAD->PNG单位转换比例
        self.subproject_name = subproject_name  # 图框子项名
        self.subproject_num_list = subproject_num_list  # 子项列表
        self.entity_bbox_list = entity_bbox_list  # 图框的构件列表，combined from (entity_bbox_list, entity_class_list, entity_ori_class_list, entity_score_list, entity_coord_list)
        self.entity_combination_result = entity_combination_result  # 构件合并结果，was entity_bbox_dict
        self.origin_border_entity_info = origin_border_entity_info  # 构件原始图元（已转换成PNG坐标）
        self.room_info = room_info  # 图框的空间列表，combined from (room_info, small_room_info)
        self.border_text_info = border_text_info  # 图框的文本列表
        self.border_text_info_with_bound_vertex = border_text_info_with_bound_vertex  # 图框的文本bound_vertex列表
        self.image_manager = image_manager  # 图片管理器
        self.parking_bbox_coord = parking_bbox_coord  # 车位字典
        self.entity_class_dict = entity_class_dict  # 字典，key为图层，value为该图层的构件类别列表
        self.entity_score_dict = entity_score_dict  # 字典，key为图层，value为该图层的构件类别得分
        self.wall_contour = wall_contour  # 列表，墙轮廓的列表
        self.border_style_info = border_style_info  # 字典，key为图层，value为该图层的 entity_bbox + cad_class + extendMsg + entity_style
        self.door_base_coords = door_base_coords  # 列表，包含所有的土建连线
        self.single_line_door_window_list = single_line_door_window_list  # 列表，包含所有的单独门窗直线图元
        self.small_room_contours = small_room_contours  # 列表，包含所有的小空间轮廓
        self.parking_contour_dict = parking_contour_dict  # 字段，包含所有的车位contour的字典
        self.axis_net_bbox_list = axis_net_bbox_list  # 处理后的轴网bbox列表，【bbox1, bbox2, ...】
        self.axis_net_line_list = axis_net_line_list  # 处理后的所有轴线列表, [line1, line2, ...]
        self.axis_net_line_num_list = axis_net_line_num_list  # 处理后的所有轴线轴号列表, [轴号1(str), 轴号2(str), ...]
        self.axis_net_line_deg_list = axis_net_line_deg_list  # 处理后的所有轴线方位角列表, [轴线1方位角(int), 轴线2方位角(int), ...]
        self.sheet_information = sheet_information  # 图框表格提取结果
        self.subdrawing_list = subdrawing_list  # 图框的子图列表 [[x1, y1, x2, y2, ''], ...]
        self.special_info_dict = special_info_dict  # 保存了规则中用到的特殊信息的字典
        self.updated_space_dict = {}
        self.cad_border_id = cad_border_id  # cad的解析id，碧桂园规则返回用
        self.layout_name = layout_name  # 图框底图id
        self.base_png_id = ""  # 底图id
        self.no_bear_wall_bbox_cnt_list = no_bear_wall_bbox_cnt_list  # 非承重墙
        self.bear_wall_bbox_cnt_list = bear_wall_bbox_cnt_list  # 承重墙
        self.entity_bbox_contour_dict = entity_bbox_contour_dict                        # 合并构件的bbox和contour映射

    @classmethod
    def read_from_dict(cls, border_entity_info):
        """
        读取图框信息字典，并将字典中存储的信息存入BorderEntity对象实例中
        Args:
            border_entity_info: 存储图框信息以及其构件等信息的字典

        Returns:
            对象化后的BorderEntity对象实例
        """
        # BorderEntity members
        major = border_entity_info["major"]
        drawing_type = border_entity_info["drawing_type"]
        drawing_name = border_entity_info["drawing_name"]
        space_name = border_entity_info["space_name"]
        layout_name = border_entity_info.get("layout_name", "")
        space_scale = border_entity_info["space_scale"]
        border_coord = border_entity_info["border_coord"]
        ext_margin = border_entity_info["ext_margin"]
        ratio = border_entity_info["ratio"]
        subproject_name = border_entity_info["subproject_name"]
        cad_border_id = border_entity_info['cad_border_id']

        # 通过图框名称获取该图框的楼层信息，通过图框名称和子项名称获取该图框的子项信息（存在图框名称中明确了子项信息，但子项名称中比较笼统的情况）
        # 楼层格式有：[2]、[8, 6, 7]、[3, '屋顶']、[3, 4, 5, 6, 7, 8, 9, '屋面']、['标准']、['机房']，所以存在整型和字符串并存的情况
        # 楼层信息为空：设计说明、材料表可能不包含楼层信息，整个项目共用一个设计说明、材料表
        # 子项格式有：['1']、['9', '12', '6']、['1B']、['A']、['S1']、['综合楼']、['门楼']、['临建板房']
        # 子项信息为空：设计说明、材料表可能不包含子项信息，整个项目共用一个设计说明或材料表
        subproject_num_list, floor_num_list = get_building_floor_info(subproject_name, drawing_name)

        entity_list = []
        entity_combination_result = {}
        parking_contour_result = {}
        origin_border_entity_info = {}
        room_list = []
        text_info = {}
        text_info_bound_vertex = {}
        wall_contour_info = []
        door_base_info = []
        single_line_door_window_info = []
        small_room_contour_info = []

        # 保存一些特殊信息的字典
        special_info_dict = {}

        # 轴网解析信息
        axis_net_bbox_list = border_entity_info.get("axis_net_bbox_list", [])
        axis_net_line_list = border_entity_info.get('axis_net_line_list', [])
        axis_net_line_num_list = border_entity_info.get('axis_net_line_num_list', [])
        axis_net_line_deg_list = border_entity_info.get('axis_net_line_deg_list', [])

        # 解析的表格文本信息
        sheet_information = border_entity_info.get("border_information", [])

        # 解析子图信息
        subdrawing_list = border_entity_info.get("subdrawing_list", [])

        # **** entity_list ****

        entity_bbox_dict = border_entity_info.get("entity_bbox_dict", {})
        parking_cnt_dict = entity_bbox_dict.get('parking_contour_dict', {})
        cabinet_cnt_dict = entity_bbox_dict.get('cabinet_contour_dict', {})
        transformer_cnt_dict = entity_bbox_dict.get('transformer_contour_dict', {})
        transformer_cabinet_cnt_dict = cabinet_cnt_dict.copy()
        transformer_cabinet_cnt_dict.update(transformer_cnt_dict)
        dist_box_num_dict = border_entity_info.get('distribution_box_num_dict', {})
        e_window_open_area_dict = border_entity_info.get('elevation_window_open_area_dict', {})
        e_window_num_dict = border_entity_info.get('elevation_window_num_dict', {})
        door_orientation_info_dict = border_entity_info.get("door_orientation_info_dict", {})
        entity_bbox_contour_dict = border_entity_info.get("entity_bbox_contour_dict", {})
        gutter_cont_bbox_list = entity_bbox_dict.get('gutter_cont_bbox_list', [])
        sanshui_cont_bbox_list = entity_bbox_dict.get('sanshui_cont_bbox_list', [])

        # 分类构件
        entity_bbox_list = border_entity_info.get("entity_bbox_list", [])
        entity_class_list = border_entity_info.get("entity_class_list", [])
        entity_annotation_list = border_entity_info.get("entity_annotation_list", [])
        if len(entity_annotation_list) == 0:
            entity_annotation_list = [[]] * len(entity_class_list)
        entity_ori_class_list = border_entity_info.get("entity_ori_class_list", [])
        entity_score_list = border_entity_info.get("entity_score_list", [])
        entity_coord_list = border_entity_info.get("entity_coord_list", [])

        if entity_bbox_list:
            checked_entity_info_list = cls.nodup_entity_by_bbox(entity_bbox_list, entity_class_list,
                                                                entity_ori_class_list, entity_score_list,
                                                                entity_coord_list, entity_annotation_list)
            for bbox, c, ori_class, score, CAD_coord, anno_list in checked_entity_info_list:
                b = BoundingRectangle(bbox)
                cad_b = BoundingRectangle(CAD_coord)
                e = Entity(c, b, cad_b, ori_class, score, anno_list)
                if c in ['cd_parking', 'wza_cd_parking', 'wza_parking', 'normal_parking', 'truck_parking', 'parking']:
                    cnt = parking_cnt_dict.get(tuple(bbox), [])
                    if type(cnt) is not list:
                        e.contour = cnt
                if c == 'distribution_cabinet':
                    cnt = transformer_cabinet_cnt_dict.get(tuple(bbox), [])
                    if type(cnt) is not list:
                        e.contour = cnt
                if c == 'transformer':
                    cnt = transformer_cabinet_cnt_dict.get(tuple(bbox), [])
                    if type(cnt) is not list:
                        e.contour = cnt
                if c == 'distribution_box':
                    num = dist_box_num_dict.get(tuple(bbox), '')
                    e.electric_distribution_box_number = num
                if c == 'limianchuang':
                    open_area = e_window_open_area_dict.get(tuple(bbox), 0)
                    num = e_window_num_dict.get(tuple(bbox), [])
                    e.window_fan_shape_area = open_area
                    e.window_number = num
                if c in ["door", "menlianchuang", "others_m", "others_d", "tuila_door", "elevator_door"]:
                    door_orientation = door_orientation_info_dict.get(tuple(bbox), 'unknown')
                    e.door_orientation = door_orientation
                # 补充门窗类构件的contour，后面有其他构件的需求再添加
                if c in ['door', "single_door", "double_door", "unequal_double_door", 'elevator_door', 'tuila_door',
                         'sealed_door', 'juanlianmen', 'other_door',
                         'window', 'corner_window', 'tuchuang', 'baiye', 'elevation_window',
                         'limianchuang', 'other_window', 'guanjingmen', 'menlianchuang', 'renfang_door',
                         'zhexianchuang', 'bay_window', "others_m", "others_d"]:
                    door_contour = entity_bbox_contour_dict.get(tuple(extend_margin(bbox, ext_margin)), None)
                    if door_contour is not None:
                        e.contour = Contour(door_contour, ratio)

                entity_list.append(e)
                # print('--> classified entity class converted: {}'.format(c))
        # 排水管
        if gutter_cont_bbox_list:
            for contour, bbox in gutter_cont_bbox_list:
                b = BoundingRectangle(bbox)
                e = Entity("gutter", b, None, None, 1, None)
                e.contour = contour
                entity_list.append(e)
        # 散水
        if sanshui_cont_bbox_list:
            for sanshui in sanshui_cont_bbox_list:
                b = BoundingRectangle(sanshui)
                e = Entity("apron", b, None, None, 1, None)
                e.contour = None
                entity_list.append(e)

        # 结构相关构件
        structure_entity_dict = border_entity_info.get("structure_entity_dict", {})  # 结构相关构件和属性
        for entity_type, entity_info_list in structure_entity_dict.items():
            if entity_type in ['structure_beam']:  # 结构梁
                for entity_info in entity_info_list:
                    e = Entity(entity_type, BoundingRectangle(entity_info['bbox']), None, None, None, [],
                               Contour(entity_info['contour'], ratio))
                    e.beam_width = entity_info['beam_width']
                    e.beam_height = entity_info['beam_height']
                    e.beam_class = entity_info['beam_class']
                    e.beam_number = entity_info['beam_number']
                    e.kbmbHoop_diameter = entity_info['kbmbHoop_diameter']
                    e.kbmbHoop_distance = entity_info['kbmbHoop_distance']
                    e.kbmbHoop_limb = entity_info['kbmbHoop_limb']
                    e.kbmbJiaLi_number = entity_info['kbmbJiaLi_number']
                    e.kbmbJiaLi_diameter = entity_info['kbmbJiaLi_diameter']
                    e.kbmbNYao_number = entity_info['kbmbNYao_number']
                    e.kbmbNYao_diameter = entity_info['kbmbNYao_diameter']
                    e.kbmbGYao_number = entity_info['kbmbGYao_number']
                    e.kbmbGYao_diameter = entity_info['kbmbGYao_diameter']
                    e.kbmbTong_number = entity_info['kbmbTong_number']
                    e.kbmbTong_diameter = entity_info['kbmbTong_diameter']

                    entity_list.append(e)

            elif entity_type in ['structure_pillar']:  # 结构柱
                for entity_info in entity_info_list:
                    e = Entity(entity_type, BoundingRectangle(entity_info['bbox']), None, None, None, [],
                               Contour(entity_info['contour'], ratio))
                    e.pillar_number = entity_info['pillar_number']
                    e.pillar_type = entity_info['pillar_type']
                    e.angle_bar_dia = entity_info['angle_bar_dia']
                    e.angle_bar_num = entity_info['angle_bar_num']
                    e.Hside_middle_bar_dia = entity_info['Hside_middle_bar_dia']
                    e.Hside_middle_bar_num = entity_info['Hside_middle_bar_num']
                    e.Bside_middle_bar_dia = entity_info['Bside_middle_bar_dia']
                    e.Bside_middle_bar_num = entity_info['Bside_middle_bar_num']
                    e.Hside_stirrup_bodynum = entity_info['Hside_stirrup_bodynum']
                    e.Bside_stirrup_bodynum = entity_info['Bside_stirrup_bodynum']
                    e.dense_stirrup_dia = entity_info['dense_stirrup_dia']
                    e.dense_stirrup_dis = entity_info['dense_stirrup_dis']
                    e.Ndense_stirrup_dia = entity_info['Ndense_stirrup_dia']
                    e.Ndense_stirrup_dis = entity_info['Ndense_stirrup_dis']
                    e.node_core_stirrup_dia = entity_info['node_core_stirrup_dia']
                    e.node_core_stirrup_dis = entity_info['node_core_stirrup_dis']
                    e.longitud_bar_dia = entity_info['longitud_bar_dia']
                    e.longitud_bar_num = entity_info['longitud_bar_num']
                    e.cross_border_flag = entity_info['cross_border_flag']
                    e.pillar_number_flag = entity_info['pillar_number_flag']
                    e.pillar_number_bbox = entity_info['pillar_number_bbox']

                    entity_list.append(e)

            elif entity_type in ['structure_slab']:  # 结构板
                for entity_info in entity_info_list:
                    e = Entity(entity_type, BoundingRectangle(entity_info['bbox']), None, None, None, [],
                               Contour(entity_info['contour'], ratio))
                    e.slab_number = entity_info['slab_number']
                    e.slab_thickness = entity_info['slab_thickness']
                    e.bottom_x_reinforceing_bar_dia = entity_info['bottom_x_reinforceing_bar_dia']
                    e.bottom_x_reinforceing_bar_dis = entity_info['bottom_x_reinforceing_bar_dis']
                    e.bottom_y_reinforceing_bar_dia = entity_info['bottom_y_reinforceing_bar_dia']
                    e.bottom_y_reinforceing_bar_dis = entity_info['bottom_y_reinforceing_bar_dis']
                    e.top_x_reinforceing_bar_dia = entity_info['top_x_reinforceing_bar_dia']
                    e.top_x_reinforceing_bar_dis = entity_info['top_x_reinforceing_bar_dis']
                    e.top_y_reinforceing_bar_dia = entity_info['top_y_reinforceing_bar_dia']
                    e.top_y_reinforceing_bar_dis = entity_info['top_y_reinforceing_bar_dis']
                    e.top_bear_reinforceing_dia = entity_info['top_bear_reinforceing_dia']
                    e.top_bear_reinforceing_dis = entity_info['top_bear_reinforceing_dis']

                    entity_list.append(e)

            else:
                for entity_info in entity_info_list:
                    e = Entity(entity_type, BoundingRectangle(entity_info['bbox']), None, None, None, [],
                               Contour(entity_info['contour'], ratio))
                    entity_list.append(e)

        # 墙构件
        new_wall_info_list = border_entity_info.get("new_wall", [])  # 墙中心线和厚度
        for wall_info_dic in new_wall_info_list:
            wall_center_line = wall_info_dic['line']
            wall_thickness = wall_info_dic['thickness']
            wall_contour = wall_info_dic['contour']
            wall_bbox = wall_info_dic['bbox']
            e = Entity('new_wall', BoundingRectangle(wall_bbox), None, None, None, [],
                       Contour(wall_contour, ratio))
            e.wall_center_line = wall_center_line
            e.wall_thickness = wall_thickness

            entity_list.append(e)

        #  承重墙构件
        bear_wall_bbox_cnt_list = border_entity_info.get('bear_wall_bbox_cnt_list', [])
        for bear_wall_bbox_cnt in bear_wall_bbox_cnt_list:
            bear_wall_bbox, bear_wall_cnt, _ = bear_wall_bbox_cnt
            e = Entity('bear_wall', BoundingRectangle(bear_wall_bbox), None, None, None, [],
                       Contour(bear_wall_cnt, ratio))
            entity_list.append(e)

        #  非承重墙构件
        no_bear_wall_bbox_cnt_list = border_entity_info.get('no_bear_wall_bbox_cnt_list', [])
        for no_bear_wall_bbox_cnt in no_bear_wall_bbox_cnt_list:
            no_bear_wall_bbox, no_bear_wall_cnt, _ = no_bear_wall_bbox_cnt
            e = Entity('no_bear_wall', BoundingRectangle(no_bear_wall_bbox), None, None, None, [],
                       Contour(no_bear_wall_cnt, ratio))
            entity_list.append(e)

        # 橱柜构件
        kitchen_cabinet_contour_bbox_list = border_entity_info.get('kitchen_cabinet_contour_bbox', [])
        for cabinet_contour_bbox in kitchen_cabinet_contour_bbox_list:
            cabinet_bbox, cabinet_cnt = cabinet_contour_bbox
            e = Entity('kitchen_cabinet', BoundingRectangle(cabinet_bbox), None, None, None, [],
                       Contour(cabinet_cnt, ratio))
            entity_list.append(e)
        # "照明分支回路"、"插座分支回路"、"照明插座分支回路" 构件
        zhaoming_chazuo_branch_list = border_entity_info.get('zhaoming_chazuo_branch_list', [])
        for zhaoming_chazuo_branch in zhaoming_chazuo_branch_list:
            socket_num = zhaoming_chazuo_branch['socket_num']
            lamp_num = zhaoming_chazuo_branch['lamp_num']
            branch_bbox = zhaoming_chazuo_branch['branch_bbox']
            c = ''
            if socket_num != 0 and lamp_num == 0:
                b = BoundingRectangle(branch_bbox)
                c = 'socket_branch'
            elif socket_num == 0 and lamp_num != 0:
                b = BoundingRectangle(branch_bbox)
                c = 'lamp_branch'
            else:
                b = BoundingRectangle(branch_bbox)
                c = 'lamp_socket_branch'
            e = Entity(c, b)
            e.light_amount = lamp_num
            e.outlet_amount = socket_num
            entity_list.append(e)
            # print('--> classified entity class converted: {}'.format(c))

        # "配电箱出线回路"构件
        peidianxiang_outlet_branch_list = border_entity_info.get('peidianxiang_outlet_branch_list', [])
        for peidianxiang_outlet_branch_dict in peidianxiang_outlet_branch_list:
            outlet_bbox = peidianxiang_outlet_branch_dict['bbox']  # bbox
            c = 'peidianxiang_outlet_branch'
            b = BoundingRectangle(outlet_bbox)
            e = Entity(c, b)
            e.disconnector_type = peidianxiang_outlet_branch_dict['breaker_type']  # 断路器属性
            e.thermal_relay_type = peidianxiang_outlet_branch_dict['thermorelay_type']  # 热继电器属性
            e.electric_meter_type = peidianxiang_outlet_branch_dict['electricity_meter_type']  # 电表属性
            e.contactor_type = peidianxiang_outlet_branch_dict['contactor_type']  # 接触器属性
            e.disconnector_parameter = peidianxiang_outlet_branch_dict['breaker_parameter']  # 断路器参数属性
            e.thermal_relay_parameter = peidianxiang_outlet_branch_dict['thermorelay_parameter']  # 热继电器参数属性
            e.circuit_phase_sequence = peidianxiang_outlet_branch_dict['phase']  # 相序属性
            e.circuit_number = peidianxiang_outlet_branch_dict['branch_num']  # 回路编号属性
            e.wire_parameter = peidianxiang_outlet_branch_dict['cable_spec']  # 电缆规格属性
            e.circuit_usage = peidianxiang_outlet_branch_dict['usage']  # 用途属性
            e.circuit_power = peidianxiang_outlet_branch_dict['power']  # 功率属性
            e.electric_meter_parameter = peidianxiang_outlet_branch_dict['electricity_meter_parameter']  # 电表参数属性
            e.contactor_parameter = peidianxiang_outlet_branch_dict['contactor_parameter']  # 接触器参数属性
            entity_list.append(e)
            # print('--> classified entity class converted: {}'.format(c))

        # **** room_list ****

        room_info_list = border_entity_info.get("room_info", [])
        small_room_info_list = border_entity_info.get("small_room_info", [])
        # "配电箱子图"空间
        # peidianxiang_room_info: [contour, bbox, ['配电箱子图'], dist_box_num, power, coef, cos, current, usage]
        peidianxiang_room_info_list = border_entity_info.get("peidianxiang_room_info", [])

        def room_info_to_space(room_info_list, is_small):
            """
            将空间信息转为space对象
            Args:
                room_info_list: 空间信息列表
                is_small: 是否是小空间

            Returns:
                初始化的空间对象列表
            """
            new_list = []
            for room in room_info_list:
                c = Contour(room[0], ratio)
                b = BoundingRectangle(room[1])
                s = Space(c, b, room[2], is_small)
                new_list.append(s)
                # print('--> room class converted: {}'.format(room[2]))
            return new_list

        def peidianxiang_room_info_to_space(room_info_list, is_small):
            """
            将配电箱空间信息转为space对象
            Args:
                room_info_list: 空间信息列表
                is_small: 是否是小空间对象

            Returns:
                初始化的空间对象列表
            """
            new_list = []
            for room in room_info_list:
                c = Contour(room[0], ratio)
                b = BoundingRectangle(room[1])
                s = Space(c, b, room[2], is_small, room[3], room[4], room[5], room[6], room[7], room[8])
                s.main_switch_bbox_list = room[9]
                s.title_info = room[10]
                s.wire_line_list = room[11]
                s.switch_bbox_list = room[12]
                s.text_list = room[13]
                new_list.append(s)
                # print('--> room class converted: {}'.format(room[2]))
            return new_list

        room_list.extend(room_info_to_space(room_info_list, False) + room_info_to_space(small_room_info_list, True) +
                         peidianxiang_room_info_to_space(peidianxiang_room_info_list, False))

        # **** text_info ****

        border_text_info_with_layer = border_entity_info.get("border_text_info_with_layer", [])

        for text_type, text_list in border_text_info_with_layer.items():
            text_info[text_type] = []
            for text in text_list:
                b = BoundingRectangle(text[:4])
                t = TextEntity(b, text_type, text[4], text[5])
                text_info[text_type].append(t)

        # **** text_info_bound_vertex ****

        border_text_info_with_bound_vertex = border_entity_info.get("border_text_info_with_bound_vertex", [])
        for text_type, text_list in border_text_info_with_bound_vertex.items():
            text_info_bound_vertex[text_type] = []
            for text in text_list:
                b = BoundingVertex(text[:4])
                t = TextEntityWithBoundVertex(b, text_type, text[4])
                text_info_bound_vertex[text_type].append(t)

        # **** image_manager ****

        image_manager = border_entity_info['image_manager']
        image_manager.zip_image_to_bytesio()

        # **** entity_combination_result ****

        entity_bbox_dict = border_entity_info.get("entity_bbox_dict", {})
        for layer, combined_result_list in entity_bbox_dict.items():
            # 对于管道，不需要合并结果
            if layer in ["bu_feng_guan", "pai_yan_jian_pai_feng_guan", "pai_feng_guan", "xin_feng_guan",
                         "song_bu_feng_guan", "jia_ya_feng_guan", 'gutter_cont_bbox_list']:
                continue
            # 对于 parking_contour_dict，combined_result_list 对应的是一个字典
            if layer in ['parking_contour_dict']:
                parking_contour_result = combined_result_list
                # print('--> combined entity class converted: {}'.format(layer))
                continue

            if layer in ['cabinet_contour_dict', 'transformer_contour_dict']:
                continue

            entity_combination_result[layer] = []

            # 对于 door_intersect_bboxes，combined_result_list 的格式为[[bbox, bbox], ...]
            if layer in ['door_intersect_bboxes']:
                for combined_bbox_1, combined_bbox_2 in combined_result_list:
                    bbox_1 = BoundingRectangle(combined_bbox_1)
                    bbox_2 = BoundingRectangle(combined_bbox_2)
                    entity_combination_result[layer].append([bbox_1, bbox_2])
                # print('--> combined entity class converted: {}'.format(layer))
                continue

            # 对于 processed_red_lines，combined_result_list 的格式为 [red_line_bbox, red_line_list]
            if layer in ['processed_red_lines']:
                entity_combination_result[layer] = combined_result_list
                # print('--> combined entity class converted: {}'.format(layer))
                continue

            for combined_bbox in combined_result_list:
                # 这里不是所有的都是bbox，有些是线段，但是暂时不影响使用
                bbox = BoundingRectangle(combined_bbox)
                entity_combination_result[layer].append(bbox)
                # print('--> combined entity class converted: {}'.format(layer))

        # 将箭头信息暂时存在合并结果中，后面进行对象化
        arrow_info_list = border_entity_info.get('arrow_info_list', [])
        entity_combination_result['arrow_info_list'] = arrow_info_list
        # 将平面楼梯踏步信息暂时存在合并结果中，后面进行对象化
        tabu_mark_list = border_entity_info.get('tabu_mark_list', [])
        entity_combination_result['tabu_info_list'] = tabu_mark_list
        # 将厨房操作台边线信息暂时存在合并结果中，后面进行对象化
        kit_operate_line = border_entity_info.get('kit_operate_line', [])
        entity_combination_result['kit_operate_line'] = kit_operate_line
        # 栏杆完成面、空间完成面、窗台完成面信息暂时存在合并结果中，后面进行对象化
        space_completion_surface_list = border_entity_info.get('space_completion_surface_list', [])
        entity_combination_result['space_completion_surface_list'] = space_completion_surface_list
        sill_completion_surface_list = border_entity_info.get('sill_completion_surface_list', [])
        entity_combination_result['sill_completion_surface_list'] = sill_completion_surface_list
        handrail_completion_surface_list = border_entity_info.get('handrail_completion_surface_list', [])
        entity_combination_result['handrail_completion_surface_list'] = handrail_completion_surface_list
        kt_surface_list = border_entity_info.get('kt_surface_list', [])
        entity_combination_result['kt_surface_list'] = kt_surface_list
        arch_area_text_list = border_entity_info.get('arch_area_text_list', [])
        entity_combination_result['arch_area_text_list'] = arch_area_text_list
        anno_size_list = border_entity_info.get('anno_size_list', [])
        entity_combination_result['anno_size_list'] = anno_size_list
        door_number_list = border_entity_info.get('door_number_list', [])
        entity_combination_result['door_number_list'] = door_number_list
        window_number_list = border_entity_info.get('window_number_list', [])
        entity_combination_result['window_number_list'] = window_number_list
        arch_section_anno_list = border_entity_info.get('arch_section_anno_list', [])
        entity_combination_result['arch_section_anno_list'] = arch_section_anno_list
        arch_index_list = border_entity_info.get('arch_index_list', [])
        entity_combination_result['arch_index_list'] = arch_index_list
        # **** origin_border_entity_info ****

        origin_border_entity_info_dict = border_entity_info.get("origin_border_entity_info", {})
        origin_border_entity_style = border_entity_info.get("origin_border_entity_style", {})
        origin_border_line_description = border_entity_info.get("origin_border_line_description", {})
        origin_border_line_weight = border_entity_info.get("origin_border_line_weight", {})
        origin_border_entity_color = border_entity_info.get("origin_border_entity_color", {})
        for layer in origin_border_entity_info_dict:
            origin_border_entity_info[layer] = []
            info_list = origin_border_entity_info_dict[layer]
            style_list = origin_border_entity_style[layer]
            line_description_list = origin_border_line_description[layer]
            line_weight_list = origin_border_line_weight[layer]
            color_list = origin_border_entity_color[layer]
            for info, style, line_description, line_weight, color in zip(info_list, style_list, line_description_list,
                                                                         line_weight_list, color_list):
                # TODO：GBE 应该已经处理好extend_storage等字段，并全部转换到PNG坐标
                gbe = GraphicBasicEntity(
                    info[1],
                    "",
                    layer,
                    info[0],
                    info[2],
                    style[0],
                    line_weight[0],
                    color[0],
                    line_description[0]
                )
                origin_border_entity_info[layer].append(gbe)
            # print('--> origin entity class converted: {}'.format(layer))

        # **** parking_bbox_coord ****

        parking_bbox_coord = border_entity_info.get("parking_bbox_coord", {})

        # **** entity_class_dict ****

        entity_class_dict = border_entity_info.get("entity_class_dict", {})

        # **** entity_score_dict ****

        entity_score_dict = border_entity_info.get("entity_score_dict", {})

        # **** wall_contour ****

        wall_contour_list = border_entity_info.get("wall_contour", [])
        for wall_contour in wall_contour_list:
            c = Contour(wall_contour, ratio)
            wall_contour_info.append(c)

        # **** border_style_info ****

        border_style_info = border_entity_info.get("border_style_info", {})

        # **** door_base_coords ****

        door_base_coords = border_entity_info.get("door_base_coords", [])
        for door_base in door_base_coords:
            db = Line(door_base)
            door_base_info.append(db)

        # **** single_line_door_window_list ****

        single_line_door_window_list = border_entity_info.get("single_line_door_window_list", [])
        for single_line_door_window in single_line_door_window_list:
            single_line = Line(single_line_door_window)
            single_line_door_window_info.append(single_line)

        # **** small_room_contours ****

        small_room_contours = border_entity_info.get("small_room_contours", [])
        for small_room in small_room_contours:
            c = Contour(small_room, ratio)
            small_room_contour_info.append(c)

        # **** special_info_dict ****

        # "引注" 构件，List，图框内的所有引线组合 [[[line1, line2], [str1, str2]], ...]
        annotation_info_list = []
        # main_branch_text_list - [main_line, main_end_point, branch_list, text_list]，text_list：[[text_points, text_angle, text_center, content], ...]
        main_branch_text_list = border_entity_info.get("main_branch_text_list", [])
        for m_b_t in main_branch_text_list:
            line_l = []  # 保存所有的引线图元
            text_l = []  # 保存所有的标注文本
            main_line, main_end_point, branch_list, text_list = m_b_t
            line_l.append(main_line)
            line_l.extend(branch_list)
            text_l = [text[-1] for text in text_list]
            annotation_info = [line_l, text_l, main_end_point]
            annotation_info_list.append(annotation_info)
        special_info_dict['annotation_info_list'] = annotation_info_list
        special_info_dict['main_branch_text_list'] = main_branch_text_list

        # 总图上园区道路的宽度直线列表，List[List]，总图道路宽度直线列表 [[x1, y1, x2, y2], ...]
        road_width_line_list = border_entity_info.get('road_width_line_list', [])
        special_info_dict['road_width_line_list'] = road_width_line_list

        # penlin_system_draw_info_list，List[Dict]，喷淋系统图子图列表 [dict1, dict2]
        penlin_system_draw_info_list = border_entity_info.get("penlin_system_draw_info_list", [])
        special_info_dict['penlin_system_draw_info_list'] = penlin_system_draw_info_list

        # xiaohuoshuan_system_draw_info_list，List[Dict]，消火栓系统图子图列表 [dict1, dict2]
        xiaohuoshuan_system_draw_info_list = border_entity_info.get("xiaohuoshuan_system_draw_info_list", [])
        special_info_dict['xiaohuoshuan_system_draw_info_list'] = xiaohuoshuan_system_draw_info_list

        # stair_dayang_subdraw_cnt_list，List，楼梯大样图子图contour的列表 [contour1, contour2]
        stair_dayang_subdraw_cnt_list = border_entity_info.get("stair_dayang_subdraw_cnt_list", [])
        special_info_dict['stair_dayang_subdraw_cnt_list'] = stair_dayang_subdraw_cnt_list

        # road_arc_ellipse_contour_dict，Dict[tuple, List]，总图中车道边线图层弧形图元轮廓字典 {tuple(arc): [bbox, ent_cnt]}
        road_arc_ellipse_contour_dict = border_entity_info.get("road_arc_ellipse_contour_dict", {})
        special_info_dict['road_arc_ellipse_contour_dict'] = road_arc_ellipse_contour_dict

        # road_center_arc_ellipse_contour_dict，Dict[tuple, List]，总图中车道中线图层弧形图元轮廓字典 {tuple(arc): [bbox, ent_cnt]}
        road_center_arc_ellipse_contour_dict = border_entity_info.get("road_center_arc_ellipse_contour_dict", {})
        special_info_dict['road_center_arc_ellipse_contour_dict'] = road_center_arc_ellipse_contour_dict

        # sprinkler_system_draw_bbox_list，List[List]，喷淋子图bbox列表 [bbox1, bbox2]
        sprinkler_system_draw_bbox_list = border_entity_info.get("sprinkler_system_draw_bbox_list", [])
        special_info_dict['sprinkler_system_draw_bbox_list'] = sprinkler_system_draw_bbox_list

        # fire_system_draw_bbox_list，List[List]，消火栓子图bbox列表 [bbox1, bbox2]
        fire_system_draw_bbox_list = border_entity_info.get("fire_system_draw_bbox_list", [])
        special_info_dict['fire_system_draw_bbox_list'] = fire_system_draw_bbox_list

        # 由剖面图解析到的楼层高度、楼层数目等信息,放在special_info_dict里面
        underground_floor_num = border_entity_info.get('underground_floor_num', 0)
        above_ground_floor_num = border_entity_info.get('above_ground_floor_num', 0)
        floor_r_height = border_entity_info.get('floor_r_height', {})
        floor_r_height_bbox = border_entity_info.get('floor_r_height_bbox', {})
        floor_l_r_height = border_entity_info.get('floor_l_r_height', {})
        floor_abs_height = border_entity_info.get('floor_abs_height', {})
        floor_abs_height_bbox = border_entity_info.get('floor_abs_height_bbox', {})
        special_info_dict['underground_floor_num'] = underground_floor_num
        special_info_dict['above_ground_floor_num'] = above_ground_floor_num
        special_info_dict['floor_r_height'] = floor_r_height
        special_info_dict['floor_r_height_bbox'] = floor_r_height_bbox
        special_info_dict['floor_l_r_height'] = floor_l_r_height
        special_info_dict['floor_abs_height'] = floor_abs_height
        special_info_dict['floor_abs_height_bbox'] = floor_abs_height_bbox
        # 机房、屋顶平面图中添加对应的楼层离地高度， 也放在special_info_dict里面
        special_info_dict['jf_abs_height'] = border_entity_info.get('jf_abs_height', 0)
        special_info_dict['rf_abs_height'] = border_entity_info.get('rf_abs_height', 0)

        # 户门列表放在special_info_dict里面
        special_info_dict['indoor_door_info_list'] = border_entity_info.get('indoor_door_info_list', [])

        # 图框内户型、单元
        door_direction_line_dict = border_entity_info.get('door_direction_line_dict', {})
        door_base_line_dict = border_entity_info.get('door_base_line_dict', {})
        room_graph = border_entity_info.get('room_graph', None)
        household_list = border_entity_info.get('household_list', [])
        household_type_num = border_entity_info.get('household_type_num', 0)
        public_room_list = border_entity_info.get('public_room_list', [])
        household_rooms_list = border_entity_info.get('household_rooms_list', [])
        unit_list = border_entity_info.get('unit_list', [])
        building_obj = border_entity_info.get('building_object', None)
        special_info_dict['door_direction_line_dict'] = door_direction_line_dict
        special_info_dict['door_base_line_dict'] = door_base_line_dict
        special_info_dict['room_graph'] = room_graph
        special_info_dict['household_list'] = household_list
        special_info_dict['household_type_num'] = household_type_num
        special_info_dict['public_room_list'] = public_room_list
        special_info_dict['household_rooms_list'] = household_rooms_list
        special_info_dict['unit_list'] = unit_list
        special_info_dict['building_obj'] = building_obj

        # 暖通专业系统图楼层标高信息和层高信息
        floor_elevation_pair_dict = border_entity_info.get('floor_elevation_pair_dict', {})
        floor_height_dict = border_entity_info.get('floor_height_dict', {})
        special_info_dict['floor_elevation_pair_dict'] = floor_elevation_pair_dict
        special_info_dict['floor_height_dict'] = floor_height_dict

        # 建筑专业屋顶层平面图建筑的最大长，宽信息
        building_width_length_dict = border_entity_info.get('building_width_length_dict', {})
        special_info_dict['building_width_length_dict'] = building_width_length_dict

        # 建筑首层平面图的疏散外门保存
        evacuating_doors_list = border_entity_info.get("evacuating_doors_list", [])
        special_info_dict['evacuating_doors_list'] = evacuating_doors_list

        # 建筑平面图的开敞阳台、封闭阳台保存
        close_balcony_bbox_list = border_entity_info.get('close_balcony_bbox_list', [])
        special_info_dict['close_balcony_bbox_list'] = close_balcony_bbox_list
        open_balcony_bbox_list = border_entity_info.get('open_balcony_bbox_list', [])
        special_info_dict['open_balcony_bbox_list'] = open_balcony_bbox_list

        # 建筑平面图的外窗保存
        outer_window_bbox_list = border_entity_info.get('outer_window_bbox_list', [])
        special_info_dict['outer_window_bbox_list'] = outer_window_bbox_list

        # 门窗大样图中的内部小窗保存
        inside_li_mian = border_entity_info.get('inside_li_mian', [])
        special_info_dict['inside_li_mian'] = inside_li_mian

        # 门窗大样图的门窗编号-宽高材质属性保存
        dw_size_material = border_entity_info.get('dw_size_material', {})
        special_info_dict['dw_size_material'] = dw_size_material

        # 记录下多个开关靠的很近时，手动拆分的开关bbox和其对应的作为拆分单位的圆
        abnormal_switch = border_entity_info.get('abnormal_switch', {})
        special_info_dict['abnormal_switch'] = abnormal_switch

        # 虚线框加入special_info_dict
        special_info_dict['dash_border_list'] = entity_bbox_dict.get('dash_border', [])

        # 电路回路框
        special_info_dict['circuit_bbox_list'] = border_entity_info.get('peidianxiang_system_small_draw_bboxes', [])

        return cls(
            major,
            drawing_type,
            drawing_name,
            floor_num_list,
            space_name,
            space_scale,
            border_coord,
            ext_margin,
            ratio,
            subproject_name,
            subproject_num_list,
            entity_list,
            entity_combination_result,
            origin_border_entity_info,
            room_list,
            text_info,
            text_info_bound_vertex,
            image_manager,
            parking_bbox_coord,
            entity_class_dict,
            entity_score_dict,
            wall_contour_info,
            border_style_info,
            door_base_info,
            single_line_door_window_info,
            small_room_contour_info,
            parking_contour_result,
            axis_net_bbox_list,
            axis_net_line_list,
            axis_net_line_num_list,
            axis_net_line_deg_list,
            sheet_information,
            subdrawing_list,
            special_info_dict,
            cad_border_id,
            layout_name,
            no_bear_wall_bbox_cnt_list,
            bear_wall_bbox_cnt_list,
            entity_bbox_contour_dict
        )

    def to_json(self, path: Union[str, Path] = None) -> list:
        """
        序列化方法
        Args:
            path: 序列化结果保存路径

        Returns:
            按照普通构件、空间构件、文本分别封装成字典后保存的list
        """
        js = []
        basic_dict = {
            "border_name": self.drawing_name,
            "border_type": self.drawing_type.value,
            "border_coord": self.border_coord,
            "border_layout": self.space_name,
            "border_name_coord": "",
            "sub_project_name": self.subproject_name
        }
        # Entity
        for entity in self.entity_bbox_list:
            entity_dict = entity.to_dict()
            # entity_dict["layer"] = layer
            entity_dict.update(basic_dict.copy())
            js.append(entity_dict)

        # Space
        for space in self.room_info:
            space_dict = space.to_dict()
            space_dict.update(basic_dict.copy())
            js.append(space_dict)

        # Text
        for text in self.border_text_info:
            text_dict = text.to_dict()
            text_dict["class_type"] = "text"
            text_dict.update(basic_dict.copy())
            js.append(text_dict)

        output = json.dumps(js, ensure_ascii=False)

        if path:
            with open(path, "w", encoding='utf-8') as writer:
                writer.write(output)

        return js

    def update_mark_result(self, mark_dict: Dict[str, List[Mark]]):
        """
        将标记更新到对象属性中
        Args:
            mark_dict: 标记信息

        Returns:
            None
        """
        self.mark_object_dict = mark_dict

    def update_objectification_result(self,
                                      entity_dict: Dict[str, List[Entity]],
                                      space_dict: Dict[str, List[Space]]):
        """
        将构件信息和空间信息更新到对象属性中
        Args:
            entity_dict: 构件信息
            space_dict: 空间信息

        Returns:
            None
        """
        self.entity_object_dict = entity_dict
        self.space_object_dict = space_dict

    def update_project_info(self, project_info_result: Dict):
        """
        将项目信息更新到对象化属性中
        Args:
            project_info_result: 项目信息

        Returns:
            None

        """
        project_info_dict = {}
        projecet_info_list = project_info_result.get("projectInfo", [])

        for project_info in projecet_info_list:
            info_name = project_info["infoFieldName"]
            project_info_dict[info_name] = project_info["infoValues"]

        self.project_info = project_info_dict

    @classmethod
    def nodup_entity_by_bbox(cls, entity_bbox_list, entity_class_list, entity_ori_class_list, entity_score_list,
                             entity_coord_list,
                             entity_annotation_list):
        """
        根据entity class名称以及bbox，计算iou去重
        Args:
            entity_bbox_list: [[5664, 5882, 5722, 5894], [4659, 5804, 4671, 5862], [5675, 4111, 5702, 4261]]
            entity_class_list: ['others', 'others', 'others']
            entity_ori_class_list: ['others', 'window', 'others']
            entity_score_list: [0.987934113, 0.783335388, 0.999832869]
            entity_coord_list: [[75701.793, 85100.963, 76225.207, 85299.033], [68593.256, 85327.329, 68791.305, 85850.802],
                                [75779.598, 96652.731, 76083.744, 97827.008]]
            entity_annotation_list: [[], ['KD1'], []]

        Returns:
            [([5664, 5882, 5722, 5894], 'others', 'others', 0.987934113, [75701.793, 85100.963, 76225.207, 85299.033], []),
            ([4659, 5804, 4671, 5862], 'others', 'window', 0.783335388, [68593.256, 85327.329, 68791.305, 85850.802], ['KD1']),
            ([5675, 4111, 5702, 4261], 'others', 'others', 0.999832869, [75779.598, 96652.731, 76083.744, 97827.008], [])]
        """
        check_dict = {}
        check_result = []
        for bbox, c, ori_class, score, CAD_coord, anno_list in \
                zip(entity_bbox_list, entity_class_list, entity_ori_class_list, entity_score_list,
                    entity_coord_list, entity_annotation_list):
            if c not in check_dict:
                check_dict[c] = [bbox]
                check_result.append((bbox, c, ori_class, score, CAD_coord, anno_list))
            else:
                verify_list = [min(Iou_temp(bbox, verified_entity_bbox), Iou_temp(verified_entity_bbox, bbox)) > 0.7 for
                               verified_entity_bbox in check_dict[c]]
                if not any(verify_list):
                    check_result.append((bbox, c, ori_class, score, CAD_coord, anno_list))
        return check_result

    def update_room_graph(self):
        if not getattr(self, "updated_space_dict", {}):
            return
        new_room_info = []
        temp_border_entity_info = {
            "border_coord": self.border_coord,
            "space_scale": self.space_scale,
            "ext_margin": self.ext_margin,
            "ratio": self.ratio,
            "image_manager": self.image_manager,
            "indoor_door_info_list": self.special_info_dict["indoor_door_info_list"],
            "door_base_coords": [l.list for l in self.door_base_coords],

            # 需要下面重新构建的列表
            "room_info": new_room_info,
            "entity_bbox_list": [],
            "entity_class_list": [],
            "origin_border_entity_info": defaultdict(list)
        }

        # 构建 room_info
        original_space_list = self.special_info_dict["public_room_list"].copy()
        for l in self.special_info_dict["household_rooms_list"]:
            original_space_list.extend(l)

        for space in original_space_list:
            new_room = [space.contour, space.bbox, space.name_list]
            new_room_info.append(new_room)

        for space in self.updated_space_dict.values():
            new_room = [space.contour.contour, space.contour.bounding_rectangle, space.name_list]
            new_room_info.append(new_room)

        # 构建entity_bbox_list和entity_class_list（仅包含部分构件）
        entity_class_list = ['menlianchuang', 'juanlianmen', 'door', 'elevator_door', 'tuila_door', 'guanjingmen',
                             'renfang_door', 'baiye', 'window', 'corner_window']
        entity_name_list = ["门联窗", "卷帘门", "平开门", "电梯门", "推拉门", "管井门",
                            "人防门", "百叶窗", "普通窗", "转角窗"]
        entity_name_map = {name: class_name for name, class_name in zip(entity_name_list, entity_class_list)}
        for entity_name, entity_list in self.entity_object_dict.items():
            if entity_name not in entity_name_map:
                continue

            for entity in entity_list:
                temp_border_entity_info["entity_bbox_list"].append(entity.bounding_rectangle.list)
                temp_border_entity_info["entity_class_list"].append(entity_name_map[entity_name])

        # 构建origin_border_entity_info
        for layer_name, gbe_list in self.origin_border_entity_info.items():
            for gbe in gbe_list:
                if gbe.entity_type == CADBasicEntityType.UNKNOWN:
                    continue
                new_basic_entity = [gbe.coord, gbe.entity_type.value, gbe.extend_storage]
                temp_border_entity_info["origin_border_entity_info"][layer_name].append(new_basic_entity)

        temp_border_entity_info["origin_border_entity_info"] = dict(
            temp_border_entity_info["origin_border_entity_info"])

        temp_border_entity_info = build_room_graph_pre(temp_border_entity_info)
        temp_border_entity_info = get_household_list_pre(temp_border_entity_info, os.getcwd())

        self.special_info_dict["room_graph"] = temp_border_entity_info["room_graph"]
        self.special_info_dict["door_direction_line_dict"] = temp_border_entity_info["door_direction_line_dict"]
        self.special_info_dict["door_base_line_dict"] = temp_border_entity_info["door_base_line_dict"]
        self.special_info_dict["household_list"] = temp_border_entity_info.get("household_list", [])
        self.special_info_dict["public_room_list"] = temp_border_entity_info.get("public_room_list", [])
        self.special_info_dict["household_rooms_list"] = temp_border_entity_info.get("household_rooms_list", [])

    def update_base_png_id(self):
        self.base_png_id = upload_drawing_pkl(self.image_manager.load_from_manager(IMG_WITH_WALL_KEY))


"""
border_entity_info= {
            "space_name": border_space,                      # 图框所属空间名称，str
            "drawing_name": drawing_name,                    # 图框里面的图名, str
            "space_scale": space_scale,                      # 视口缩放比例（custom_scale）* CAD坐标转成mm的比例(unit_scale)
            "border_coord": border_coord,                    # 图框CAD坐标，[x1, y1, x2, y2]
            "border_image": img,                             # 图框图像矩阵（BGR格式）array, shape=[h,w,3]
            "border_image_with_wall": img_with_wall,         # 包含墙层的图框图像矩阵（BGR格式）array, shape=[h,w,3]
            "space_recog_image": img_space,                  # 空间识别图框图像矩阵（BGR格式）array, shape=[h,w,3]
            "entity_bbox_list": border_entity_bbox_list,     # 构件png坐标, list, shape=[n,4]
            "entity_bbox_dict": border_entity_bbox_dict,     # 构件png坐标, 按图层分开, dict, key为layer，value shape=[n,4]
            "entity_class_list": border_entity_class_list,   # 构件类别, list, shape=[n]
            "entity_class_dict": border_entity_class_dict,   # 构件类别, 按图层分开, dict, key为layer，value shape=[n]
            "entity_score_list": border_entity_score_list,   # 构件类别置信度, list, shape=[n]
            "entity_score_dict": border_entity_score_dict,   # 构件类别置信度, 按图层分开, dict, key为layer，value shape=[n]
            "entity_coord_list": border_entity_coord_list,   # 构件CAD坐标，list，shape=[n,4]
            "ext_margin": ext_margin,                        # 构件外扩的像素值, int
            "ratio": (w_ratio, h_ratio),                     # CAD坐标转换成png图像坐标的比例, float
            "room_text_info": room_name_info,                # 房间文本信息, 包含房间名称与文本坐标, list, shape=[n,5], 最后一维为 [x1, y1, x2, y2, text]
            "room_info": room_info,                          # 空间信息，包括空间轮廓，bbox，空间文本list，[contours, bbox, text_list]，其中 contour shape=[-1,1,2], bbox shape=[4]
            "door_info": door_text_info,                     # 门的文本信息，包含文本与文本坐标, list, shape=[n,5], 最后一维为 [x1, y1, x2, y2, text]
            "origin_border_entity_info": origin_border_entity_info  # 未合并前的构件信息，dict, 按图层存储，value 为 list,shape=[n,2]，最后一维为 [bbox, CAD_class_name]
            "border_text_info": border_text_info,            # 图框文本信息，dict，key为TextType，value为list，shape=[n,5], 最后一维为 [x1, y1, x2, y2, text]
            "border_text_info_with_layer": border_text_info_with_layer,  # 图框文本信息，dict，key为TextType，value为list，shape=[n,5], 最后一维为 [x1, y1, x2, y2, text, layer]
            "subproject_name": subproject_name,              # 图框子项名称
            "border_style_info": border_style_info,          # 三个图层['wall', 'pillar', 'structure']的style信息
}

"""
