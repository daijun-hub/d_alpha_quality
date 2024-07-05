# -*- coding: utf-8 -*-

from enum import Enum

from .layer_config import LayerConfig


class DrawingType(Enum):

    DECORATION_ELECTRIC_PLAN = "户型电气平面图"
    DECORATION_PLUG_SWITCH_PLAN = "户型插座及开关安装尺寸子图"
    DECORATION_ELECTRIC_EQUIPMENT_SCHEDULE = "图例及主要设备表"
    DECORATION_STRONG_ELECTRIC_SYSTEM = "户型强电系统图"

    IGNORE = "其他电气图纸类型"  # 未审查图框


class DrawingConfig(Enum):
    DRAWING_OPERATION_CONFIG = {
        "extend_pixel_indoor": [DrawingType.DECORATION_ELECTRIC_PLAN, DrawingType.DECORATION_PLUG_SWITCH_PLAN,
                                DrawingType.DECORATION_ELECTRIC_EQUIPMENT_SCHEDULE, DrawingType.DECORATION_STRONG_ELECTRIC_SYSTEM,
                              ],
        "extend_pixel_underground": [],
        # "电气专业构件" 都按照地上构件做合并
        "combine_indoor": [DrawingType.DECORATION_ELECTRIC_PLAN, DrawingType.DECORATION_STRONG_ELECTRIC_SYSTEM],
        "combine_underground": [],
        "classify_electric": [DrawingType.DECORATION_ELECTRIC_PLAN, DrawingType.DECORATION_PLUG_SWITCH_PLAN,
                              DrawingType.DECORATION_ELECTRIC_EQUIPMENT_SCHEDULE, DrawingType.DECORATION_STRONG_ELECTRIC_SYSTEM,
                              ],
    }

    DRAWING_SEGMENT_LAYER_CONFIG = {
        DrawingType.DECORATION_ELECTRIC_PLAN: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.DECORATION_PLUG_SWITCH_PLAN: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.DECORATION_ELECTRIC_EQUIPMENT_SCHEDULE: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.DECORATION_STRONG_ELECTRIC_SYSTEM: [],
    }

    DRAWING_PRINT_LAYER_SEPARATE = [
        DrawingType.DECORATION_ELECTRIC_PLAN,
        # DrawingType.DECORATION_PLUG_SWITCH_PLAN,
        #                             DrawingType.DECORATION_ELECTRIC_EQUIPMENT_SCHEDULE, DrawingType.DECORATION_STRONG_ELECTRIC_SYSTEM,
                                    ]

    DRAWING_WITH_DETECTION = [
        DrawingType.DECORATION_ELECTRIC_PLAN, DrawingType.DECORATION_PLUG_SWITCH_PLAN,
        DrawingType.DECORATION_ELECTRIC_EQUIPMENT_SCHEDULE, DrawingType.DECORATION_STRONG_ELECTRIC_SYSTEM,
    ]

    DRAWING_PRINT_CONFIG = {
        DrawingType.DECORATION_ELECTRIC_PLAN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.DECORATION_PLUG_SWITCH_PLAN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.DECORATION_ELECTRIC_EQUIPMENT_SCHEDULE: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.DECORATION_STRONG_ELECTRIC_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
       
    }

    GLOBAL_IGNORE_NAME_LIST = [
        # "屋面",
        # "屋顶",  # 防雷平面图目前都是屋顶平面图
        # "天面",
        "顶面",
        "避难",
        # "示意",
        # "消防",
        "火警",
        "景观",
        "采暖",
        "通风",
        "地面",
        # "竖向",
        "道路",
        # "机房",
        "标高",
        "水施",
        "底板",
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
        "架构",
        # "构架",
        "物管用房",
        "喷淋",
        # "详图",
        # "坡道",
        "人防孔况",
        # "布置",
        "绿地",
        "墙身平面",
        # "楼梯",  # 楼梯大样图
        "自行车",
        "装饰线脚",
        "标准层平面图",
        "管线",
        "地暖",
        "墙面排版",
        # "商业",
        "核心筒"
    ]

    GLOBAL_IGNORE_SUBPROJECT_NAME_LIST = []  # 幼儿园不过滤

    MAJOR_LIST = ["建筑", "结构", "给排水", "暖通", "电气", "装修", "园林", "道路"]

    IGNORE_SUBPROJECT_DRAWING_TYPE = []

    SUBPROJECT_ADJUSTION_CONFIG = {}

    DRAWING_RECOMMEND_ENTITY_CONFIG = {
        DrawingType.DECORATION_ELECTRIC_PLAN: ['device_box', 'device_switch', ],
        DrawingType.DECORATION_PLUG_SWITCH_PLAN: [],
        DrawingType.DECORATION_ELECTRIC_EQUIPMENT_SCHEDULE: [],
        DrawingType.DECORATION_STRONG_ELECTRIC_SYSTEM: [],
    }
    DRAWING_RECOMMEND_OPERATION_CONFIG = {
        DrawingType.DECORATION_ELECTRIC_PLAN: ['combination', 'classification', 'text_information', 'segmentation'],
        DrawingType.DECORATION_STRONG_ELECTRIC_SYSTEM: ['combination', 'classification', 'text_information'],
    }
