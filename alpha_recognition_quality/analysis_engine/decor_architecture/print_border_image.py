# -*- coding: utf-8 -*-

import json
import os
import subprocess
import datetime
from time import time

from PIL import Image
import numpy as np

# from config_manager.cad_config import RealDWG
from ...config_manager.decor_architecture.layer_config import LayerConfig
from ...config_manager.decor_architecture.drawing_config import DrawingType, DrawingConfig

from . import get_recommended_layers
from ...common.CONSTANTS import IMAGE_PRINT_EXTENSION, IMAGE_PRINT_EXTENSION_ENTITY_CLEAR
from ...common.decorator import timer


# 获取需要打印的图层
def get_printing_layers(layer_recommendation, drawing_type, all_layers_list):
    """

    Args:
        layer_recommendation: 推荐的图层
        drawing_type: 图纸类型
        all_layers_list: 所有图层列表

    Returns:
        需要打印的图层
    """
    all_layers = []
    layers_clear = []
    space_recog_layers = []

    # step 1: all_layers.png所需图层
    for hyper_layer, layer_list in layer_recommendation.items():
        if len(layer_list) == 0:
            continue

        all_layers.extend(layer_list)

    all_layers = list(set(all_layers))
    if '0' in all_layers:
        all_layers.remove('0')  # 打印程序去掉0图层

    # step 2: entity_clear.png所需图层
    # 不包含墙层柱子层的图纸，用于构件合并与分类
    exclude_layers = LayerConfig.CLASSIFICATION_EXCLUDE_LAYERS.value
    entity_layers = list(set(layer_recommendation.keys()) - set(exclude_layers))
    for hyper_layer in entity_layers:
        layers_clear.extend(layer_recommendation[hyper_layer])
    # print('---> get_printing_layers layer_recommendation', layer_recommendation)  # for debug

    # 不进行分类的hyper_layer的图层不会在entity_clear.png中打印，但这里有一个特例：
    # 水沟的填充物"filling"虽然不走分类，但是仍然要打印出来，否则gutter这个类的小图
    # 分类时，只有排水沟的外框没有内部填充，分类正确率会很低
    if 'filling' in layer_recommendation.keys():
        print('entity_clear.png中额外打印不需要分类的构件类别filling')
        layers_clear.extend(layer_recommendation['filling'])

    layers_clear = list(set(layers_clear))
    if '0' in layers_clear:
        layers_clear.remove('0')

    # step 3: space_recog.png所需图层
    # 用于空间识别的图纸的所需图层，地下图纸空间分割因为只需获取坡道空间，所以不使用door和window
    space_recog_hyper_layers = DrawingConfig.DRAWING_SEGMENT_LAYER_CONFIG.value.get(drawing_type, [])

    for hyper_layer in space_recog_hyper_layers:
        if hyper_layer in layer_recommendation:
            space_recog_layers.extend(layer_recommendation[hyper_layer])

    space_recog_layers = list(set(space_recog_layers))
    if '0' in space_recog_layers:
        space_recog_layers.remove('0')  # 打印程序去掉0图层

    print('space_recog_layers', space_recog_layers)

    # TODO: 由于某些图纸类型空间图层配置或规则配置有问题，打印所有的图层会造成空间错误，但是暂时不修改该处，以免造成某些规则的问题
    # 当图纸不需要分割的时候，可以将分割所需图层设置为全部图层，打印包含所有图层的图纸
    if len(space_recog_layers) == 0:
        space_recog_layers = all_layers_list
        # if drawing_type in[DrawingType.ELEVATION,DrawingType.SIDE_ELEVATION]:  # 立面图打印全部图层需要去掉栏杆和涂料，防止规则43误检
        #     # 这部分暂时hard-coding，不然需要大动干戈来满足这个feat
        #     remove_layers_dict = get_recommended_layers.run(['elevation_handrail', 'elevation_window_exclude'],
        #                                                     all_layers_list)
        #     remove_layers = remove_layers_dict['elevation_handrail'] + remove_layers_dict['elevation_window_exclude']
        #     space_recog_layers = list(set(space_recog_layers) - set(remove_layers))
        # elif drawing_type in [DrawingType.SITE_PLAN_BUILDING, DrawingType.SITE_PLAN_ROAD,
        #                       DrawingType.XIAOFANG_SITE_PLAN, DrawingType.FIRST_FLOOR_SITE_PLAN]:
        #     ignore_layers = ['red_line', 'red_line_sub', 'axis_grid', 'building', 'door', 'window', 'elevation_mark',
        #                      'wall_hatch', 'annotation', 'annotation_line', 'garage_exit', "basement_contour",
        #                      "kitchen_exhaust_pipe", "second_third_space", "elevation_mark","plan_handrail",
        #                      "parking", "gutter", "elevator_stair", "door", "window", "pipe", "arrow", "dayang_handrail",
        #                      "floor_drain_mix", "emergency_door", "pave", "engineering_work_table_line", "filter_road_layer"]
        #     remove_layers_dict = get_recommended_layers.run(ignore_layers, all_layers_list)
        #     remove_layers = []
        #     for layers_list in remove_layers_dict.values():
        #         remove_layers.extend(layers_list)
        #     space_recog_layers = list(set(space_recog_layers) - set(remove_layers))

    # img_print_layers = [all_layers, layers_clear, space_recog_layers]
    img_print_layers = {
        IMAGE_PRINT_EXTENSION[0]: all_layers,
        IMAGE_PRINT_EXTENSION[1]: layers_clear,
        IMAGE_PRINT_EXTENSION[2]: space_recog_layers,
    }
    # print('---> get_printing_layers layers_clear', layers_clear)

    # step 4: 其他, 比如地上住宅类型图纸需要entity_clear_1.png与entity_clear_2.png,
    # 总平图类型图纸需要building_recog.png
    if drawing_type in DrawingConfig.DRAWING_PRINT_LAYER_SEPARATE.value:
        # 地上住宅类型的图纸, 图层分两个集合分别打印, 防止构件像素重合导致的分类错误
        entity_separate_layers = get_entity_separate_layers(layer_recommendation)
        # img_print_layers.extend(entity_separate_layers)
        img_print_layers.update(entity_separate_layers)

    # 立面图和侧立面图打印的遮挡图层
    elif drawing_type in DrawingConfig.DRAWING_PRINT_SHELTER.value:
        elevation_shelter_hyper_layers = LayerConfig.BASIC_LAYERS.value['elevation_shelter']
        elevation_shelter_layers = []
        for hyper_layer in elevation_shelter_hyper_layers:
            # elevation_shelter_layers.extend(layer_recommendation[hyper_layer])
            elevation_shelter_layers.extend(layer_recommendation.get(hyper_layer, []))
        # 有些图纸中没有遮挡图层，从而会打印出来一些其他图层，此种情况，不添加空列表来请求打印
        if len(elevation_shelter_layers) != 0:
            # img_print_layers.append(elevation_shelter_layers)
            img_print_layers[IMAGE_PRINT_EXTENSION[9]] = elevation_shelter_layers
    # elif drawing_type in [DrawingType.SITE_PLAN_BUILDING, DrawingType.SITE_PLAN_ROAD,
    #                       DrawingType.XIAOFANG_SITE_PLAN, DrawingType.FIRST_FLOOR_SITE_PLAN]:
    #     # 注意underground_building会干扰住宅识别, 所以是在rule_55.py内部重新生成一张全
    #     # 黑底图用cv2打印, 这里不要用CAD_printer打印在png上
    #     building_recog_hyper_layers = LayerConfig.BASIC_LAYERS.value['building_segment']
    #     building_recog_layers = []
    #     for hyper_layer in building_recog_hyper_layers:
    #         # building_recog_layers.extend(layer_recommendation[hyper_layer])
    #         building_recog_layers.extend(layer_recommendation.get(hyper_layer, []))
    #     # img_print_layers.append(building_recog_layers)
    #
    #     img_print_layers[IMAGE_PRINT_EXTENSION[8]] = building_recog_layers

    return img_print_layers


# 获取分别打印构件的图层
def get_entity_separate_layers(layer_recommendation):
    """

    Args:
        layer_recommendation: 推荐图层

    Returns:
        分别打印构件的图层列表
    """
    exclude_layers = LayerConfig.CLASSIFICATION_EXCLUDE_LAYERS.value
    entity_layers = list(set(layer_recommendation.keys()) - set(exclude_layers))
    entity_layers_with_wall = entity_layers.copy()
    entity_layers_with_wall.extend(['wall', 'pillar'])
    entity_separate_hyper_layers_1 = set(entity_layers).intersection(
        LayerConfig.INDOOR_DRAWING_PRINT_LAYER_SEPARATE_SET.value['set_1'])
    entity_separate_hyper_layers_2 = set(entity_layers).intersection(
        LayerConfig.INDOOR_DRAWING_PRINT_LAYER_SEPARATE_SET.value['set_2'])
    entity_separate_hyper_layers_3 = set(entity_layers).intersection(
        LayerConfig.INDOOR_DRAWING_PRINT_LAYER_SEPARATE_SET.value['set_3'])
    entity_separate_hyper_layers_4 = set(entity_layers_with_wall).intersection(
        LayerConfig.INDOOR_DRAWING_PRINT_LAYER_SEPARATE_SET.value['set_4'])
    entity_separate_layers_1 = []
    entity_separate_layers_2 = []
    entity_separate_layers_3 = []
    entity_separate_layers_4 = []
    for hyper_layer in entity_separate_hyper_layers_1:
        # entity_separate_layers_1.extend(layer_recommendation[hyper_layer])
        entity_separate_layers_1.extend(layer_recommendation.get(hyper_layer, []))

    for hyper_layer in entity_separate_hyper_layers_2:
        # entity_separate_layers_2.extend(layer_recommendation[hyper_layer])
        entity_separate_layers_2.extend(layer_recommendation.get(hyper_layer, []))

    for hyper_layer in entity_separate_hyper_layers_3:
        # entity_separate_layers_3.extend(layer_recommendation[hyper_layer])
        entity_separate_layers_3.extend(layer_recommendation.get(hyper_layer, []))

    for hyper_layer in entity_separate_hyper_layers_4:
        # entity_separate_layers_4.extend(layer_recommendation[hyper_layer])
        entity_separate_layers_4.extend(layer_recommendation.get(hyper_layer, []))

    return {
        IMAGE_PRINT_EXTENSION_ENTITY_CLEAR[0]: entity_separate_layers_1, 
        IMAGE_PRINT_EXTENSION_ENTITY_CLEAR[1]: entity_separate_layers_2, 
        IMAGE_PRINT_EXTENSION_ENTITY_CLEAR[2]: entity_separate_layers_3, 
        IMAGE_PRINT_EXTENSION_ENTITY_CLEAR[3]: entity_separate_layers_4
    }