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

from ...common.utils import convert_CAD_coord_to_bbox, convert_CAD_coord_to_coord, convert_CAD_point, get_vector_angle_2D
from ...common.utils import point_in_bbox


# ######################################################
#                         劲松整理                      #
# ######################################################


# 表格从CAD转到png
def table_CAD_to_png_object(border_coord, border_information_info, ratio):
    """

    Args:
        border_coord: 图框坐标
        border_information_info: 图框全量信息
        ratio: 转换比

    Returns:
        表格信息
    """
    # print(border_information_info)
    table_info_list = []
    coordinate_fun = lambda x: [x[0][0], x[0][1], x[1][0], x[1][1]]
    for table in border_information_info['tables']:
        cell_list = []
        table_name = table['tableName']
        table_bound = convert_CAD_coord_to_bbox(border_coord, coordinate_fun(eval(table['bound'])), ratio)
        for cell in table['cells']:
            cell_text = cell['text']
            cell_coordinate = convert_CAD_coord_to_bbox(border_coord, coordinate_fun(eval(cell['cell'])), ratio)
            cell_coordinate.append(cell_text)
            cell_list.append(cell_coordinate)
        table_info = {'tableName': table_name, 'bound': table_bound, 'cells': cell_list}
        table_info_list.append(table_info)

    return table_info_list


# 扩大bbox用于合并
def extend_margin_by_side_object(bbox, margin, side='long'):
    """

    Args:
        bbox: 矩形框
        margin: 外扩间距
        side: 外扩方向

    Returns:
        外扩后的矩形框
    """
    width, height = (bbox[2] - bbox[0], bbox[3] - bbox[1])

    if (side == 'long' and width > height) or (side == 'short' and width <= height):
        return [bbox[0], bbox[1] - margin, bbox[2], bbox[3] + margin]
    else:
        return [bbox[0] - margin, bbox[1], bbox[2] + margin, bbox[3]]


def bbox_intersect_bbox_object(bbox1, bbox2):
    '''
    判断bbox1与bbox2是否有交叠
    Param:
        bbox1: [x1,y1,x2,y2]，检测框的左上角和右下角顶点的坐标
        bbox2: [x1,y1,x2,y2]，检测框的左上角和右下角顶点的坐标
    Return:
        若bbox1与bbox2存在交叠区域，则返回True，否则返回False
    '''
    x_min, y_min, x_max, y_max = bbox2[0], bbox2[1], bbox2[2], bbox2[3]
    x1, y1, x2, y2 = bbox1[0], bbox1[1], bbox1[2], bbox1[3]

    if y2 < y_min or y1 > y_max:  # bbox1处于bbox2的上方或下方
        return False
    elif x2 < x_min or x1 > x_max:  # bbox1处于bbox2的左方或右方
        return False

    return True


def get_floor_contour_object(img, tree=False):
    '''
    从包含若干楼栋轮廓的大图中，获取每个楼栋轮廓的坐标。
    Param:
        img: 包含若干楼栋轮廓的BGR大图
        tree: 若为True，则使用cv2.RETR_TREE选项提取轮廓内嵌套的子轮廓
    Return:
        floor_contour_list: list of numpy array of shape (-1,1,2)
    '''

    assert type(img) == np.ndarray and len(img.shape) == 3, print(
        "Input image to get_floor_contour() should be BGR numpy array.")

    # 去掉外框并转为灰度图
    gray = cv2.cvtColor(img[20:-20, 20:-20, :], cv2.COLOR_BGR2GRAY).astype(np.uint8)
    _, gray = cv2.threshold(gray, 10, 255, 0)

    edges = cv2.Canny(gray, 20, 255)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))

    opened = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=1)

    # 获取轮廓
    if tree:
        if "3.4" in cv2.__version__:
            _, contours, hierarchy = cv2.findContours(
                opened, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, hierarchy = cv2.findContours(
                opened, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        N = len(contours)
        contours = [contours[i] for i in range(N) if hierarchy[0][i][3] >= 0]
    else:
        if "3.4" in cv2.__version__:
            _, contours, hierarchy = cv2.findContours(
                opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, hierarchy = cv2.findContours(
                opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 后处理
    floor_contour_list = []

    for cnt in contours:
        # 楼栋轮廓的顶点不会少于4个
        if cnt.shape[0] < 4:
            continue
        floor_contour = cnt + 20  # 加回去掉外框时缩进的距离
        floor_contour_list.append(floor_contour)

    return floor_contour_list


def get_hatch_info_object(bounding_rectangle_list, border_entity):
    """
    获取墙填充的信息
    :param bounding_rectangle_list: 所有墙填充的边界
    :param border_entity: 全量信息
    :return: hatch_info_list: 墙填充信息
    """
    hatch_info_list = []

    height, width = border_entity.image_manager.img_height, border_entity.image_manager.img_width
    ext_margin = border_entity.ext_margin
    backgroud_image = np.zeros((height, width, 3), dtype=np.float32)

    # 将直线画在背景图上
    for line in bounding_rectangle_list:
        cv2.line(backgroud_image, tuple(line[:2]), tuple(line[2:4]), (255, 255, 255), 1)

    gray = cv2.cvtColor(backgroud_image, cv2.COLOR_BGR2GRAY)
    gray = gray.astype(np.uint8)

    # 寻找轮廓，注意cv2版本不同，findContours函数返回值有差异
    if '3.4' in cv2.__version__:
        _, contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        line_list = []
        rect = cv2.boundingRect(cnt)
        bbox = [rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]]
        bbox = [bbox[0] - ext_margin, bbox[1] - ext_margin, bbox[2] + ext_margin, bbox[3] + ext_margin]
        for line in bounding_rectangle_list:
            if point_in_bbox(line[:2], bbox) and point_in_bbox(line[2:], bbox):
                line_list.append(line)
        hatch_info_list.append([bbox, line_list])

    return hatch_info_list


# 弧度转角度
def rad_to_angle_object(rad, radius):
    """

    Args:
        rad: 弧度
        radius: 半径

    Returns:
        角度
    """
    if rad and radius:
        angle = round((rad * 180) / math.pi, 2)
    else:
        angle = 0
    return angle


# 返回一个轮廓的最小外接矩形
def get_bbox_from_contour_object(contour):
    """

    Args:
        contour: 轮廓

    Returns:
        矩形框

    """
    x, y, w, h = cv2.boundingRect(contour)

    return [x, y, x + w, y + h]


def get_origin_border_entity_info_rule_object(origin_border_entity_info, layer_to_check, class_to_check, scale, border_coord,
                                       ratio):
    '''
    通过原始解析数据中，整理图层构件附加信息
    Param:
        origin_border_entity_info: 是包含该图框所有信息的一个字典
        layer_to_check: 待整理图层
        class_to_check：待整理图元类型
        scale: CAD图纸中图框布局空间和模型空间单位比例
        border_coord： CAD图框组表
        ratio： CAD转png坐标比例
    Return:
        entity_info_all: 字典，key为图层名，value是整理后的构件信息列表
    '''
    entity_info_all = defaultdict(list)  # 初始化，默认值为列表的字典
    # 遍历原始字典内容，判断是否为所需图层
    for layer, layer_entity_info in origin_border_entity_info.items():
        if layer in layer_to_check:
            # 遍历图层内构件信息，构件信息依次为图元坐标，图元类别，图元附加信息
            for entity_info in layer_entity_info:
                # print('entity_info', entity_info)
                # entity_coord, entity_class, ex_info = entity_info
                entity_coord, entity_class, ex_info = entity_info.coord, entity_info.entity_type.value, entity_info.extend_storage
                if entity_class not in class_to_check:
                    continue
                if entity_class == 'Line':  # line坐标直接转model坐标后转png坐标
                    ex_info_cov = [_ * scale for _ in eval(ex_info)]  # 处理string形信息并scale换算
                    ex_info_cov_pix = convert_CAD_coord_to_coord(border_coord, ex_info_cov, ratio)  # 转为png坐标
                    if ex_info_cov_pix is None or len(ex_info_cov_pix) != 4:
                        continue
                    entity_info_all[layer].append(ex_info_cov_pix)  # 添加信息
                elif entity_class in ['Polyline', 'Polyline2d']:
                    # print('ex_info', ex_info)
                    ex_info_list = re.split(r'[?::|;|L|A]', ex_info)[2::3]  # 去掉标志符号转png坐标
                    # 遍历多段线
                    for ex_info_split in ex_info_list:
                        ex_info_split = eval(ex_info_split)  # 处理string信息
                        # 2020年8月之前的万翼解析不含有线宽信息
                        if len(ex_info_split) == 4:
                            ex_info_cov = (np.array(ex_info_split) * scale).tolist()  # 直线型
                        elif len(ex_info_split) == 8:
                            ex_info_cov = [_ * scale for _ in ex_info_split[:-1]] + [
                                rad_to_angle_object(ex_info_split[-1], ex_info_split[-2])]  # arc型
                        # TODO: 2020年8月之后的万翼解析中含有线宽，但目前不需要，若后期需要，在这里提取
                        elif len(ex_info_split) == 6:
                            ex_info_cov = (np.array(ex_info_split[:4]) * scale).tolist()  # 含有线宽的直线型
                        elif len(ex_info_split) == 10:
                            ex_info_cov = [_ * scale for _ in ex_info_split[:-3]] + [
                                rad_to_angle_object(ex_info_split[-3], ex_info_split[-4])]  # 含有线宽的arc型
                        else:
                            print('unknown lenth', ex_info_split)
                            continue
                        ex_info_cov_pix = convert_CAD_coord_to_coord(border_coord, ex_info_cov, ratio)  # 转png坐标
                        if ex_info_cov_pix is None or (len(ex_info_cov_pix) != 4 and len(ex_info_cov_pix) != 8):
                            continue
                        entity_info_all[layer].append(ex_info_cov_pix)  # 添加信息
                elif entity_class == 'Arc':
                    ex_info = eval(ex_info)  # string型
                    ex_info_cov = [_ * scale for _ in ex_info[:-1]] + [rad_to_angle_object(ex_info[-1], ex_info[-2])]  # 转模型空间
                    ex_info_cov_pix = convert_CAD_coord_to_coord(border_coord, ex_info_cov, ratio)  # 转png坐标
                    if ex_info_cov_pix is None or len(ex_info_cov_pix) != 8:
                        continue
                    entity_info_all[layer].append(ex_info_cov_pix)
                elif entity_class == 'Hatch':  # Hatch仅返回了bbox
                    entity_bbox = entity_coord
                    if len(entity_bbox) != 4:
                        continue
                    entity_info_all[layer].append(entity_bbox)
                elif entity_class == "Circle":
                    ex_info_cov = [_ * scale for _ in eval(ex_info)]  # 处理string形信息并scale换算
                    ex_info_cov_pix = convert_CAD_point(border_coord, ex_info_cov[:2], ratio) + \
                                      [int(ex_info_cov[-1] * ratio[0])]  # 转为png坐标
                    entity_info_all[layer].append(ex_info_cov_pix)
                elif entity_class == 'Ellipse':
                    ex_info = eval(ex_info)  # string型
                    if len(ex_info) != 13:
                        continue
                    # 转模型空间
                    ex_info_cov = [_ * scale for _ in ex_info[:4]] + \
                                  [get_vector_angle_2D(ex_info[4:6]), rad_to_angle_object(ex_info[7], True),
                                   rad_to_angle_object(ex_info[8], True)] + \
                                  [_ * scale for _ in ex_info[9:]]
                    ex_info_cov_pix = convert_CAD_coord_to_coord(border_coord, ex_info_cov, ratio)  # 转png坐标
                    if ex_info_cov_pix is None or len(ex_info_cov_pix) != 11:
                        continue
                    entity_info_all[layer].append(ex_info_cov_pix)
                elif entity_class == "Solid":  # Solid仅返回bbox rule506006 通过箭头找引下线
                    entity_bbox = entity_coord
                    if len(entity_bbox) != 4:
                        continue
                    entity_info_all[layer].append(entity_bbox)
                else:
                    # print('unresolved entity_class', entity_class)  # 包括hatch poly2d等
                    continue
    return entity_info_all

def is_business_material_border(drawing_name):
    '''
    判断是不是商业外墙材料表
    '''
    if re.search("商(业|铺)", drawing_name) or re.search("公(共|建)", drawing_name):
        return True
    else:
        return False




