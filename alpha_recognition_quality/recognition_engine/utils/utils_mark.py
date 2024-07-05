# -*- coding: utf-8 -*-

import functools
import math
import re
from copy import deepcopy
from collections import defaultdict

import cv2
import numpy as np
import shapely
from shapely.geometry import LineString, Polygon, MultiLineString, Point
from .utils_objectification_common import *
from ...config_manager.text_config import TextType
from ...common.utils import *
from ...common.utils_draw_and_rule import *


########################################
#            吕琨整理                  ##
#######################################


# 获取标高信息
def labeled_height_mark(mark_bbox, border_entity_info):
    """

    Args:
        mark_bbox: 标记的外接矩形框
        border_entity_info: 图层全量信息

    Returns:
        标高信息
    """
    return_elevation_info = None
    ratio = border_entity_info.ratio

    bbox_long = 2000 * ratio[0]
    bbox_short = 1000 * ratio[0]
    point_A = get_centroid(mark_bbox)
    bbox_temp = extend_margin_by_side_object(mark_bbox, bbox_long, "long")
    bbox_temp = extend_margin_by_side_object(bbox_temp, bbox_short, "short")
    # bbox_temp = extend_rect(mark_bbox, line_ext=bbox_short, direction='short', double_side=(True, True))
    # bbox_temp = extend_rect(bbox_temp, line_ext=bbox_long, direction='long', double_side=(True, True))

    pattern = "-?\d+\.\d+|SLAN"
    all_text_info = border_entity_info.border_text_info[TextType.ALL]
    all_elevation_text = [text.bbox.list + [text.extend_message]
                          for text in all_text_info if re.search(pattern, text.extend_message)]

    height = border_entity_info.image_manager.img_height
    width = border_entity_info.image_manager.img_width
    n_num = 10  # 图框划分成20*20个网格
    h = np.ceil(height / n_num)  # 网格高度
    w = np.ceil(width / n_num)  # 网格宽度
    elevation_text = get_mesh_grid_dict(all_elevation_text, w, h)
    nearby_elevation_text_list = get_grid_range(bbox_temp, elevation_text, w, h)
    min_distance = float("inf")
    for text in nearby_elevation_text_list:
        point_B = text[0:4]
        distance_A_B = point_euclidean_distance(point_A, point_B)
        if distance_A_B < min_distance:
            return_elevation_info = re.search(pattern,text[-1]).group()
            min_distance = distance_A_B
    return return_elevation_info

########################################
#            马玄整理                  ##
#######################################

def get_elevation_type_mark(bbox, border_entity):
    """
    根据标高构件获取标高类型属性
    Args:
        bbox：标高构件外接矩形框
        border_entity:
    Returns:
        标高属性列表，数据类型：List
    """
    elevation_type = []
    ratio = border_entity.ratio
    elevation_bbox = bbox
    ext_margin_long = int(2000 * ratio[0])
    ext_margin_short = int(1000 * ratio[0])
    border_text_info = border_entity.border_text_info
    all_text_info = border_text_info[TextType.ALL]
    # 对标高沿长短边外扩
    if (elevation_bbox[2] - elevation_bbox[0]) > (elevation_bbox[3] - elevation_bbox[1]):
        ext_elevation_bbox = [elevation_bbox[0] - ext_margin_long, elevation_bbox[1] - ext_margin_short,
                              elevation_bbox[2] + ext_margin_long, elevation_bbox[3] + ext_margin_short]
    else:
        ext_elevation_bbox = [elevation_bbox[0] - ext_margin_short, elevation_bbox[1] - ext_margin_long,
                              elevation_bbox[2] + ext_margin_short, elevation_bbox[3] + ext_margin_long]
    #  查找外扩后框内的标高数字文本
    elevation_text_info_list = []
    for text_info in all_text_info:
        text_bbox = text_info.bbox.list
        if bbox_intersect_bbox(ext_elevation_bbox, text_bbox):
            if re.search("\d\.\d{3}", text_info.extend_message):
                elevation_text_info_list.append(text_info)

    # 遍历每一个标高数字文本，将其外扩5个文字
    for text_info in elevation_text_info_list:
        text_bbox = text_info.bbox.list
        text_bbox.append(text_info.extend_message)
        width, height = get_word_info(text_bbox)
        ext_margin = width * 5
        ext_text_bbox = [text_bbox[0] - ext_margin, text_bbox[1], text_bbox[2] + ext_margin, text_bbox[3]]
        # 寻找标高数值附近的属性值
        text_type = None
        for info in all_text_info:
            bbox = info.bbox.list
            if bbox_intersect_bbox(ext_text_bbox, bbox):
                if re.search("建", info.extend_message):
                    text_type = "建筑标高"
                elif re.search("结", info.extend_message):
                    text_type = "结构标高"
                elif re.search("绝", info.extend_message):
                    text_type = "绝对标高"
                elif re.search("H", info.extend_message):
                    continue
            if text_type is not None:
                elevation_type.append(text_type)
                break
    return elevation_type


# 获取标高类型数值对应字典
def get_elevation_type_value_dict_mark(bbox, border_entity):
    """
    根据标高构件获取标高类型和数值
    Args:
        bbox：标高构件外接矩形框
        border_entity:
    Returns:
        标高类型和数值属性字典，数据类型：Dict
    """
    elevation_type = []
    ratio = border_entity.ratio
    elevation_bbox = bbox
    ext_margin_long = int(2000 * ratio[0])
    ext_margin_short = int(1000 * ratio[0])
    border_text_info = border_entity.border_text_info
    all_text_info = border_text_info[TextType.ALL]
    elevation_type_value_dict = dict()
    # 对标高沿短边外扩以及长边向上扩充
    ext_elevation_bbox = [elevation_bbox[0] - ext_margin_short, elevation_bbox[1] - ext_margin_long,
                          elevation_bbox[2] + ext_margin_short, elevation_bbox[1]]
    #  查找外扩后框内的标高数字文本
    elevation_text_info_list = []
    elevation_value = []
    for text_info in all_text_info:
        text_bbox = text_info.bbox.list
        if bbox_intersect_bbox_object(ext_elevation_bbox, text_bbox):
            if re.search("-?\d\.\d{3}", text_info.extend_message):
                elevation_text_info_list.append(text_info)
                elevation_value.append(eval(re.search("-?\d\.\d{3}", text_info.extend_message).group()))
    # 遍历每一个标高数字文本，将其外扩5个文字
    for text_info in elevation_text_info_list:
        text_bbox = text_info.bbox.list
        text_bbox.append(text_info.extend_message)
        width, height = get_word_info(text_bbox)
        ext_margin = width * 5
        ext_text_bbox = [text_bbox[0] - ext_margin, text_bbox[1], text_bbox[2] + ext_margin, text_bbox[3]]
        # 寻找标高数值附近的属性值
        text_type = None
        for info in all_text_info:
            bbox = info.bbox.list
            if bbox_intersect_bbox(ext_text_bbox, bbox):
                if re.search("建", info.extend_message):
                    text_type = "建筑标高"
                elif re.search("结", info.extend_message):
                    text_type = "结构标高"
                elif re.search("绝", info.extend_message):
                    text_type = "绝对标高"
                elif re.search("H", info.extend_message):
                    text_type = "楼层相对标高"
            if text_type is not None:
                break
        elevation_type.append(text_type)
    if "建筑标高" in elevation_type:
        for i, ele_type in enumerate(elevation_type):
            if ele_type == "建筑标高" or ele_type == "结构标高" or ele_type == "绝对标高":
                elevation_type_value_dict[ele_type] = elevation_value[i]
    else:
        for i, ele_type in enumerate(elevation_type):
            if ele_type == "结构标高" or ele_type == "绝对标高":
                elevation_type_value_dict[ele_type] = elevation_value[i]
            elif ele_type == None:
                elevation_type_value_dict["建筑标高"] = elevation_value[i]
    return elevation_type_value_dict
