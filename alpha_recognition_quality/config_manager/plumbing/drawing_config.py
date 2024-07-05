# -*- coding: utf-8 -*-

from enum import Enum

from .layer_config import LayerConfig


class DrawingType(Enum):
    # 给排水平面图
    TOWER_WATER_SUPPLY = "塔楼给水平面图"  # 塔楼给水平面图
    TOWER_WATER_DRAIN = "塔楼排水平面图"  # 塔楼排水平面图
    WUMIAN_WATER_SUPPLY = "屋面给水平面图"  # 屋面给水平面图
    WUMIAN_WATER_DRAIN = "屋面排水平面图"  # 屋面排水平面图
    WUDING_WATER_SUPPLY = "屋顶给水平面图"  # 屋顶给水平面图
    WUDING_WATER_DRAIN = "屋顶排水平面图"  # 屋顶排水平面图
    UNDERGROUND_WATER_SUPPLY = "地下室给水平面图"  # 地下室给水平面图
    UNDERGROUND_WATER_DRAIN = "地下室排水平面图"  # 地下室排水平面图
    # 喷淋平面图
    SPRINKLER = "喷淋平面图"  # 喷淋平面图
    UNDERGROUND_SPRINKLER = "地下室喷淋平面图"  # 地下室喷淋平面图
    # 给排水系统图
    INDOOR_WATER_SUPPLY_SYSTEM = "地上给水系统图"  # 地上给水系统图
    INDOOR_WATER_DRAIN_SYSTEM = "地上排水系统图"  # 地上排水系统图
    UNDERGROUND_WATER_SUPPLY_SYSTEM = "地下室给水系统图"  # 地下室给水系统图
    UNDERGROUND_WATER_DRAIN_SYSTEM = "地下室排水系统图"  # 地下室排水系统图
    UNDERGROUND_SPRINKLER_SYSTEM = "地下室喷淋系统图"  # 地下室喷淋系统图
    UNDERGROUND_FIRE_HYDRANT_SYSTEM = "地下室消火栓系统图"  # 地下室消火栓系统图
    # 给排水设计说明
    GEIPAISHUI_DESIGN = "给排水设计说明"  # 给排水设计说明
    # 给排水总图
    WATER_SUPPLY_SITE_PLAN = "给水总图"  # 给水总图
    WATER_DRAIN_SITE_PLAN = "排水总图"  # 排水总图
    # 大样图
    PUMP_DAYANG = "泵房大样图"  # 水泵房大样图
    GEIPAISHUI_HUXING_DAYANG = "户型大样图"  # 户型大样图
    RAINWATER_RECLAIM_DAYANG = "雨水回收大样图"  # 雨水回收大样图
    # 10.9添加系统图，暂时不启用
    # INDOOR_SPRINKLER_SYSTEM = 3023  # 地上喷淋系统图
    # INDOOR_FIRE_HYDRANT_SYSTEM = 3024  # 地上消火栓系统图
    # 11.1添加图纸类型
    OUTDOOR_GEIPAISHUI_DESIGN = "室外给排水设计说明"  # 室外给排水设计说明
    TOWER_FIRST_FLOOR_SUPPLY = "塔楼首层给水平面图"  # 塔楼首层给水平面图
    TOWER_FIRST_FLOOR_DRAIN = "塔楼首层排水平面图"  # 塔楼首层排水平面图
    TOWER_SECOND_FLOOR_SUPPLY = "塔楼二层给水平面图"  # 塔楼二层给水平面图
    TOWER_SECOND_FLOOR_DRAIN = "塔楼二层排水平面图"  # 塔楼二层排水平面图
    GAS_EXTINGUISH = "气体灭火图"  # 气体灭火图
    TOWER_BINAN_SUPPLY = "塔楼避难层给水平面图"  # 塔楼避难层给水平面图
    TOWER_BINAN_DRAIN = "塔楼避难层排水平面图"  # 塔楼避难层排水平面图

    IGNORE = "其他给排水图纸类型"  # 未审查图框


class DrawingConfig(Enum):
    # 待添加
    DRAWING_OPERATION_CONFIG = {
        "extend_pixel_indoor": [
            DrawingType.TOWER_WATER_SUPPLY, DrawingType.TOWER_WATER_DRAIN,
            DrawingType.WUMIAN_WATER_SUPPLY, DrawingType.WUMIAN_WATER_DRAIN,
            DrawingType.WUDING_WATER_SUPPLY, DrawingType.WUDING_WATER_DRAIN,
            DrawingType.SPRINKLER, DrawingType.INDOOR_WATER_SUPPLY_SYSTEM,
            DrawingType.INDOOR_WATER_DRAIN_SYSTEM, DrawingType.WATER_SUPPLY_SITE_PLAN,
            DrawingType.WATER_DRAIN_SITE_PLAN, DrawingType.PUMP_DAYANG,
            DrawingType.GEIPAISHUI_HUXING_DAYANG, DrawingType.RAINWATER_RECLAIM_DAYANG,
            DrawingType.UNDERGROUND_WATER_SUPPLY, DrawingType.UNDERGROUND_WATER_DRAIN,
            DrawingType.UNDERGROUND_SPRINKLER, DrawingType.UNDERGROUND_WATER_SUPPLY_SYSTEM,
            DrawingType.UNDERGROUND_WATER_DRAIN_SYSTEM, DrawingType.UNDERGROUND_SPRINKLER_SYSTEM,
            DrawingType.UNDERGROUND_FIRE_HYDRANT_SYSTEM,
            DrawingType.TOWER_FIRST_FLOOR_SUPPLY, DrawingType.TOWER_FIRST_FLOOR_DRAIN, 
            DrawingType.TOWER_SECOND_FLOOR_SUPPLY, DrawingType.TOWER_SECOND_FLOOR_DRAIN,
            DrawingType.GAS_EXTINGUISH, DrawingType.TOWER_BINAN_SUPPLY, DrawingType.TOWER_BINAN_DRAIN
        ],
        "extend_pixel_underground": [],

        "combine_indoor": [
            DrawingType.TOWER_WATER_SUPPLY, DrawingType.TOWER_WATER_DRAIN,
            DrawingType.WUMIAN_WATER_SUPPLY, DrawingType.WUMIAN_WATER_DRAIN,
            DrawingType.WUDING_WATER_SUPPLY, DrawingType.WUDING_WATER_DRAIN,
            DrawingType.SPRINKLER, DrawingType.INDOOR_WATER_SUPPLY_SYSTEM,
            DrawingType.INDOOR_WATER_DRAIN_SYSTEM, DrawingType.WATER_SUPPLY_SITE_PLAN,
            DrawingType.WATER_DRAIN_SITE_PLAN, DrawingType.PUMP_DAYANG,
            DrawingType.GEIPAISHUI_HUXING_DAYANG, DrawingType.RAINWATER_RECLAIM_DAYANG,
            DrawingType.UNDERGROUND_WATER_SUPPLY, DrawingType.UNDERGROUND_WATER_DRAIN,
            DrawingType.UNDERGROUND_SPRINKLER, DrawingType.UNDERGROUND_WATER_SUPPLY_SYSTEM,
            DrawingType.UNDERGROUND_WATER_DRAIN_SYSTEM, DrawingType.UNDERGROUND_SPRINKLER_SYSTEM,
            DrawingType.UNDERGROUND_FIRE_HYDRANT_SYSTEM,
            DrawingType.TOWER_FIRST_FLOOR_SUPPLY, DrawingType.TOWER_FIRST_FLOOR_DRAIN, 
            DrawingType.TOWER_SECOND_FLOOR_SUPPLY, DrawingType.TOWER_SECOND_FLOOR_DRAIN,
            DrawingType.GAS_EXTINGUISH, DrawingType.TOWER_BINAN_SUPPLY, DrawingType.TOWER_BINAN_DRAIN
        ],
        "combine_underground": [],

        "classify_plumbing": [
            DrawingType.TOWER_WATER_SUPPLY, DrawingType.TOWER_WATER_DRAIN,
            DrawingType.WUMIAN_WATER_SUPPLY, DrawingType.WUMIAN_WATER_DRAIN,
            DrawingType.WUDING_WATER_SUPPLY, DrawingType.WUDING_WATER_DRAIN,
            DrawingType.SPRINKLER, DrawingType.INDOOR_WATER_SUPPLY_SYSTEM,
            DrawingType.INDOOR_WATER_DRAIN_SYSTEM, DrawingType.WATER_SUPPLY_SITE_PLAN,
            DrawingType.WATER_DRAIN_SITE_PLAN, DrawingType.PUMP_DAYANG,
            DrawingType.GEIPAISHUI_HUXING_DAYANG, DrawingType.RAINWATER_RECLAIM_DAYANG,
            DrawingType.UNDERGROUND_WATER_SUPPLY, DrawingType.UNDERGROUND_WATER_DRAIN,
            DrawingType.UNDERGROUND_SPRINKLER, DrawingType.UNDERGROUND_WATER_SUPPLY_SYSTEM,
            DrawingType.UNDERGROUND_WATER_DRAIN_SYSTEM, DrawingType.UNDERGROUND_SPRINKLER_SYSTEM,
            DrawingType.UNDERGROUND_FIRE_HYDRANT_SYSTEM,
            DrawingType.TOWER_FIRST_FLOOR_SUPPLY, DrawingType.TOWER_FIRST_FLOOR_DRAIN, 
            DrawingType.TOWER_SECOND_FLOOR_SUPPLY, DrawingType.TOWER_SECOND_FLOOR_DRAIN,
            DrawingType.GAS_EXTINGUISH, DrawingType.TOWER_BINAN_SUPPLY, DrawingType.TOWER_BINAN_DRAIN
        ],
    }

    DRAWING_SEGMENT_LAYER_CONFIG = {
        # 给排水平面图
        DrawingType.TOWER_WATER_SUPPLY: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.TOWER_WATER_DRAIN: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.WUMIAN_WATER_SUPPLY: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.WUMIAN_WATER_DRAIN: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.WUDING_WATER_SUPPLY: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.WUDING_WATER_DRAIN: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.UNDERGROUND_WATER_SUPPLY: LayerConfig.BASIC_LAYERS.value['underground_segment'],
        DrawingType.UNDERGROUND_WATER_DRAIN: LayerConfig.BASIC_LAYERS.value['underground_segment'],
        # 喷淋平面图
        DrawingType.SPRINKLER: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.UNDERGROUND_SPRINKLER: LayerConfig.BASIC_LAYERS.value['underground_segment'],
        # 给排水系统图
        DrawingType.INDOOR_WATER_SUPPLY_SYSTEM: [],
        DrawingType.INDOOR_WATER_DRAIN_SYSTEM: [],
        DrawingType.UNDERGROUND_WATER_SUPPLY_SYSTEM: [],
        DrawingType.UNDERGROUND_WATER_DRAIN_SYSTEM: [],
        DrawingType.UNDERGROUND_SPRINKLER_SYSTEM: [],
        DrawingType.UNDERGROUND_FIRE_HYDRANT_SYSTEM: [],
        # 给排水设计说明
        DrawingType.GEIPAISHUI_DESIGN: [],
        # 给排水总图
        DrawingType.WATER_SUPPLY_SITE_PLAN: LayerConfig.BASIC_LAYERS.value['building_segment'],
        DrawingType.WATER_DRAIN_SITE_PLAN: LayerConfig.BASIC_LAYERS.value['building_segment'],
        # 大样图
        DrawingType.PUMP_DAYANG: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.GEIPAISHUI_HUXING_DAYANG: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.RAINWATER_RECLAIM_DAYANG: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        # 11.1添加图纸类型
        DrawingType.OUTDOOR_GEIPAISHUI_DESIGN: [],
        DrawingType.TOWER_FIRST_FLOOR_SUPPLY: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.TOWER_FIRST_FLOOR_DRAIN: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.TOWER_SECOND_FLOOR_SUPPLY: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.TOWER_SECOND_FLOOR_DRAIN: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.GAS_EXTINGUISH: [],
        # 塔楼避难层给水平面图、塔楼避难层排水平面图
        DrawingType.TOWER_BINAN_SUPPLY: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.TOWER_BINAN_DRAIN: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
    }

    DRAWING_PRINT_LAYER_SEPARATE = [
        DrawingType.TOWER_WATER_SUPPLY, DrawingType.TOWER_WATER_DRAIN,
        DrawingType.WUMIAN_WATER_SUPPLY, DrawingType.WUMIAN_WATER_DRAIN,
        DrawingType.WUDING_WATER_SUPPLY, DrawingType.WUDING_WATER_DRAIN,
        DrawingType.SPRINKLER, DrawingType.INDOOR_WATER_SUPPLY_SYSTEM,
        DrawingType.INDOOR_WATER_DRAIN_SYSTEM, DrawingType.WATER_SUPPLY_SITE_PLAN,
        DrawingType.WATER_DRAIN_SITE_PLAN, DrawingType.PUMP_DAYANG,
        DrawingType.GEIPAISHUI_HUXING_DAYANG, DrawingType.RAINWATER_RECLAIM_DAYANG,
        DrawingType.UNDERGROUND_WATER_SUPPLY, DrawingType.UNDERGROUND_WATER_DRAIN,
        DrawingType.UNDERGROUND_SPRINKLER, DrawingType.UNDERGROUND_WATER_SUPPLY_SYSTEM,
        DrawingType.UNDERGROUND_WATER_DRAIN_SYSTEM, DrawingType.UNDERGROUND_SPRINKLER_SYSTEM,
        DrawingType.UNDERGROUND_FIRE_HYDRANT_SYSTEM,
        DrawingType.TOWER_FIRST_FLOOR_SUPPLY, DrawingType.TOWER_FIRST_FLOOR_DRAIN,
        DrawingType.TOWER_SECOND_FLOOR_SUPPLY, DrawingType.TOWER_SECOND_FLOOR_DRAIN,
        DrawingType.TOWER_BINAN_SUPPLY, DrawingType.TOWER_BINAN_DRAIN,
    ]

    DRAWING_WITH_DETECTION = [
        DrawingType.INDOOR_WATER_SUPPLY_SYSTEM, DrawingType.INDOOR_WATER_DRAIN_SYSTEM,
        DrawingType.UNDERGROUND_WATER_SUPPLY_SYSTEM, DrawingType.UNDERGROUND_WATER_DRAIN_SYSTEM,
        DrawingType.UNDERGROUND_SPRINKLER_SYSTEM, DrawingType.UNDERGROUND_FIRE_HYDRANT_SYSTEM,
        DrawingType.TOWER_WATER_SUPPLY, DrawingType.TOWER_WATER_DRAIN,
        DrawingType.TOWER_FIRST_FLOOR_SUPPLY, DrawingType.TOWER_FIRST_FLOOR_DRAIN,
        DrawingType.TOWER_SECOND_FLOOR_SUPPLY, DrawingType.TOWER_SECOND_FLOOR_DRAIN,
        DrawingType.GEIPAISHUI_HUXING_DAYANG,
    ]

    DRAWING_PRINT_CONFIG = {
        # 给排水平面图
        DrawingType.TOWER_WATER_SUPPLY: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        DrawingType.TOWER_WATER_DRAIN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        DrawingType.WUMIAN_WATER_SUPPLY: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        DrawingType.WUMIAN_WATER_DRAIN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        DrawingType.WUDING_WATER_SUPPLY: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        DrawingType.WUDING_WATER_DRAIN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        DrawingType.UNDERGROUND_WATER_SUPPLY: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        DrawingType.UNDERGROUND_WATER_DRAIN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        # 喷淋平面图
        DrawingType.SPRINKLER: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        DrawingType.UNDERGROUND_SPRINKLER: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        # 给排水系统图
        DrawingType.INDOOR_WATER_SUPPLY_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.INDOOR_WATER_DRAIN_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.UNDERGROUND_WATER_SUPPLY_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.UNDERGROUND_WATER_DRAIN_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.UNDERGROUND_SPRINKLER_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.UNDERGROUND_FIRE_HYDRANT_SYSTEM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        # 给排水设计说明
        DrawingType.GEIPAISHUI_DESIGN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        # 给排水总图
        DrawingType.WATER_SUPPLY_SITE_PLAN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.WATER_DRAIN_SITE_PLAN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        # 大样图
        DrawingType.PUMP_DAYANG: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.GEIPAISHUI_HUXING_DAYANG: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.RAINWATER_RECLAIM_DAYANG: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.OUTDOOR_GEIPAISHUI_DESIGN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.TOWER_FIRST_FLOOR_SUPPLY: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        DrawingType.TOWER_FIRST_FLOOR_DRAIN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        DrawingType.TOWER_SECOND_FLOOR_SUPPLY: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        DrawingType.TOWER_SECOND_FLOOR_DRAIN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        DrawingType.GAS_EXTINGUISH: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.TOWER_BINAN_SUPPLY: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.TOWER_BINAN_DRAIN: {
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

    IGNORE_SUBPROJECT_DRAWING_TYPE = [DrawingType.UNDERGROUND_WATER_SUPPLY, DrawingType.UNDERGROUND_WATER_DRAIN,
                                      DrawingType.UNDERGROUND_FIRE_HYDRANT_SYSTEM, DrawingType.UNDERGROUND_SPRINKLER,
                                      DrawingType.UNDERGROUND_SPRINKLER_SYSTEM, DrawingType.UNDERGROUND_WATER_DRAIN_SYSTEM,
                                      DrawingType.UNDERGROUND_WATER_SUPPLY_SYSTEM, DrawingType.WATER_DRAIN_SITE_PLAN,
                                      DrawingType.WATER_SUPPLY_SITE_PLAN]

    SUBPROJECT_ADJUSTION_CONFIG = {
        DrawingType.TOWER_WATER_SUPPLY: {
            "总平面|总图": {DrawingType.WATER_SUPPLY_SITE_PLAN},
            "负|地[下库]|车库": {DrawingType.UNDERGROUND_WATER_SUPPLY}
        },
        DrawingType.TOWER_WATER_DRAIN: {
            "总平面|总图": {DrawingType.WATER_DRAIN_SITE_PLAN},
            "负|地[下库]|车库": {DrawingType.UNDERGROUND_WATER_DRAIN}
        },
        DrawingType.INDOOR_WATER_SUPPLY_SYSTEM: {
            "负|地[下库]|车库": {DrawingType.UNDERGROUND_WATER_SUPPLY_SYSTEM}
        },
        DrawingType.INDOOR_WATER_DRAIN_SYSTEM: {
            "负|地[下库]|车库": {DrawingType.UNDERGROUND_WATER_DRAIN_SYSTEM}
        },
        # DrawingType.INDOOR_SPRINKLER_SYSTEM:{
        #     "负|地[下库]|车库": {DrawingType.UNDERGROUND_SPRINKLER_SYSTEM}
        # },
        # DrawingType.INDOOR_FIRE_HYDRANT_SYSTEM:{
        #     "负|地[下库]|车库": {DrawingType.UNDERGROUND_FIRE_HYDRANT_SYSTEM}
        # },
        DrawingType.SPRINKLER: {
            "负|地[下库]|车库": {DrawingType.UNDERGROUND_SPRINKLER}
        },
        DrawingType.TOWER_FIRST_FLOOR_SUPPLY: {
            "总平面|总图": {DrawingType.WATER_SUPPLY_SITE_PLAN},
            "负|地[下库]|车库": {DrawingType.UNDERGROUND_WATER_SUPPLY}
        },
        DrawingType.TOWER_FIRST_FLOOR_DRAIN: {
            "总平面|总图": {DrawingType.WATER_DRAIN_SITE_PLAN},
            "负|地[下库]|车库": {DrawingType.UNDERGROUND_WATER_DRAIN}
        },
        DrawingType.TOWER_SECOND_FLOOR_SUPPLY: {
            "总平面|总图": {DrawingType.WATER_SUPPLY_SITE_PLAN},
            "负|地[下库]|车库": {DrawingType.UNDERGROUND_WATER_SUPPLY}
        },
        DrawingType.TOWER_SECOND_FLOOR_DRAIN: {
            "总平面|总图": {DrawingType.WATER_DRAIN_SITE_PLAN},
            "负|地[下库]|车库": {DrawingType.UNDERGROUND_WATER_DRAIN}
        },
        DrawingType.GEIPAISHUI_DESIGN: {
            "总图|室外": {DrawingType.OUTDOOR_GEIPAISHUI_DESIGN}
        }
    }

    DRAWING_RECOMMEND_ENTITY_CONFIG = {
        DrawingType.TOWER_WATER_SUPPLY: ['elevation_symbol', 'rain_vpipe', 'cold_life_supply_hpipe', 'hydrant_vpipe',
                                         'hot_life_supply_hpipe', 'condensate_hpipe', 'sewage_hpipe', 'pillar',
                                         'relief_valve_and_hpipe', 'waste_hpipe', 'waste_vpipe', 'wall',
                                         'life_supply_vpipe', 'sprinkler_hpipe', 'condensate_vpipe', 'fire_hydrant',
                                         'sewage_vpipe', 'sprinkler_vpipe', 'relief_valve', 'hydrant_hpipe'],
        DrawingType.TOWER_WATER_DRAIN: ['elevation_symbol', 'rain_vpipe', 'cold_life_supply_hpipe', 'hydrant_vpipe',
                                        'hot_life_supply_hpipe', 'condensate_hpipe', 'sewage_hpipe', 'pillar',
                                        'relief_valve_and_hpipe', 'waste_hpipe', 'waste_vpipe', 'wall',
                                        'life_supply_vpipe', 'sprinkler_hpipe', 'condensate_vpipe', 'fire_hydrant',
                                        'sewage_vpipe', 'sprinkler_vpipe', 'relief_valve', 'hydrant_hpipe'],
        DrawingType.WUMIAN_WATER_SUPPLY: ['hot_life_supply_hpipe', 'waste_vpipe', 'wall', 'condensate_vpipe',
                                          'sprinkler_vpipe', 'elevation_symbol', 'hydrant_vpipe', 'sewage_hpipe',
                                          'life_supply_vpipe', 'relief_valve', 'hydrant_hpipe', 'rain_vpipe',
                                          'condensate_hpipe', 'fire_hydrant', 'overflow_hole', 'sewage_vpipe',
                                          'cold_life_supply_hpipe', 'pillar', 'relief_valve_and_hpipe', 'waste_hpipe',
                                          'sprinkler_hpipe'],
        DrawingType.WUMIAN_WATER_DRAIN: ['hot_life_supply_hpipe', 'waste_vpipe', 'wall', 'condensate_vpipe',
                                         'sprinkler_vpipe', 'elevation_symbol', 'hydrant_vpipe', 'sewage_hpipe',
                                         'life_supply_vpipe', 'relief_valve', 'hydrant_hpipe', 'rain_vpipe',
                                         'condensate_hpipe', 'fire_hydrant', 'overflow_hole', 'sewage_vpipe',
                                         'cold_life_supply_hpipe', 'pillar', 'relief_valve_and_hpipe', 'waste_hpipe',
                                         'sprinkler_hpipe'],
        DrawingType.WUDING_WATER_SUPPLY: ['hot_life_supply_hpipe', 'waste_vpipe', 'wall', 'condensate_vpipe',
                                          'sprinkler_vpipe', 'elevation_symbol', 'hydrant_vpipe', 'sewage_hpipe',
                                          'life_supply_vpipe', 'relief_valve', 'hydrant_hpipe', 'rain_vpipe',
                                          'condensate_hpipe', 'fire_hydrant', 'overflow_hole', 'sewage_vpipe',
                                          'cold_life_supply_hpipe', 'pillar', 'relief_valve_and_hpipe', 'waste_hpipe',
                                          'sprinkler_hpipe'],
        DrawingType.WUDING_WATER_DRAIN: ['hot_life_supply_hpipe', 'waste_vpipe', 'wall', 'condensate_vpipe',
                                         'sprinkler_vpipe', 'elevation_symbol', 'hydrant_vpipe', 'sewage_hpipe',
                                         'life_supply_vpipe', 'relief_valve', 'hydrant_hpipe', 'rain_vpipe',
                                         'condensate_hpipe', 'fire_hydrant', 'overflow_hole', 'sewage_vpipe',
                                         'cold_life_supply_hpipe', 'pillar', 'relief_valve_and_hpipe', 'waste_hpipe',
                                         'sprinkler_hpipe'],
        DrawingType.UNDERGROUND_WATER_SUPPLY: ['hot_life_supply_hpipe', 'waste_vpipe', 'wall', 'water_pit',
                                               'condensate_vpipe', 'sprinkler_vpipe', 'elevation_symbol',
                                               'hydrant_vpipe', 'sewage_hpipe', 'life_supply_vpipe', 'relief_valve',
                                               'hydrant_hpipe', 'rain_vpipe', 'condensate_hpipe', 'fire_hydrant',
                                               'sewage_vpipe', 'valve', 'cold_life_supply_hpipe', 'pillar',
                                               'relief_valve_and_hpipe', 'waste_hpipe', 'sprinkler_hpipe'],
        DrawingType.UNDERGROUND_WATER_DRAIN: ['hot_life_supply_hpipe', 'waste_vpipe', 'wall', 'water_pit',
                                              'condensate_vpipe', 'sprinkler_vpipe', 'elevation_symbol',
                                              'hydrant_vpipe', 'sewage_hpipe', 'life_supply_vpipe', 'relief_valve',
                                              'hydrant_hpipe', 'rain_vpipe', 'condensate_hpipe', 'fire_hydrant',
                                              'sewage_vpipe', 'valve', 'cold_life_supply_hpipe', 'pillar',
                                              'relief_valve_and_hpipe', 'waste_hpipe', 'sprinkler_hpipe'],
        DrawingType.TOWER_FIRST_FLOOR_SUPPLY: ['elevation_symbol', 'rain_vpipe', 'cold_life_supply_hpipe',
                                               'hydrant_vpipe', 'hot_life_supply_hpipe', 'condensate_hpipe',
                                               'sewage_hpipe', 'pillar', 'relief_valve_and_hpipe', 'waste_hpipe',
                                               'waste_vpipe', 'wall', 'life_supply_vpipe', 'sprinkler_hpipe',
                                               'condensate_vpipe', 'fire_hydrant', 'sewage_vpipe', 'sprinkler_vpipe',
                                               'relief_valve', 'hydrant_hpipe'],
        DrawingType.TOWER_FIRST_FLOOR_DRAIN: ['elevation_symbol', 'rain_vpipe', 'cold_life_supply_hpipe',
                                              'hydrant_vpipe', 'hot_life_supply_hpipe', 'condensate_hpipe',
                                              'sewage_hpipe', 'pillar', 'relief_valve_and_hpipe', 'waste_hpipe',
                                              'waste_vpipe', 'wall', 'life_supply_vpipe', 'sprinkler_hpipe',
                                              'condensate_vpipe', 'fire_hydrant', 'sewage_vpipe', 'sprinkler_vpipe',
                                              'relief_valve', 'hydrant_hpipe'],
        DrawingType.INDOOR_WATER_SUPPLY_SYSTEM: ['elevation_symbol', 'cold_life_supply_hpipe', 'rain_well',
                                                 'hot_life_supply_hpipe', 'condensate_hpipe', 'sewage_hpipe',
                                                 'inspection_hole', 'relief_valve_and_hpipe', 'waste_hpipe',
                                                 'sprinkler_hpipe', 'fire_hydrant', 'relief_valve', 'hydrant_hpipe',
                                                 'wall_floor_line'],
        DrawingType.INDOOR_WATER_DRAIN_SYSTEM: ['elevation_symbol', 'cold_life_supply_hpipe', 'rain_well',
                                                'hot_life_supply_hpipe', 'condensate_hpipe', 'sewage_hpipe',
                                                'inspection_hole', 'relief_valve_and_hpipe', 'waste_hpipe',
                                                'sprinkler_hpipe', 'fire_hydrant', 'relief_valve', 'hydrant_hpipe',
                                                'wall_floor_line'],
        DrawingType.UNDERGROUND_WATER_SUPPLY_SYSTEM: ['elevation_symbol', 'cold_life_supply_hpipe', 'rain_well',
                                                      'hot_life_supply_hpipe', 'condensate_hpipe', 'sewage_hpipe',
                                                      'inspection_hole', 'relief_valve_and_hpipe', 'waste_hpipe',
                                                      'sprinkler_hpipe', 'fire_hydrant', 'relief_valve',
                                                      'hydrant_hpipe', 'wall_floor_line'],
        DrawingType.UNDERGROUND_WATER_DRAIN_SYSTEM: ['elevation_symbol', 'cold_life_supply_hpipe', 'rain_well',
                                                     'hot_life_supply_hpipe', 'condensate_hpipe', 'sewage_hpipe',
                                                     'inspection_hole', 'relief_valve_and_hpipe', 'waste_hpipe',
                                                     'sprinkler_hpipe', 'fire_hydrant', 'relief_valve',
                                                     'hydrant_hpipe', 'wall_floor_line'],
        DrawingType.UNDERGROUND_SPRINKLER_SYSTEM: ['elevation_symbol', 'cold_life_supply_hpipe', 'rain_well',
                                                   'hot_life_supply_hpipe', 'condensate_hpipe', 'sewage_hpipe',
                                                   'inspection_hole', 'relief_valve_and_hpipe', 'waste_hpipe',
                                                   'sprinkler_hpipe', 'fire_hydrant', 'relief_valve', 'hydrant_hpipe',
                                                   'wall_floor_line'],
        DrawingType.UNDERGROUND_FIRE_HYDRANT_SYSTEM: ['elevation_symbol', 'cold_life_supply_hpipe', 'rain_well',
                                                      'hot_life_supply_hpipe', 'condensate_hpipe', 'sewage_hpipe',
                                                      'inspection_hole', 'relief_valve_and_hpipe', 'waste_hpipe',
                                                      'sprinkler_hpipe', 'fire_hydrant', 'relief_valve',
                                                      'hydrant_hpipe', 'wall_floor_line'],
        DrawingType.SPRINKLER: [],
        DrawingType.UNDERGROUND_SPRINKLER: [],
        DrawingType.TOWER_BINAN_SUPPLY: [],
        DrawingType.TOWER_BINAN_DRAIN: [],
    }
