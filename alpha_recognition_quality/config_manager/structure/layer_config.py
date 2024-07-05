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
            "AD[-_]NUMB",
            "尺寸",
            "道",
            "线",
            "增补",
            "VALVE",
            "LINE",
            "IDEN",
            "窗沿",
            "DIM",
            "索引",
            "标注",
        ]
    }

    ENTITY_LAYER_DICT = {
        "border": {
            "layer_sub": [
                "图框",
                "SHET",
                "BORDER",
                "内框",
                "PLOT",
                "PUB[-_]TITLE",
                # "TK",  # 遇到有图框内的表格图层在TK，造成空间分割错误，暂时将TK注释掉
                "BOLDER",
                "^0+$",
                "^4$",
                "PLTW",
                "X[-_]Tlbk",
            ],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "wall": {  # 墙
            "layer_sub": ["wall", "墙", "侧壁", "0[-_]结构", "0[-_]现浇混凝土", "CONC", "WAL", "STRU", "W[-_]LINE",
                          "^C[-_]1$", "C-L"],  # STRU-249183 & 249178
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"线", "LINE"}) +
                           ["COLS", "挡墙", "外墙轮廓", "STRU[-_]MATE", "P[-_]S[-_]CASI[-_]CONC",
                            "集水坑", "HOLE", "^A-WALL-INSL$", "A_SIGN_STRU", "降板线", "P[-_]结构孔洞[-_]穿墙"],
        },  # 经业务确定，对"wall"构件，忽略关键字中删除"线"，1530 - wall-虚线
        "pillar": {  # 柱子
            "layer_sub": ["柱", "COLU", "COLUMN", "COLS", "S[-_]Col", "S[-_]Col[-_]hatch", "S[-_]WC", "CLOS"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] +
                           ["柱帽", "填充", "构造", "尺寸", "详图", "钢筋", "文字", "DIM", "TEXT", "墙", "集中标注", "标注",
                            "边线", "帽"],
        },
        "beam": {  # 梁
            "layer_sub": ["beam$", "梁", "beam[-_][con|dash]", "^[a-zA-Z]-beam-[a-zA-Z]$", "beam"],
            "ignore_word": ["钢筋", "详图", "文字", "TEXT", 'JZBZ', '标注', '编号', '箍筋', '截面', 'KLTH', 'REIN', '附加吊筋'],
        },
        # "slab": {  # 板并不会画实体，而是靠墙和梁围合，所以不存在板的图层
        #     "layer_sub": [".*板.*筋", "REIN", "钢筋"],
        #     "ignore_word": ["文字", "长度", "TEXT", "NOTE", "DIM", "详图"],
        # },
        "wall_hatch": {  # 墙填充
            "layer_sub": ["填充", "HATCH"],
            "ignore_word": []
        },
        "axis_net": {
            "layer_sub": ["建-标注", "建-轴线", "axis", "GRID", "^DIM$", "S-DETL-TEXT", "DOTE", "轴号", "S-轴网-标注", "轴网", "轴线",],
            "ignore_word":[],  #list(set(BASIC_IGNORE_WORDS["basic"]) - {"标注"}),
        },
        "axis_grid": {  # 轴标
            "layer_sub": ["A[-_]AXIS[-_]CRCL.*轴线圈", "AXIS", "0A[-_]A[-_]GRID[-_]NOTE", "ACO[-_]AXIS[-_]NUMB",
                          "AL[-_]DIMS[-_]AXIS.*轴线标注", "AXIS[-_]轴号[-_]A", "A[-_]Grid[-_]Iden", "A[-_]AXIS",
                          "P[-_]BUID[-_]AXIS", "AXIS[-_]轴标", "AXIS[-_]轴号[-_]A", "P[-_]BUID[-_]AXIS",
                          "ACO[-_]AXIS[-_]NUMB", "AXIS[-_]轴标", "A-ANNO-DOTE-AXIS", "P-BUID-AXIS", "A_AXIS_CRCL(轴线圈)",
                          "JZ-坐标", "Z_LCAT_AXIS(定位轴号)", "AG-坐标", "G-AXIS-NUMB", "z-轴号", "HHDZ-DW-AXIS",
                          "DM-坐标", "A-坐标标注", "Z_LCAT_AXIS(定位轴号)", "0-定位-轴号", "G-轴网标注"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]).difference(set(["AXIS"]))),
        },
        "engineering_work_table_line": {  # 用于识别表格线
            "layer_sub": ["HS-A-说明文字", '通用-轴网标注', "ANNO-TABS", "底框", "0-TTLB", "A-BORD", "TK",
                          "AAD-A1$0$AAD-FR-LINE", "图框线", "A-文字-功能", "PUB_TAB", "表"],
            "ignore_word": []
        },
        "other_layers": {
            "layer_sub": [".*"],
            "ignore_word": ["wall", "墙", "侧壁", "0[-_]结构", "0[-_]现浇混凝土", "CONC", "WAL", "STRU", "W[-_]LINE",
                          "^C[-_]1$", "C-L", "柱", "COLU", "COLUMN", "COLS", "S[-_]Col", "S[-_]Col[-_]hatch", "S[-_]WC",
                            "CLOS", "beam$", "梁", "beam_con", "填充", "HATCH", "A[-_]AXIS[-_]CRCL.*轴线圈", "AXIS", "0A[-_]A[-_]GRID[-_]NOTE", "ACO[-_]AXIS[-_]NUMB",
                          "AL[-_]DIMS[-_]AXIS.*轴线标注", "AXIS[-_]轴号[-_]A", "A[-_]Grid[-_]Iden", "A[-_]AXIS",
                          "P[-_]BUID[-_]AXIS", "AXIS[-_]轴标", "AXIS[-_]轴号[-_]A", "P[-_]BUID[-_]AXIS",
                          "ACO[-_]AXIS[-_]NUMB", "AXIS[-_]轴标", "A-ANNO-DOTE-AXIS", "P-BUID-AXIS", "A_AXIS_CRCL(轴线圈)",
                          "JZ-坐标", "Z_LCAT_AXIS(定位轴号)", "AG-坐标", "G-AXIS-NUMB", "z-轴号", "HHDZ-DW-AXIS",
                          "DM-坐标", "A-坐标标注", "Z_LCAT_AXIS(定位轴号)", "0-定位-轴号", "G-轴网标注", "建-标注", "建-轴线", "axis", "GRID"]
        },
        "segment": {  # 住宅平面空间识别图层
            "layer_sub": ["FLOR", "栏杆", "BALCONY", "HANDRAIL", "阳台", "Rail",
                          "HRAL", "blcn", "0425[-_]致逸结构", "surface", "SURFACE",
                          "外包石材", "HEAT", "SILL", "空调板", "OVER", "Hdrl",
                          "0A[-_]P[-_]ROOF", "AE[-_]FNSH", "A[-_]VISI", "HANDRA"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + [
                "SPCL", "OVHD", "FURN", "SPCL", "OVHD", "FURN", "BORD", "FLUE", "FLOR[-_]PLAN", "GRND", "TPTN", "IDEN",
                "LEVL", "SHFT", "SIGH", "WDWK", "PATT", "CASE", "GRID", "FTMT", "STAIR", "MOVE", "家具", "Fixt",
                "A[-_]Flor[-_]Path", "A[-_]FLOR[-_]FURN", "AE[-_]FLOR", "A[-_]FLOR[-_]PARK", "A[-_]FLOR[-_]EVTR",
                "A[-_]FLOR[-_]STR", "DRAN", "P[-_]FLOR", "A-FLOR.*边缘", "A-FLOR-STAR", "FLOR-EVTR", "FLOR-STAIR",
                "S-FLOR_ZM", "A-FLOR-LOOK", "A-FLOR-DRAI", "A-FLOR-SANI", "A[-_]FLOR[-_]AIRC", "集水坑"]
        },  # FLOR-HRAL - 阳台的边界
        "segment_extra": {  # 住宅平面空间分割需要用到但不常用的图层, 若广泛测试后没有问题可以放到segment中
            "layer_sub": ["0S[-_]C[-_]LINE", "0S[-_]CC[-_]LINE", "A[-_]LIN", "^造型线$", "A[-_]HDWR",
                          "AR_LINE"],
            "ignore_word": [],
        },
        "segment_underground": {  # 地下室空间识别
            "layer_sub": ["wall", "pillar", "door", "栏", "HANDRAIL", "Rail", "HRAL",
                          "SYMB", "PD", "坡道", "车流线", "车道中线", "行车方向", "AE[-_]DICH[-_]STRU",
                          "地下室墙柱线", "FLOR", "CON", "TY", "WATER", "排水", "水沟", "水井", 
                          "水坑", "GUTT", "WELL", "GLASS", "Stair", "STAIR", "Hole", "SUMP",
                          "FZ", "水管井", "AE[-_]STAR"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["TEXT", "AXIS", "字", "编号", "标号", "名", "NAME", "AD[-_]NUMB",
                                                          "尺寸", "道", "增补", "VALVE", "IDEN", "窗沿", "家具", "索引",
                                                          "配件", "洞口", "GUTT", "SUMP", "PARK", "0-DOOR\.T"],
        },
        "annotation_line": {  # 引线图层
            "layer_sub": ["DIM", "IDEN", "ANNO", "SYMB", "LEAD", "0[-_]坐标标注", "NO\..*编号", "TEXt", "-TEXT",
                          "F-废水-TEXT", "W-污水-TEXT", "YT-阳台雨-TEXT", "污水文字", "废水文字", "雨水文字", "凝结水文字",
                          "通气文字", "P-负一层消火栓标准", "P[-_]生活污水管线[-_]注释", "A[-_]INDEX",
                          "YCS[-_]通气管[-_]立管标注", "标注$", "编号$", "JZBZ", "梁[-_]截面", "标注引线", "BEAM[-_]KLTH"],
            "ignore_word": ["PUB", "标高", "红线", "流线", "坐标", "尺寸", "中线", "ELEV", "^TWT[-_]SYMB$", "FROM",
                            "FORM", "GRID", "A-COND-IDEN-TEXT", "LEVL", "LEVEL", "P[-_]FS[-_]EQPM[-_]TEXT", "轴网",
                            "A[-_]DIM[-_]AXIS", "P[-_]WS[-_]EQPM.*TEXT", "A[-_]ANNO[-_]NOTE", "A[-_]ANNO[-_]DIMS","TWT_DIM"],
        },
        "elevation_symbol": {  # 标高符号（目前主要使用的是建筑专业中的"标注"图层）
            "layer_sub": ["标高", "ELEV", "LEVL", "TWT[-_]TITLE", "TWT_DIM", "S－GG公共标注", "PUB_DIM", "层高线", "楼层线"],
            "ignore_word": ["^地面标高$"],
        },
        "arrow": {  # 箭头
            "layer_sub": ["DIM", "SYMB", "ANNO", "符号标注", "AD-SIGN", "DIM[-_]SYMB", "A[-_]ANNO[-_]SYMB",
                          "0A[-_]A[-_]SYMB", "A[-_]Anno[-_]Dims", "箭头", "A[-_]Index.*建筑索引线剖切号线", "坡向线",
                          "A[-_]3[-_]Symb", "A[-_]TEXT", "G[-_]ANNO[-_]INDX", "A[-_]ANNO[-_]IDEN", "A[-_]FLOR[-_]STRS",
                          "A_SIGN_ARRO(上下行箭头线)", "A_SYMB_DRCT(坡向线)", "AD-SIGN", "A-INDEX", "A-注释-符号", "^DS$"],
            "ignore_word": ["PUB", "标高", "红线", "流线", "坐标", "尺寸", "中线", "ELEV", "^TWT[-_]SYMB$", "FROM",
                            "FORM", "GRID", "A-COND-IDEN-TEXT", "LEVL", "LEVEL", "P[-_]FS[-_]EQPM[-_]TEXT",
                            "A[-_]DIM[-_]AXIS", "A[-_]ANNO[-_]NOTE", "A[-_]ANNO[-_]DIMS"],
        },
    }
    
    # 分图层打印配置
    INDOOR_DRAWING_PRINT_LAYER_SEPARATE_SET = {
        'set_1': ['vpipe', 'floor_drain', 'system_floor_drain', 'door', 'elevator_door', 'window', 'air_conditioner'],
        'set_2': ['floor_drain_mix', 'furniture', 'fire_hydrant', 'elevator_box', 'rain_outlet'],
        'set_3': ['vpipe', 'life_supply_vpipe', 'sewage_vpipe', 'waste_vpipe', 'rain_vpipe', 'sprinkler_vpipe',
                  'hydrant_vpipe', 'condensate_vpipe', 'floor_drain', 'ventilate_vpipe', 'fire_hydrant',
                  'kitchen_toilet', 'furniture', 'elevator_box', 'elevator_stair', 'air_conditioner'],
        'set_4': ['window', 'elevator_door', 'door', 'emergency_door', 'wall', 'pillar', 'elevation_window'],
    }
    CLASSIFICATION_EXCLUDE_LAYERS = [
        "wall", "pillar", "special_pillar", "segment", "podao", "podao_extra", "separator", "filling",
        "pillar_line", "road", "car_lane", "red_line", "red_line_sub", "building", "elevation_handrail",
        "mentou", "underground_building", "wall_hatch", "podao_mark", "structure", "elevation_window_exclude",
        "hatch", "podao_edge", "pipe_barrier", "hatch_outline", "wall_line", "text_with_bound_vertex",
        "annotation_line", "lobby_platform_border", "segment_underground", "segment_extra", "overflow_level",
        "text", "cold_life_supply_hpipe", "hot_life_supply_hpipe", "hydrant_hpipe", "sprinkler_hpipe",
        "inflow_hpipe", "sewage_hpipe", "waste_hpipe", "rain_hpipe", "condensate_hpipe", "ventilate_hpipe",
        "parking_contour_dict", "road_center_line", "rain_recycle_supply_hpipe", "solid_wall_line",
        "non_solid_wall_line", "mleader", "waste_hpipe_short", "hydrant_hpipe_short", "sprinkler_hpipe_short",
        "cold_life_supply_hpipe_short", "sprinkler_hpipe_short", "wall_floor_line"
    ]

    # 不会用函数get_hyper_layer进行匹配的图层
    MATCH_EXCLUDE_LAYERS = ["podao_extra", "podao_mark", "podao_edge", "pipe_barrier"]

    # 存在斜线的图层，（需要对像素坐标进行特殊处理，确保能真实反映图纸上的线段走势） add by yanct01 2020-5-16
    # 处理结果，保存到一个新的逻辑层 ： 原图层名 + '_line'
    LAYERS_WITH_SLOPE_LINE_SUFFIX = '_line'
    LAYERS_WITH_SLOPE_LINE = ['wall', 'pillar', 'red_line', 'red_line_sub', 'beam', 'annotation_line']
    LAYERS_WITH_SLOPE_LINE_REVISED = [x + '_line' for x in LAYERS_WITH_SLOPE_LINE]
    # 对于线型是虚线的墙线，单独保存
    DASH_LINE_SUFFIX = '_dash'
    DASH_LINE_REVISED = [x + '_dash' for x in LAYERS_WITH_SLOPE_LINE_REVISED]

