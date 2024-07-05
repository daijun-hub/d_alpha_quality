# -*- coding: utf-8 -*-

from enum import Enum

from .layer_config import LayerConfig


class DrawingType(Enum):
    XIAOFANG = "消防非首层平面图"  # 消防非首层平面图
    XIAOFANG_FIRST_FLOOR = "消防首层平面图"  # 消防首层平面图
    XIAOFANG_UNDERGROUND = "地下消防平面图"  # 地下消防平面图
    PEIDIAN_PEIDIANXIANG_SYSTEM = "配电箱系统图"  # 配电箱系统图
    PEIDIAN_MAIN_ROUTE_SYSTEM = "配电箱干线系统图"  # 配电箱干线系统图
    DIANQI = "电气平面图"  # 电气平面图
    # DIANQI_FIRST_FLOOR = "dianqi_first_floor"  # TODO: 目前电气不分首层、非首层、地下平面图
    ZHAOMING = "照明非首层平面图"  # 照明非首层平面图
    ZHAOMING_FIRST_FLOOR = "照明首层平面图"  # 照明首层平面图
    ZHAOMING_UNDERGROUND = "地下照明平面图"  # 地下照明平面图
    HUXING_DAYANG = "户型大样图"  # 户型大样图
    FANGLEI = "防雷平面图"  # （11.11已弃用）防雷平面图，目前都是屋顶平面图
    DIANJING_DAYANG = "电井大样图"  # 电井大样图
    DIANQI_DESIGN = "电气设计说明"  # 电气设计说明
    HUOZAI_AUTO_SYSTEM = "火灾自动报警系统图"  # 火灾自动报警系统图

    # 11.9新增电气图纸类型
    STRONG_ELECTRICITY_SITE_PLAN = "强电总图"  # 强电总图
    WEAK_ELECTRICITY_SITE_PLAN = "弱电总图"  # 弱电总图
    PEIDIAN_ROOM_DAYANG = "配电房大样图"  # 配电房大样图
    GENERATOR_ROOM_DAYANG = "发电机房大样图"  # 发电机房大样图
    LOW_VOLTAGE_PEIDIAN_SYSTEM = "低压配电系统图"  # 低压配电系统图
    HIGH_VOLTAGE_SYSTEM = "高压系统图"  # 高压系统图
    BROADCAST = "广播平面图"  # 广播平面图
    BROADCAST_SYSTEM = "广播系统图"  # 广播系统图
    ELECTRICITY_MONITOR_SYSTEM = "电力监控系统图"  # 电力监控系统图

    # 11.11 新增拆分电气图纸类型
    ROOF_FANGLEI = "屋顶防雷平面图"  # 屋顶防雷平面图
    NON_ROOF_FANGLEI = "非屋顶防雷平面图"  # 非屋顶防雷平面图
    GROUND_CONNECTION = "基础接地平面图"  # 基础接地平面图
    FIRE_DOOR_MONITOR_SYSTEM = "防火门监控系统图"  # 防火门监控系统图
    ELECTRIC_FIRE_MONITOR_SYSTEM = "电气火灾监控系统图"  # 电气火灾监控系统图
    XIAOFANG_POWER_MONITOR_SYSTEM = "消防电源监控系统图"  # 消防电源监控系统图

    # 12.4 新增应急照明系统图
    EMERGENCY_ILLUMINATION_SYSTEM = "应急照明系统图"  # 应急照明系统图

    # 12.11 新增图纸类型
    XIAOFANG_CONTROL_ROOM_DAYANG = "消防控制室大样"  # 消防控制室大样
    EMERGENCY_ILLUMINATION_FIRST_FLOOR = "地上首层应急照明平面图"  # 地上首层应急照明平面图
    EMERGENCY_ILLUMINATION = "地上非首层应急照明平面图"  # 地上非首层应急照明平面图

    # 3.1 新增图纸类型
    QIANGDIAN_DESIGN = "强电设计说明"  # 强电设计说明
    XIAOFANG_DESIGN = "消防设计说明"  # 消防设计说明
    RUODIAN_DESIGN = "弱电设计说明"  # 弱电设计说明

    # 3.18 新增图纸类型
    # TULI_SHEET = 5037  # 图例表

    WEAK_ELECTRICITY = "弱电平面图"  # 弱电平面图
    STRONG_ELECTRICITY = "强电平面图" # 强电平面图

    IGNORE = "其他电气图纸类型"  # 未审查图框


class DrawingConfig(Enum):
    DRAWING_OPERATION_CONFIG = {
        "extend_pixel_indoor": [DrawingType.ZHAOMING, DrawingType.ZHAOMING_FIRST_FLOOR,
                                DrawingType.XIAOFANG, DrawingType.XIAOFANG_FIRST_FLOOR,
                                DrawingType.DIANQI, DrawingType.PEIDIAN_PEIDIANXIANG_SYSTEM,
                                DrawingType.HUOZAI_AUTO_SYSTEM, DrawingType.FANGLEI,
                                DrawingType.STRONG_ELECTRICITY_SITE_PLAN, DrawingType.WEAK_ELECTRICITY_SITE_PLAN,
                                DrawingType.PEIDIAN_ROOM_DAYANG, DrawingType.GENERATOR_ROOM_DAYANG,
                                DrawingType.LOW_VOLTAGE_PEIDIAN_SYSTEM, DrawingType.HIGH_VOLTAGE_SYSTEM,
                                DrawingType.BROADCAST, DrawingType.BROADCAST_SYSTEM,
                                DrawingType.ELECTRICITY_MONITOR_SYSTEM, DrawingType.ROOF_FANGLEI,
                                DrawingType.NON_ROOF_FANGLEI, DrawingType.GROUND_CONNECTION,
                                DrawingType.FIRE_DOOR_MONITOR_SYSTEM, DrawingType.ELECTRIC_FIRE_MONITOR_SYSTEM,
                                DrawingType.XIAOFANG_POWER_MONITOR_SYSTEM, DrawingType.EMERGENCY_ILLUMINATION_SYSTEM,
                                DrawingType.XIAOFANG_CONTROL_ROOM_DAYANG, DrawingType.EMERGENCY_ILLUMINATION_FIRST_FLOOR,
                                DrawingType.EMERGENCY_ILLUMINATION, DrawingType.PEIDIAN_MAIN_ROUTE_SYSTEM,
                                DrawingType.HUXING_DAYANG, DrawingType.DIANJING_DAYANG],
        "extend_pixel_underground": [DrawingType.ZHAOMING_UNDERGROUND, DrawingType.XIAOFANG_UNDERGROUND, ],

        # "电气专业构件" 都按照地上构件做合并
        "combine_indoor": [DrawingType.ZHAOMING, DrawingType.ZHAOMING_FIRST_FLOOR,
                           DrawingType.XIAOFANG, DrawingType.XIAOFANG_FIRST_FLOOR,
                           DrawingType.ZHAOMING_UNDERGROUND, DrawingType.XIAOFANG_UNDERGROUND,
                           DrawingType.DIANQI, DrawingType.PEIDIAN_PEIDIANXIANG_SYSTEM,
                           DrawingType.HUOZAI_AUTO_SYSTEM, DrawingType.FANGLEI,
                           DrawingType.STRONG_ELECTRICITY_SITE_PLAN, DrawingType.WEAK_ELECTRICITY_SITE_PLAN,
                           DrawingType.PEIDIAN_ROOM_DAYANG, DrawingType.GENERATOR_ROOM_DAYANG,
                           DrawingType.LOW_VOLTAGE_PEIDIAN_SYSTEM, DrawingType.HIGH_VOLTAGE_SYSTEM,
                           DrawingType.BROADCAST, DrawingType.BROADCAST_SYSTEM,
                           DrawingType.ELECTRICITY_MONITOR_SYSTEM, DrawingType.ROOF_FANGLEI,
                           DrawingType.NON_ROOF_FANGLEI, DrawingType.GROUND_CONNECTION,
                           DrawingType.FIRE_DOOR_MONITOR_SYSTEM, DrawingType.ELECTRIC_FIRE_MONITOR_SYSTEM,
                           DrawingType.XIAOFANG_POWER_MONITOR_SYSTEM, DrawingType.EMERGENCY_ILLUMINATION_SYSTEM,
                           DrawingType.XIAOFANG_CONTROL_ROOM_DAYANG, DrawingType.EMERGENCY_ILLUMINATION_FIRST_FLOOR,
                           DrawingType.EMERGENCY_ILLUMINATION, DrawingType.PEIDIAN_MAIN_ROUTE_SYSTEM,
                           DrawingType.HUXING_DAYANG, DrawingType.DIANJING_DAYANG,
                           DrawingType.WEAK_ELECTRICITY, DrawingType.STRONG_ELECTRICITY],
        "combine_underground": [],

        # "classify_indoor": [DrawingType.ZHAOMING, DrawingType.ZHAOMING_FIRST_FLOOR,
        #                     DrawingType.XIAOFANG, DrawingType.XIAOFANG_FIRST_FLOOR,
        #                     DrawingType.DIANQI, ],
        # "classify_underground": [DrawingType.ZHAOMING_UNDERGROUND, ]
        #
        # "extend_pixel_electric": [DrawingType.ZHAOMING, DrawingType.ZHAOMING_FIRST_FLOOR,
        #                     DrawingType.XIAOFANG, DrawingType.XIAOFANG_FIRST_FLOOR,
        #                     DrawingType.DIANQI,
        #                     DrawingType.ZHAOMING_UNDERGROUND, ],
        #
        # "combine_electric": [DrawingType.ZHAOMING, DrawingType.ZHAOMING_FIRST_FLOOR,
        #                     DrawingType.XIAOFANG, DrawingType.XIAOFANG_FIRST_FLOOR,
        #                     DrawingType.DIANQI,
        #                     DrawingType.ZHAOMING_UNDERGROUND, ],

        "classify_electric": [DrawingType.ZHAOMING, DrawingType.ZHAOMING_FIRST_FLOOR,
                              DrawingType.XIAOFANG, DrawingType.XIAOFANG_FIRST_FLOOR,
                              DrawingType.DIANQI, DrawingType.PEIDIAN_PEIDIANXIANG_SYSTEM,
                              DrawingType.ZHAOMING_UNDERGROUND, DrawingType.XIAOFANG_UNDERGROUND,
                              DrawingType.HUOZAI_AUTO_SYSTEM, DrawingType.FANGLEI,
                              DrawingType.STRONG_ELECTRICITY_SITE_PLAN, DrawingType.WEAK_ELECTRICITY_SITE_PLAN,
                              DrawingType.PEIDIAN_ROOM_DAYANG, DrawingType.GENERATOR_ROOM_DAYANG,
                              DrawingType.LOW_VOLTAGE_PEIDIAN_SYSTEM, DrawingType.HIGH_VOLTAGE_SYSTEM,
                              DrawingType.BROADCAST, DrawingType.BROADCAST_SYSTEM,
                              DrawingType.ELECTRICITY_MONITOR_SYSTEM, DrawingType.ROOF_FANGLEI,
                              DrawingType.NON_ROOF_FANGLEI, DrawingType.GROUND_CONNECTION,
                              DrawingType.FIRE_DOOR_MONITOR_SYSTEM, DrawingType.ELECTRIC_FIRE_MONITOR_SYSTEM,
                              DrawingType.XIAOFANG_POWER_MONITOR_SYSTEM, DrawingType.EMERGENCY_ILLUMINATION_SYSTEM,
                              DrawingType.XIAOFANG_CONTROL_ROOM_DAYANG, DrawingType.EMERGENCY_ILLUMINATION_FIRST_FLOOR,
                              DrawingType.EMERGENCY_ILLUMINATION, DrawingType.PEIDIAN_MAIN_ROUTE_SYSTEM,
                              DrawingType.HUXING_DAYANG, DrawingType.DIANJING_DAYANG,
                              DrawingType.WEAK_ELECTRICITY, DrawingType.STRONG_ELECTRICITY, ]
    }

    DRAWING_SEGMENT_LAYER_CONFIG = {
        DrawingType.ZHAOMING: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.ZHAOMING_FIRST_FLOOR: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.ZHAOMING_UNDERGROUND: LayerConfig.BASIC_LAYERS.value['underground_segment'],
        DrawingType.XIAOFANG: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.XIAOFANG_FIRST_FLOOR: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.XIAOFANG_UNDERGROUND: LayerConfig.BASIC_LAYERS.value['underground_segment'],
        DrawingType.DIANQI: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.PEIDIAN_PEIDIANXIANG_SYSTEM: [],
        DrawingType.PEIDIAN_MAIN_ROUTE_SYSTEM: [],
        DrawingType.HUXING_DAYANG: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.FANGLEI: [],
        DrawingType.DIANJING_DAYANG: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.DIANQI_DESIGN: [],
        DrawingType.QIANGDIAN_DESIGN: [],
        DrawingType.XIAOFANG_DESIGN: [],
        DrawingType.RUODIAN_DESIGN: [],
        DrawingType.HUOZAI_AUTO_SYSTEM: [],
        DrawingType.STRONG_ELECTRICITY_SITE_PLAN: LayerConfig.BASIC_LAYERS.value['building_segment'],
        DrawingType.WEAK_ELECTRICITY_SITE_PLAN: LayerConfig.BASIC_LAYERS.value['building_segment'],
        DrawingType.PEIDIAN_ROOM_DAYANG: [],
        DrawingType.GENERATOR_ROOM_DAYANG: [],
        DrawingType.LOW_VOLTAGE_PEIDIAN_SYSTEM: [],
        DrawingType.HIGH_VOLTAGE_SYSTEM: [],
        DrawingType.BROADCAST: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.BROADCAST_SYSTEM: [],
        DrawingType.ELECTRICITY_MONITOR_SYSTEM: [],
        DrawingType.ROOF_FANGLEI: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.NON_ROOF_FANGLEI: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.GROUND_CONNECTION: LayerConfig.BASIC_LAYERS.value['underground_segment'],
        DrawingType.FIRE_DOOR_MONITOR_SYSTEM: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.ELECTRIC_FIRE_MONITOR_SYSTEM: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.XIAOFANG_POWER_MONITOR_SYSTEM: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.EMERGENCY_ILLUMINATION_SYSTEM: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.XIAOFANG_CONTROL_ROOM_DAYANG: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.EMERGENCY_ILLUMINATION_FIRST_FLOOR: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.EMERGENCY_ILLUMINATION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.WEAK_ELECTRICITY: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.STRONG_ELECTRICITY: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        # DrawingType.TULI_SHEET: [],
    }

    DRAWING_PRINT_LAYER_SEPARATE = [DrawingType.ZHAOMING, DrawingType.ZHAOMING_FIRST_FLOOR,
                                    DrawingType.XIAOFANG, DrawingType.XIAOFANG_FIRST_FLOOR,
                                    DrawingType.ZHAOMING_UNDERGROUND, DrawingType.XIAOFANG_UNDERGROUND,
                                    DrawingType.DIANQI, DrawingType.BROADCAST, DrawingType.ROOF_FANGLEI,
                                    DrawingType.NON_ROOF_FANGLEI, DrawingType.GROUND_CONNECTION,
                                    DrawingType.EMERGENCY_ILLUMINATION_FIRST_FLOOR, DrawingType.EMERGENCY_ILLUMINATION]

    DRAWING_WITH_DETECTION = [
        DrawingType.PEIDIAN_PEIDIANXIANG_SYSTEM, DrawingType.ZHAOMING, DrawingType.ZHAOMING_FIRST_FLOOR,
        DrawingType.ZHAOMING_UNDERGROUND,
    ]

    DRAWING_PRINT_CONFIG = {
        DrawingType.XIAOFANG: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.XIAOFANG_FIRST_FLOOR: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.XIAOFANG_UNDERGROUND: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.PEIDIAN_PEIDIANXIANG_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.PEIDIAN_MAIN_ROUTE_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.DIANQI: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.ZHAOMING: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.ZHAOMING_FIRST_FLOOR: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.ZHAOMING_UNDERGROUND: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.HUXING_DAYANG: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.FANGLEI: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.DIANJING_DAYANG: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.DIANQI_DESIGN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.HUOZAI_AUTO_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.STRONG_ELECTRICITY_SITE_PLAN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.WEAK_ELECTRICITY_SITE_PLAN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.PEIDIAN_ROOM_DAYANG: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.GENERATOR_ROOM_DAYANG: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.LOW_VOLTAGE_PEIDIAN_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.HIGH_VOLTAGE_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.BROADCAST: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.BROADCAST_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.ELECTRICITY_MONITOR_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.ROOF_FANGLEI: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.NON_ROOF_FANGLEI: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.GROUND_CONNECTION: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.FIRE_DOOR_MONITOR_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.ELECTRIC_FIRE_MONITOR_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.XIAOFANG_POWER_MONITOR_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.EMERGENCY_ILLUMINATION_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.XIAOFANG_CONTROL_ROOM_DAYANG: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.EMERGENCY_ILLUMINATION_FIRST_FLOOR: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.EMERGENCY_ILLUMINATION: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.QIANGDIAN_DESIGN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.XIAOFANG_DESIGN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.RUODIAN_DESIGN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        # DrawingType.TULI_SHEET: {
        #     "solidline": True,
        #     "textclean": True,
        #     "hatchclean": True
        # },
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

    IGNORE_SUBPROJECT_DRAWING_TYPE = [DrawingType.XIAOFANG_UNDERGROUND, DrawingType.ZHAOMING_UNDERGROUND,
                                      DrawingType.STRONG_ELECTRICITY_SITE_PLAN, DrawingType.WEAK_ELECTRICITY_SITE_PLAN]

    SUBPROJECT_ADJUSTION_CONFIG = {}

    DRAWING_RECOMMEND_ENTITY_CONFIG = {
        DrawingType.PEIDIAN_PEIDIANXIANG_SYSTEM: [],
        DrawingType.LOW_VOLTAGE_PEIDIAN_SYSTEM: [],
        DrawingType.XIAOFANG: ['device', 'device_communication', 'device_fire', 'device_fire'],
        DrawingType.XIAOFANG_FIRST_FLOOR: ['device', 'device_communication', 'device_fire', 'device_fire'],
        DrawingType.XIAOFANG_UNDERGROUND: ['device', 'device_communication', 'device_fire', 'device_fire'],
        DrawingType.HUOZAI_AUTO_SYSTEM: ['device', 'device_communication', 'device_fire', 'device_fire'],
        DrawingType.ZHAOMING: ['device_box', 'single_tube_lamp', 'device_light', 'common_lamp', 'device'],
        DrawingType.ZHAOMING_FIRST_FLOOR: ['device_box', 'single_tube_lamp', 'device_light', 'common_lamp', 'device'],
        DrawingType.ZHAOMING_UNDERGROUND: ['device_box', 'single_tube_lamp', 'device_light', 'common_lamp', 'device'],
        DrawingType.ROOF_FANGLEI: ['yinxiaxian'],
        DrawingType.NON_ROOF_FANGLEI: ['yinxiaxian']
    }
