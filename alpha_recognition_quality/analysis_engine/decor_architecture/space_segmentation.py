# -*- coding: utf-8 -*-

import os
import math
import re
import gc

from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2
from shapely.geometry import LineString, Polygon
from concurrent.futures import ProcessPoolExecutor
from ...common.decorator import timer
from ...common.utils import *
from ...common.CONSTANTS import wall_thickness_CAD, IMAGE_PRINT_EXTENSION

from ...config import DEBUG_MODEL, SAVE_RECOG_GEN_IMG_ONLINE

from ...config_manager.decor_architecture.drawing_config import DrawingType
from ...config_manager.text_config import TextType
from ...design_object.cad_base.cad_manager.fonts import FONT_DIR
from ..utils.utils_analysis_common import *
from ..utils.utils_segmentation import *
from ..CONSTANTS import *


def get_mesh_grid_for_wall_pillar(wall_pillar_line_list, width, height):
    """
    根据墙线的数量，调整网格划分粒度，若墙线数量很多，说明图纸很大，可以划分的较细
    Args:
        wall_pillar_line_list: 墙柱图元集合
        width: 图像总宽度
        height: 图像总高度
    Returns:
        wall_pillar_line_dict: 墙柱图元划分结果。一个字典，key为一个坐标范围，value为一个bbox_list
        w_range: 每个格子的宽度，单位：像素个数
        h_range: 每个格子的高度，单位：像素个数
    """
    len_wall_pillar = len(wall_pillar_line_list)
    if len_wall_pillar < 10000:
        n_num = 10
    elif len_wall_pillar < 25000:
        n_num = 20
    elif len_wall_pillar < 50000:
        n_num = 30
    elif len_wall_pillar < 100000:
        n_num = 40
    else:
        n_num = 50
    h_range, w_range = tuple(map(lambda x: np.ceil(x / n_num), (height, width)))  # grid size
    wall_pillar_line_dict = get_mesh_grid_dict(wall_pillar_line_list, w_range, h_range)

    return wall_pillar_line_dict, w_range, h_range


def get_base_segmentation_img(image_manager, border_entity_bbox_dict):
    """
    得到空间分割的底图（只包含墙柱的实线图元）
    Args:
        image_manager: 图片管理器
        border_entity_bbox_dict: 构件合并后的结果信息
    Returns: img_space: 底图
    """
    img_space = image_manager.load_from_manager(IMG_SPACE_RECOG_KEY)
    # 将img_space中的虚线wall_line_dash和pillar_line_dash擦除;
    for dash_line in border_entity_bbox_dict['wall_line_dash'] + border_entity_bbox_dict['pillar_line_dash']:
        cv2.line(img_space, (dash_line[0], dash_line[1]), (dash_line[2], dash_line[3]), (0, 0, 0), 1)
    return img_space


def get_door_base_coords_by_entity(entity_infos, border_entity_info, arc_entity_dict, line_entity_dict, ellipse_entity_dict,
                                   w_range, h_range, wall_pillar_line_dict, line_dash_entity_list, line_entity_list):
    """
    获取能代替门窗构件entity的土建联线
    Args:
        entity_infos: [[bbox, layer], ...]
                       bbox:  构件的bbox坐标
                       layer: 构件所在的图层
        border_entity_info:   图框构件信息
        arc_entity_dict:      图框内所有arc的原始图元按网格划分后的结果
        line_entity_dict:     图框内所有line的原始图元按网格划分后的结果
        ellipse_entity_dict:  图框内所有ellipse的原始图元按网格划分后的结果
        w_range:              网格划分标准。每个格子的宽度
        h_range:              网格划分标准。每个格子的高度
        wall_pillar_line_dict:图框内所有墙柱原始图元按网格划分后的结果
        line_dash_entity_list:图框内所有虚线line原始图元
        line_entity_list:     图框内所有line的原始图元
    Returns: draw_lines:[[line, color, line_width, save_target], ...] 需要画在space_seg中的土建连线
                 line:线的png坐标；color:画在space_seg中时的颜色, line_width: 画在space_seg中时的长度,
                 save_target:线需要存储的话，为对应存储列表的str；不需要存储则此项为None
             used_origin_lines:[line1, line2, ...] 土建连线所代替的门窗图元集合
    """
    ext_margin = border_entity_info['ext_margin']
    ratio = border_entity_info['ratio']
    image_manager = border_entity_info['image_manager']
    # for debug
    img_copy = image_manager.load_from_manager(IMG_WITH_WALL_KEY)
    wall_thickness = math.ceil(wall_thickness_CAD * ratio[0])
    major = border_entity_info["major"]
    draw_lines = []
    used_origin_lines = []
    for ei, (entity, layer) in enumerate(entity_infos):
        # for debug
        # if ei not in [16]: continue
        # if layer not in ["door"]: continue
        # cv2.rectangle(img_copy, (entity[0], entity[1]), (entity[2], entity[3]), (255,255,0), 3)
        # cv2.putText(img_copy, f'{ei}', (entity[0], entity[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        # 非电梯厢层
        if layer not in ["elevator_box", 'stair_dayang_plan_stair']:
            expanded_door_bbox = extend_margin(entity, ext_margin * 3)
            shrinked_door_bbox = remove_margin(entity, ext_margin - 2)

            # 记录构件的四种原始信息，内部arc、内部line，内部长直线、内部有平行关系的线
            arc_in_list = entity_in_bbox(get_grid_range(entity, arc_entity_dict, w_range, h_range), shrinked_door_bbox)
            # 硬装专业需要过滤掉小的圆弧
            arc_in_list = list(filter(lambda x: x[-2] > wall_thickness, arc_in_list))
            line_in_list = entity_in_bbox(get_grid_range(entity, line_entity_dict, w_range, h_range), shrinked_door_bbox)
            ellipse_in_list = entity_in_bbox(get_grid_range(entity, ellipse_entity_dict, w_range, h_range), shrinked_door_bbox)
            # 因为有些门的弧线是用ellipse类型画的，这里将所有的arc和ellipse进行合并
            arc_in_list = arc_in_list + ellipse_in_list

            # 将包含在门窗bbox内的直线图元记录在used_origin_lines中，不参与之后的single_dw_line的计算。但若门窗bbox内只有一条直线的也需
            # 在singlw_dw_line中重新计算
            if len(line_in_list) != 1:
                used_origin_lines.extend(line_in_list)

            # 之所以要过滤一些短线，是因为有些门画了很多短线，容易干扰我们的判断，但是这个过滤阈值200不知道可不可靠
            filtered_line_in_list = [_ for _ in line_in_list if
                                     point_euclidean_distance(_[0:2], _[2:4]) > 200 * ratio[0]]
            # 根据玉霖detect_parallel_line中的注释，返回值parallel_line_list是门联窗形式平行线，数量大于两条，距离小于200cad单位
            parallel_line_list = detect_parallel_line(filtered_line_in_list, ratio)

            # TODO:带圆弧的折线窗不能作为带弧线的门处理，可能造成空间闭合错误的情况（issue2060中带弧线的折线窗弧线合并在一起，除弧线之外的部分合并在一起）
            # TODO:已添加带弧线的折线窗的处理逻辑，根据issue 1940，有待后续验证

            # 有些很长的窗户也带有弧线，走弧线门的逻辑可能导致空间不封闭，所以判断 parallel_line_list 中是否有3条及以上的直线长度大于2500的平行直线，若有，则走窗户构件的逻辑
            longer_than_2500 = [True if point_euclidean_distance(l[:2], l[2:]) > 2500 * ratio[0] else False
                                for l in parallel_line_list]
            num_longer_than_2500 = sum(longer_than_2500)

            # 无弧线情况 (包括普通窗、折线窗、推拉门、电梯门、某些管井门、不含弧线的普通门)，先尝试获取土建连线，并画出内部直线
            if len(arc_in_list) == 0 or num_longer_than_2500 >= 3:
                # 对于没有弧线的门窗，判断是不是其bbox内的所有直线都是虚线类型，如果是则跳过
                is_all_dash = True
                for line_dw in line_in_list:
                    if line_dw not in line_dash_entity_list:
                        is_all_dash = False
                        break
                if is_all_dash:
                    continue
                # 没有弧线的门如果直接画出门中的直线，会造成空间不闭合的情况，通过尝试获取构件bbox内的土建连线来处理此类门
                _, _, inside_wall_point_list, _ = get_entity_wall_width_v2(
                    wall_pillar_line_dict, [entity], ext_margin, wall_thickness, (ratio[0], ratio[1]),
                    (w_range, h_range), to_mesh_grid=False)
                if len(inside_wall_point_list) != 0:
                    inside_wall_point_list = inside_wall_point_list[0]
                    point_end_1 = inside_wall_point_list[0]
                    point_end_2 = inside_wall_point_list[1]
                    # 对找到的线段进行延长
                    extend_line = get_extend_line([point_end_1[0], point_end_1[1], point_end_2[0], point_end_2[1]], entity)
                    # 获得与entity相交的线段
                    # 先通过原始门窗bbox相交获得交线
                    extend_line_point = line_intercept_by_poly(extend_line, entity)
                    # 若原始bbox未获得交线，将bbox稍微外扩尝试获取交线
                    if extend_line_point is None:
                        extend_line_point = line_intercept_by_poly(extend_line, expanded_door_bbox)

                    if extend_line_point is not None:
                        draw_lines.append([extend_line_point, (0, 0, 255), 5, "door_base_coords"])

                # 对于没有弧线的门窗，同时画内部直线，以免土建连线获取失败造成空间不封闭
                entity_box_area = (entity[2] - entity[0]) / ratio[0] * (entity[3] - entity[1]) / ratio[1] / 1000000
                # 图上面积小于30平方米，是考虑了阳台上的折线窗。倾斜图纸中会有倾斜的折线窗，bbox面积阈值暂定为30平米
                if entity_box_area < 30:
                    for line in line_in_list:
                        draw_lines.append([line, (0, 0, 255), 1, None])

            # 有弧线情况，包括，单扇门、双扇门、管井门、门连窗、门连折线窗、带弧线的窗，先处理内部圆弧，再处理内部直线
            else:
                # # for debug
                # inside_wall_list, expanded_door_bbox_list = get_entity_wall_width_debug(
                #     border_entity_bbox_dict['wall_line'] + border_entity_bbox_dict['pillar_line'], [entity],
                #     ext_margin, wall_thickness, (w_ratio, h_ratio), (w_range, h_range), multi_width=False,
                #     is_wider_door=False)

                # print('----> expanded_door_bbox_list', expanded_door_bbox_list)
                # print('----> inside_wall_list', inside_wall_list)
                if len(arc_in_list) == 2:
                    arc_in_list.sort(key=lambda x: x[0])
                    temp = [arc_in_list[0][0:2], arc_in_list[0][2:4]]
                    temp.sort(key=lambda x: x[0])
                    arc_1_poin1 = temp[0]
                    arc_1_poin2 = temp[1]
                    arc_1_center = arc_in_list[0][4:6]

                    temp = [arc_in_list[1][0:2], arc_in_list[1][2:4]]
                    temp.sort(key=lambda x: x[0])
                    arc_2_poin1 = temp[0]
                    arc_2_poin2 = temp[1]
                    arc_2_center = arc_in_list[1][4:6]

                    expand_width = expanded_door_bbox[2] - expanded_door_bbox[0]
                    expand_height = expanded_door_bbox[3] - expanded_door_bbox[1]
                    long_side = max(expand_width, expand_height)

                    d_center = point_euclidean_distance(arc_1_center, arc_2_center) < long_side
                    if (arc_1_poin1 == arc_2_poin1 or arc_1_poin2 == arc_2_poin1) and d_center:
                        draw_lines.append([list(arc_1_center + arc_2_center), (0, 0, 255), 10, "door_base_coords"])
                        arc_in_list = []

                # for debug
                # shrinked_door_bbox = remove_margin(entity, ext_margin - 2)
                # cv2.rectangle(img_debug, tuple(shrinked_door_bbox[:2]), tuple(shrinked_door_bbox[2:4]),
                #               (255, 255, 255), 1)
                # if max(entity[2] - entity[0], entity[3] - entity[1]) > 900 * ratio[0]:
                #     color = get_random_color()
                #     cv2.rectangle(img_debug, tuple(entity[:2]), tuple(entity[2:4]), color, 1)
                #     for arc in arc_in_list:
                #         cv2.line(img_debug, tuple(arc[:2]), tuple(arc[2:4]), color, 5)

                # 记录两组信息，圆弧的圆心list、直线的斜率list，后续辅助判断需要画的line
                entity_k_list = []
                entity_arc_center_list = []
                # 找出过滤直线中的斜线
                slope_line_point = []
                arc_point = []
                for l in filtered_line_in_list:
                    angel = getLineDeg(l)
                    if abs(angel) < 5 or abs(angel) > 85:
                        continue
                    slope_line_point.append(l[0:2])
                    slope_line_point.append(l[2:4])
                point_flag = 0
                for arc in arc_in_list:
                    # 需要将圆弧的一个端点和圆心相连，闭合封闭空间，通过判断point_1、point_2端点是否连接有门板判断（与point相接的直线数量）
                    point = get_door_arc_connection_point(arc, entity, filtered_line_in_list, border_entity_info,
                                                          wall_thickness, (w_range, h_range), arc_in_list,
                                                          wall_pillar_line_dict)
                    # print('----> point', point)  # for debug
                    if point is None:
                        if 15 < abs(arc[-1]) < 50:
                            arc_point.append(arc[0:2])
                            arc_point.append(arc[2:4])
                            point_flag += 1
                        continue
                    else:
                        # 有些圆弧的圆心不在墙线附近，直接连接圆心和point不能将空间封闭。所以如果找到了土建连线，直接用土建连线
                        if isinstance(point[0], list):
                            point_end_1 = point[0]
                            point_end_2 = point[1]
                            # # for debug
                            # cv2.line(img_space_copy, (point_end_1[0], point_end_1[1]),
                            #          (point_end_2[0], point_end_2[1]), (255, 0, 0), 10)

                        # 如果返回的是弧线的某个端点
                        else:
                            point_end_1 = arc[4:6]
                            point_end_2 = point
                            # 找出相距很近的平行线，作为门板
                            door_parallel_line = detcect_parallel_line_in_door(filtered_line_in_list, ratio)
                            # 若找到的要与圆心相连的点与平行线的距离很近，那么认为这个点查找错误，圆弧上的另一点才是正确的点，原因见issue1764
                            flag = 0
                            for l in door_parallel_line:
                                p1 = point_project_on_line(point, l[0])
                                p2 = point_project_on_line(point, l[1])
                                d1 = point_euclidean_distance(point, p1)
                                d2 = point_euclidean_distance(point, p2)
                                if d1 < 50 * ratio[0] or d2 < 50 * ratio[0]:
                                    flag = 1
                                    break
                            # 如果找到的point距离疑似门板的平行线比较近，对point进行替换
                            if flag:
                                point_end_2 = [i for i in [arc[0:2], arc[2:4]] if i != point][0]

                        # 对找到的线段进行延长
                        extend_line = get_extend_line(
                            [point_end_1[0], point_end_1[1], point_end_2[0], point_end_2[1]], entity)
                        # print('-----> extend_line', extend_line)  # for debug
                        # print('-----> entity', entity)  # for debug

                        # 获得与entity相交的线段
                        # 先通过原始门窗bbox相交获得交线
                        extend_line_point = line_intercept_by_poly(extend_line, entity)

                        # print('------> extend_line_point', extend_line_point)  # for debug

                        # 若原始bbox未获得交线，将bbox稍微外扩尝试获取交线
                        if extend_line_point is None:
                            extend_line_point = line_intercept_by_poly(extend_line, expanded_door_bbox)

                        if extend_line_point is not None:
                            draw_lines.append([extend_line_point, (0, 0, 255), 5, "door_base_coords"])

                    entity_k = None if point_end_1[0] == point_end_2[0] else round(
                        ((point_end_1[1] - point_end_2[1]) / (point_end_1[0] - point_end_2[0])), 2)
                    entity_k_list.append(entity_k)
                    entity_arc_center_list.append([arc[4], arc[5]])
                # 如果有弧线没有找到与圆心相连的点，比如issue1629中的管井门
                if point_flag:
                    # 没有找到与圆心相连的点，那么分两种情况讨论
                    d_flag = [True] * len(slope_line_point)
                    arc_flag = [True] * len(arc_point)
                    # 第一种，entity中只有一个圆弧，取斜线上与圆弧两点都远的那个点和圆弧上与斜线点都远的那个点相连
                    if 0 < len(slope_line_point) <= 4 and len(arc_point) == 2 and point_flag == 1:
                        for i in range(len(slope_line_point)):
                            for j in range(len(arc_point)):
                                d = point_euclidean_distance(slope_line_point[i], arc_point[j])
                                if d < 50 * ratio[0]:
                                    d_flag[i] = False
                                    arc_flag[j] = False
                        slope_idx = np.where(d_flag)[0].tolist()
                        arc_idx = np.where(arc_flag)[0].tolist()
                        if len(slope_idx) > 0 and len(arc_idx) > 0:
                            slope_point_x = (slope_line_point[slope_idx[0]][0])
                            slope_point_y = (slope_line_point[slope_idx[0]][1])
                            extend_line = get_extend_line(
                                [slope_point_x, slope_point_y, arc_point[arc_idx[0]][0], arc_point[arc_idx[0]][1]], entity)
                            extend_line_point = line_intercept_by_poly(extend_line, entity)
                            if extend_line_point is None:
                                extend_line_point = [slope_point_x, slope_point_y, arc_point[arc_idx[0]][0], arc_point[arc_idx[0]][1]]
                            draw_lines.append([extend_line_point, (0, 0, 255), 5, "door_base_coords"])

                    else:
                        # 第二种，存在多个圆弧和多条直线，连接斜线上距离最远的两个点
                        p1, p2 = None, None
                        max_value = 0
                        for i in range(len(slope_line_point) - 1):
                            for j in range(i + 1, len(slope_line_point)):
                                d = point_euclidean_distance(slope_line_point[i], slope_line_point[j])
                                if d > max_value:
                                    max_value = d
                                    p1 = slope_line_point[i]
                                    p2 = slope_line_point[j]
                        if p1 and p2:
                            draw_lines.append([[p1[0], p1[1], p2[0], p2[1]], (0, 0, 255), 5, "door_base_coords"])

                # 处理内部直线，与entity_k偏差大 (斜率不同) 且距离圆弧圆心近的直线过滤（过滤门板，因为门板会在房间空间内分出一小块区域，有可能影响规则判断）
                # TODO: 这里对parallel_line_list进行遍历，因为parallel_line_list要求必须有多于两条平行线的时候才加入列表，会造成门连窗的多条平行线画出来，只不过对空间分割没有影响
                # 记录不平行于门窗土建连线的直线，之后判断是否是带弧线的折线窗
                unparalel2entity_l_list = []
                unparalel2entity_k_list = []
                for line in parallel_line_list:
                    line_k = None if line[2] == line[0] else round(((line[3] - line[1]) / (line[2] - line[0])), 2)
                    is_filter_line = False
                    for entity_k, entity_arc_center in zip(entity_k_list, entity_arc_center_list):
                        if line_k != entity_k and (point_euclidean_distance(entity_arc_center, line[0:2]) <= 35 or
                                                   point_euclidean_distance(entity_arc_center, line[2:4]) <= 35):
                            is_filter_line = True
                            unparalel2entity_l_list.append(line)
                            unparalel2entity_k_list.append(line_k)
                            break
                    if not is_filter_line:
                        draw_lines.append([line, (0, 0, 255), 1, None])
                # 判断是否是带弧线的折线窗，这些直线是否有三条以上、相互平行且之间的距离大于30mm（目前遇到的折线窗两侧墙线长度最小100mm，四条折线）
                unparalel2entity_k_l_dict = {}
                for line, line_k in zip(unparalel2entity_l_list, unparalel2entity_k_list):
                    if line_k not in unparalel2entity_k_l_dict:
                        unparalel2entity_k_l_dict[line_k] = [line]
                    else:
                        unparalel2entity_k_l_dict[line_k].append(line)
                for line_k, parallel_lines in unparalel2entity_k_l_dict.items():
                    is_L_window = False
                    if len(parallel_lines) >= 3:
                        is_L_window = True
                        # 判断两两之间的距离是不是都大于30mm
                        for i in range(len(parallel_lines) - 1):
                            for j in range(i + 1, len(parallel_lines)):
                                point_pjt = point_project_on_line(parallel_lines[i][:2], parallel_lines[j])
                                line_dist = point_euclidean_distance(parallel_lines[i][:2], point_pjt)
                                if line_dist <= 30 * ratio[0]:
                                    is_L_window = False
                                    break
                            if not is_L_window:
                                break
                    # 然后判断构件中的弧线圆心角是不是都小于80度
                    for arc in arc_in_list:
                        if abs(arc[-1]) > 70:
                            is_L_window = False
                    # 画出折线窗中垂直的直线
                    if is_L_window:
                        for line in parallel_lines:
                            draw_lines.append([line, (0, 0, 255), 1, None])
        # 收集电梯厢层中疑似电梯门，有个别电梯门在电梯厢图层中，收集后直接绘制内部线
        else:
            origin_bbox = remove_margin(entity, ext_margin)
            long_side = max((origin_bbox[2] - origin_bbox[0]), (origin_bbox[3] - origin_bbox[1]))
            side_side = min((origin_bbox[2] - origin_bbox[0]), (origin_bbox[3] - origin_bbox[1]))
            line_in_list = entity_in_bbox(line_entity_list, entity)
            real_side_side = side_side / ratio[0]
            real_long_side = long_side / ratio[1]
            # 电梯门尺寸限制
            if 20 < real_side_side < 150 and 900 < real_long_side < 1500:
                for line in line_in_list:
                    draw_lines.append([line, (0, 0, 255), 3, None])

            # 判断电梯厢
            if 1100 < real_side_side < 2500 and 1100 < real_long_side < 2500:
                ext_bbox = extend_margin(entity, 500 * ratio[0])
                x1, y1, x2, y2 = ext_bbox
                ext_bbox_polygen = Polygon([(x1, y1), (x1, y2), (x2, y2), (x2, y1)])
                wall_list = []
                border_entity_bbox_dict = border_entity_info['entity_bbox_dict']
                for wall in border_entity_bbox_dict['wall_line'] + border_entity_bbox_dict['pillar_line']:
                    wall_LineString = LineString([(wall[0], wall[1]), (wall[2], wall[3])])
                    real_wall_length = wall_LineString.length / ratio[0]
                    if ext_bbox_polygen.contains(wall_LineString) and 100 < real_wall_length < 300:
                        # draw_lines.append([wall, (255, 0, 0), 2, None])
                        wall_list.append(wall)
                pair_wall_list = []
                if len(wall_list) > 1:
                    pair_wall_list = detcect_parallel_line(wall_list, ratio)
                if pair_wall_list:
                    for pair_wall in pair_wall_list:
                        wall_t_point1 = pair_wall[0][:2]
                        wall_t_point2 = pair_wall[1][:2]
                        wall_b_point1 = pair_wall[0][2:]
                        wall_b_point2 = pair_wall[1][2:]
                        draw_lines.append([list(wall_t_point1 + wall_t_point2), (215, 0, 255), 2, None])
                        draw_lines.append([list(wall_b_point1 + wall_b_point2), (215, 0, 255), 2, None])

    # for debug
    # for di, line in enumerate([item for item in draw_lines if item[3] in ["door_base_coords"]]):
    #     cv2.line(img_copy, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (255,255,0), 3)
    #     cv2.putText(img_copy, f'{di}', (line[0][0], line[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
    # cv2.imwrite("door_base_line_debug.png", img_copy)

    return draw_lines, used_origin_lines


def draw_door_base_coord(border_entity_info, img_space):
    """
    将之前合并得到的门窗构件，用土建连线来代替内部的所有门窗图元参与空间分割
    Args:
        border_entity_info:      图框构件信息
        img_space:               未添加土建连线的分割底图
    Returns:
        door_base_coords:        得到的土建连线的集合,
        draw_line_list:          土建连线代替的原始门窗图元的集合,
        img_space_copy:          添加了土建连线的分割底图
    """
    ratio = border_entity_info['ratio']
    border_entity_bbox_dict = border_entity_info['entity_bbox_dict']
    origin_border_entity_info = border_entity_info['origin_border_entity_info']
    origin_border_entity_style = border_entity_info['origin_border_entity_style']
    space_scale = border_entity_info['space_scale']
    border_coord = border_entity_info['border_coord']
    image_manager = border_entity_info['image_manager']
    height, width = image_manager.img_height, image_manager.img_width
    print('height, width:{}\t{}'.format(height, width))

    wall_pillar_line_list = border_entity_bbox_dict['wall_line'] + border_entity_bbox_dict['pillar_line']
    # 将墙线按网格划分
    wall_pillar_line_dict, w_range, h_range = get_mesh_grid_for_wall_pillar(wall_pillar_line_list, width, height)

    # 空间分割需要处理的图层
    check_layer = ['door', 'window', 'elevator_door', 'emergency_door']
    # 获取目标图层内arc和line类型的原始构件数据
    arc_entity_list = []
    line_entity_list = []
    line_dash_entity_list = []
    ellipse_entity_list = []
    arc_entity_dict = get_origin_border_entity_info_with_style(origin_border_entity_info, origin_border_entity_style,
                                                               check_layer, ['Arc', 'Polyline', 'Polyline2d'],
                                                               space_scale,
                                                               border_coord, ratio)
    line_entity_dict = get_origin_border_entity_info_with_style(origin_border_entity_info, origin_border_entity_style,
                                                                check_layer, ['Line', 'Polyline', 'Polyline2d'],
                                                                space_scale,
                                                                border_coord, ratio)
    ellipse_entity_dict = get_origin_border_entity_info_with_style(origin_border_entity_info,
                                                                   origin_border_entity_style,
                                                                   check_layer, ['Ellipse'], space_scale,
                                                                   border_coord, ratio)
    for layer, entity_list in arc_entity_dict.items():
        for entity_bbox_style in entity_list:
            arc_entity_list.append(entity_bbox_style[0])
    for layer, entity_list in line_entity_dict.items():
        for entity_bbox_style in entity_list:
            line_entity_list.append(entity_bbox_style[0])
            # 将线型为虚线的门窗直线单独保存一份
            e_style = entity_bbox_style[1].split('$')[-1].upper()
            # 之后遇到新的虚线门窗style关键字，在这里添加
            if re.search(r'DASH', e_style):
                line_dash_entity_list.append(entity_bbox_style[0])
    for layer, entity_list in ellipse_entity_dict.items():
        for entity_bbox_style in entity_list:
            # 由于直接获取的是ellipse的起始角度和终止角度，这里转换成圆心角
            ellipse_entity_list.append(entity_bbox_style[0][:-2] +
                                       [abs(entity_bbox_style[0][-1] - entity_bbox_style[0][-2])])
    # Polyline 中也有arc，需要过滤
    arc_entity_list = list(filter(lambda x: len(x) == 8, arc_entity_list))
    arc_entity_dict = get_mesh_grid_dict(arc_entity_list, w_range, h_range)

    line_entity_list = list(filter(lambda x: len(x) == 4, line_entity_list))
    line_entity_dict = get_mesh_grid_dict(line_entity_list, w_range, h_range)

    # 这里将起始角度和终止角度合并为圆心角
    ellipse_entity_list = list(filter(lambda x: len(x) == 10, ellipse_entity_list))
    ellipse_entity_dict = get_mesh_grid_dict(ellipse_entity_list, w_range, h_range)

    line_dash_entity_list = list(filter(lambda x: len(x) == 4, line_dash_entity_list))
    # 门窗的土建连线
    door_base_coords = []

    img_space_copy = img_space.copy()  # 真正用于空间分割图像处理的图片
    # 墙线画白色
    for bbox in wall_pillar_line_list:
        cv2.line(img_space_copy, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 255, 255), 2)

    check_layer_segment = ['door', 'window', 'elevator_door', 'elevator_box', 'stair_dayang_plan_stair',
                           'emergency_door']

    used_line_list = []
    entity_lists = [[entity, layer] for layer in check_layer_segment for entity in border_entity_bbox_dict.get(layer, [])]
    num = len(entity_lists)
    with ProcessPoolExecutor(max_workers=PROCESS_WORKER_NUM) as executor:
        futures = [executor.submit(get_door_base_coords_by_entity,
                                   entity_lists[num*i//PROCESS_WORKER_NUM:num*(i+1)//PROCESS_WORKER_NUM],
                                   border_entity_info, arc_entity_dict, line_entity_dict, ellipse_entity_dict,
                                   w_range, h_range, wall_pillar_line_dict, line_dash_entity_list, line_entity_list)
                   for i in range(PROCESS_WORKER_NUM)]
        for f in as_completed(futures):
            try:
                dw_line_list, used_origin_line_list = f.result()
                for line in dw_line_list:
                    if line[3] == 'door_base_coords':
                        door_base_coords.append(line[0])
                    cv2.line(img_space_copy, tuple(line[0][:2]), tuple(line[0][2:4]), line[1], line[2])
                used_line_list.extend(used_origin_line_list)
            except BaseException as e:
                print('ProcessPool break down:', e)

    # 原始代单进程代码
    # dw_line_list, used_origin_line_list = get_door_base_coords_by_entity(entity_lists,
    #                                                                      border_entity_info, arc_entity_dict, line_entity_dict, ellipse_entity_dict,
    #                                                                      w_range, h_range, wall_pillar_line_dict, line_dash_entity_list, line_entity_list)
    #
    # for line in dw_line_list:
    #     if line[3] == 'door_base_coords':
    #         door_base_coords.append(line[0])
    #     cv2.line(img_space_copy, tuple(line[0][:2]), tuple(line[0][2:4]), line[1], line[2])
    # used_line_list.extend(used_origin_line_list)

    filter_line_list = used_line_list + line_dash_entity_list
    never_draw_line_list = [line for line in line_entity_list if line not in filter_line_list]
    return door_base_coords, never_draw_line_list, img_space_copy


def get_against_wall_lines(origin_lines, wall_pillar_line_dict, w_range, h_range):
    """
    得到靠墙的线段
    Args:
        origin_lines:          所有要判断的线段
        wall_pillar_line_dict: 图框内所有墙柱原始图元按网格划分后的结果
        w_range:               网格划分标准。每个格子的宽度
        h_range:               网格划分标准。每个格子的高度
    Returns:
        against_wall_lines:    靠墙的线段集合
    """
    against_wall_lines = []
    for line in origin_lines:
        # 记录每个端点是否靠近墙线
        n_wall_nearby_1 = False
        n_wall_nearby_2 = False
        # 考虑到有些门窗直线在像素上不直接与墙线相交，在直线的两端构建出两个小框，用来判断是否有墙线穿过
        line_entity_bbox_1 = [line[0] - 3, line[1] - 3, line[0] + 3, line[1] + 3]
        line_entity_bbox_2 = [line[2] - 3, line[3] - 3, line[2] + 3, line[3] + 3]
        wall_pillar_line_near_list = get_grid_range(line, wall_pillar_line_dict, w_range, h_range)
        for wall_bbox in wall_pillar_line_near_list:
            # 为降低计算量
            if not n_wall_nearby_1 and line_overlap_poly(line_entity_bbox_1, wall_bbox):
                n_wall_nearby_1 = True
            if not n_wall_nearby_2 and line_overlap_poly(line_entity_bbox_2, wall_bbox):
                n_wall_nearby_2 = True
            if n_wall_nearby_1 and n_wall_nearby_2:
                break
        if n_wall_nearby_1 and n_wall_nearby_2:
            against_wall_lines.append(line)
    return against_wall_lines


def draw_single_dw_line(border_entity_info, never_draw_line_list, img_space_copy):
    """
    如果有不包含在任何门窗bbox内的直线门窗图元（issue 250216），判断其两端是否靠近墙线，若是则直接画出该直线，从而防止空间分割错误
    Args:
        border_entity_info:    图框构件信息
        never_draw_line_list:  没被门窗土建连线代替的原始门窗图元
        img_space_copy:        画了门窗土建连线的底图
    Returns:
        single_line_dw_list: 单独门窗直线图元
        img_space_copy:    画了门窗土建连线和单独门窗直线图元的图片
    """
    ratio = border_entity_info['ratio']
    image_manager = border_entity_info['image_manager']
    height, width = image_manager.img_height, image_manager.img_width
    border_entity_bbox_dict = border_entity_info['entity_bbox_dict']

    wall_pillar_line_list = border_entity_bbox_dict['wall_line'] + border_entity_bbox_dict['pillar_line']
    wall_pillar_line_dict, w_range, h_range = get_mesh_grid_for_wall_pillar(wall_pillar_line_list, width, height)
    single_line_dw_list = []

    # 对单独的门窗直线根据长度进行筛选,
    line_entity_list_dw = [line for line in never_draw_line_list if
                           (point_euclidean_distance(line[0:2], line[2:4]) > 200 * ratio[0])]
    num = len(line_entity_list_dw)
    with ProcessPoolExecutor(max_workers=PROCESS_WORKER_NUM) as executor:
        futures = [executor.submit(get_against_wall_lines,
                                   line_entity_list_dw[num*i//PROCESS_WORKER_NUM:num*(i+1)//PROCESS_WORKER_NUM],
                                   wall_pillar_line_dict, w_range, h_range) for i in range(PROCESS_WORKER_NUM)]
        for f in as_completed(futures):
            try:
                single_dw_lines = f.result()
                for line_entity in single_dw_lines:
                    single_line_dw_list.append(line_entity)
                    cv2.line(img_space_copy, tuple(line_entity[:2]), tuple(line_entity[2:]), (0, 0, 0), 5)
            except BaseException as e:
                print('ProcessPool break down:', e)
    # 打印出单独的门窗直线信息
    print('----> single_line_door_window_list: {}'.format(len(single_line_dw_list)))
    return single_line_dw_list, img_space_copy


def segment_and_save(border_entity_info,  img_space_copy, img_space, img_path_temp, drawing_type, rule_index):
    """
    对图像进行轮廓腐蚀找到一个个空间，并用文本正则判定空间用途\类型
    Args:
        border_entity_info:      图框构件信息
        img_space_copy:          添加了门窗的分割底图
        img_space:               未添加门窗的分割底图
        img_path_temp:           中间结果保存路径
        drawing_type:            图框类型
        rule_index:              规则序号，为None 表示按照图纸类型粒度来运行，如果不为None，表示按照规则粒度来运行
    Returns:
        room_info:,               大房间集合
        small_room_info:,         小房间集合
        small_room_contour_list:  小房间的轮廓集合,
        wall_contour_list:        墙轮廓集合
    """
    ratio = border_entity_info['ratio']
    border_entity_bbox_dict = border_entity_info['entity_bbox_dict']
    image_manager = border_entity_info['image_manager']
    height, width = image_manager.img_height, image_manager.img_width

    if SAVE_RECOG_GEN_IMG_ONLINE:
        img_space_copy_temp = img_space_copy.copy()  # 保存在本地的分割temp图片
        # 墙线画黄线
        for bbox in border_entity_bbox_dict['wall_line'] + border_entity_bbox_dict['pillar_line']:
            cv2.line(img_space_copy_temp, (bbox[0], bbox[1]), (bbox[2], bbox[3]),
                     (0, 215, 255), 2)

    # 获取图纸的外框
    inner_border = get_border_margin_naive(img_space_copy[10:height - 10, 10:width:width - 10, :])
    if inner_border is None:
        inner_border = [300, 500, width - 300, height]
    x1, y1, x2, y2 = inner_border

    img_seg = img_space_copy[y1:y2, x1:x2]
    print("image for space seg origin shape:{} \t\t cropped shape:{}\n".format(img_space_copy.shape, img_seg.shape))
    if not SAVE_RECOG_GEN_IMG_ONLINE:
        del img_space_copy
        gc.collect()

    # 对地上图纸和地下图纸使用不同的墙体厚度
    if drawing_type in []:
        wall_thickness_CAD_seg = WALL_THICKNESS_CAD_SEG_UNDERGROUND
    else:
        wall_thickness_CAD_seg = WALL_THICKNESS_CAD_SEG_INDOOR
    seg_img, room_bbox, room_contours, small_room_bbox_list, small_room_contour_list, wall_contour_list = space_segment(
        img_seg, ratio[::-1], img_path_temp, wall_thickness_CAD_seg, major='decor_architecture', drawing_type=drawing_type)
    del img_seg
    gc.collect()

    print('img for segmentation result shape:{} \n seg room num:{}\n'.format(seg_img.shape, len(room_bbox)))
    if not SAVE_RECOG_GEN_IMG_ONLINE:
        del seg_img
        gc.collect()
    else:
        img_space_copy[y1:y2, x1:x2, :] = seg_img
        space_img_pil = Image.fromarray(img_space_copy[:, :, ::-1])
        draw_temp = ImageDraw.Draw(space_img_pil)

    room_text_info = border_entity_info['border_text_info'].get(TextType.ROOM, [])
    font = ImageFont.truetype(os.path.join(FONT_DIR, "NotoSansCJK-Black.otf"), int(width * 0.004))
    fill_color = (255, 0, 0)
    # 将房间文本画在图像上
    img_space_pil = Image.fromarray(img_space[:, :, ::-1])  # 保存的画出各个空间轮廓的space_reg图片

    draw = ImageDraw.Draw(img_space_pil)
    for room_text in room_text_info:
        room_coord = room_text[:4]
        room_name = room_text[-1]
        name_position = (room_coord[0], room_coord[1])

        if not valid_int32(name_position[0]) or not valid_int32(name_position[1]):
            print('text position number overflow C long range:{}'.format(name_position))
            continue

        draw.text(name_position, room_name, font=font, fill=fill_color)

        if SAVE_RECOG_GEN_IMG_ONLINE:
            draw_temp.text(name_position, room_name, font=font, fill=fill_color)
            draw_temp.rectangle(room_coord, outline='red')

    img_space = cv2.cvtColor(np.asarray(img_space_pil), cv2.COLOR_RGB2BGR)
    del img_space_pil, draw
    gc.collect()

    for room_con in room_contours:
        cv2.polylines(img_space, [room_con], True, get_random_color(), 2)

    room_info = get_room_info(room_contours, room_bbox, room_text_info, border_entity_info)
    # 添加了小空间的信息，因为有些图纸中阳台等空间的面积很小，某些规则中需要用到这些空间的信息
    small_room_info = get_room_info(small_room_contour_list, small_room_bbox_list, room_text_info, border_entity_info)

    image_manager.load_to_manager(SPACE_RECOG_IMAGE_KEY, img_space)
    del img_space

    if SAVE_RECOG_GEN_IMG_ONLINE:
        space_img_pil_temp = Image.fromarray(img_space_copy_temp[:, :, ::-1])

        if rule_index is None:
            save_name = '{}_{}_{}'.format(img_path_temp, drawing_type.value, IMAGE_PRINT_EXTENSION[5])
            save_name_temp = '{}_{}_{}'.format(img_path_temp, drawing_type.value, IMAGE_PRINT_EXTENSION[6])
        else:
            save_name = '{}_{}_rule_{}_{}'.format(img_path_temp, drawing_type.value, rule_index,
                                                  IMAGE_PRINT_EXTENSION[5])
            save_name_temp = '{}_{}_rule_{}_{}'.format(img_path_temp, drawing_type.value, rule_index,
                                                       IMAGE_PRINT_EXTENSION[6])

        # 保存中间结果，部署的时候需要注释掉
        space_img_pil.save(save_name)
        space_img_pil_temp.save(save_name_temp)
        del img_space_copy_temp, space_img_pil_temp,  draw_temp # space_img_pil,

        # 将空间分割结果保存到image manager
        image_manager.load_to_manager(IMG_SEG_RESULT, np.array(space_img_pil)[:, :, ::-1])
        # for debug
        # seg = image_manager.load_from_manager(IMG_SEG_RESULT)
        # cv2.imwrite("/Users/xuan.ma/Desktop/seg.png", seg)
        del space_img_pil

    gc.collect()

    return room_info, small_room_info, small_room_contour_list, wall_contour_list


@timer('space_segmentation')
def run(border_name, border_entity_info, result_path, drawing_type, rule_index=None):
    """
    空间分割
    :param border_name: 图框序号，例如 Model_0
    :param border_entity_info: 图框构件信息
    :param result_path: 中间结果保存路径
    :param drawing_type: 图框类型
    :param rule_index: 规则序号，为None 表示按照图纸类型粒度来运行，如果不为None，表示按照规则粒度来运行
    :return: 补充信息的 border_entity_info
    """
    room_info = []
    small_room_contour_list = []
    small_room_info = []
    door_base_coords = []
    single_line_dw_list = []
    wall_contour_list = []
    img_path_temp = os.path.join(result_path, border_name)
    # 非总图类型、非墙身大样图的图框进行套内空间的分割
    if drawing_type not in []:

        border_entity_bbox_dict = border_entity_info['entity_bbox_dict']
        image_manager = border_entity_info['image_manager']
        if 'wall' in border_entity_bbox_dict:
            img_space = get_base_segmentation_img(image_manager, border_entity_bbox_dict)

            door_base_coords, never_draw_line_list, img_space_copy = draw_door_base_coord(border_entity_info, img_space)

            single_line_dw_list, img_space_copy = draw_single_dw_line(border_entity_info, never_draw_line_list, img_space_copy)

            room_info, small_room_info, small_room_contour_list, wall_contour_list = segment_and_save(border_entity_info, img_space_copy, img_space, img_path_temp, drawing_type, rule_index)
        else:
            img_space = image_manager.load_from_manager(IMG_SPACE_RECOG_KEY)
            image_manager.load_to_manager(SPACE_RECOG_IMAGE_KEY, img_space)
    # 部分图纸不需要空间分割
    elif drawing_type in []:
        room_info = []
    # 为总图类型图框获取 "总图建筑轮廓"、"变电站"、"调压站"、"垃圾房"、"换热站"、"锅炉房"、"开关站" 空间
    else:
        extra_room_info = get_site_plan_building_contours(border_entity_info, result_path)
        room_info.extend(extra_room_info)

    print('----> this border has room: {}\n'.format(len(room_info)))

    border_space_info = {
        "room_info": room_info,
        "small_room_contours": small_room_contour_list,
        "small_room_info": small_room_info,
        "door_base_coords": door_base_coords,
        "single_line_door_window_list": single_line_dw_list,
        "wall_contour": wall_contour_list
    }
    border_entity_info.update(border_space_info)

    return border_entity_info
