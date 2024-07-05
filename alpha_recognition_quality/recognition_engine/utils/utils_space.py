# -*- coding: utf-8 -*-

import functools
import math
import re
import sys
from copy import deepcopy
from collections import defaultdict

import cv2
import numpy as np
import shapely
from shapely.geometry import LineString, Polygon, MultiLineString, Point

from ...common.utils import *
from ...common.utils_draw_and_rule import *

from ...config_manager.text_config import TextType
from ...common.utils import Iou_temp
from ...common.utils_draw_and_rule import get_contours_iou, get_contour_from_bbox, get_public_contours_list, \
    get_living_room_door_via_contours2, door_usage, extend_contour_morphology, get_bbox_from_contour, \
    bbox_intersect_bbox, get_elevation_text_type, get_origin_border_entity_info_rule
from ...common.CONSTANTS import wall_thickness_CAD
from .utils_objectification_common import extend_margin_by_side_object
from ...config_manager.space_config import SpaceConfig
from ...common.utils import extend_margin


def space_use_attribute(Space, border_entity_info, key_words_dict, default_use):
    """
    :param Space: 空间对象
    :param border_entity_info:
    :param key_words_dict: {属性值：[包含的字段],属性值：[包含的字段],...}
    :return: 最终属性值
    """
    all_text_list = border_entity_info.border_text_info[TextType.ALL]
    space_con = Space.contour.contour
    space_use_attr = default_use
    for k, v in key_words_dict.items():
        have_key_word = False
        for key_word in v:
            for text in all_text_list:
                if get_contours_iou(space_con, get_contour_from_bbox(text.bbox.list)) > 0 and re.search(key_word,
                                                                                                        text.extend_message):
                    have_key_word = True
                    break
            if have_key_word:
                break
        if have_key_word:
            space_use_attr = k
            break
    return space_use_attr


def get_room_type(room_cnt, border_entity, keyword_type_dict, default_type=None):
    """
    根据文本获取某个空间的细分类型
    Args:
        room_cnt:
        border_entity:
        keyword_type_dict: {keyword: room_type, ...}
        default_type: 默认类型

    Returns:
        空间细分类型
    """
    type_result = default_type
    border_text_info = border_entity.border_text_info
    all_text_info = border_text_info[TextType.ALL]

    for text_info in all_text_info:
        text_bbox = text_info.bbox.list
        text_cnt = get_contour_from_bbox(text_bbox)
        if get_contours_iou(room_cnt, text_cnt) > 0.5:
            text_str = text_info.extend_message
            for keyword, room_type in keyword_type_dict.items():
                if re.search(keyword, text_str):
                    type_result = room_type
                    break
        if type_result is not None and type_result != default_type:
            break

    return type_result


def get_elevator_well_type(room_cnt, border_entity, keyword_type_dict, default_type=[]):
    """
    根据文本获取某个空间的细分类型
    Args:
        room_cnt:
        border_entity:
        keyword_type_dict: {keyword: room_type, ...}
        default_type: 默认类型（电梯井细分类型用到）

    Returns:
        空间细分类型
    """
    type_result_list = list()
    border_text_info = border_entity.border_text_info
    all_text_info = border_text_info[TextType.ALL]

    for text_info in all_text_info:
        text_bbox = text_info.bbox.list
        text_cnt = get_contour_from_bbox(text_bbox)
        if get_contours_iou(room_cnt, text_cnt) > 0.5:
            text_str = text_info.extend_message
            for keyword, room_type in keyword_type_dict.items():
                if re.search(keyword, text_str) and room_type not in type_result_list:
                    type_result_list.append(room_type)

    if len(type_result_list) == 0:
        type_result_list = default_type

    return type_result_list


def get_car_entrance_type(room_cnt, border_entity):
    """
    根据文本获取车行出入口空间的细分类型
    Args:
        room_cnt:空间轮廓
        border_entity:
    Returns:
        车行出入空间的细分类型
    """
    type_result = "普通车行出入口"
    all_text_info = border_entity.border_text_info[TextType.ALL]

    for text_info in all_text_info:
        text_bbox = text_info.bbox.list
        text_cnt = get_contour_from_bbox(text_bbox)
        if get_contours_iou(room_cnt, text_cnt) > 0.5:
            text_str = text_info.extend_message
            if re.search("消防", text_str):
                type_result = "消防车行出入口"
                break
    return type_result


def get_stair_type(stair_contour, border_entity_info):
    """

    Args:
        stair_contour: 轮廓
        border_entity_info: 图框全量信息

    Returns:
        楼梯间细分类型
    """
    entity_bbox_list = border_entity_info.entity_bbox_list  # 构件信息
    wall_line_list = border_entity_info.entity_combination_result['wall_line']
    pillar_line_list = border_entity_info.entity_combination_result['pillar_line']  # 柱子
    ratio = border_entity_info.ratio
    # 获取门窗bbox内只有一条直线的线，判断是否是入户门，issue 250216
    single_line_dw_list = border_entity_info.single_line_door_window_list

    door_bbox_list_src = [entity.bounding_rectangle.list for entity in entity_bbox_list if
                      entity.entity_class in ['door']]  # 门构件

    stair_bbox_list = [entity.bounding_rectangle.list for entity in entity_bbox_list if
                       entity.entity_class in ['stair']]  # 楼梯构件

    elevator_door_bbox_list = [entity.bounding_rectangle.list for entity in entity_bbox_list if
                               entity.entity_class in ['elevator_door']]  # 电梯门构件

    wall_thickness_pixel = int(wall_thickness_CAD * ratio[0])  # 墙的厚度值
    width, height = border_entity_info.image_manager.img_width, border_entity_info.image_manager.img_height  # 获取宽和高

    door_bbox_list = []
    for door_bbox in door_bbox_list_src:
        width = door_bbox[2] - door_bbox[0]
        height = door_bbox[3] - door_bbox[1]
        if width > height:
            margin_ex = int(width * 0.2)
        else:
            margin_ex = int(height * 0.2)
        door_bbox_ex = extend_margin_by_side_object(door_bbox, margin_ex, side='short')
        door_cut = get_contour_from_bbox(door_bbox_ex)
        if get_contours_iou(stair_contour, door_cut):
            door_bbox_list.append(door_bbox)

    # 构件网格化分割基础参数
    n_num = 20  # grid number
    h_range = np.ceil(height / n_num)  # grid size
    w_range = np.ceil(width / n_num)  # grid size

    # 空间信息
    room_info = border_entity_info.room_info

    # 提取空间轮廓名字不为空的空间
    contours_with_name_list = [[room.contour.contour, room.name_list] for room in room_info if len(room.name_list) != 0]
    # 提取客厅空间信息
    living_room_contours_list = [contour for contour in contours_with_name_list if '客厅' in contour[1] or
                                 '开放式厨房' in contour[1]]
    # 提取公共空间信息
    public_contours_list = get_public_contours_list(contours_with_name_list)

    # 非客厅空间不一定只有一个名称，所以都要判断，比如主卧室内有衣帽间
    other_contours_list = []
    for contour in contours_with_name_list:
        is_other_contour = False
        for contour_name in contour[1]:
            for other_space in SpaceConfig.IGNORE_OTHER_SPACE_LIST.value:
                # 如果因为解析问题，造成非客厅空间与客厅之间的门没有识别出来，那么该混合空间的名称列表中既有客厅又有非客厅名称
                if re.search(other_space, contour_name) and ('客厅' not in contour[1]) and \
                        ('开放式厨房' not in contour[1]):
                    other_contours_list.append(contour)
                    is_other_contour = True
                    break
            if is_other_contour:
                break
    # 入户门
    indoor_door_info_list = get_living_room_door_via_contours2(living_room_contours_list, other_contours_list,
                                                               door_bbox_list,
                                                               border_entity_info, stair_bbox_list,
                                                               wall_line_list + pillar_line_list,
                                                               wall_thickness_pixel, (w_range, h_range),
                                                               single_line_dw_list, public_contours_list)

    # 单元门
    unit_door_list = []
    for door_bbox in door_bbox_list:
        door_type = door_usage(door_bbox, border_entity_info)
        if door_type == "单元门":
            unit_door_list.append(door_bbox)

    ########## 判断楼梯间空间是否存在相邻的入户门、单元门、电梯门或直接连接室外的门 ##############
    for door_info in unit_door_list + indoor_door_info_list + elevator_door_bbox_list:
        if door_info:
            door_bbox = door_info[:4]
            door_cnt = get_contour_from_bbox(door_bbox)

            if get_contours_iou(stair_contour, door_cnt):
                return "开敞楼梯间"

    #########   判断楼梯间的相邻空间是否有“前室”文本  ############

    # 外扩2个墙的厚度
    cnt_ext_margin = int(ratio[0] * 2000)  # 外扩大小是卷积核半径
    dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cnt_ext_margin + 1, cnt_ext_margin + 1))
    contour_ex = extend_contour_morphology(stair_contour, dilate_kernel, border_entity_info)

    stair_bbox = get_bbox_from_contour(stair_contour)
    stair_bbox_ex = extend_margin(stair_bbox, cnt_ext_margin)

    # 查找"前室"空间
    front_room_list = [room_ for room_ in room_info if re.search('前室', ''.join(room_.name_list))]
    for front_room_info in front_room_list:
        front_room_info_con, front_room_info_box, front_room_info_name = front_room_info.contour.contour, front_room_info.bbox.list, front_room_info.name_list
        if Iou_temp(stair_bbox_ex, front_room_info_box):
            return "防烟楼梯间"

    return '封闭楼梯间'


def get_labeled_height_plumping(room_cnt, border_entity):
    """
    获取空间标高数值属性（给排水）
    Args:
        room_cnt:
        border_entity:

    Returns:
        空间标高数值属性（给排水）
    """
    labeled_height = None
    # 构件
    entity_bbox_list = border_entity.entity_bbox_list
    # 获取空间范围内的标高符号
    elevation_symbol_list = list()
    for item in entity_bbox_list:
        item_class = item.entity_class
        if item_class == "elevation_symbol":
            item_bbox = item.bounding_rectangle.list
            item_cnt = get_contour_from_bbox(item_bbox)
            if get_contours_iou(room_cnt, item_cnt) > 0.5:
                elevation_symbol_list.append(item)
    # 文本
    border_text_info = border_entity.border_text_info
    all_text_info = border_text_info[TextType.ALL]
    # 获取空间范围内的标高格式文本 *.***
    elevation_text_info = list()
    for text_info in all_text_info:
        text_bbox = text_info.bbox.list
        text_cnt = get_contour_from_bbox(text_bbox)
        text_str = text_info.extend_message
        if re.search("[+-H]?\d+\.\d{3}", text_str) and get_contours_iou(room_cnt, text_cnt) > 0.5:
            elevation_text_info.append(text_info)

    if len(elevation_symbol_list) > 0:
        # 标高符号外扩, 长边扩2m, 短边扩1m
        EXT_LONG = 2000
        EXT_SHORT = 1000
        # 建筑标高，结构标高，绝对标高
        jianzhu_elevation_list = list()
        jiegou_elevation_list = list()
        juedui_elevation_list = list()
        for elevation_symbol in elevation_symbol_list:
            symbol_bbox = elevation_symbol.bounding_rectangle.list
            width, height = (symbol_bbox[2] - symbol_bbox[0], symbol_bbox[3] - symbol_bbox[1])
            # 按长短边扩展
            if width >= height:
                ext_symbol_bbox = [symbol_bbox[0] - EXT_LONG,
                                   symbol_bbox[1] - EXT_SHORT,
                                   symbol_bbox[2] + EXT_LONG,
                                   symbol_bbox[3] + EXT_SHORT]
            else:
                ext_symbol_bbox = [symbol_bbox[0] - EXT_SHORT,
                                   symbol_bbox[1] - EXT_LONG,
                                   symbol_bbox[2] + EXT_SHORT,
                                   symbol_bbox[3] + EXT_LONG]
            # 扩展范围内的标高文本
            need_elevation_text_info = list()
            for text_info in elevation_text_info:
                text_bbox = text_info.bbox.list
                if bbox_intersect_bbox(ext_symbol_bbox, text_bbox):
                    need_elevation_text_info.append(text_info)
            # 获取该标高符号的对应的建筑标高，结构标高，绝对标高
            for text_info in need_elevation_text_info:
                text_type = get_elevation_text_type(text_info, all_text_info)
                if text_type is not None:
                    if text_type == "建筑标高":
                        jianzhu_elevation_list.append(text_info)
                    elif text_type == "结构标高":
                        jiegou_elevation_list.append(text_info)
                    elif text_type == "绝对标高":
                        juedui_elevation_list.append(text_info)
        if len(jianzhu_elevation_list) > 0:
            # 标高数值为负数（建筑标高）
            elevation_num_list = list()
            for text_info in jianzhu_elevation_list:
                text_str = text_info.extend_message
                if re.search("-\d+\.\d{3}", text_str):
                    elevation_num = eval(re.search("-\d+\.\d{3}", text_str).group())
                    elevation_num_list.append(elevation_num)
            if len(elevation_num_list) > 0:
                labeled_height = sorted(elevation_num_list, key=lambda item: abs(item))[0]
        elif len(jiegou_elevation_list) > 0:
            # 标高数值为负数（结构标高）
            elevation_num_list = list()
            for text_info in jiegou_elevation_list:
                text_str = text_info.extend_message
                if re.search("-\d+\.\d{3}", text_str):
                    elevation_num = eval(re.search("-\d+\.\d{3}", text_str).group())
                    elevation_num_list.append(elevation_num)
            if len(elevation_num_list) > 0:
                labeled_height = sorted(elevation_num_list, key=lambda item: abs(item))[0]

    if labeled_height is None:
        # 如果没有获取到标高数值
        elevation_num_list = list()
        for text_info in elevation_text_info:
            text_str = text_info.extend_message
            if re.search("-\d+\.\d{3}", text_str):  # 去掉相对标高
                elevation_num = eval(re.search("-?\d+\.\d{3}", text_str).group())
                if abs(elevation_num) <= 30:
                    elevation_num_list.append(elevation_num)
        if len(elevation_num_list) > 0:
            labeled_height = sorted(elevation_num_list, key=lambda item: abs(item))[0]

    if labeled_height is None:
        print("[Note] 没有获取到标高数值")

    return labeled_height


def get_labeled_height_architecture(room_cnt, border_entity):
    """
    获取空间标高数值属性（建筑）
    Args:
        room_cnt:
        border_entity:

    Returns:
        空间标高数值属性（建筑）
    """
    labeled_height = None
    # 标记
    mark_object_dict = border_entity.mark_object_dict
    # 标高符号
    elevation_symbol_list = mark_object_dict["标高符号"]
    if len(elevation_symbol_list) > 0:
        elevation_num_list = list()
        for elevation_symbol in elevation_symbol_list:
            symbol_bbox = elevation_symbol.bounding_rectangle.list
            symbol_cnt = get_contour_from_bbox(symbol_bbox)
            # 空间内
            if get_contours_iou(room_cnt, symbol_cnt) > 0.5:
                elevation_type = elevation_symbol.labeled_type  # Todo: 标高类型属性
                if elevation_type == "建筑标高":
                    elevation_num = elevation_symbol.labeled_height
                    elevation_num_list.append(elevation_num)
        if len(elevation_num_list) > 0:
            labeled_height = sorted(elevation_num_list, key=lambda item: abs(item))[0]

    return labeled_height


def fetch_building_width_length(building_bbox, border_entity):
    building_width_length_dict = border_entity.special_info_dict['building_width_length_dict']
    if tuple(building_bbox) in building_width_length_dict:
        return building_width_length_dict[tuple(building_bbox)]
    else:
        return [None, None]


def get_inner_space_dict(space, border_entity_info):
    d = defaultdict(list)
    for be_room_name, be_room_list in border_entity_info.space_object_dict.items():
        l = [r for r in be_room_list if space.is_inner_space(r)]
        if l:
            d[be_room_name].extend(l)
    return d


def judge_front_room_open(room_cnt, border_entity):
    """
    判断前室是否开敞的属性
    Args:
        room_cnt:
        border_entity:

    Returns:
        true or false
    """
    # 图框基础信息
    front_room_open = False
    border_coord = border_entity.border_coord
    ratio = border_entity.ratio
    space_scale = border_entity.space_scale
    origin_border_entity_info = border_entity.origin_border_entity_info
    # 获取栏杆构件的线
    layer_to_check = ['elevation_handrail']
    class_to_check = ['Line', 'Polyline', 'Polyline2d']
    rail_line_dict = get_origin_border_entity_info_rule(origin_border_entity_info,
                                                   layer_to_check,
                                                   class_to_check, space_scale,
                                                   border_coord, ratio)
    rail_line_list = []
    for layer, entity_list in rail_line_dict.items():
        rail_line_list.extend(entity_list)
    rail_line_list = list(filter(lambda x: len(x) == 4, rail_line_list))

    # 剔除与window贴在一起的栏杆
    for i in border_entity.entity_bbox_list:
        if i.entity_class != 'window':
            continue
        bbox = extend_margin(i.bounding_rectangle, 20)
        pop_index = []
        for index, line in enumerate(rail_line_list):
            line_bbox = extend_margin(line, 20)
            if Iou_temp(line_bbox, bbox) > 0.5:
                pop_index.append(index)
        rail_line_list = [rail_line_list[j] for j in range(len(rail_line_list)) if j not in pop_index]

    for line in rail_line_list:
        ext_line = extend_margin(line, 20)
        ext_line_cnt = get_contour_from_bbox(ext_line)
        if get_contours_iou(room_cnt, ext_line_cnt) > 0:
            front_room_open = True
            break
    return front_room_open


def get_household_entity_list_by_anit_clockwise_seq(room_obj, entity_list, room_indoor_door_base_center_point, expand_margin=0):
    """
    获取每个空间所包含的构件列表，并按照极坐标角度和极径长短来进行排序
    Args:
        room_obj:
        room_entity_list:
        room_indoor_door_base_center_point:

    Returns: 空间中构件按
    """
    # 空间的质心
    room_cnt = room_obj.contour.contour
    expand_room = expand_contour(room_cnt, expand_margin)
    room_center = get_centroid(room_cnt)
    # 空间质心到入空间门中心的基础向量
    base_vector = [room_indoor_door_base_center_point[0] - room_center[0], room_indoor_door_base_center_point[1] - room_center[1]]
    entity_info_list = []
    # 计算每个构件到空间质心的距离和基础极坐标到构件至空间质心的向量的逆时针夹角
    for entity in entity_list:
        entity_bbox = entity.bounding_rectangle.list
        if not get_contours_iou(get_contour_from_bbox(entity_bbox), expand_room): continue
        entity_center = get_centroid(entity_bbox)
        entity_vector = [entity_center[0] - room_center[0], entity_center[1] - room_center[1]]
        dis = point_euclidean_distance(entity_center, room_center)
        angle = anti_clockwise_angle(base_vector, entity_vector)
        entity_info_list.append([entity, entity_center, dis, angle])
        # print("angle, dis", angle, dis)
        entity.angle_against_apartment = angle
        entity.dist_to_apartment_centroid = dis
    # 先按照夹角和径向距离进行排序
    entity_info_list.sort(key=lambda x: (x[3], x[2]))
    sorted_entity_list = [entity[0] for entity in entity_info_list]
    return sorted_entity_list


def get_space_related_entity(space_object, border_entity, entity_name, ext_len=1, use_bbox=False):
    """
    根据构件名得到空间相关的构件列表
    Args:
        space_object:
        border_entity:
        entity_name:

    Returns:

    """
    related_entity_list = []
    entity_list = border_entity.entity_object_dict.get(entity_name, [])
    space_cnt = space_object.contour.contour
    if use_bbox:
        space_cnt = get_contour_from_bbox(space_object.bbox.list)
    # 如果获取空间所属的墙， 需要将空间轮廓外扩
    if re.search("墙|窗|门", entity_name): space_cnt = expand_contour(space_cnt, ext_len)
    for entity in entity_list:
        entity_cnt  = get_contour_from_bbox(entity.bounding_rectangle.list)
        # 最差的情况下为0.5
        if get_contours_iou(space_cnt, entity_cnt) > 0.:
            related_entity_list.append(entity)
    return related_entity_list


def get_space_related_space(space_object, border_entity, space_name, margin=0):
    related_space_list = []
    space_list = border_entity.space_object_dict.get(space_name, [])
    space_object_bbox = extend_margin(space_object.bbox.list, margin)
    for space in space_list:
        bbox = space.bbox.list
        if Iou_temp(bbox, space_object_bbox) > 0.2:
            related_space_list.append(space)

    return related_space_list

def get_contour_perimeter(contour):
    """
    获取轮廓周长
    contour: 空间轮廓
    """
    contour = contour.squeeze()
    pts = len(contour)
    perimeter = 0.
    for i in range(pts):
        if i == pts -1:
            perimeter += point_euclidean_distance(contour[i], contour[0])
        else:
            perimeter += point_euclidean_distance(contour[i], contour[i+1])

    return perimeter


def get_space_related_door(space_object, border_entity):
    """
    获取空间相关联的门
    Args:
        space_object: 空间对象
        border_entity: 图框全量信息

    Returns:关联的门列表

    """
    space_cnt = space_object.contour.contour
    door_list = border_entity.entity_object_dict.get("子母门", []) + border_entity.entity_object_dict.get("推拉门", []) +\
                border_entity.entity_object_dict.get("单开门", []) + border_entity.entity_object_dict.get("双开门", []) +\
                border_entity.entity_object_dict.get("门联窗", [])
    related_door_list = []
    # 遍历门，判断门朝向线或扩大的bbox是否和空间相交
    for door in door_list:
        if door.door_direction_line is not None:
            if line_overlap_poly(door.door_direction_line, space_cnt):
                related_door_list.append(door)
                continue
        else:
            door_bbox = door.bounding_rectangle.list
            ext_door_bbox = extend_margin(door_bbox, 10)
            ext_door_cnt = get_contour_from_bbox(ext_door_bbox)
            if get_contours_iou(space_cnt, ext_door_cnt) > 0:
                related_door_list.append(door)
    return related_door_list


def get_space_related_entity_by_extend_entity_bbox(space_object, border_entity, entity_name):
    """
    通过外扩构件bbox来获取空间所属构件
    Args:
        space_object: 空间对象
        border_entity: 图框全量信息
        entity_name: 构件中文名称

    Returns:关联构件列表

    """
    space_cnt = space_object.contour.contour
    entity_list = border_entity.entity_object_dict.get(entity_name, [])
    related_entity_list = []
    for entity in entity_list:
        entity_bbox = entity.bounding_rectangle.list
        ext_entity_bbox = extend_margin(entity_bbox, 5)
        ext_entity_cnt = get_contour_from_bbox(ext_entity_bbox)
        if get_contours_iou(space_cnt, ext_entity_cnt) > 0:
            related_entity_list.append(entity)
    return related_entity_list


def get_space_related_nonbear_wall_list(space_object, border_entity):
    """
    获取空间的关联墙
    Args:
        space_object: 空间对象
        border_entity: 图框全量信息

    Returns:关联墙列表

    """
    nonbear_wall_list = border_entity.entity_object_dict.get("墙", [])
    related_wall_list = []
    for wall in nonbear_wall_list:
        wall_cnt = wall.contour.contour
        expand_wall_cnt = expand_contour(wall_cnt, 5)
        if get_contours_iou(space_object.contour.contour, expand_wall_cnt) > 0:
            related_wall_list.append(wall)
    return related_wall_list


def get_bounding_axis_line_and_label(space_object, border_entity):


    axis_line_list = []
    axis_label_list = []

    axis_line_list_list = border_entity.axis_net_line_list.copy()
    axis_label_list_list = border_entity.axis_net_line_num_list.copy()
    axis_net_bbox_list = border_entity.axis_net_bbox_list.copy()

    #选取空间所在的这个轴网bbox
    for index, bbox in enumerate(axis_net_bbox_list):
        if get_contours_iou(get_contour_from_bbox(bbox), space_object.contour.contour):
            axis_line_list = axis_line_list_list[index]
            axis_label_list = axis_label_list_list[index]
            continue

    space_centre_point = [int((space_object.bbox.list[0] + space_object.bbox.list[2])/2),
                          int((space_object.bbox.list[1] + space_object.bbox.list[3])/2)]

    final_bounding_axis_line, final_bounding_axis_label = [], []
    for i in range(2):
        bounding_axis_line = []
        bounding_axis_label = []
        point_distance_list = []
        for line in final_bounding_axis_line:
            axis_line_list.remove(line)
        for label in final_bounding_axis_label:
            axis_label_list.remove(label)
        #轴线数和轴标数必须大于0
        if len(axis_line_list) > 2 and len(axis_label_list) > 2:
            #计算每个轴线距离空间中心点的距离并添加进一个新的list中
            for index, line in enumerate(axis_line_list):
                corre_point = point_project_on_line(space_centre_point, line)
                point_distance = point_euclidean_distance(space_centre_point, corre_point)
                point_distance_list.append([point_distance, index])
            #对[[距中心点距离，轴线index], ....]进行排序
            point_distance_list.sort(key=lambda x: x[0])
            sorted_point_distance_list = point_distance_list
            sorted_point_distance_list_copy = sorted_point_distance_list.copy()
            for i, point_distance in enumerate(sorted_point_distance_list_copy):
                if i == len(sorted_point_distance_list_copy) - 1: break
                line_index = point_distance[1]
                for distance_index_pair in sorted_point_distance_list_copy[i+1:]:
                    line_index_pair = distance_index_pair[1]
                    if line_index_pair != line_index:
                        line_degree = angle_between_segment2(np.array(reshape_line(axis_line_list[line_index])),
                                                             np.array(reshape_line(axis_line_list[line_index_pair])))
                        # cross_point = get_line_cross_point(axis_line_list[line_index], axis_line_list[line_index_pair])
                        if 87 < line_degree < 92:
                            bounding_axis_line.append(axis_line_list[line_index])
                            bounding_axis_label.append(axis_label_list[line_index])

                            bounding_axis_line.append(axis_line_list[line_index_pair])
                            bounding_axis_label.append(axis_label_list[line_index_pair])
                            break
                if len(bounding_axis_line) == 2: break
            #     #如果筛选结果里没有互相垂直的一对
            #     if len(bounding_axis_line) == 0:
            #         for distance_index_pair in sorted_point_distance_list:
            #             distance_pair = distance_index_pair[0]
            #             line_index_pair = distance_index_pair[1]
            #             if line_index_pair != line_index:
            #                 line_degree = angle_between_segment2(np.array(reshape_line(axis_line_list[line_index])),
            #                                                      np.array(reshape_line(axis_line_list[line_index_pair])))
            #                 cross_point = get_line_cross_point(axis_line_list[line_index], axis_line_list[line_index_pair])
            #                 if 87 < line_degree < 92 :
            #                     bounding_axis_line.append(axis_line_list[line_index])
            #                     bounding_axis_label.append(axis_label_list[line_index])
            #
            #                     bounding_axis_line.append(axis_line_list[line_index_pair])
            #                     bounding_axis_label.append(axis_label_list[line_index_pair])
            #                     break
            # #如果筛选结果没有一个符合条件，那么挑选两个最近的互相垂直的轴线
            # else:
            #     if len(sorted_point_distance_list) > 0:
            #         distance = sorted_point_distance_list[0][0]
            #         line_index = sorted_point_distance_list[0][1]
            #         for distance_index_pair in sorted_point_distance_list:
            #             distance_pair = distance_index_pair[0]
            #             line_index_pair = distance_index_pair[1]
            #             if line_index_pair != line_index:
            #                 line_degree = angle_between_segment2(np.array(reshape_line(axis_line_list[line_index])),
            #                                                      np.array(reshape_line(axis_line_list[line_index_pair])))
            #                 cross_point = get_line_cross_point(axis_line_list[line_index], axis_line_list[line_index_pair])
            #                 if 87 < line_degree < 92:
            #                     bounding_axis_line.append(axis_line_list[line_index])
            #                     bounding_axis_label.append(axis_label_list[line_index])
            #
            #                     bounding_axis_line.append(axis_line_list[line_index_pair])
            #                     bounding_axis_label.append(axis_label_list[line_index_pair])
            #                     break
        print("bounding_axis_line: ", bounding_axis_line, "bounding_axis_label: ", bounding_axis_label)
        final_bounding_axis_line.extend(bounding_axis_line)
        final_bounding_axis_label.extend(bounding_axis_label)

    #返回两个互相垂直的轴线和两个对应的轴标
    return final_bounding_axis_line, final_bounding_axis_label

def get_stair_room_wall_thickness(entity_object, border_entity):

    space_scale = border_entity.space_scale
    border_coord = border_entity.border_coord
    ratio = border_entity.ratio
    origin_border_entity_info = border_entity.origin_border_entity_info
    wall_point_list = [None, None]
    plan_stair_tabu_list_ori = border_entity.mark_object_dict["平面楼梯踏步"]
    wall_list = entity_object.related_wall
    image_manager = border_entity.image_manager
    height, width = image_manager.img_height, image_manager.img_width
    img_temp = np.zeros((height, width, 3), dtype=np.uint8)

    plan_stair_tabu_list = []
    for tabu in plan_stair_tabu_list_ori:
        tabu_bbox = tabu.bounding_rectangle.list
        tabu_cnt = get_contour_from_bbox(tabu_bbox)
        if get_contours_iou(entity_object.contour.contour, tabu_cnt) > 0.5:
            plan_stair_tabu_list.append(tabu)

    if len(wall_list) == 0:
        print("未获取到墙列表")
        return wall_point_list
    if len(plan_stair_tabu_list) == 0:
        print("[Note]楼梯踏步未获取到！")
        return wall_point_list
    plan_stair_tabu = plan_stair_tabu_list[0]
    tabu_bbox = plan_stair_tabu.bounding_rectangle.list


    stair_line_list = []  # 楼梯踏脚线段

    # 获取所有楼梯层中的直线
    layer_to_check = ['stair_dayang_plan_stair', 'elevator_stair', 'elevator_box', 'elevation_handrail',
                      'indoor_access']
    class_to_check = ['Line', 'Polyline', 'Polyline2d']
    stair_line_dict = get_origin_border_entity_info_rule(origin_border_entity_info, layer_to_check,
                                                    class_to_check, space_scale, border_coord, ratio)
    for layer, entity_list in stair_line_dict.items():
        stair_line_list.extend(entity_list)
    # Polyline中有arc，需要过滤
    stair_line_list = list(filter(lambda x: len(x) == 4, stair_line_list))
    need_stair_line_list = entity_in_bbox(stair_line_list, tabu_bbox)
    max_length = 0
    need_stair_line = None
    for line in need_stair_line_list:
        line_length = point_euclidean_distance(line[:2], line[2:])
        if max_length < line_length:
            max_length = line_length
            need_stair_line = line
    if need_stair_line is None:
        print("没有找到合适的楼梯线！！")
        return wall_point_list
    print("need_stair_line: ", need_stair_line)
    cv2.line(img_temp, tuple(need_stair_line[:2]), tuple(need_stair_line[2:]), (0,0,255),3)

    pair_paralell_line_list = []
    for wall in wall_list:

        wall_contour = wall.contour.contour
        wall_lines = get_contour_lines(wall_contour)
        wall_lines = list(filter(lambda x: point_euclidean_distance(x[:2], x[2:]) > 2, wall_lines))
        # print("len of wall_lines: ", len(wall_lines))
        parallel_wall_line = None
        min_dis_1 = float("inf")
        for wall_line_1 in wall_lines:
            duplicate_wall = False
            cv2.line(img_temp, tuple(wall_line_1[:2]), tuple(wall_line_1[2:]), (0, 255, 255), 3)

            angle = angle_between_segment2(np.array([need_stair_line[:2], need_stair_line[2:]]),
                                           np.array([wall_line_1[:2], wall_line_1[2:]]))
            # print("angle: ", angle, " wall_line_1: ", wall_line_1)
            if 3 < angle < 177: continue
            shadow_line, shadow_length = line_project_on_line_v3(wall_line_1, need_stair_line)
            # print("shadow_length: ", shadow_length)
            if shadow_length < 1: continue
            for line_temp_list in pair_paralell_line_list:
                for line_temp in line_temp_list:
                    dis_temp = get_parallel_line_distance(line_temp, wall_line_1)
                    if dis_temp < 1000 * ratio[0]:
                        duplicate_wall = True
                        break
            if duplicate_wall: continue
            dis_1 = get_parallel_line_distance(need_stair_line, wall_line_1)
            if dis_1 < min_dis_1:
                min_dis_1 = dis_1

                parallel_wall_line = wall_line_1
            # print("找到一根平行的墙的墙线： ", wall_line_1)
            # break
        if parallel_wall_line is not None:
            parallel_wall_line_2 = None
            min_dis_2 = float("inf")
            for wall_line_2 in wall_lines:
                if wall_line_2 == parallel_wall_line: continue
                angle = angle_between_segment2(np.array([parallel_wall_line[:2], parallel_wall_line[2:]]),
                                               np.array([wall_line_2[:2], wall_line_2[2:]]))
                if 3 < angle < 177: continue
                shadow_line, shadow_length = line_project_on_line_v3(parallel_wall_line, wall_line_2)
                if shadow_length < 1: continue
                dis_2 = get_parallel_line_distance(parallel_wall_line, wall_line_2)
                if dis_2 < min_dis_2:
                    min_dis_2 = dis_2
                    parallel_wall_line_2 = wall_line_2
                # print("找到第二根平行的墙的墙线： ", parallel_wall_line_2)
            if parallel_wall_line_2 is not None:
                pair_paralell_line_list.append([parallel_wall_line, parallel_wall_line_2])
        if len(pair_paralell_line_list) == 2: break
    # cv2.imwrite("/Users/shanks/desktop/img_temp/stairroom_wall.png", img_temp)
    for i, pair_wall_lines in enumerate(pair_paralell_line_list):
        wall_line_1, wall_line_2 = pair_wall_lines[0], pair_wall_lines[1]
        p1 = point_project_on_line(need_stair_line[:2], wall_line_1)
        p2 = point_project_on_line(need_stair_line[:2], wall_line_2)
        wall_point_list[i] = [list(p1), list(p2)]

    return wall_point_list


def get_hu_type_from_subproject(subproject_name):
    """

    Args:
        subproject_name:

    Returns:

    """
    re_result = re.finditer('Y[a-zA-Z0-9]+', subproject_name)
    hu_type_list = [j.group() for j in re_result]
    return hu_type_list
