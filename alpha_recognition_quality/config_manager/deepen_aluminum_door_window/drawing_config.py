# -*- coding: utf-8 -*-
from enum import Enum

from .layer_config import LayerConfig


class DrawingType(Enum):
    IGNORE = "其他建筑图纸类型"   # 忽略
    DEEPEN_DOOR_WINDOW_DESCRIPTION = "门窗深化设计说明"  # 门窗深化设计说明



class DrawingConfig(Enum):
    DRAWING_OPERATION_CONFIG = {
        "extend_pixel_indoor": [],
        "extend_pixel_underground": [],

        "combine_indoor": [],
        "combine_underground": [],

        "classify_indoor": [],
        "classify_underground": [],
    }

    DRAWING_SEGMENT_LAYER_CONFIG = {

    }

    DRAWING_PRINT_LAYER_SEPARATE = []

    DRAWING_PRINT_SHELTER = []

    DRAWING_WITH_DETECTION = [

    ]

    DRAWING_PRINT_CONFIG = {

    }

    GLOBAL_IGNORE_NAME_LIST = [
        # "天面",
        "顶面",
        # "避难",
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
        "夹层",
        "电气",
        "配电",
        "照明",
        "弱电",
        "战时",
        # "架构",
        # "构架",
        "物管用房",
        "喷淋",
        #"详图",
        #"坡道",
        "人防孔况",
        # "布置",
        "绿地",
        "墙身平面",
        "自行车",
        "装饰线脚",
        # "标准层平面图",
        "管线",
        "地暖",
        "墙面排版",
        # "商业",
        # "核心筒",
        "平战"
    ]

    GLOBAL_IGNORE_SUBPROJECT_NAME_LIST = [
        "幼儿园"
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
