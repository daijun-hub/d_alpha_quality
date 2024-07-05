# -*- coding: utf-8 -*-

from enum import Enum

from .layer_config import LayerConfig


class DrawingType(Enum):
    # 采暖通风施工与设计说明
    HVAC_DESIGN = "设计与施工说明"
    B_HVAC_DESIGN = "设计与施工说明（地下）"
    MATERIAL_LIST = "主要设备材料表"
    B_MATERIAL_LIST = "主要设备材料表（地下）"
    B_VENTILATION = "车库顶板通风防排烟平面图"
    B_ROOF_VENTILATION = "地下车库通风平面图"
    B_HVAC_WATER = "地下车库暖通水管平面图"
    B_BOILER_ROOM = "锅炉房管路平面图"
    B_REFRIGERATION_ROOM = "制冷站管路平面图"
    T_HVAC = "地下层暖通平面图"
    T_1F_HEATING_VENTILATION = "一层采暖通风平面图"
    T_HEATING_VENTILATION = "标准层采暖通风平面图"
    T_RF_HEATING_VENTILATION = "屋顶层通风平面图"
    T_1F_AIR = "一层空调平面图"
    T_AIR = "标准层空调平面图"
    T_AIR_PRE_CAVITATION = "标准层预留洞口平面图"
    HEATING_SYSTEM = "采暖系统图"
    AIR_SYSTEM = "空调系统图"
    SMOKE_SYSTEM = "防排烟系统图"
    INSTALL_DAYANG = "安装大样图"
    CIVIL_AIR_DEFENSE_DESIGN = "暖通人防设计说明"
    CIVIL_AIR_DEFENSE_MATERIAL_LIST = "人防主要设备表"
    CIVIL_AIR_DEFENSE_B_VENTILATION = "地下室战时通风平面图"

    IGNORE = "其他暖通图纸类型"



class DrawingConfig(Enum):
    # 待添加
    DRAWING_OPERATION_CONFIG = {
        "extend_pixel_indoor": [
            DrawingType.B_VENTILATION, DrawingType.B_ROOF_VENTILATION,
            DrawingType.B_HVAC_WATER, DrawingType.MATERIAL_LIST,
            DrawingType.B_MATERIAL_LIST, DrawingType.T_1F_HEATING_VENTILATION,
            DrawingType.T_HEATING_VENTILATION, DrawingType.T_RF_HEATING_VENTILATION,
            DrawingType.T_AIR, DrawingType.T_1F_AIR, DrawingType.T_HVAC,
            DrawingType.T_AIR_PRE_CAVITATION, DrawingType.HEATING_SYSTEM,
            DrawingType.AIR_SYSTEM, DrawingType.SMOKE_SYSTEM,
            DrawingType.INSTALL_DAYANG, DrawingType.CIVIL_AIR_DEFENSE_DESIGN,
            DrawingType.CIVIL_AIR_DEFENSE_MATERIAL_LIST, DrawingType.CIVIL_AIR_DEFENSE_B_VENTILATION
        ],
        "extend_pixel_underground": [],

        "combine_indoor": [
            DrawingType.B_VENTILATION, DrawingType.B_ROOF_VENTILATION,
            DrawingType.B_HVAC_WATER, DrawingType.MATERIAL_LIST,
            DrawingType.B_MATERIAL_LIST, DrawingType.T_1F_HEATING_VENTILATION,
            DrawingType.T_HEATING_VENTILATION, DrawingType.T_RF_HEATING_VENTILATION,
            DrawingType.T_AIR, DrawingType.T_1F_AIR, DrawingType.T_HVAC,
            DrawingType.T_AIR_PRE_CAVITATION, DrawingType.HEATING_SYSTEM,
            DrawingType.AIR_SYSTEM, DrawingType.SMOKE_SYSTEM,
            DrawingType.INSTALL_DAYANG, DrawingType.CIVIL_AIR_DEFENSE_DESIGN,
            DrawingType.CIVIL_AIR_DEFENSE_MATERIAL_LIST, DrawingType.CIVIL_AIR_DEFENSE_B_VENTILATION
        ],
        "combine_underground": [],

        "classify_hvac": [
            DrawingType.CIVIL_AIR_DEFENSE_B_VENTILATION, DrawingType.B_ROOF_VENTILATION,
            DrawingType.B_HVAC_WATER, DrawingType.T_1F_HEATING_VENTILATION,
            DrawingType.T_HEATING_VENTILATION, DrawingType.T_AIR_PRE_CAVITATION,
            DrawingType.T_RF_HEATING_VENTILATION, DrawingType.SMOKE_SYSTEM,
            DrawingType.T_1F_AIR, DrawingType.T_AIR,
        ],
    }

    DRAWING_SEGMENT_LAYER_CONFIG = {
        # 平面图
        DrawingType.B_HVAC_WATER: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.CIVIL_AIR_DEFENSE_B_VENTILATION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.B_VENTILATION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.B_ROOF_VENTILATION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.B_BOILER_ROOM: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.B_REFRIGERATION_ROOM: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.T_HVAC: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.T_1F_HEATING_VENTILATION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.T_HEATING_VENTILATION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.T_RF_HEATING_VENTILATION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.T_1F_AIR: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.T_AIR: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.T_AIR_PRE_CAVITATION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.CIVIL_AIR_DEFENSE_MATERIAL_LIST: LayerConfig.BASIC_LAYERS.value['indoor_segment'],

        # # 系统图
        DrawingType.HEATING_SYSTEM: [],
        DrawingType.AIR_SYSTEM: [],
        DrawingType.SMOKE_SYSTEM: [],

        # 暖通设计说明
        DrawingType.HVAC_DESIGN: [],
        DrawingType.B_HVAC_DESIGN: [],
        DrawingType.B_HVAC_DESIGN: [],
        DrawingType.MATERIAL_LIST: [],
        DrawingType.B_MATERIAL_LIST: [],
        DrawingType.CIVIL_AIR_DEFENSE_DESIGN: [],

        # # 暖通详图
        DrawingType.INSTALL_DAYANG: [],
    }

    DRAWING_PRINT_LAYER_SEPARATE = [
        DrawingType.B_VENTILATION, DrawingType.B_ROOF_VENTILATION,
        DrawingType.B_HVAC_WATER, DrawingType.MATERIAL_LIST,
        DrawingType.B_MATERIAL_LIST, DrawingType.T_1F_HEATING_VENTILATION,
        DrawingType.T_HEATING_VENTILATION, DrawingType.T_RF_HEATING_VENTILATION,
        DrawingType.T_AIR, DrawingType.T_1F_AIR,
        DrawingType.T_AIR_PRE_CAVITATION, DrawingType.HEATING_SYSTEM,
        DrawingType.AIR_SYSTEM, DrawingType.SMOKE_SYSTEM,
        DrawingType.INSTALL_DAYANG, DrawingType.CIVIL_AIR_DEFENSE_DESIGN,
        DrawingType.CIVIL_AIR_DEFENSE_MATERIAL_LIST, DrawingType.CIVIL_AIR_DEFENSE_B_VENTILATION
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
        # DrawingType.INDOOR_FIRST_FLOOR_VENTILATION: {
        #     "solidline": True,
        #     "textclean": True,
        #     "hatchclean": False
        # },
        # DrawingType.WUDING_VENTILATION: {
        #     "solidline": True,
        #     "textclean": True,
        #     "hatchclean": False
        # },
        # DrawingType.JIFANG_VENTILATION: {
        #     "solidline": True,
        #     "textclean": True,
        #     "hatchclean": False
        # },
        # DrawingType.UNDERGROUND_VENTILATION: {
        #     "solidline": True,
        #     "textclean": True,
        #     "hatchclean": False
        # },
        # # 空调（采暖）平面图
        # DrawingType.INDOOR_AC_HEATING: {
        #     "solidline": True,
        #     "textclean": True,
        #     "hatchclean": False
        # },
        # DrawingType.INDOOR_FIRST_FLOOR_AC_HEATING: {
        #     "solidline": True,
        #     "textclean": True,
        #     "hatchclean": False
        # },
        # DrawingType.UNDERGROUND_AC_HEATING: {
        #     "solidline": True,
        #     "textclean": True,
        #     "hatchclean": False
        # },
        # # 防排烟系统图
        # DrawingType.SMOKE_MANAGEMENT_SYSTEM: {
        #     "solidline": True,
        #     "textclean": True,
        #     "hatchclean": True
        # },
        # # 暖通系统图
        # DrawingType.AC_HEATING_SYSTEM: {
        #     "solidline": True,
        #     "textclean": True,
        #     "hatchclean": True
        # },
        # 暖通设计说明
        DrawingType.HVAC_DESIGN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        # 设计与施工说明（地下）
        DrawingType.B_HVAC_DESIGN: {
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
        DrawingType.MATERIAL_LIST: {
            "负|地(下库)?|车库": {DrawingType.B_MATERIAL_LIST},
            "人防": {DrawingType.CIVIL_AIR_DEFENSE_MATERIAL_LIST}
        },
        DrawingType.HVAC_DESIGN: {
            "负|地(下库)?|车库": {DrawingType.B_HVAC_DESIGN},
            "人防": {DrawingType.CIVIL_AIR_DEFENSE_DESIGN}
        },
        DrawingType.T_1F_HEATING_VENTILATION: {
            "负|地(下库)?|车库": {DrawingType.B_ROOF_VENTILATION}
        },
        DrawingType.T_HEATING_VENTILATION: {
            "负|地(下库)?|车库": {DrawingType.B_ROOF_VENTILATION}
        },
    }

    # 图框推荐构件
    DRAWING_RECOMMEND_ENTITY_CONFIG = {
        # 平面图
        DrawingType.B_VENTILATION: [], # "车库顶板通风防排烟平面图"
        DrawingType.B_ROOF_VENTILATION: [], # "地下车库通风平面图"
        DrawingType.B_HVAC_WATER: [], # "地下车库暖通水管平面图"
        DrawingType.B_BOILER_ROOM: [], # "锅炉房管路平面图"
        DrawingType.B_REFRIGERATION_ROOM: [], # "制冷站管路平面图"
        DrawingType.T_HVAC: [], # "地下层暖通平面图"
        DrawingType.T_1F_HEATING_VENTILATION: [], # "一层采暖通风平面图"
        DrawingType.T_HEATING_VENTILATION: [], # "标准层采暖通风平面图"
        DrawingType.T_RF_HEATING_VENTILATION: [], # "屋顶层通风平面图"
        DrawingType.T_1F_AIR: [], # "一层空调平面图"
        DrawingType.T_AIR: [], # "标准层空调平面图"
        DrawingType.T_AIR_PRE_CAVITATION: [], # "标准层预留洞口平面图"
        DrawingType.CIVIL_AIR_DEFENSE_B_VENTILATION: [], # "地下室战时通风平面图"

        # 系统图
        DrawingType.HEATING_SYSTEM: [], # = "采暖系统图"
        DrawingType.AIR_SYSTEM: [], # = "空调系统图"
        DrawingType.SMOKE_SYSTEM: [], # = "防排烟系统图"

        # 暖通设计说明
        DrawingType.HVAC_DESIGN: [], # = "设计与施工说明"
        DrawingType.B_HVAC_DESIGN: [], # = "设计与施工说明（地下）"
        DrawingType.MATERIAL_LIST: [], # = "主要设备材料表"
        DrawingType.B_MATERIAL_LIST: [], # = "主要设备材料表（地下）"
        DrawingType.CIVIL_AIR_DEFENSE_DESIGN: [], #"暖通人防设计说明"
        DrawingType.CIVIL_AIR_DEFENSE_MATERIAL_LIST: [], # = "人防主要设备表"
        # 暖通详图
        # DrawingType.HVAC_DETAIL: []
        DrawingType.INSTALL_DAYANG: [], #  = "安装大样图"
    }
