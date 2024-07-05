# -*- coding: utf-8 -*-
from enum import Enum

from .layer_config import LayerConfig


class DrawingType(Enum):
    IGNORE = "其他图纸类型"  # 忽略

    DECORATION_PLAN_LAYOUT = "户型平面布置图"  # 户型平面布置图
    DECORATION_CEILING_LAYOUT = "户型天花布置图"  # 户型天花布置图
    DECORATION_LIGHTING_SCHEDULE = "灯具选型明细表"  # 灯具选型明细表
    DECORATION_EQUIPMENT_SCHEDULE = "电器图参考表"  # 电器图参考表
    DECORATION_MATERIAL_SCHEDULE = "彩色材料表"  # 彩色材料表
    DECORATION_SANITARY_SCHEDULE = "洁具及五金选型明细表"  # 洁具及五金选型明细表
    DECORATION_METAL_SCHEDULE = "随楼附送五金参考图"  # 随楼附送五金参考图
    DECORATION_DOOR_SCHEDULE = "随楼附送门参考图"  # 随楼附送门参考图
    DECORATION_BATHROOM_ELEVATION = "卫生间立面图"  # 卫生间立面图
    DECORATION_KITCHEN_ELEVATION = "厨房立面图"  # 厨房立面图
    DECORATION_PLASTER_DETAIL = "线条大样图"  # 线条大样图
    DECORATION_GROUND_MATERIAL = "地面材质开线图"  # 地面材质开线图
    DECORATION_PUBLIC_STAIRCASE_ELEVATION = "公共梯间立面图"  # 公共梯间立面图
    DEEPEN_DOOR_WINDOW_DESCRIPTION = "门窗深化设计说明"  # 门窗深化设计说明
    # DECORATION_GROUND_PAVING = "地面铺贴图"
    DECORATION_GROUND_PAVING_DETAIL = "地面铺贴大样图"


class DrawingConfig(Enum):
    DRAWING_OPERATION_CONFIG = {
        "extend_pixel_indoor": [DrawingType.DECORATION_PLAN_LAYOUT, DrawingType.DECORATION_PLASTER_DETAIL,
                                DrawingType.DECORATION_EQUIPMENT_SCHEDULE, DrawingType.DECORATION_MATERIAL_SCHEDULE,
                                DrawingType.DECORATION_METAL_SCHEDULE],
        "extend_pixel_underground": [],

        "combine_indoor": [DrawingType.DECORATION_PLAN_LAYOUT, DrawingType.DECORATION_PLASTER_DETAIL,
                           DrawingType.DECORATION_SANITARY_SCHEDULE,
                           DrawingType.DECORATION_EQUIPMENT_SCHEDULE, DrawingType.DECORATION_MATERIAL_SCHEDULE,
                           DrawingType.DECORATION_METAL_SCHEDULE,
                           DrawingType.DECORATION_LIGHTING_SCHEDULE, DrawingType.DECORATION_CEILING_LAYOUT,
                           DrawingType.DECORATION_DOOR_SCHEDULE,
                           DrawingType.DECORATION_KITCHEN_ELEVATION, DrawingType.DECORATION_BATHROOM_ELEVATION,
                           DrawingType.DECORATION_GROUND_MATERIAL,
                           DrawingType.DECORATION_GROUND_PAVING_DETAIL],

        "combine_underground": [],

        "classify_indoor": [DrawingType.DECORATION_PLAN_LAYOUT, DrawingType.DECORATION_PLASTER_DETAIL,
                            DrawingType.DECORATION_EQUIPMENT_SCHEDULE, DrawingType.DECORATION_MATERIAL_SCHEDULE,
                            DrawingType.DECORATION_SANITARY_SCHEDULE, DrawingType.DECORATION_CEILING_LAYOUT,
                            DrawingType.DECORATION_GROUND_MATERIAL],
        "classify_underground": []
    }

    DRAWING_SEGMENT_LAYER_CONFIG = {
        DrawingType.DECORATION_PLAN_LAYOUT: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.DECORATION_CEILING_LAYOUT: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.DECORATION_BATHROOM_ELEVATION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.DECORATION_KITCHEN_ELEVATION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.DECORATION_LIGHTING_SCHEDULE: [],
        DrawingType.DECORATION_MATERIAL_SCHEDULE: [],
        DrawingType.DECORATION_EQUIPMENT_SCHEDULE: [],
        DrawingType.DECORATION_SANITARY_SCHEDULE: [],
        DrawingType.DECORATION_METAL_SCHEDULE: [],  # 新增
        DrawingType.DECORATION_PLASTER_DETAIL: LayerConfig.BASIC_LAYERS.value['indoor_segment'],  # 新增
        DrawingType.DECORATION_GROUND_MATERIAL: LayerConfig.BASIC_LAYERS.value['indoor_segment'],  # 新增
        DrawingType.DECORATION_PUBLIC_STAIRCASE_ELEVATION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.DECORATION_GROUND_PAVING_DETAIL: []

    }

    DRAWING_PRINT_LAYER_SEPARATE = [DrawingType.DECORATION_PLAN_LAYOUT,
                                    DrawingType.DECORATION_CEILING_LAYOUT,
                                    DrawingType.DECORATION_BATHROOM_ELEVATION,
                                    DrawingType.DECORATION_KITCHEN_ELEVATION,
                                    DrawingType.DECORATION_LIGHTING_SCHEDULE,
                                    DrawingType.DECORATION_MATERIAL_SCHEDULE,
                                    DrawingType.DECORATION_EQUIPMENT_SCHEDULE,
                                    DrawingType.DECORATION_SANITARY_SCHEDULE,
                                    DrawingType.DECORATION_METAL_SCHEDULE,
                                    DrawingType.DECORATION_PLASTER_DETAIL,
                                    DrawingType.DECORATION_GROUND_MATERIAL,  # 新增
                                    DrawingType.DECORATION_PUBLIC_STAIRCASE_ELEVATION,
                                    DrawingType.DECORATION_GROUND_PAVING_DETAIL]

    DRAWING_PRINT_SHELTER = [DrawingType.DECORATION_BATHROOM_ELEVATION,
                             DrawingType.DECORATION_KITCHEN_ELEVATION]

    DRAWING_WITH_DETECTION = [DrawingType.DECORATION_PLAN_LAYOUT,
                              DrawingType.DECORATION_CEILING_LAYOUT,
                              DrawingType.DECORATION_BATHROOM_ELEVATION,
                              DrawingType.DECORATION_KITCHEN_ELEVATION,
                              DrawingType.DECORATION_LIGHTING_SCHEDULE,
                              DrawingType.DECORATION_MATERIAL_SCHEDULE,
                              DrawingType.DECORATION_EQUIPMENT_SCHEDULE,
                              DrawingType.DECORATION_SANITARY_SCHEDULE,
                              DrawingType.DECORATION_METAL_SCHEDULE,
                              DrawingType.DECORATION_PLASTER_DETAIL,
                              DrawingType.DECORATION_GROUND_MATERIAL,  # 新增
                              DrawingType.DECORATION_PUBLIC_STAIRCASE_ELEVATION,
                              DrawingType.DECORATION_GROUND_PAVING_DETAIL
                              ]

    DRAWING_PRINT_CONFIG = {
        DrawingType.DECORATION_PLAN_LAYOUT: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.DECORATION_CEILING_LAYOUT: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.DECORATION_BATHROOM_ELEVATION: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.DECORATION_KITCHEN_ELEVATION: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.DECORATION_LIGHTING_SCHEDULE: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.DECORATION_MATERIAL_SCHEDULE: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.DECORATION_EQUIPMENT_SCHEDULE: {  # SIDE_ELEVATION打印填充
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        DrawingType.DECORATION_SANITARY_SCHEDULE: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.DECORATION_METAL_SCHEDULE: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False  # 设成True会在打印时去掉排水沟填充物，造成gutter分类错误
        },
        DrawingType.DECORATION_PLASTER_DETAIL: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        DrawingType.DECORATION_GROUND_MATERIAL: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False,
        },
        DrawingType.DECORATION_PUBLIC_STAIRCASE_ELEVATION: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.DECORATION_GROUND_PAVING_DETAIL: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False,
        }
    }

    GLOBAL_IGNORE_NAME_LIST = [

    ]

    GLOBAL_IGNORE_SUBPROJECT_NAME_LIST = [

    ]

    MAJOR_LIST = ["建筑", "结构", "给排水", "暖通", "电气", "装修", "园林", "道路"]

    SITEPLAN_IGNORE_NAME_LIST = ["排水", "地下"]

    IGNORE_SUBPROJECT_DRAWING_TYPE = []

    SUBPROJECT_ADJUSTION_CONFIG = {

    }

    SPACE_FILTER_CONFIG = {

    }

    ENTITY_IGNORE_CALLBCAK_CONFIG = {

    }

    # 有条件的过滤返回图纸类型的对象结果，A:[[B,C],[C,E]] 当A,B,C图纸类型或者A,C,E 同时存在时忽略A类型返回
    CONDITIONAL_ENTITY_IGNORE_CALLBACK_CONFIG = {

    }

    DRAWING_RECOMMEND_ENTITY_CONFIG = {

    }
