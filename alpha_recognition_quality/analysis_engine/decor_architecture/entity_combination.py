# -*- coding: utf-8 -*-

import os
from time import time
from collections import defaultdict
import re
import gc

from PIL import Image
import numpy as np
import cv2

from ...config_manager.decor_architecture.drawing_config import DrawingType, DrawingConfig
from ...config_manager.decor_architecture.layer_config import LayerConfig
from ...config_manager.line_style_config import LineStyleConfig

from ...config import DEBUG_MODEL, SAVE_RECOG_GEN_IMG_ONLINE

from ..CONSTANTS import *
from ..utils.utils_combination import *
from ..utils.utils_analysis_common import *

from ...common.utils import *
from ...common.CONSTANTS import *
from ...common.decorator import timer
from ...common.multi_processing_unit import ProcessPoolExecutor, WORKERS, as_completed


# 合并地上图纸构件
def combine_entity_indoor(origin_border_entity_info, origin_border_entity_style, layer_bbox_list, layer_cad_class_dict,
                          image_size, ext_margin, ratio_w_h, scale, border_coord, image_manager, img_copy, drawing_type,
                          img_path=None):
    """

    Args:
        origin_border_entity_info: 构件原始图元
        origin_border_entity_style: 构件原始图元类型
        layer_bbox_list: 图层矩形框列表
        layer_cad_class_dict: 图层cad图元类型字典
        image_size: 图像尺寸
        ext_margin: 图框的外扩bbox
        ratio_w_h: CAD->PNG单位转换比例
        scale: CAD->现实长度单位转换比例
        border_coord: CAD图框坐标
        image_manager: 图片管理器
        img_copy: 图片
        drawing_type:图纸类型
        img_path: 图片路径

    Returns:
        合并后的信息
    """
    img = image_manager.load_from_manager(IMG_WITHOUT_WALL_KEY)
    height, width = image_size
    ratio = ratio_w_h[0]
    result = {
        "wall": [],
        "pillar": [],
        "wall_hatch": [],
        "door_combine_bbox": [],
        "door_intersect_bboxes": [],
    }

    for layer, bbox_list in layer_bbox_list.items():
        print('layer:{}'.format(layer))
        start = time()

        origin_entity_info = \
            get_origin_border_entity_info_by_cad_class(origin_border_entity_info, origin_border_entity_style,
                                                       [layer], scale, border_coord, ratio_w_h)[layer]

        if len(bbox_list) == 0:
            print('[Note] layer {} has no entity!'.format(layer))
            continue
        if layer == 'pillar':
            cad_class_list = layer_cad_class_dict.get(layer, [])
            normal_pillars, special_pillars = combine_pillar(bbox_list, image_size, ratio, cad_class_list)
            # print("normal_pillars: ", normal_pillars)
            result[layer] = normal_pillars
            result['special_pillar'] = special_pillars
        # 因为在LAYERS_WITH_SLOPE_LINE_REVISED中有了pillar_line，所以将pillar_line从COMBINATION_EXCLUDE_LAYERS_INDOOR删除
        if layer in LayerConfig.COMBINATION_EXCLUDE_LAYERS_INDOOR.value:
            cad_class_list = layer_cad_class_dict.get(layer, [])
            if layer in ['wall', 'pillar', 'wall_hatch']:
                for bbox, cad_class in zip(bbox_list, cad_class_list):
                    if cad_class not in ["Hatch", "Line", "Polyline", "Polyline2d"]:
                        pass
                        # print('bbox, cad_class', bbox, cad_class)
                    if cad_class == "Hatch":
                        result["wall_hatch"].append(bbox)
                    else:
                        result["wall"].append(bbox)
            else:
                result[layer] = bbox_list
            continue
        # wall_line、pillar_line、wall_line_dash、pillar_line_dash等都走这个分支
        if layer in LayerConfig.LAYERS_WITH_SLOPE_LINE_REVISED.value + LayerConfig.DASH_LINE_REVISED.value:
            result[layer] = bbox_list
            continue
        # todo: 统一过滤一遍异常bbox
        # 天正的图坐标值异常大
        print('-------- filter tianzheng bbox --------')
        print('[Note] bbox number befor filter:{}'.format(len(bbox_list)))
        bbox_list_temp = bbox_list[:]
        bbox_list = [bbox for bbox in bbox_list if normal_bbox(bbox, height, width)]
        print('[Note] bbox number after filter:{}'.format(len(bbox_list)))
        # print([bbox for bbox in bbox_list_temp if bbox not in bbox_list])

        print('-------- filter needless bbox --------')
        print('[Note] bbox number befor filter:{}'.format(len(bbox_list)))
        bbox_list = [bbox for bbox in bbox_list if
                     min(bbox[2] - bbox[0], bbox[3] - bbox[1]) <= INDOOR_ENTITY_SHORT_SIDE_MAXIMUM * ratio + ext_margin]
        print('[Note] bbox number after filter:{}'.format(len(bbox_list)))
        # 获取门图层相交的原始构件，用于规则7判断，若获取到相交构件，添加至result['door_combine_bbox']和result['door_intersect_bboxes']
        if layer == 'door':  # get conflict door bbox
            cad_class_list = layer_cad_class_dict['door']
            door_combine_bbox = []
            door_intersect_bboxes = []
            bbox_list = list(set([tuple(bbox) for bbox in bbox_list]))  # 去重
            bbox_list = [list(i) for i in bbox_list]  # 元素转列表
            origin_door_bbox = [remove_margin(bbox, ext_margin) for bbox in bbox_list]  # 去除margin
            # 遍历原始基本构件
            for bbox, cad_class in zip(origin_door_bbox, cad_class_list):
                if cad_class != "Arc":  # 门与门之间干涉只考虑弧线（开启范围）构件的干涉
                    continue
                # filter samll bbox 过滤小构件，可能是门的一部分，原始构件相交主要考虑门的弧线相交
                if not ((INDOOR_DOOR_SIDE_MAXIMUM * ratio * 0.5 < (
                        bbox[2] - bbox[0]) < INDOOR_DOOR_SIDE_MAXIMUM * ratio) and (
                                INDOOR_DOOR_SIDE_MAXIMUM * ratio * 0.5 < (
                                bbox[3] - bbox[1]) < INDOOR_DOOR_SIDE_MAXIMUM * ratio)):
                    continue
                other_bbox_list = [box for box in origin_door_bbox if box != bbox]
                for other_bbox, o_cad_class in zip(origin_door_bbox, cad_class_list):
                    if other_bbox == bbox or o_cad_class != "Arc":  # 遍历其他弧形门构件
                        continue
                    # filter small bbox
                    if not ((INDOOR_DOOR_SIDE_MAXIMUM * ratio * 0.5 < (
                            other_bbox[2] - other_bbox[0]) < INDOOR_DOOR_SIDE_MAXIMUM * ratio) and (
                                    INDOOR_DOOR_SIDE_MAXIMUM * ratio * 0.5 < (
                                    other_bbox[3] - other_bbox[1]) < INDOOR_DOOR_SIDE_MAXIMUM * ratio)):
                        continue
                    # 条件判断：门构件相交且非相互包含，倾斜构件会有不想交但构件包含的情况，需过滤
                    if Iou_temp(bbox, other_bbox) > 0 and not bboxes_contain_bbox([other_bbox], bbox, pix_margin=18):
                        door_combine_bbox.append(Union_area(bbox, other_bbox))
                        # 这里先将bbox相交的门bbox记录下来，后面在规则7中继续判断两个bbox内的图元是否相交
                        door_intersect_bboxes.append([bbox, other_bbox])

            result['door_combine_bbox'] = door_combine_bbox
            result['door_intersect_bboxes'] = door_intersect_bboxes

        print('========= combine layer entity:{}========='.format(layer))

        # # 对立管做特殊处理，因为立管有些会离得很近，甚至会相连。
        # if layer == 'pipe':
        #     # 额外收缩一个像素，防止有些立管带方形外框会挨在一起
        #     origin_pipe_bbox = [remove_margin(bbox, ext_margin + 1) for bbox in bbox_list]
        #     combine_bbox = combine(origin_pipe_bbox, image_size)
        #     combine_bbox = [extend_margin(bbox, ext_margin + 1) for bbox in combine_bbox]
        # elif layer == 'floor_drain':
        #     # 额外收缩一个像素，防止有些立管带方形外框会挨在一起，同时过滤部分长度超限构件（可能是给排水管子），阈值从750调整为335，遇到了长度是340的水管
        #     origin_pipe_bbox = [remove_margin(bbox, ext_margin + 1) for bbox in bbox_list if
        #                         max((bbox[2] - bbox[0]), (bbox[3] - bbox[1])) <= (DILOU_SIDE_RANGE[1] - 15) * ratio]
        #     combine_bbox = combine(origin_pipe_bbox, image_size)
        #     combine_bbox = [extend_margin(bbox, ext_margin + 1) for bbox in combine_bbox]

        # 将立管、地漏的合并的方式改为只通过外层的圆弧来获取bbox，可能存在非圆形地漏合并错误
        if layer in ['floor_drain']:
            len_thres_line_floor_drain = int((DILOU_SIDE_RANGE[1] - 15) * ratio)
            combine_bbox_contour = combine_new_indoor(layer, origin_entity_info, image_size, ratio_w_h, ext_margin,
                                                      img_path, seperate_line=True, need_radius_line=False,
                                                      extra_len_thres_line=len_thres_line_floor_drain,
                                                      major='decor_architecture')
            combine_bbox = [info[0] for info in combine_bbox_contour]
        elif layer in ['pipe']:
            combine_bbox_contour = combine_new_indoor(layer, origin_entity_info, image_size, ratio_w_h, ext_margin,
                                                      img_path, seperate_line=True, need_radius_line=False,
                                                      major='decor_architecture')
            combine_bbox = [info[0] for info in combine_bbox_contour]
        elif layer in ['floor_drain_mix', 'air_conditioner_mix']:
            combine_bbox_contour = combine_new_indoor(layer, origin_entity_info, image_size, ratio_w_h, ext_margin,
                                                      img_path, need_close=True, need_radius_line=False,
                                                      small_close_kernel=True, major='decor_architecture')
            combine_bbox = [info[0] for info in combine_bbox_contour]
        # elif layer == 'floor_drain_mix':
        #     # 对于地漏规格范围内的构件收缩后合并，其余构件保留margin合并
        #     origin_bbox_list = [remove_margin(bbox, ext_margin - 1) for bbox in bbox_list if
        #                         max(bbox[2] - bbox[0], bbox[3] - bbox[1]) < PIPE_SIZE * ratio + ext_margin] + \
        #                        [bbox for bbox in bbox_list if max(bbox[2] - bbox[0], bbox[3] - bbox[1]) >=
        #                         PIPE_SIZE * ratio + ext_margin]
        #     origin_bbox_list = [bbox for bbox in origin_bbox_list if
        #                         max(bbox[2] - bbox[0], bbox[3] - bbox[1]) <= 1500 * ratio]
        #     combine_bbox = combine(origin_bbox_list, image_size)
        #     combine_bbox = [extend_margin(bbox, ext_margin - 1) for bbox in combine_bbox if
        #                     max(bbox[2] - bbox[0], bbox[3] - bbox[1]) < PIPE_SIZE * ratio] + \
        #                    [bbox for bbox in combine_bbox if max(bbox[2] - bbox[0], bbox[3] - bbox[1]) >=
        #                     PIPE_SIZE * ratio]
        elif layer == 'fire_hydrant':
            # 消防栓图层收缩margin防止和周围附件合并
            origin_pipe_bbox = [remove_margin(bbox, ext_margin) for bbox in bbox_list]
            combine_bbox = combine(origin_pipe_bbox, image_size)
            combine_bbox = [extend_margin(bbox, ext_margin) for bbox in combine_bbox]
        elif layer in ['air_conditioner', 'washbasin', 'closestool', 'diamond_bath']:
            # # 含空调的混合图层，由于部分空调外机紧挨布置，同时大部分空调会有矩形外框，无需外扩ext_margin合并，仅外扩75*ratio像素（不相连线段形式）
            # if layer == 'air_conditioner_mix':
            #     origin_pipe_bbox = [remove_margin(bbox, ext_margin - int(50 * ratio) - 1) for bbox in bbox_list]
            #     temp_combine_bbox = combine(origin_pipe_bbox, image_size)
            #     temp_combine_bbox = [extend_margin(bbox, ext_margin - int(50 * ratio) - 1) for bbox in
            #                          temp_combine_bbox]
            # else:
            origin_pipe_bbox = [remove_margin(bbox, ext_margin) for bbox in bbox_list]
            temp_combine_bbox = combine(origin_pipe_bbox, image_size)
            temp_combine_bbox = [extend_margin(bbox, ext_margin) for bbox in temp_combine_bbox]

            filter_combine_bbox_list = []
            bbox_seperation_list = []
            # 合并后增加分离步骤，提出可分离构件filter_combine_bbox_list
            for bbox in temp_combine_bbox:
                bbox_img = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
                bbox_seperation = separation_combination(bbox_img, ratio, major='decor_architecture')
                del bbox_img
                gc.collect()
                if bbox_seperation is not None:
                    combine_base_coord = np.array([bbox[0], bbox[1]])
                    for bbox_seperation in bbox_seperation:
                        bbox_seperation_coord = [int(np.array(bbox_seperation[0]) + combine_base_coord[0]),
                                                 int(np.array(bbox_seperation[1]) + combine_base_coord[1]),
                                                 int(np.array(bbox_seperation[2]) + combine_base_coord[0]),
                                                 int(np.array(bbox_seperation[3]) + combine_base_coord[1])]
                        bbox_seperation_list.append(bbox_seperation_coord)
                        # for debug
                        if SAVE_RECOG_GEN_IMG_ONLINE:
                            cv2.rectangle(img_copy, (bbox_seperation_coord[0], bbox_seperation_coord[1]),
                                          (bbox_seperation_coord[2], bbox_seperation_coord[3]), (255, 255, 255), 2)

                    filter_combine_bbox_list.append(bbox)
            # 整合构件列表，移除可拆分构件，加入拆分后的构件列表
            if SAVE_RECOG_GEN_IMG_ONLINE:
                for bbox in filter_combine_bbox_list:
                    cv2.rectangle(img_copy, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 215, 255), 2)

            bbox_seperation_list = [extend_margin(bbox, ext_margin) for bbox in bbox_seperation_list]
            combine_bbox = [bbox for bbox in temp_combine_bbox if
                            bbox not in filter_combine_bbox_list] + bbox_seperation_list
        # elif layer in ['door', 'window', 'elevator_door', 'elevation_window'] and \
        #         drawing_type in [DrawingType.DECORATION_PLAN_LAYOUT]:
        #     combine_bbox = combine(bbox_list, image_size)
        # elif layer in ['elevation_window', 'elevation_window_open_line'] and \
        #         drawing_type not in [DrawingType.DOOR_WINDOW_DAYANG]:
        #     # 立面窗稍微外扩合并
        #     small_bboxes = [remove_margin(bbox, 2) for bbox in bbox_list]
        #     combine_bbox = combine(small_bboxes, image_size)
        #     combine_bbox = [extend_margin(bbox, 2) for bbox in combine_bbox]
        elif layer in ['door', 'window', 'elevator_door'] and drawing_type  in [DrawingType.DECORATION_PLAN_LAYOUT]:
            combine_bbox_contour = combine_new_indoor(layer, origin_entity_info, image_size, ratio_w_h, ext_margin,
                                                      img_path, need_close=True, link_parallel_line=True,
                                                      small_close_kernel=True, major='decor_architecture')
            combine_bbox = [info[0] for info in combine_bbox_contour]
        elif layer in ['elevator_box', 'elevator_stair']:
            combine_bbox_contour = combine_new_indoor(layer, origin_entity_info, image_size, ratio_w_h, ext_margin,
                                                      img_path, link_parallel_line=True, line_distance=280,
                                                      major='decor_architecture')
            combine_bbox = [info[0] for info in combine_bbox_contour]
            # 倾斜的容易合并错误
            # # 对楼梯、电梯bbox再合并一次
            # combine_bbox = combine(combine_bbox, image_size)
        elif layer in ['dayang_handrail', 'elevation_handrail', 'plan_handrail']:
            origin_pipe_bbox = [remove_margin(bbox, ext_margin) for bbox in bbox_list]
            ext_pix = int(200 * ratio)
            origin_pipe_bbox = [extend_margin(bbox, ext_pix) for bbox in origin_pipe_bbox]
            combine_bbox = combine(origin_pipe_bbox, image_size)
            combine_bbox = [remove_margin(bbox, ext_pix) for bbox in combine_bbox]
            combine_bbox = [extend_margin(bbox, ext_margin) for bbox in combine_bbox]

        elif layer in ['chu_wei']:
            origin_pipe_bbox = [remove_margin(bbox, ext_margin//2) for bbox in bbox_list]
            # ext_pix = int(200 * ratio)
            # origin_pipe_bbox = [extend_margin(bbox, ext_pix) for bbox in origin_pipe_bbox]
            combine_bbox = combine(origin_pipe_bbox, image_size)
            # combine_bbox = [remove_margin(bbox, ext_pix) for bbox in combine_bbox]
            combine_bbox = [extend_margin(bbox, ext_margin) for bbox in combine_bbox]
        else:
            combine_bbox_contour = combine_new_indoor(layer, origin_entity_info, image_size, ratio_w_h, ext_margin,
                                                      img_path, major='decor_architecture', need_radius_line=False)
            combine_bbox = [info[0] for info in combine_bbox_contour]

        result[layer] = combine_bbox

        print('*' * 50, '\n', 'before combine entity num:{}'.format(len(bbox_list)), '\n',
              'after combine:{}'.format(len(result[layer])), '\n',
              'use time:{:.2f} seconds'.format(time() - start), '\n',
              '*' * 50, '\n')
    del img
    gc.collect()

    ######################################################
    # 此处去重很有可能导致一些小构件被去掉，比如立管被厨卫构件包含
    ######################################################

    # # 如果一个构件被炸开后，entity不在同一个图层，去掉被大框完全包含的小框。
    # final_result = {}
    # temp = []
    # for layer, entity_list in result.items():
    #     if layer in ['door_combine_bbox', 'door_intersect_bboxes'] + LayerConfig.COMBINATION_EXCLUDE_LAYERS_INDOOR.value + \
    #             LayerConfig.LAYERS_WITH_SLOPE_LINE_REVISED.value + LayerConfig.DASH_LINE_REVISED.value:
    #         final_result[layer] = entity_list
    #         continue
    #     final_result[layer] = []
    #     temp.extend(entity_list)
    #
    # origin_result = [remove_margin(bbox, ext_margin) for bbox in temp]
    # for layer, entity_bbox_list in result.items():
    #     if layer in ['door_combine_bbox', 'door_intersect_bboxes'] + LayerConfig.COMBINATION_EXCLUDE_LAYERS_INDOOR.value + \
    #             LayerConfig.LAYERS_WITH_SLOPE_LINE_REVISED.value + LayerConfig.DASH_LINE_REVISED.value:
    #         continue
    #     for bbox in entity_bbox_list:
    #         bbox_actual = remove_margin(bbox, ext_margin)
    #         # 尺寸特别大的构件不参与合并其他构件，防止楼梯合并楼梯间附件门
    #         other_bbox = [box for box in origin_result if box != bbox_actual and (box[2]-box[0]) * (box[3]-box[1]) <= 2000 * 2000 * ratio * ratio]
    #         if len(other_bbox) == 0:
    #             final_result[layer].append(bbox)
    #             continue
    #         iou1, iou2 = calculate_iou(np.array([bbox_actual]), np.array(other_bbox))
    #         # 去重
    #         if np.max(iou2, axis=1)[0] < 0.95:
    #             final_result[layer].append(bbox)
    #         else:
    #             # print(np.max(iou1, axis=1)[0])
    #             # print(np.argmax(iou1, axis=1)[0])
    #             # print(other_bbox[np.argmax(iou1, axis=1)[0]])
    #             origin_result.remove(bbox_actual)
    #             print('this bbox is supressed:{}'.format(bbox))
    #             cv2.rectangle(img_copy, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 0, 255), 2)

    return result


# rewrite combine_entity_underground for time complexity
def combine_entity_underground(origin_border_entity_info, origin_border_entity_style, layer_bbox_list, layer_cad_class_dict,
                               image_size, ext_margin, ratio_w_h, scale, border_coord, border_entity_info, img_path=None):
    """

    Args:
        origin_border_entity_info: 构件原始图元
        origin_border_entity_style: 构件原始图元类型
        layer_bbox_list: 图层矩形框列表
        layer_cad_class_dict: 图层cad图元类型字典
        image_size: 图像尺寸
        ext_margin: 图框的外扩bbox
        ratio_w_h: CAD->PNG单位转换比例
        scale: CAD->现实长度单位转换比例
        border_coord: CAD图框坐标
        border_entity_info:图框全量信息
        img_path: 图片路径

    Returns:
        合并后的结果信息
    """
    ratio = ratio_w_h[0]
    height, width = image_size
    final_result = {
        "parking": [],
    }

    for layer in layer_bbox_list.keys():
        print('layer: {}'.format(layer))
        start = time()
        bbox_list = layer_bbox_list[layer]
        # wall_line、pillar_line、wall_line_dash、pillar_line_dash等都走这个分支
        if layer in LayerConfig.LAYERS_WITH_SLOPE_LINE_REVISED.value + LayerConfig.DASH_LINE_REVISED.value:
            final_result[layer] = bbox_list
            continue
        origin_entity_info = get_origin_border_entity_info_by_cad_class(
            origin_border_entity_info, origin_border_entity_style, [layer], scale, border_coord, ratio_w_h)[layer]
        # cad_class_list = layer_cad_class_dict[layer]
        cad_class_list = layer_cad_class_dict.get(layer, [])
        # assert len(bbox_list) == len(cad_class_list), print('bbox_list and cad_class_list is not of equal length!')
        if len(bbox_list) == 0:
            print('[Note] layer {} has no entity!'.format(layer))
            continue

        if layer in LayerConfig.COMBINATION_EXCLUDE_LAYERS_UNDERGROUND_AND_SITEPLAN.value:
            if layer == 'wall':
                wall_line_list = []
                for bbox, cad_class in zip(bbox_list, cad_class_list):
                    if cad_class not in ['Arc', 'Hatch']:
                        wall_line_list.append(bbox)
                bbox_list = wall_line_list[:]

            final_result[layer] = bbox_list
            continue

        # 天正的图坐标值异常大
        print('========= combine layer entity:{}========='.format(layer))
        print('-------- filter tianzheng bbox --------')
        num_bbox_before_filter = len(bbox_list)
        print('[Note] bbox number before filter: {}'.format(num_bbox_before_filter))
        # bbox_list = [bbox for bbox in bbox_list if normal_bbox(bbox, height, width)]
        cad_class_list = [cad_class_list[i] for i in range(num_bbox_before_filter)
                          if normal_bbox(bbox_list[i], height, width)]
        bbox_list = [bbox_list[i] for i in range(num_bbox_before_filter)
                     if normal_bbox(bbox_list[i], height, width)]
        print('[Note] bbox number after filter: {}'.format(len(bbox_list)))

        # 根据构件短边大小来过滤不需要的构件
        print('-------- filter needless bbox --------')
        num_bbox_before_filter = len(bbox_list)
        print('[Note] bbox number before filter: {}'.format(len(bbox_list)))
        cad_class_list = [cad_class_list[i] for i in range(num_bbox_before_filter) if
                          min(bbox_list[i][2] - bbox_list[i][0], bbox_list[i][3] - bbox_list[i][1])
                          <= UNDER_ENTITY_SHORT_SIDE_MAXIMUM * ratio + ext_margin]
        # bbox_list = [bbox for bbox in bbox_list if
        #        min(bbox[2] - bbox[0], bbox[3] - bbox[1]) <= UNDER_ENTITY_SHORT_SIDE_MAXIMUM * ratio + ext_margin]
        # 过滤构件原始尺寸过大的
        bbox_list = [bbox_list[i] for i in range(num_bbox_before_filter) if
                     min(bbox_list[i][2] - bbox_list[i][0], bbox_list[i][3] - bbox_list[i][1])
                     <= UNDER_ENTITY_SHORT_SIDE_MAXIMUM * ratio + ext_margin]
        print('[Note] bbox number after filter: {}'.format(len(bbox_list)))
        result = []
        if layer == 'pillar':
            normal_pillars, special_pillars = combine_pillar(bbox_list, image_size, ratio, cad_class_list)
            result += normal_pillars
            final_result['special_pillar'] = special_pillars

        # 对建筑专业的停车位也采用新的合并逻辑，因为发生多个停车位合并在一起的情况
        elif layer == 'parking':
            combine_bbox_1, parking_dict_1 = combine_parking(border_entity_info)
            combine_bbox_2, parking_dict_2 = combine_truck_parking(border_entity_info)
            result = [extend_margin(bbox, ext_margin) for bbox in combine_bbox_1 + combine_bbox_2]
            parking_dict_1.update(parking_dict_2)
            final_result['parking_contour_dict'] = parking_dict_1

            # start = time()
            # # 初始化网格参数
            # n_num = 20  # grid number
            # h_range = np.ceil(height / n_num)  # grid size
            # w_range = np.ceil(width / n_num)  # grid size
            # parking_bbox = []  # 初始化车位bbox表
            # park_long = []  # 车位长边线表
            # park_short = []  # 车位短边线表
            # origin_bbox_list = [remove_margin(box, ext_margin) for box in bbox_list]  # 移除margin
            # skew_parking_line_bbox = []  # 可由倾斜直线合并为车位的bbox表
            # origin_bbox_list_dict = get_mesh_grid_dict(origin_bbox_list, w_range, h_range)
            # # combine skew line into parking 非水平单根直线合并为车位
            # for origin_bbox in origin_bbox_list:
            #     # 过滤水平直线
            #     if min(origin_bbox[2] - origin_bbox[0], origin_bbox[3] - origin_bbox[1]) <= ext_margin * 2:
            #         continue
            #     # 过滤比车位短边段的线，不能是车位外框线
            #     if max(origin_bbox[2] - origin_bbox[0], origin_bbox[3] - origin_bbox[1]) < PARKING_SIZE[0] * ratio:
            #         continue
            #     # 车位线搜索范围
            #     other_origin_bbox_list = get_grid_range(origin_bbox, origin_bbox_list_dict, w_range, h_range)
            #     if len(other_origin_bbox_list) == 0:
            #         continue
            #     # 通过判断是否可以组合成直角三角形，判断是否可以组成车位
            #     if skew_parking_line_combine(origin_bbox, other_origin_bbox_list):
            #         skew_parking_line_bbox.append(skew_parking_line_combine(origin_bbox, other_origin_bbox_list))
            # # 增加skew_parking_line_bbox
            # origin_bbox_list.extend(skew_parking_line_bbox)
            # bbox_list = [extend_margin(box, ext_margin) for box in origin_bbox_list]
            # # divide bbox into diffirent size bbox
            # # 对bbox_list进行整理，满足车位尺寸的加入到parking_bbox，同时收集水平竖直线，按长度分为park_long车位长边线和park_short短边线
            # # 剩下为其余构件temp_bbox
            # temp_bbox = []
            # for bbox in bbox_list:
            #     long_side = max(bbox[2] - bbox[0], bbox[3] - bbox[1])
            #     short_side = min(bbox[2] - bbox[0], bbox[3] - bbox[1])
            #     if PARKING_SIZE[1] * ratio < long_side < PARKING_SIZE[1] * 2 * ratio and short_side > PARKING_SIZE[
            #         0] * ratio:
            #         parking_bbox.append(bbox)
            #     # size of motor parking is 2000 * 900
            #     if long_side > PARKING_SIZE[1] * ratio * 0.4 and short_side > PARKING_SIZE[0] * ratio * 0.4 and (
            #             long_side < PARKING_SIZE[1] * ratio * 0.7 or short_side < PARKING_SIZE[0] * ratio * 0.7):
            #         parking_bbox.append(bbox)
            #     # parking may be exploded as lines, collect parking lines
            #     if short_side <= ext_margin * 2:
            #         if long_side > PARKING_SIZE[1] * ratio:
            #             park_long.append(bbox)
            #         elif long_side > PARKING_SIZE[0] * ratio:
            #             park_short.append(bbox)
            #         else:
            #             temp_bbox.append(bbox)
            #     else:
            #         temp_bbox.append(bbox)
            # # combine parking lines as  parking, remove margin as true line, combine line as long side and short side get adjacent
            # # 进行长边线和短边线合并车位，遍历长短边线，根据紧邻点数进行判断，是否为可合并车位长短边，加入到车位parking_bbox中
            # if len(park_long) != 0 and len(park_short) != 0:
            #     origin_park_long = [remove_margin(box, ext_margin) for box in park_long]
            #     origin_park_short = [remove_margin(box, ext_margin) for box in park_short]
            #     origin_park_short_dict = get_mesh_grid_dict(origin_park_short, w_range, h_range)
            #     for long in origin_park_long:
            #         long_coord = get_bbox_coord(long)
            #         origin_park_short_range = get_grid_range(long, origin_park_short_dict, w_range, h_range)
            #         if len(origin_park_short_range) == 0:
            #             continue
            #         for short in origin_park_short_range:
            #             short_coord = get_bbox_coord(short)
            #             if coord_adjacent_coord(short_coord, long_coord) == 4:
            #                 parking_bbox.append(
            #                     [min(long[0], short[0]) - ext_margin, min(long[1], short[1]) - ext_margin,
            #                      max(long[2], short[2]) + ext_margin, max(long[3], short[3]) + ext_margin])
            # #                             break
            #
            # #             temp_bbox = [bbox for bbox in bbox_list if bbox not in parking_bbox and bbox not in park_long and bbox not in park_short]
            #
            # # 完全炸开的车位，会有重复的坐标定位
            # true_parking_bbox = list(set([tuple(bbox) for bbox in parking_bbox]))
            # # 去除炸开的parking里面包含的object，通过判断是否有被包含关系进行确认
            # remove_parking_bbox = []
            # final_parking_bbox = []
            # true_parking_bbox_dict = get_mesh_grid_dict(true_parking_bbox, w_range, h_range)
            # for bbox in true_parking_bbox:
            #     other_parking_bbox_range = get_grid_range(bbox, true_parking_bbox_dict, w_range, h_range)
            #     other_parking_bbox = [box for box in other_parking_bbox_range if
            #                           box != bbox and box not in remove_parking_bbox]
            #     if len(other_parking_bbox) == 0:
            #         final_parking_bbox.append(bbox)
            #         continue
            #     if not bboxes_contain_bbox(other_parking_bbox, bbox, pix_margin=1):
            #         final_parking_bbox.append(bbox)
            #     else:
            #         remove_parking_bbox.append(bbox)
            # # 去除车位中包含的内部object（不在parking_bbox中）
            # final_parking_bbox_dict = get_mesh_grid_dict(final_parking_bbox, w_range, h_range)
            # if len(final_parking_bbox) == 0:
            #     true_one_entity_bbox = temp_bbox
            # else:
            #     true_one_entity_bbox = []
            #     for bbox in temp_bbox:
            #         final_parking_bbox_range = get_grid_range(bbox, final_parking_bbox_dict, w_range, h_range)
            #         iou1, iou2 = calculate_iou(np.array([bbox]), np.array(final_parking_bbox_range))
            #         if iou2 is None:
            #             continue
            #         if np.max(iou2, axis=1)[0] < 0.5:  # clean small squre object inside a entity
            #             true_one_entity_bbox.append(bbox)
            #
            # # 去除紧挨车位的消防框，先收缩margin后通过bbox是否有两个点紧挨判断
            # origin_true_one_entity_bbox = [remove_margin(box, ext_margin) for box in true_one_entity_bbox]
            # origin_final_parking_bbox = [remove_margin(box, ext_margin) for box in final_parking_bbox]
            # origin_final_parking_bbox_dict = get_mesh_grid_dict(origin_final_parking_bbox, w_range, h_range)
            # partial_parking_list = []
            # for bbox in origin_true_one_entity_bbox:
            #     long_side = max(bbox[2] - bbox[0], bbox[3] - bbox[1])
            #     short_side = min(bbox[2] - bbox[0], bbox[3] - bbox[1])
            #     if long_side < PARKING_SIZE[0] * ratio or short_side > PARKING_SIZE[0] * ratio:
            #         continue
            #     origin_final_parking_bbox_range = get_grid_range(bbox, origin_final_parking_bbox_dict, w_range, h_range)
            #     bbox_coord = get_bbox_coord(bbox)
            #     for parking_bbox in origin_final_parking_bbox_range:
            #         parking_bbox_coord = get_bbox_coord(parking_bbox)
            #         if coord_adjacent_coord(bbox_coord, parking_bbox_coord) == 2:
            #             partial_parking_list.append(bbox)
            #             break
            # filtered_true_one_entity_bbox = [bbox for bbox in origin_true_one_entity_bbox if
            #                                  bbox not in partial_parking_list]
            # true_one_entity_bbox = [extend_margin(box, ext_margin) for box in filtered_true_one_entity_bbox]
            #
            # final_parking_bbox = [extend_margin(box, ext_margin) for box in origin_final_parking_bbox]
            # # 不是车位组件的object进行合并
            # true_combine_one_entity_bbox = combine(true_one_entity_bbox, image_size)
            # result.extend(true_combine_one_entity_bbox)
            # result.extend(final_parking_bbox)
            # print("!!!!time for underground entity combine：{:.2f} seconds!!!!".format(time() - start))

        # 地下图纸门构件的合并与地上图纸同步
        elif layer in ['door', 'window', 'elevator_door', 'emergency_door']:
            combine_bbox_contour = combine_new_underground(layer, origin_entity_info, image_size, ratio_w_h, ext_margin,
                                                           img_path, need_close=True, link_parallel_line=True,
                                                           major='decor_architecture')
            result = [info[0] for info in combine_bbox_contour]
        elif layer in ['elevator_box', 'elevator_stair']:
            combine_bbox_contour = combine_new_indoor(layer, origin_entity_info, image_size, ratio_w_h, ext_margin,
                                                      img_path, link_parallel_line=True, line_distance=280,
                                                      major='decor_architecture')
            result = [info[0] for info in combine_bbox_contour]
            # 倾斜的容易合并错误
            # # 对楼梯、电梯bbox再合并一次
            # combine_bbox = combine(combine_bbox, image_size)
        elif layer in ['water_pit']:
            # 过滤长度大于2000mm的直线图元
            water_pit_origin_entity_info = {}
            gutter_origin_entity_info = {}
            for cad_class, entity_list in origin_entity_info.items():
                # print("cad_class:", cad_class)
                if cad_class not in ['line']:
                    # water_pit_origin_entity_info[cad_class] = entity_list
                    gutter_origin_entity_info[cad_class] = entity_list
                else:
                    water_pit_entity_list = []
                    gutter_entity_list = []
                    for entity, style in entity_list:
                        if 500*ratio < point_euclidean_distance(entity[:2], entity[2:]) <= 2300*ratio:
                            # print("water pit line dist", entity, point_euclidean_distance(entity[:2], entity[2:])/ratio)
                            water_pit_entity_list.append([entity, style])
                        elif 250*ratio < point_euclidean_distance(entity[:2], entity[2:]) <= 500*ratio:
                            water_pit_entity_list.append([entity, style])
                            gutter_entity_list.append([entity, style])
                        else:
                            # print("gutter line dist", entity, point_euclidean_distance(entity[:2], entity[2:]) / ratio)
                            gutter_entity_list.append([entity, style])
                    water_pit_origin_entity_info[cad_class] = water_pit_entity_list
                    gutter_origin_entity_info[cad_class] = gutter_entity_list

            gutter_combine_bbox_contour = combine_new_indoor(layer, gutter_origin_entity_info, image_size,
                                                                ratio_w_h, ext_margin,
                                                                img_path, link_parallel_line=False, line_distance=280,
                                                                major='decor_architecture')
            water_pit_combine_bbox_contour = combine_new_indoor(layer, water_pit_origin_entity_info, image_size,
                                                                ratio_w_h, ext_margin,
                                                                img_path, link_parallel_line=False, line_distance=280,
                                                                major='decor_architecture')
            result = [info[0] for info in water_pit_combine_bbox_contour + gutter_combine_bbox_contour]
        else:
            if layer == 'gutter':  # 过滤方形水井的线条
                bbox_list = [remove_margin(bbox, ext_margin) for bbox in bbox_list]
                len_list = [((bbox[2] - bbox[0]) ** 2 + (bbox[3] - bbox[1]) ** 2) ** 0.5 for bbox in bbox_list]
                len_list = [length / (ratio * 1000) for length in len_list]
                num = len(len_list)
                bbox_list = [bbox_list[i] for i in range(num) if len_list[i] < 1.48
                             or 1.52 < len_list[i] < 1.98
                             or len_list[i] > 2.02]

            result = combine(bbox_list, image_size)

        final_result[layer] = result
        print('*' * 50, '\n', 'before combine entity num:{}'.format(len(bbox_list)), '\n',
              'after combine:{}'.format(len(final_result[layer])), '\n',
              'use time:{:.2f} seconds'.format(time() - start), '\n',
              '*' * 50, '\n')

    return final_result


def filt_bbox(layer, bbox_list, border_entity_info, drawing_type, crop_entity_image, entity_save_path):
    """

    Args:
        layer: 图层
        bbox_list:矩形框列表
        border_entity_info:图框全量信息
        drawing_type: 图纸类型
        crop_entity_image: 是否裁剪小图
        entity_save_path: 保存路径

    Returns:
        矩形框列表
    """
    # 根据图纸类型和图层类别，读入不同的图片。分图层打印和不分图层打印
    valid_entity_count = 0
    image_manager = border_entity_info['image_manager']
    ext_margin = border_entity_info['ext_margin']
    height, width = image_manager.img_height, image_manager.img_width
    if drawing_type in DrawingConfig.DRAWING_PRINT_LAYER_SEPARATE.value and \
            layer in LayerConfig.INDOOR_DRAWING_PRINT_LAYER_SEPARATE_SET.value['set_1']:
        # 截出小图
        img_whole = image_manager.load_from_manager(IMG_ENTITY_CLEAR_1_KEY)
    elif drawing_type in DrawingConfig.DRAWING_PRINT_LAYER_SEPARATE.value and \
            layer in LayerConfig.INDOOR_DRAWING_PRINT_LAYER_SEPARATE_SET.value['set_2']:
        img_whole = image_manager.load_from_manager(IMG_ENTITY_CLEAR_2_KEY)
    else:
        img_whole = image_manager.load_from_manager(IMG_WITHOUT_WALL_KEY)

    result_list = []

    # todo：对于新的图纸类型，增加新的不需要合并的图层配置
    for bbox in bbox_list:
        # 调整bbox坐标，小于0的置为0
        bbox = [i if i >= 0 else 0 for i in bbox]
        # 将bbox取值大于图片长宽的置为最大长宽值
        for i in [0, 2]:
            if bbox[i] > width - 1:
                bbox[i] = width - 1
        for i in [1, 3]:
            if bbox[i] > height - 1:
                bbox[i] = height - 1
        # 如果bbox的长、宽为0或者不是左上角和右下角的形式，跳过
        if bbox[0] >= bbox[2] or bbox[1] >= bbox[3]:
            # print('entity bbox invalid !!!')
            continue

        # 截取图元图像
        # temp = deepcopy(bbox)
        # if layer not in LayerConfig.CLASSIFICATION_EXCLUDE_LAYERS.value:
        #     temp = remove_margin(bbox, ext_margin)

        margin = ext_margin - 2 if ext_margin >= 2 else ext_margin
        temp = remove_margin(bbox, margin)

        # # 对remove_margin之后的temp进行处理和检查
        # temp = [i if i >= 0 else 0 for i in temp]
        # for i in [0, 2]:
        #     if temp[i] > width - 1:
        #         temp[i] = width - 1
        # for i in [1, 3]:
        #     if temp[i] > height - 1:
        #         temp[i] = height - 1
        if temp[0] >= temp[2] or temp[1] >= temp[3]:
            # print('temp bbox invalid !!!')
            continue

        # 截出小图
        entity_img = img_whole[temp[1]: temp[3], temp[0]: temp[2]]
        # 对小图周围补黑边
        entity_img_extend = entity_img_padding(entity_img, bbox, margin)

        # # 检查entity_img和bbox的尺寸是否相差至少1倍的margin
        # height_img, width_img = entity_img.shape[:2]
        # height_bbox, width_bbox = bbox[3] - bbox[1], bbox[2] - bbox[0]
        # # 该处不要求 bbox 比 entity_img 大出2倍的margin，只需要 bbox 比 entity_img 大出1倍的margin就行
        # if (height_bbox - height_img) <= margin or (width_bbox - width_img) <= margin:
        #     continue

        # 若补黑边的小图是全黑的，跳过
        if np.all(entity_img_extend == np.zeros(((bbox[3] - bbox[1]), (bbox[2] - bbox[0]), 3), np.uint8)):
            del entity_img, entity_img_extend
            # gc.collect()
            continue

        # 判断是否为背景图片，现在背景图片 RGB 为(0,0,0)
        background = np.zeros_like(entity_img)

        if layer not in LayerConfig.CLASSIFICATION_EXCLUDE_LAYERS.value and \
                (np.array(entity_img) == background).all():
            print('layer {} bbox {} is background'.format(layer, bbox))
            del entity_img, background, entity_img_extend
            # gc.collect()
            continue

        del entity_img, background
        # gc.collect()
        result_list.append(bbox)
        valid_entity_count += 1

        # 保存图元图像，用于训练构件分类模型
        if layer not in LayerConfig.CLASSIFICATION_EXCLUDE_LAYERS.value and crop_entity_image:
            # if border_info:
            #     entity_img_name = '{}_{}_{}.png'.format(dwg_name, border_info[0], valid_entity_count)
            # else:
            entity_img_name = '{}_{}.png'.format(layer, valid_entity_count)
            entity_save_path_by_layer = os.path.join(entity_save_path, layer)
            if not os.path.exists(entity_save_path_by_layer):
                os.makedirs(entity_save_path_by_layer)
            entity_img_saved_path = os.path.join(entity_save_path_by_layer, entity_img_name)
            entity_img_pil = Image.fromarray(entity_img_extend[:, :, ::-1])
            entity_img_pil.save(entity_img_saved_path)
            del entity_img_pil
            # gc.collect()
            
        del entity_img_extend
        # gc.collect()
    
    del image_manager, img_whole
    gc.collect()

    return result_list


@timer('entity_combination')
def run(border_name, border_entity_info, result_path, drawing_type, border_info=[], dwg_name="", rule_index=None,
        crop_entity_image=False):
    """
    构件合并

    :param border_name: 图框序号，例如 Model_0
    :param border_entity_info: 图框构件信息
    :param result_path: 中间结果保存路径
    :param drawing_type: 图框类型
    :param rule_index: 规则序号，为None 表示按照图纸类型粒度来运行，如果不为None，表示按照规则粒度来运行
    :param crop_entity_image: 是否截取构件小图，用于整理分类数据
    :return: 补充信息的 border_entity_info
    """

    border_entity_bbox = border_entity_info['border_entity_bbox']
    ext_margin = border_entity_info['ext_margin']
    w_ratio, h_ratio = border_entity_info['ratio']
    scale = border_entity_info['space_scale']
    origin_border_entity_info = border_entity_info['origin_border_entity_info']
    origin_border_entity_style = border_entity_info['origin_border_entity_style']
    border_coord = border_entity_info['border_coord']
    image_manager = border_entity_info['image_manager']
    start_time_1 = time()
    # 判断是否是本地debug环境，然后导入图片
    # 在线保存识图合并结果
    if SAVE_RECOG_GEN_IMG_ONLINE:
        img_with_wall = image_manager.load_from_manager(IMG_WITH_WALL_KEY)
        img_copy = img_with_wall.copy()
    else:
        img_copy = None

    height, width = image_manager.img_height, image_manager.img_width

    img_path_temp = os.path.join(result_path, border_name)

    layer_cad_class_dict = {}
    for layer, info in origin_border_entity_info.items():
        layer_cad_class_dict[layer] = (np.array(info)[:, 1]).tolist()

    # 创建该图框图元保存路径
    entity_save_path = os.path.join(result_path, '{}_{}'.format(border_name, drawing_type.value))
    if crop_entity_image and not os.path.exists(entity_save_path):
        os.mkdir(entity_save_path)

    # 已经在convert_border_image中创建了pillar_line
    # # 将柱子图层拆成线段的信息保留，用于得到土建墙线
    # pillar_line_bbox_list = border_entity_bbox['pillar'] if 'pillar' in border_entity_bbox.keys() else []

    # TODO: 如果有需要的话，完善其他类型图纸的合并方法
    start_time_2 = time()
    if drawing_type in DrawingConfig.DRAWING_OPERATION_CONFIG.value['combine_indoor']:
        border_entity_bbox_combined = combine_entity_indoor(
            origin_border_entity_info, origin_border_entity_style, border_entity_bbox, layer_cad_class_dict,
            (height, width), ext_margin, (w_ratio, h_ratio), scale, border_coord, image_manager, img_copy,
            drawing_type, img_path_temp)
    elif drawing_type in DrawingConfig.DRAWING_OPERATION_CONFIG.value['combine_underground']:
        border_entity_bbox_combined = combine_entity_underground(
            origin_border_entity_info, origin_border_entity_style, border_entity_bbox, layer_cad_class_dict,
            (height, width), ext_margin, (w_ratio, h_ratio), scale, border_coord, border_entity_info, img_path_temp)
    else:
        raise Exception('unsupported drawing type for combination:{}'.format(drawing_type))
    end_time_2 = time()
    print("====构件合并耗时====" * 3, end_time_2 - start_time_2)
    print('\n\n' + '=' * 20 + ' entity combination result' + '=' * 20)
    for layer, entity_bbox_list in border_entity_bbox_combined.items():
        print('after combine, layer {} entity num:{}'.format(layer, len(entity_bbox_list)))

    border_entity_bbox_dict = {}
    for layer, _ in border_entity_bbox_combined.items():
        border_entity_bbox_dict[layer] = []
    # 为防止图纸中没有wall、pillar、wall_line、pillar_line、wall_line_dash、pillar_line_dash，导致后面代码运行出错，给这些layer初始化一个空列表
    for layer in LayerConfig.LAYERS_WITH_SLOPE_LINE_REVISED.value + LayerConfig.DASH_LINE_REVISED.value + \
                 LayerConfig.LAYERS_WITH_SLOPE_LINE.value:
        border_entity_bbox_dict[layer] = []

    if 'dayang_handrail' not in border_entity_bbox_dict.keys():
        border_entity_bbox_dict['dayang_handrail'] = []
    if 'elevation_handrail' not in border_entity_bbox_dict.keys():
        border_entity_bbox_dict['elevation_handrail'] = []
    if 'plan_handrail' not in border_entity_bbox_dict.keys():
        border_entity_bbox_dict['plan_handrail'] = []

    # 在convert_border_image中已经创建了pillar_line
    # # 将柱子图层拆成线段的信息保留，用于得到土建墙线
    # border_entity_bbox_dict['pillar_line'] = pillar_line_bbox_list

    valid_entity_count = 0
    start_time = time()
    for layer, bbox_list in border_entity_bbox_combined.items():

        parallel_list = []
        # 规则52、62用到填充层的边界线，图纸类型不限于大样图
        # 如果layer是hatch_outline，填充层的边界在图纸中是没有画出来的，所以不能进行是否为背景图片的判断
        if layer in ['hatch_outline']:
            border_entity_bbox_dict[layer] = bbox_list
            continue

        if layer in ['door_intersect_bboxes', 'parking_contour_dict']:
            border_entity_bbox_dict[layer] = bbox_list
            continue

        if layer in ['dayang_handrail', 'elevation_handrail', 'plan_handrail']:
            border_entity_bbox_dict[layer] = bbox_list
            continue
        if layer in LayerConfig.LAYERS_WITH_SLOPE_LINE_REVISED.value + LayerConfig.DASH_LINE_REVISED.value:
            border_entity_bbox_dict[layer] = bbox_list
            continue

        # 过滤尺寸过大的起铺点
        if layer in ['floor_pavin']:
            bbox_list = [bbox for bbox in bbox_list if max((bbox[3]-bbox[1])/h_ratio, (bbox[2]-bbox[0])/w_ratio) < 1000]
            border_entity_bbox_dict[layer] = bbox_list
            continue

        if drawing_type in [DrawingType.DECORATION_PLAN_LAYOUT,] \
                and layer in LayerConfig.COMBINATION_EXCLUDE_LAYERS_INDOOR.value:
            bbox_list = list(set([tuple(bbox) for bbox in bbox_list]))
            bbox_list = [list(i) for i in bbox_list]
            border_entity_bbox_dict[layer] = bbox_list
            continue

        # 做了特殊处理，柱子构件比较特殊，需要合并但是不需要分类
        # if drawing_type in [DrawingType.UNDERGROUND, DrawingType.SITE_PLAN_ROAD, DrawingType.UNDERGROUND_BASEMENT,
        #                     DrawingType.SITE_PLAN_BUILDING, DrawingType.XIAOFANG_SITE_PLAN,
        #                     DrawingType.FIRST_FLOOR_SITE_PLAN]:
        #     bbox_list = list(set([tuple(bbox) for bbox in bbox_list]))
        #     bbox_list = [list(i) for i in bbox_list]
        #     border_entity_bbox_dict[layer] = bbox_list
        #     continue

        with ProcessPoolExecutor(max_workers=WORKERS) as parallel_pool:
            for i in range(WORKERS):
                temp = [bbox_tuple for j, bbox_tuple in enumerate(bbox_list) if j % WORKERS == i]
                p = parallel_pool.submit(filt_bbox, layer, temp, border_entity_info, drawing_type, crop_entity_image, entity_save_path)
                parallel_list.append(p)

            for p in as_completed(parallel_list):
                result = p.result()
                border_entity_bbox_dict[layer].extend(result)
        # border_entity_bbox_dict[layer] = filt_bbox(layer, bbox_list, border_entity_info, drawing_type, crop_entity_image, entity_save_path)

        gc.collect()

        if SAVE_RECOG_GEN_IMG_ONLINE:
            for bbox in border_entity_bbox_dict[layer]:
                cv2.rectangle(img_copy, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 1)
                cv2.putText(img_copy, str(valid_entity_count), (bbox[0], bbox[1] - 5), cv2.CHAIN_APPROX_SIMPLE, 0.5,
                            (0, 0, 255), 1)
        valid_entity_count += len(border_entity_bbox_dict[layer])
        del parallel_list

    end_time = time()
    print("======过滤bbox耗时======="*3, end_time - start_time)

    # todo 根据规则开发需要增加其他图纸类型（出现门）
    if drawing_type in [DrawingType.DECORATION_PLAN_LAYOUT, DrawingType.DECORATION_CEILING_LAYOUT]:
        # 获取像素相交分离构件并画粗黄线
        # separation_combination_pixel_list = separation_combination_pixel(border_entity_bbox_dict, img_copy, border_entity_info['ratio'], ext_margin)
        print('\n\ncheck intersection door....\n\n')
        intersection_door_list, recombine_door_list = check_intersection_door(border_entity_info,
                                                                              border_entity_bbox_dict, ext_margin)
        if SAVE_RECOG_GEN_IMG_ONLINE:
            for intersection_door in intersection_door_list:
                cv2.rectangle(img_copy, (intersection_door[0], intersection_door[1]),
                              (intersection_door[2], intersection_door[3]),
                              (0, 215, 255), 2)

            # 将重新合并的bbox画白框
            for recombine_door_l in recombine_door_list:
                for i, door_bbox in enumerate(recombine_door_l):
                    cv2.rectangle(img_copy, tuple(door_bbox[:2]), tuple(door_bbox[2:]), get_random_color(), 2)
                    cv2.putText(img_copy, str(i), (door_bbox[0], door_bbox[1] - 5), cv2.CHAIN_APPROX_SIMPLE, 0.5,
                                (0, 0, 255), 1)

        # 更新 border_entity_bbox_dict
        for origin_bbox, recombine_bbox_list in zip(intersection_door_list, recombine_door_list):
            for layer, bbox_list in border_entity_bbox_dict.items():
                if layer in ['door', 'window', 'elevator_door']:
                    if origin_bbox in bbox_list:
                        border_entity_bbox_dict[layer].remove(origin_bbox)
                        border_entity_bbox_dict[layer].extend(recombine_bbox_list)

    # 对柱子画黄框，for debug
    if SAVE_RECOG_GEN_IMG_ONLINE and 'pillar' in border_entity_bbox_dict:
        for i, bbox in enumerate(border_entity_bbox_dict['pillar']):
            cv2.rectangle(img_copy, (bbox[0] - 3, bbox[1] - 3), (bbox[2] + 3, bbox[3] + 3), (0, 215, 255), 1)

    print('LAYERS_WITH_SLOPE_LINE_REVISED layer:{}'.format(LayerConfig.LAYERS_WITH_SLOPE_LINE_REVISED.value))
    print('DASH_LINE_REVISED layer:{}'.format(LayerConfig.DASH_LINE_REVISED.value))

    # combination在对list进行排重时，会打乱list的顺序，所以在此对线段进行排序
    for layer_name in LayerConfig.LAYERS_WITH_SLOPE_LINE_REVISED.value + LayerConfig.DASH_LINE_REVISED.value:
        print('LAYERS_WITH_SLOPE_LINE_REVISED / DASH_LINE_REVISED layer:{}'.format(layer_name))
        try:
            print('---> before combine: {} lines'.format(len(border_entity_bbox_dict[layer_name])))
            start_time = time()
            border_entity_bbox_dict[layer_name] = sort_line_list_v2(border_entity_bbox_dict[layer_name])
            border_entity_bbox_dict[layer_name] = combine_lines_v2(border_entity_bbox_dict[layer_name], border_entity_info)
            print('---> after combine: {} lines'.format(len(border_entity_bbox_dict[layer_name])))
            print('---> used time: {} s'.format(time() - start_time))
        except Exception as ex_layer:
            pass

    # 进行引线系统合并

    main_branch_text_list, _ = get_annotation_group_decor(border_entity_info, result_path, img_anno=img_copy)

    img_with_wall = image_manager.load_from_manager(IMG_WITH_WALL_KEY)
    image_manager.load_to_manager(TOTLE_IMG_KEY, img_with_wall)  # 后面分类会在img_with_wall画分类框，保存img_with_wall for vanke-self rules
    del img_with_wall
    gc.collect()

    border_entity_info_update = {
        "entity_bbox_dict": border_entity_bbox_dict,  # 合并后的entity bbox 信息
        "main_branch_text_list": main_branch_text_list,  # 合并后的引线标注系统
    }

    border_entity_info.update(border_entity_info_update)

    border_entity_info.pop('border_entity_bbox')  # 去掉未合并的entity bbox 信息

    # 保存中间结果，部署的时候需要注释掉
    if SAVE_RECOG_GEN_IMG_ONLINE:
        whole_img_pil = Image.fromarray(img_copy[:, :, ::-1])
        img_path_temp = os.path.join(result_path, border_name)
        rule_str = f'_rule_{rule_index}' if rule_index else ''
        save_name = '{}_{}{}_{}'.format(img_path_temp, drawing_type.value, rule_str, IMAGE_PRINT_EXTENSION[3])
        whole_img_pil.save(save_name)

        # 将合并结果保存到image manager
        image_manager.load_to_manager(IMG_BBOX_RESULT, np.array(whole_img_pil)[:, :, ::-1])
        # for debug
        # bbox = image_manager.load_from_manager(IMG_BBOX_RESULT)
        # cv2.imwrite("/Users/xuan.ma/Desktop/bbox.png", bbox)

    end_time_1 = time()
    print("=====合并总耗时======"*3, end_time_1-start_time_1)
    return border_entity_info
