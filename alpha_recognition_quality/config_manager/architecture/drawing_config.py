# -*- coding: utf-8 -*-
from enum import Enum

from .layer_config import LayerConfig


class DrawingType(Enum):
    IGNORE = "其他建筑图纸类型"   # 忽略
    INDOOR = "住宅非首层平面图"  # 住宅非首层平面图
    UNDERGROUND = "地下车库平面图"  # 地下车库平面图
    INDOOR_FIRST_FLOOR = "住宅首层平面图"  # 住宅首层平面图
    INDOOR_FIRST_FLOOR_NO_SPACE = "住宅首层平面图（非住宅类型）"  # 住宅首层平面图（非住宅类型）
    SITE_PLAN_ROAD = "总平面图（道路相关）"  # 总平面图1 针对规则 22, 23, 26, 35 提取车道线
    SITE_PLAN_BUILDING = "总平面图（建筑轮廓相关）"  # 总平面图2 针对规则 27 31~34 提取轮廓
    ELEVATION = "立面图"  # 立面图
    SIDE_ELEVATION = "侧面立面图"  # 侧面立面图
    UNDERGROUND_DINGBAN = "车库顶板平面图"  # 车库顶板平面图
    UNDERGROUND_BASEMENT = "车库负一层平面图"  # 车库负一层平面图
    PUZHUANG = "铺装平面图"  # 铺装平面图
    PAISHUI = "排水平面图"  # 排水平面图
    WALL_DAYANG = "墙身大样图"  # 墙身大样图
    SECOND_THIRD_FLOOR = "住宅二三层平面图"  # 住宅二三层平面图
    INDOOR_FIRST_FLOOR_ACCESS = "住宅首层无障碍通道"  # 住宅首层无障碍通道
    PODAO = "坡道图纸"  # 坡道图纸
    STAIR_DAYANG = "楼梯大样图"  # 楼梯大样图
    BUILDING_DESIGN = "建筑设计说明"  # 建筑设计说明
    ENGINEERING_WORK = "工程做法表"  # 工程做法表
    DINGCENG = "屋顶层平面图"  # 屋顶层平面图
    WUMIAN = "屋面层平面图"   # 屋面层平面图
    SECTION = "剖面图"  # 剖面图
    JIFANG = "机房层平面图"  # 机房平面图

    # 12.5 新增总平面图
    XIAOFANG_SITE_PLAN = "消防总平面图"  # 消防总平面图
    FIRST_FLOOR_SITE_PLAN = "首层总平面图"  # 首层总平面图

    # 12.11 新增门窗大样
    DOOR_WINDOW_DAYANG = "门窗大样图"  # 门窗大样
    JIANZHU_HUXING_DAYANG = "户型大样图"  # 建筑户型大样
    
    # 12.16 新增避难层平面图
    BINANCENG = "避难层平面图"  # 避难层平面图

    INDOOR_BATHROOM = 0

    # 2021.09.22 添加碧桂园图纸类型 外墙材料表
    EXTERIOR_WALL_MATERIAL_LIST = '外墙材料表'


class DrawingConfig(Enum):
    DRAWING_OPERATION_CONFIG = {
        "extend_pixel_indoor": [DrawingType.INDOOR, DrawingType.INDOOR_BATHROOM, DrawingType.INDOOR_FIRST_FLOOR,
                                DrawingType.SIDE_ELEVATION, DrawingType.PAISHUI, DrawingType.ELEVATION,
                                DrawingType.SECOND_THIRD_FLOOR, DrawingType.INDOOR_FIRST_FLOOR_ACCESS,
                                DrawingType.WALL_DAYANG, DrawingType.WUMIAN, DrawingType.JIFANG, DrawingType.SECTION,
                                DrawingType.DOOR_WINDOW_DAYANG, DrawingType.JIANZHU_HUXING_DAYANG,
                                DrawingType.BINANCENG, DrawingType.DINGCENG],
        "extend_pixel_underground": [DrawingType.UNDERGROUND, DrawingType.UNDERGROUND_BASEMENT,
                                     DrawingType.SITE_PLAN_ROAD, DrawingType.PODAO, DrawingType.SITE_PLAN_BUILDING,
                                     DrawingType.XIAOFANG_SITE_PLAN, DrawingType.FIRST_FLOOR_SITE_PLAN],

        "combine_indoor": [DrawingType.INDOOR, DrawingType.INDOOR_BATHROOM, DrawingType.INDOOR_FIRST_FLOOR,
                           DrawingType.SIDE_ELEVATION, DrawingType.PAISHUI, DrawingType.ELEVATION,
                           DrawingType.SECOND_THIRD_FLOOR, DrawingType.JIFANG,
                           DrawingType.INDOOR_FIRST_FLOOR_ACCESS, DrawingType.WALL_DAYANG, DrawingType.STAIR_DAYANG,
                           DrawingType.WUMIAN, DrawingType.SECTION, DrawingType.DINGCENG, DrawingType.DOOR_WINDOW_DAYANG, 
                           DrawingType.JIANZHU_HUXING_DAYANG, DrawingType.BINANCENG],
        "combine_underground": [DrawingType.UNDERGROUND, DrawingType.UNDERGROUND_BASEMENT, 
                                DrawingType.SITE_PLAN_ROAD, DrawingType.PODAO, DrawingType.SITE_PLAN_BUILDING,
                                DrawingType.XIAOFANG_SITE_PLAN, DrawingType.FIRST_FLOOR_SITE_PLAN],

        "classify_indoor": [DrawingType.INDOOR, DrawingType.INDOOR_BATHROOM, DrawingType.INDOOR_FIRST_FLOOR,
                           DrawingType.SECOND_THIRD_FLOOR, DrawingType.SIDE_ELEVATION, DrawingType.PAISHUI, DrawingType.ELEVATION,
                            DrawingType.INDOOR_FIRST_FLOOR_ACCESS, DrawingType.WALL_DAYANG, DrawingType.WUMIAN,
                            DrawingType.JIFANG, DrawingType.STAIR_DAYANG, DrawingType.SECTION, DrawingType.DINGCENG,
                            DrawingType.DOOR_WINDOW_DAYANG, DrawingType.JIANZHU_HUXING_DAYANG, DrawingType.BINANCENG,
                            DrawingType.SECOND_THIRD_FLOOR],
        "classify_underground": [DrawingType.UNDERGROUND, DrawingType.UNDERGROUND_BASEMENT, 
                                 DrawingType.SITE_PLAN_ROAD, DrawingType.PODAO,
                                 DrawingType.SITE_PLAN_BUILDING, DrawingType.XIAOFANG_SITE_PLAN,
                                 DrawingType.FIRST_FLOOR_SITE_PLAN]
    }

    DRAWING_SEGMENT_LAYER_CONFIG = {
        DrawingType.INDOOR: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.INDOOR_BATHROOM: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.INDOOR_FIRST_FLOOR: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.INDOOR_FIRST_FLOOR_NO_SPACE: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.SIDE_ELEVATION: [],
        DrawingType.PAISHUI: [],
        DrawingType.ELEVATION: [],
        DrawingType.UNDERGROUND: LayerConfig.BASIC_LAYERS.value['underground_segment'],
        DrawingType.UNDERGROUND_BASEMENT: LayerConfig.BASIC_LAYERS.value['underground_segment'],
        DrawingType.PODAO: ["wall", "pillar", "podao", "podao_extra", "separator", "gutter"],
        # DrawingType.SITE_PLAN_ROAD: LayerConfig.BASIC_LAYERS.value['building_segment'],
        DrawingType.SITE_PLAN_ROAD: [],
        DrawingType.UNDERGROUND_DINGBAN: [],
        DrawingType.PUZHUANG: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        # DrawingType.SITE_PLAN_BUILDING: LayerConfig.BASIC_LAYERS.value['building_segment'],
        DrawingType.SITE_PLAN_BUILDING: [],
        DrawingType.WALL_DAYANG: [],
        DrawingType.SECOND_THIRD_FLOOR: LayerConfig.BASIC_LAYERS.value['second_third_segment'],
        DrawingType.INDOOR_FIRST_FLOOR_ACCESS: LayerConfig.BASIC_LAYERS.value['indoor_access_segment'],
        DrawingType.BUILDING_DESIGN: [],  # 新增
        DrawingType.EXTERIOR_WALL_MATERIAL_LIST: [],
        DrawingType.DINGCENG: LayerConfig.BASIC_LAYERS.value['indoor_segment'],  # 新增
        DrawingType.STAIR_DAYANG: LayerConfig.BASIC_LAYERS.value['indoor_segment'],  # 新增
        DrawingType.JIFANG: LayerConfig.BASIC_LAYERS.value['indoor_segment'],  # 新增
        DrawingType.WUMIAN: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.SECTION: LayerConfig.BASIC_LAYERS.value['indoor_segment'],  # 新增
        DrawingType.ENGINEERING_WORK: [],  # 新增
        # DrawingType.XIAOFANG_SITE_PLAN: LayerConfig.BASIC_LAYERS.value['building_segment'],
        DrawingType.XIAOFANG_SITE_PLAN: [],
        # DrawingType.FIRST_FLOOR_SITE_PLAN: LayerConfig.BASIC_LAYERS.value['building_segment'],
        DrawingType.FIRST_FLOOR_SITE_PLAN: [],
        DrawingType.DOOR_WINDOW_DAYANG: [],
        DrawingType.JIANZHU_HUXING_DAYANG: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
        DrawingType.BINANCENG: LayerConfig.BASIC_LAYERS.value['indoor_segment'],
    }

    DRAWING_PRINT_LAYER_SEPARATE = [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.UNDERGROUND,
                                    DrawingType.INDOOR_FIRST_FLOOR_NO_SPACE, DrawingType.INDOOR_FIRST_FLOOR_ACCESS,
                                    DrawingType.BINANCENG, DrawingType.JIANZHU_HUXING_DAYANG]

    DRAWING_PRINT_SHELTER = [DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION]

    DRAWING_WITH_DETECTION = [
        DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR,
        DrawingType.INDOOR_FIRST_FLOOR_NO_SPACE, DrawingType.INDOOR_FIRST_FLOOR_ACCESS,
        DrawingType.BINANCENG, DrawingType.JIANZHU_HUXING_DAYANG
    ]

    DRAWING_PRINT_CONFIG = {
        DrawingType.INDOOR: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.INDOOR_BATHROOM: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.INDOOR_FIRST_FLOOR: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.SIDE_ELEVATION: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.PAISHUI: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.ELEVATION: {  # SIDE_ELEVATION打印填充
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        }, 
        DrawingType.UNDERGROUND: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.UNDERGROUND_BASEMENT: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False   # 设成True会在打印时去掉排水沟填充物，造成gutter分类错误
        }, 
        DrawingType.PODAO: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },  
        DrawingType.SITE_PLAN_ROAD: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False,
        },
        DrawingType.UNDERGROUND_DINGBAN: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.PUZHUANG: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.SITE_PLAN_BUILDING: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False,
        },
        DrawingType.WALL_DAYANG: {
            "solidline": True,
            "textclean": True,
            "hatchclean": False
        },
        DrawingType.SECOND_THIRD_FLOOR: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.INDOOR_FIRST_FLOOR_ACCESS: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.BUILDING_DESIGN: {  # 新增
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.EXTERIOR_WALL_MATERIAL_LIST: {  # 新增
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.DINGCENG: {  # 新增
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.STAIR_DAYANG: {  # 新增
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.JIFANG: {  # 新增
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.WUMIAN: {  # 新增
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.INDOOR_FIRST_FLOOR_NO_SPACE: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.SECTION: {  # 新增
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.ENGINEERING_WORK: {  # 新增
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.XIAOFANG_SITE_PLAN: {  # 新增
            "solidline": True,
            "textclean": True,
            "hatchclean": False,
        }, 
        DrawingType.FIRST_FLOOR_SITE_PLAN: {  # 新增
            "solidline": True,
            "textclean": True,
            "hatchclean": False,
        },
        DrawingType.DOOR_WINDOW_DAYANG: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.JIANZHU_HUXING_DAYANG: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
        DrawingType.BINANCENG: {
            "solidline": True,
            "textclean": True,
            "hatchclean": True
        },
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

    IGNORE_SUBPROJECT_DRAWING_TYPE = [DrawingType.SITE_PLAN_ROAD, DrawingType.SITE_PLAN_BUILDING,
                                      DrawingType.XIAOFANG_SITE_PLAN, DrawingType.FIRST_FLOOR_SITE_PLAN,
                                      DrawingType.UNDERGROUND]

    SUBPROJECT_ADJUSTION_CONFIG = {
        DrawingType.INDOOR: {
            "总平面|总图": {DrawingType.SITE_PLAN_ROAD, DrawingType.SITE_PLAN_BUILDING,
                       DrawingType.XIAOFANG_SITE_PLAN, DrawingType.FIRST_FLOOR_SITE_PLAN},
            "负|地[下库]|车库": {DrawingType.UNDERGROUND}
        },
        DrawingType.INDOOR_FIRST_FLOOR: {
            "总平面|总图": {DrawingType.SITE_PLAN_ROAD, DrawingType.SITE_PLAN_BUILDING,
                       DrawingType.XIAOFANG_SITE_PLAN, DrawingType.FIRST_FLOOR_SITE_PLAN},
            "负|地[下库]|车库": {DrawingType.UNDERGROUND}
        },
        DrawingType.INDOOR_FIRST_FLOOR_ACCESS: {
            "总平面|总图": {DrawingType.SITE_PLAN_ROAD, DrawingType.SITE_PLAN_BUILDING,
                       DrawingType.XIAOFANG_SITE_PLAN, DrawingType.FIRST_FLOOR_SITE_PLAN},
            "负|地[下库]|车库": {DrawingType.UNDERGROUND}
        }
    }

    SPACE_FILTER_CONFIG = {
        DrawingType.INDOOR_FIRST_FLOOR_ACCESS: [],
        DrawingType.SECOND_THIRD_FLOOR: ["雨篷"]
    }

    ENTITY_IGNORE_CALLBCAK_CONFIG = {
        DrawingType.INDOOR_FIRST_FLOOR_ACCESS,
        DrawingType.SECOND_THIRD_FLOOR
    }

    # 有条件的过滤返回图纸类型的对象结果，A:[[B,C],[C,E]] 当A,B,C图纸类型或者A,C,E 同时存在时忽略A类型返回
    CONDITIONAL_ENTITY_IGNORE_CALLBACK_CONFIG = {
        DrawingType.SECTION: [
            [DrawingType.STAIR_DAYANG]  # 当楼梯大样图 与 剖面图 同时存在时，忽略剖面图返回
        ],
    }

    DRAWING_RECOMMEND_ENTITY_CONFIG = {
        DrawingType.INDOOR_FIRST_FLOOR: ['floor_drain', 'pipe', 'plan_handrail', 'elevator_box', 'floor_drain_mix',
                                         'window', 'air_conditioner_mix', 'door', 'annotation_line', 'elevator_stair',
                                         'mailbox', 'elevator_door'],
        DrawingType.INDOOR_FIRST_FLOOR_NO_SPACE: ['floor_drain', 'pipe', 'plan_handrail', 'elevator_box',
                                                  'floor_drain_mix', 'window', 'air_conditioner_mix', 'door',
                                                  'annotation_line', 'elevator_stair', 'mailbox', 'elevator_door'],
        DrawingType.INDOOR: ['floor_drain', 'pipe', 'plan_handrail', 'elevator_box', 'floor_drain_mix', 'window',
                             'air_conditioner_mix', 'door', 'annotation_line', 'elevator_stair', 'mailbox',
                             'elevator_door'],
        DrawingType.SECOND_THIRD_FLOOR: ['floor_drain', 'pipe', 'plan_handrail', 'elevator_box', 'floor_drain_mix',
                                         'window', 'air_conditioner_mix', 'door', 'annotation_line', 'elevator_stair',
                                         'mailbox', 'elevator_door'],
        DrawingType.WUMIAN: ['floor_drain', 'pipe', 'plan_handrail', 'elevator_box', 'floor_drain_mix', 'window',
                             'door', 'elevator_stair', 'elevator_door'],
        DrawingType.JIFANG: ['floor_drain', 'pipe', 'plan_handrail', 'elevator_box', 'floor_drain_mix', 'window',
                             'door', 'elevator_stair', 'elevator_door'],
        DrawingType.UNDERGROUND: ['floor_drain', 'pipe', 'plan_handrail', 'elevator_box', 'floor_drain_mix', 'window',
                                  'air_conditioner_mix', 'door', 'elevator_stair', 'elevator_door', 'water_pit'],
        DrawingType.UNDERGROUND_BASEMENT: ['floor_drain', 'pipe', 'plan_handrail', 'elevator_box', 'floor_drain_mix',
                                           'window', 'air_conditioner_mix', 'door', 'elevator_stair', 'elevator_door'],
        DrawingType.JIANZHU_HUXING_DAYANG: ['floor_drain', 'pipe', 'plan_handrail', 'elevator_box', 'floor_drain_mix',
                                            'window', 'air_conditioner_mix', 'door', 'elevator_stair', 'elevator_door'],
        DrawingType.BINANCENG: ['floor_drain', 'pipe', 'plan_handrail', 'elevator_box', 'floor_drain_mix', 'window',
                                'door', 'elevator_stair', 'elevator_door'],
        DrawingType.FIRST_FLOOR_SITE_PLAN: ['plan_handrail', 'elevator_box', 'window', 'door', 'elevator_stair',
                                            'elevator_door'],
        DrawingType.STAIR_DAYANG: ['pillar', 'elevator_box', 'window', 'wall', 'stair_dayang_profile_stair', 'door',
                                   'dayang_handrail', 'elevation_window', 'elevator_stair', 'stair_dayang_plan_stair'],
        DrawingType.SITE_PLAN_BUILDING: [],
        DrawingType.WALL_DAYANG: ['window', 'wall', 'door', 'dayang_handrail', 'elevation_window',
                                  'completion_surface'],
        DrawingType.SECTION: ['pillar', 'window', 'wall', 'stair_dayang_profile_stair', 'door', 'dayang_handrail',
                              'elevation_window', 'stair_dayang_plan_stair', 'elevation_mark'],
        DrawingType.ELEVATION: [],
        DrawingType.SIDE_ELEVATION: [],
        DrawingType.INDOOR_FIRST_FLOOR_ACCESS: ['plan_handrail'],
        DrawingType.PAISHUI: ['floor_drain', 'pipe', 'floor_drain_mix'],
        DrawingType.PODAO: ["annotation"],
        DrawingType.DINGCENG: ['air_conditioner'],
    }
