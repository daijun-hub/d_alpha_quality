# -*- coding: utf-8 -*-

from enum import Enum


class LayerConfig(Enum):
    BASIC_IGNORE_WORDS = {
        "basic": [
            "TEXT",
            "DIMS",
            "AXIS",
            "字",
            "编号",
            "标号",
            "名",
            "NAME",
            "AD-NUMB",
            "尺寸",
            "道",
            "线",
            "增补",
            "VALVE",
            "LINE",
            "IDEN",
            "窗沿",
            # "DIM",
            "索引",
            "标注",
        ]
    }

    # 根据业务逻辑保存构件对应推荐图层应包含的字段
    ENTITY_LAYER_DICT = {
        "border": {
            "layer_sub": [
                "图框",
                "SHET",
                "BORDER",
                "内框",
                "PLOT",
                "PUB_TITLE",
                # "TK",  # 遇到有图框内的表格图层在TK，造成空间分割错误，暂时将TK注释掉
                "BOLDER",
                "^0+$",
                "^4$",
                "PLTW",
                "X-Tlbk",
            ],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },

        # "window": {  # 窗户
        #     "layer_sub": ["WINDOW", "WIN", "窗", "DRWD", "WIND", "Window", "D&W", "W&D", "L-玻璃", "DOWI", "dowi",
        #                   "GLAZ", "百叶", "CHUANG"],
        #     "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立面门窗", "WINDOW[-_]BLIN", "0A[-_]B[-_]GLAZ[-_]OPEN",
        #                                                   "开启", "A[-_]EQPM[-_]WIND"],
        # },  # GLAZ-255679
    }

    BASIC_LAYERS = {
        "basic": ["wall", "axis_net"],  # 去掉了 border
        # "indoor_segment": ["wall", "pillar", "segment", "segment_extra", "elevation_handrail", "dayang_handrail",
        #                    "plan_handrail"],  # 去掉了 border
        # # 暂时删除 "indoor_first_floor_segment"，因为经过评估，"segment_lobby_platform" 不适合作为空间图层，可以直接在规则中使用
        # # "indoor_first_floor_segment": ["wall", "pillar", "segment", "segment_extra", "segment_lobby_platform", "border"],
        # "underground_segment": ["wall", "pillar", "segment", "segment_extra", "elevation_handrail", "dayang_handrail",
        #                         "plan_handrail"],  # 去掉了 border
        # "building_segment": ["building", "door", "window"],
        # "second_third_segment": ["wall", "pillar", "segment", "segment_extra", "second_third_space",
        #                          "elevation_handrail", "dayang_handrail", "plan_handrail"],  # 去掉了 border
        # "indoor_access_segment": ["wall", "pillar", "segment", "segment_extra", "indoor_access", "elevation_handrail",
        #                           "dayang_handrail", "plan_handrail"],  # 去掉了 border
        # "stair_dayang": ["wall", "pillar", "annotation", "stair_dayang_plan_stair", "stair_dayang_profile_stair",
        #                  "elevation_handrail", "plan_handrail"],  # 去掉了 border
        # "elevation_shelter": ["decoration"],
    }

    COMBINATION_EXCLUDE_LAYERS_INDOOR = [
        "wall", "segment", "pillar", "mentou", "wall_hatch", "hatch", "second_third_space", "pipe_barrier",
        "hatch_outline", "annotation_line", "text_with_bound_vertex", "text", "lobby_platform_border", "segment_extra",
        "podao_edge", "decoration", "solid_wall_line", "non_solid_wall_line", "mleader", "elevation_window_open_line",
        "annotation", "axis_grid"
    ]

    COMBINATION_EXCLUDE_LAYERS_UNDERGROUND_AND_SITEPLAN = [
        "wall", "podao", "separator", "filling", "road", "car_lane", "hatch", "red_line", "red_line_sub",
        "building", "underground_building", "podao_extra", "podao_mark", "podao_edge", "hatch_outline",
        "annotation_line", "text_with_bound_vertex", "text", "segment", "segment_extra",
        "road_center_line", "decoration", "solid_wall_line", "non_solid_wall_line", "mleader", "fire_road",
        "garage_podao_exit", "annotation", "axis_grid", "wall_hatch"
    ]  # 总图的"elevation_mark"暂时走合并

    CLASSIFICATION_EXCLUDE_LAYERS = [
        "wall", "pillar", "special_pillar", "segment", "podao", "podao_extra", "separator", "filling", "pillar_line",
        "road", "car_lane", "red_line", "red_line_sub", "building", "elevation_handrail", "mentou",
        "underground_building", "wall_hatch", "podao_mark", "structure", "elevation_window_exclude",
        "hatch", "podao_edge", "pipe_barrier", "hatch_outline", "wall_line", "annotation_line",
        "text_with_bound_vertex",
        "arrow", "text", "lobby_platform_border", "second_third_space", "segment_extra", "parking_contour_dict",
        "dayang_handrail", "stair_dayang_profile_stair", "road_center_line", "plan_handrail", "decoration",
        "solid_wall_line", "non_solid_wall_line", "mleader", "fire_road", "garage_podao_exit",
        "elevation_window_open_line", "annotation", "axis_grid"
    ]

    # 分图层打印配置
    INDOOR_DRAWING_PRINT_LAYER_SEPARATE_SET = {
        # 'set_1': ['pipe', 'floor_drain', 'door', 'elevator_door', 'window', 'air_conditioner', "water_pit"],
        # 'set_2': ['floor_drain_mix', 'air_conditioner_mix', 'fire_hydrant', 'elevator_box', "parking"],
        # 'set_3': ['floor_drain_mix', 'air_conditioner_mix', 'fire_hydrant', 'elevator_box', 'pipe', 'floor_drain',
        #           'air_conditioner', 'elevator_stair', 'washbasin', 'closestool', 'diamond_bath'],
        # 'set_4': ['window', 'elevator_door', 'door', 'emergency_door', 'wall', 'pillar', 'elevation_window'],
    }

    # 不会用函数get_hyper_layer进行匹配的图层
    MATCH_EXCLUDE_LAYERS = [] # "podao_extra", "podao_mark", "podao_edge", "pipe_barrier"

    # 存在斜线的图层，（需要对像素坐标进行特殊处理，确保能真实反映图纸上的线段走势） add by yanct01 2020-5-16
    # 处理结果，保存到一个新的逻辑层 ： 原图层名 + '_line'
    LAYERS_WITH_SLOPE_LINE_SUFFIX = '_line'
    LAYERS_WITH_SLOPE_LINE = ['wall', 'pillar', 'red_line', 'red_line_sub']
    LAYERS_WITH_SLOPE_LINE_REVISED = [x + '_line' for x in LAYERS_WITH_SLOPE_LINE]
    # 对于线型是虚线的墙线，单独保存
    DASH_LINE_SUFFIX = '_dash'
    DASH_LINE_REVISED = [x + '_dash' for x in LAYERS_WITH_SLOPE_LINE_REVISED]
