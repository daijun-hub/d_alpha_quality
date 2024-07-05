# -*- coding: utf-8 -*-

from enum import Enum

from .layer_config import LayerConfig


class DrawingType(Enum):
    # 给排水平面图
    WATER_SUPPLY_DRAIN_PLAN = "给排水平面图",
    WATER_SUPPLY_SYSTEM_SUB = "给水系统子图",
    HOT_WATER_SUPPLY_SYSTEM_SUB = "热水系统子图",
    DECORATION_PLUMBING_DESCRIPTION = "装修给排水设计说明"

    IGNORE = "其他类型"


class DrawingConfig(Enum):
    # 待添加
    DRAWING_OPERATION_CONFIG = {
        "extend_pixel_indoor": [
            DrawingType.WATER_SUPPLY_DRAIN_PLAN
        ],

        "combine_indoor": [
            DrawingType.WATER_SUPPLY_DRAIN_PLAN,
            DrawingType.WATER_SUPPLY_SYSTEM_SUB,
            DrawingType.HOT_WATER_SUPPLY_SYSTEM_SUB,
            DrawingType.DECORATION_PLUMBING_DESCRIPTION
        ],
        "combine_underground": [],
        "extend_pixel_underground": [],

        "classify_plumbing": [
            DrawingType.WATER_SUPPLY_DRAIN_PLAN,
            DrawingType.WATER_SUPPLY_SYSTEM_SUB,
            DrawingType.HOT_WATER_SUPPLY_SYSTEM_SUB
        ],
    }

    DRAWING_SEGMENT_LAYER_CONFIG = {
        # 给排水平面图
        DrawingType.WATER_SUPPLY_DRAIN_PLAN: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
    }

    DRAWING_PRINT_LAYER_SEPARATE = [
        DrawingType.WATER_SUPPLY_DRAIN_PLAN,
    ]

    DRAWING_WITH_DETECTION = [
    ]

    DRAWING_PRINT_CONFIG = {
        # 给排水平面图
        DrawingType.WATER_SUPPLY_DRAIN_PLAN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
    }

    GLOBAL_IGNORE_NAME_LIST = [
        # "屋面",
        # "屋顶",  # 防雷平面图目前都是屋顶平面图
        # "天面",
        "顶面",
        # "避难",
        # "示意",
        # "消防",
        "火警",
        "景观",
        "采暖",
        "通风",
        # "地面",
        "竖向",
        "道路",
        # "机房",
        # "标高",
        # "水施",  # 给排水
        # "底板",
        "模板",
        "管桩",
        "承台",
        "灌注",
        "桩基础",
        "墙柱",
        "配筋",
        # "夹层",  # 夹层消防平面图
        # "电气",
        # "配电",
        # "照明",
        # "弱电",
        "战时",
        # "架构",  # 给排水
        # "构架",
        # "物管用房",
        # "喷淋",  # 给排水
        # "详图",
        # "坡道",
        "人防",
        # "布置",
        "绿地",
        "墙身平面",
        # "楼梯",  # 楼梯大样图
        "自行车",
        "装饰线脚",
        # "标准层平面图",
        # "管线",
        "地暖",
        "墙面排版",
        # "商业",
        # "核心筒",
        "防空",
        "覆土层",
    ]

    GLOBAL_IGNORE_SUBPROJECT_NAME_LIST = []  # 幼儿园不过滤

    MAJOR_LIST = ["建筑", "结构", "给排水", "暖通", "电气", "装修", "园林", "道路"]

    IGNORE_SUBPROJECT_DRAWING_TYPE = []

    SUBPROJECT_ADJUSTION_CONFIG = {
    }

    DRAWING_RECOMMEND_ENTITY_CONFIG = {
        DrawingType.WATER_SUPPLY_DRAIN_PLAN: ['elevation_symbol', 'rain_vpipe', 'cold_life_supply_hpipe',
                                              'hydrant_vpipe', 'hot_life_supply_hpipe', 'condensate_hpipe',
                                              'sewage_hpipe', 'pillar', 'relief_valve_and_hpipe', 'waste_hpipe',
                                              'waste_vpipe', 'wall', 'life_supply_vpipe', 'sprinkler_hpipe',
                                              'condensate_vpipe', 'fire_hydrant', 'sewage_vpipe', 'sprinkler_vpipe',
                                              'relief_valve', 'hydrant_hpipe']
    }
