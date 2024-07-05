# -*- coding: utf-8 -*-

from enum import Enum

from .layer_config import LayerConfig


class DrawingType(Enum):
    # 设计说明图
    GENERAL_DESCRIPTION = "结构设计总说明"
    PILE_DESCRIPTION = "桩设计说明"

    # 住宅施工图
    WALL_COLUMN_GRAPH = "住宅墙柱平法施工图"
    WALL_COLUMN_DETAILS = "住宅墙柱详图"
    BEAM_GRAPH = "住宅梁平法施工图"
    STRUCTURE_GRAPH = "住宅结构平面图"
    SLAB_GRAPH = "住宅板平法施工图"

    # 地下室施工图
    BASEMENT_WALL_COLUMN_GRAPH = "地下室墙柱平法施工图"
    BASEMENT_WALL_COLUMN_DETAILS = "地下室墙柱详图"
    BASEMENT_BEAM_GRAPH = "地下室梁平法施工图"
    BASEMENT_SLAB_GRAPH = "地下室板平法施工图"
    BASEMENT_STRUCTURE_GRAPH = "地下室结构平面图"

    # 基础施工图
    PILE_GRAPH = "桩位平面布置图"
    BOLT_GRAPH = "锚杆平面布置图"
    BASIC_GRAPH = "基础平面布置图"
    PLATFORM_GRAPH = "承台平面布置图"
    BASE_STRUCTURE_DETAILS = "基础详图"

    # 大样详图
    STAIR_STRUCTURE_DETAILS = "楼梯详图"
    WALL_STRUCTURE_DETAILS = "墙身详图"
    BICYCLE_RAMP_STRUCTURE_DETAILS = "非机动车坡道详图"
    CAR_RAMP_STRUCTURE_DETAILS = "机动车坡道详图"
    CIVIL_AIR_DEFENSE_DETAILS = "人防详图"

    IGNORE = "其他图纸类型"


class DrawingConfig(Enum):

    DRAWING_OPERATION_CONFIG = {
        "extend_pixel_indoor": [
            DrawingType.GENERAL_DESCRIPTION,  DrawingType.PILE_DESCRIPTION,
            DrawingType.WALL_COLUMN_GRAPH, DrawingType.WALL_COLUMN_DETAILS, DrawingType.BEAM_GRAPH,
            DrawingType.STRUCTURE_GRAPH, DrawingType.SLAB_GRAPH,
            DrawingType.BASEMENT_WALL_COLUMN_GRAPH, DrawingType.BASEMENT_WALL_COLUMN_DETAILS,
            DrawingType.BASEMENT_BEAM_GRAPH, DrawingType.BASEMENT_SLAB_GRAPH, DrawingType.BASEMENT_STRUCTURE_GRAPH,
            DrawingType.PILE_GRAPH, DrawingType.BOLT_GRAPH, DrawingType.BASIC_GRAPH, DrawingType.PLATFORM_GRAPH,
            DrawingType.BASE_STRUCTURE_DETAILS,
            DrawingType.STAIR_STRUCTURE_DETAILS, DrawingType.WALL_STRUCTURE_DETAILS,
            DrawingType.BICYCLE_RAMP_STRUCTURE_DETAILS, DrawingType.CAR_RAMP_STRUCTURE_DETAILS,
            DrawingType.CIVIL_AIR_DEFENSE_DETAILS,
        ],
        "extend_pixel_underground": [],
        "combine_solid_wall": [
            DrawingType.BEAM_GRAPH, DrawingType.SLAB_GRAPH, DrawingType.WALL_COLUMN_GRAPH, DrawingType.BASIC_GRAPH
        ],
        "combine_wall_column": [
            DrawingType.WALL_COLUMN_GRAPH
        ],
        "combine_wall_body": [
            DrawingType.WALL_COLUMN_GRAPH
        ],
        "combine_pillar": [
            DrawingType.WALL_COLUMN_GRAPH, DrawingType.BEAM_GRAPH, DrawingType.SLAB_GRAPH, DrawingType.BASIC_GRAPH,
            DrawingType.BASEMENT_WALL_COLUMN_GRAPH, DrawingType.BASEMENT_BEAM_GRAPH, DrawingType.BASEMENT_SLAB_GRAPH
        ],
        "combine_beam": [
            DrawingType.BEAM_GRAPH, DrawingType.BASEMENT_BEAM_GRAPH, DrawingType.SLAB_GRAPH,
            DrawingType.BASEMENT_SLAB_GRAPH, DrawingType.WALL_COLUMN_GRAPH, DrawingType.STRUCTURE_GRAPH
        ],
        "combine_slab": [
            DrawingType.SLAB_GRAPH, DrawingType.BASEMENT_SLAB_GRAPH, DrawingType.STRUCTURE_GRAPH,
            DrawingType.BASEMENT_STRUCTURE_GRAPH
        ],
    }

    DRAWING_SEGMENT_LAYER_CONFIG = {
        # 通风平面图
        # DrawingType.INDOOR_VENTILATION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        # DrawingType.INDOOR_FIRST_FLOOR_VENTILATION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        # DrawingType.WUDING_VENTILATION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        # DrawingType.JIFANG_VENTILATION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        # DrawingType.UNDERGROUND_VENTILATION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        #
        # # 空调（采暖）平面图
        # DrawingType.INDOOR_AC_HEATING: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        # DrawingType.INDOOR_FIRST_FLOOR_AC_HEATING: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        # DrawingType.UNDERGROUND_AC_HEATING: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        #
        # # 系统图
        # DrawingType.SMOKE_MANAGEMENT_SYSTEM: [],
        # DrawingType.AC_HEATING_SYSTEM: [],
        #
        # 暖通设计说明
        # DrawingType.HVAC_DESIGN: [],
        # DrawingType.B_HVAC_DESIGN: [],
        #
        # # 暖通详图
        # DrawingType.HVAC_DETAIL: []
    }

    DRAWING_PRINT_LAYER_SEPARATE = [
            # DrawingType.B_VENTILATION,
            # DrawingType.B_HVAC_WATER, DrawingType.MATERIAL_LIST,
            # DrawingType.B_MATERIAL_LIST, DrawingType.T_1F_HEATING_VENTILATION,
            # DrawingType.T_HEATING_VENTILATION, DrawingType.T_RF_HEATING_VENTILATION,
            # DrawingType.T_AIR, DrawingType.T_1F_AIR,
            # DrawingType.T_AIR_PRE_CAVITATION, DrawingType.HEATING_SYSTEM,
            # DrawingType.AIR_SYSTEM, DrawingType.SMOKE_SYSTEM,
            # DrawingType.INSTALL_DAYANG, DrawingType.CIVIL_AIR_DEFENSE_DESIGN,
            # DrawingType.CIVIL_AIR_DEFENSE_MATERIAL_LIST, DrawingType.CIVIL_AIR_DEFENSE_B_VENTILATION
    ]

    DRAWING_WITH_DETECTION = []

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
        # DrawingType.HVAC_DESIGN: {
        #     "solidline": True,
        #     "textclean": True,
        #     "hatchclean": True
        # },
        # # 设计与施工说明（地下）
        # DrawingType.B_HVAC_DESIGN: {
        #     "solidline": True,
        #     "textclean": True,
        #     "hatchclean": True
        # },
        # # 暖通详图
        # DrawingType.HVAC_DETAIL: {
        #     "solidline": True,
        #     "textclean": True,
        #     "hatchclean": True
        # },
    }
    # 需要过滤的图名
    GLOBAL_IGNORE_NAME_LIST = [

    ]

    GLOBAL_IGNORE_SUBPROJECT_NAME_LIST = []  # 幼儿园不过滤

    MAJOR_LIST = ["建筑", "结构", "给排水", "暖通", "电气", "装修", "园林", "道路"]

    IGNORE_SUBPROJECT_DRAWING_TYPE = [
        # DrawingType.UNDERGROUND_VENTILATION, DrawingType.UNDERGROUND_AC_HEATING
    ]

    # 子项调整
    SUBPROJECT_ADJUSTION_CONFIG = {
        DrawingType.WALL_COLUMN_GRAPH: {
            "负|地(下库)?|车库": {DrawingType.BASEMENT_WALL_COLUMN_GRAPH},
        },
        DrawingType.WALL_COLUMN_DETAILS: {
            "负|地(下库)?|车库": {DrawingType.BASEMENT_WALL_COLUMN_DETAILS},
        },
        DrawingType.SLAB_GRAPH: {
            "负|地(下库)?|车库": {DrawingType.BASEMENT_SLAB_GRAPH}
        },
    }

    # 图框推荐构件 TODO
    DRAWING_RECOMMEND_ENTITY_CONFIG = {
        # # 通风平面图
        # DrawingType.INDOOR_VENTILATION: [],
        # DrawingType.INDOOR_FIRST_FLOOR_VENTILATION: [],
        # DrawingType.WUDING_VENTILATION: [],
        # DrawingType.JIFANG_VENTILATION: [],
        # DrawingType.UNDERGROUND_VENTILATION: [],
        #
        # # 空调（采暖）平面图
        # DrawingType.INDOOR_AC_HEATING: [],
        # DrawingType.INDOOR_FIRST_FLOOR_AC_HEATING: [],
        # DrawingType.UNDERGROUND_AC_HEATING: [],
        #
        # # 系统图
        # DrawingType.SMOKE_MANAGEMENT_SYSTEM: [],
        # DrawingType.AC_HEATING_SYSTEM: [],
        #
        # # 暖通设计说明
        # DrawingType.HVAC_DESIGN: [],
        #
        # # 暖通详图
        # DrawingType.HVAC_DETAIL: []
    }
