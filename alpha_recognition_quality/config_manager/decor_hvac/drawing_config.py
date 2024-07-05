# -*- coding: utf-8 -*-

from enum import Enum

from .layer_config import LayerConfig


class DrawingType(Enum):
    DECORATION_HVAC_VENTILATION_PLAN = "户型空调通风平面图"
    DECORATION_HEATING_DESCRIPTION = "户型供暖设计与施工说明"
    HEATING_PLAN = "供暖平面图"
    DECORATION_AC_DESCRIPTION = "空调设计与施工说明"
    IGNORE = "其他暖通图纸类型"



class DrawingConfig(Enum):
    # 待添加
    DRAWING_OPERATION_CONFIG = {
        "extend_pixel_indoor": [DrawingType.DECORATION_HVAC_VENTILATION_PLAN, DrawingType.HEATING_PLAN

        ],
        "extend_pixel_underground": [],

        "combine_indoor": [DrawingType.DECORATION_HVAC_VENTILATION_PLAN, DrawingType.HEATING_PLAN

        ],
        "combine_underground": [],

        "classify_decor_hvac": [DrawingType.DECORATION_HVAC_VENTILATION_PLAN, DrawingType.HEATING_PLAN

        ],
    }

    DRAWING_SEGMENT_LAYER_CONFIG = {
        # 平面图
        DrawingType.DECORATION_HVAC_VENTILATION_PLAN: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.HEATING_PLAN: LayerConfig.BASIC_LAYERS.value['indoor_segment'],

        # # 系统图
        # DrawingType.HEATING_SYSTEM: [],
        # DrawingType.AIR_SYSTEM: [],
        # DrawingType.SMOKE_SYSTEM: [],

        # 暖通设计说明
        DrawingType.DECORATION_HEATING_DESCRIPTION: [],

        # # 暖通详图
        # DrawingType.INSTALL_DAYANG: [],
    }

    DRAWING_PRINT_LAYER_SEPARATE = [
        DrawingType.DECORATION_HVAC_VENTILATION_PLAN,
        DrawingType.HEATING_PLAN,
    ]

    DRAWING_WITH_DETECTION = []

    # TODO 咨询将达
    DRAWING_PRINT_CONFIG = {
        # 通风平面图
        # DrawingType.INDOOR_VENTILATION: {
        #     "solidline": True,
        #     "textclean": True,
        #     "hatchclean": False
        # },

        # 暖通设计说明
        DrawingType.DECORATION_HEATING_DESCRIPTION: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        # # 暖通详图
        # DrawingType.HVAC_DETAIL: {
        #     "solidline": True,
        #     "textclean": True,
        #     "hatchclean": True
        # },
    }
    # 需要过滤的图名
    GLOBAL_IGNORE_NAME_LIST = [
        # "天面",
        # "顶面",
        # "避难",
        # "示意",
        # "消防",
        # "火警",
        # "景观",
        # "采暖",
        # "通风",
        # "地面",
        # "竖向",
        # "道路",
        # "机房",
        # "标高",
        # "水施",
        # "底板",
        # "模板",
        # "管桩",
        # "承台",
        # "灌注",
        # "桩基础",
        # "墙柱",
        # "配筋",
        # "夹层",
        # "电气",
        # "配电",
        # "照明",
        # "弱电",
        # "战时",
        # "架构",
        # "构架",
        # "物管用房",
        # "喷淋",
        # "详图",
        # "坡道",
        # "人防孔况",
        # "布置",
        # "绿地",
        # "墙身平面",
        # "自行车",
        # "装饰线脚",
        # "标准层平面图",
        # "管线",
        # "地暖",
        # "墙面排版",
        # "商业",
        # "核心筒",
        # "平战"
    ]

    GLOBAL_IGNORE_SUBPROJECT_NAME_LIST = []  # 幼儿园不过滤

    MAJOR_LIST = ["建筑", "结构", "给排水", "暖通", "电气", "装修", "园林", "道路"]

    IGNORE_SUBPROJECT_DRAWING_TYPE = [] # DrawingType.SITE_PLAN_ROAD

    # 子项调整
    SUBPROJECT_ADJUSTION_CONFIG = {
        # DrawingType.MATERIAL_LIST: {
        #     "负|地(下库)?|车库": {DrawingType.B_MATERIAL_LIST},
        #     "人防": {DrawingType.CIVIL_AIR_DEFENSE_MATERIAL_LIST}
        # },
        # DrawingType.HVAC_DESIGN: {
        #     "负|地(下库)?|车库": {DrawingType.B_HVAC_DESIGN},
        #     "人防": {DrawingType.CIVIL_AIR_DEFENSE_DESIGN}
        # },
        # DrawingType.T_1F_HEATING_VENTILATION: {
        #     "负|地(下库)?|车库": {DrawingType.B_ROOF_VENTILATION}
        # },
        # DrawingType.T_HEATING_VENTILATION: {
        #     "负|地(下库)?|车库": {DrawingType.B_ROOF_VENTILATION}
        # },
    }

    # 图框推荐构件
    DRAWING_RECOMMEND_ENTITY_CONFIG = {
        # 平面图
        # DrawingType.B_VENTILATION: [], # "车库顶板通风防排烟平面图"

        # 系统图
        # DrawingType.HEATING_SYSTEM: [], # = "采暖系统图"

        # 暖通设计说明
        # DrawingType.HVAC_DESIGN: [], # = "设计与施工说明"

        # 暖通详图
        # DrawingType.HVAC_DETAIL: []
        # DrawingType.INSTALL_DAYANG: [], #  = "安装大样图"
    }
