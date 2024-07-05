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

        "air_conditioner": {  # 空调s
            "layer_sub": ["空调", "^空_$", "Aircontroe", "^AC$", "Aircondition", "EQPM[-_]MECH", "EQPM[-_]SMAL",
                          "M[-_]AC", "KT", "FLOR[-_]OVHD", "LA[-_]plan[-_]smal", "RS[-_]A", "^A[-_]AC$",
                          "A[-_]FLOR[-_]AIRC",
                          "室内机", "机组", "DOOR_FIRE", "DM-尺寸标注", "SWJ", "DM-空调-设备",
                          "BGJ", "GJ", "SNJ", "DM-供暖", "ACS"
                          "室外机", "多联机",
                        ], #  "ACS_COM_BZ", "标注",
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["洞", "孔", "水", "空调管", "标注$", "LN", "管", 'DM-供暖-设备'],
        },
        "door": {  # 门
            "layer_sub": ["WINDOW", "DOOR", "门", "D&W", "W&D", "WIN", "DOWI"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立面门窗", "人防", "0-DOOR\.T", "WINDOW[-_]BLIN", "开启范围", "阀门"],
        },
        "window": {  # 窗户
            "layer_sub": ["WINDOW", "WIN", "窗", "DRWD", "WIND", "Window", "D&W", "W&D", "L[-_]玻璃", "DOWI", "dowi",
                          "0A[-_]B[-_]GLAZ", "百叶", "CHUANG"],  # 0A-B-GLAZ-255679
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立面门窗", "WINDOW[-_]BLIN", "0A[-_]B[-_]GLAZ[-_]OPEN", "窗帘", "人防"],
        },  # GLAZ-255679
        "wall": {  # 墙
            "layer_sub": ["wall", "墙", "侧壁", "0[-_]结构", "0[-_]现浇混凝土", "CONC", "WAL", "STRU", "W[-_]LINE",
                          "^C[-_]1$", "C-L"],  # STRU-249183 & 249178
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"线", "LINE"}) +
                           ["COLS", "墙柱", "挡墙", "外墙轮廓", "STRU[-_]MATE", "P[-_]S[-_]CASI[-_]CONC",
                            "集水坑", "HOLE", "^A-WALL-INSL$", "A_SIGN_STRU", "降板线", "P[-_]结构孔洞[-_]穿墙"],
        },  # 经业务确定，对"wall"构件，忽略关键字中删除"线"，1530 - wall-虚线
        "pillar": {  # 柱子
            "layer_sub": ["柱", "COLU", "COLUMN", "COLS", "S[-_]Col", "S[-_]Col[-_]hatch", "S[-_]WC", "CLOS"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["柱帽", "填充"],
        },
        "wall_hatch": {
            "layer_sub": ["填充", "HATCH"],
            "ignore_word": []
        },
        "segment": {  # 住宅平面空间识别图层
            "layer_sub": ["FLOR", "栏杆", "BALCONY", "HANDRAIL", "阳台", "Rail",
                          "HRAL", "blcn", "0425[-_]致逸结构", "surface", "SURFACE",
                          "外包石材", "HEAT", "SILL", "空调板", "OVER", "Hdrl",
                          "0A[-_]P[-_]ROOF", "AE[-_]FNSH", "A[-_]VISI", "HANDRA", "饰线"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) -set("线")) + [
                "SPCL", "OVHD", "FURN", "SPCL", "OVHD", "FURN", "BORD", "FLUE", "FLOR[-_]PLAN", "GRND", "TPTN", "IDEN",
                "LEVL", "SHFT", "SIGH", "WDWK", "PATT", "CASE", "GRID", "FTMT", "STAIR", "MOVE", "家具", "Fixt",
                "A[-_]Flor[-_]Path", "A[-_]FLOR[-_]FURN", "AE[-_]FLOR", "A[-_]FLOR[-_]PARK", "A[-_]FLOR[-_]EVTR",
                "A[-_]FLOR[-_]STR", "DRAN", "P[-_]FLOR", "A-FLOR.*边缘", "A-FLOR-STAR", "FLOR-EVTR", "FLOR-STAIR",
                "S-FLOR_ZM", "A-FLOR-LOOK", "A-FLOR-DRAI", "A-FLOR-SANI", "A[-_]FLOR[-_]AIRC", "集水坑",
                "M-HEAT-(RT|SP)WT"]
        },  # FLOR-HRAL - 阳台的边界
        "segment_extra": {  # 住宅平面空间分割需要用到但不常用的图层, 若广泛测试后没有问题可以放到segment中
            "layer_sub": ["0S[-_]C[-_]LINE", "0S[-_]CC[-_]LINE", "A[-_]LIN", "^造型线$", "A[-_]HDWR",
                          "AR_LINE"],
            "ignore_word": [],
        },
        "axis_net": {
            "layer_sub": ["建-标注", "建-轴线", "axis"],
            "ignore_word": [],
        },
        "annotation_line": {  # 引线图层
            "layer_sub": ["DIM", "ANNO", "SYMB", "LEAD", "0[-_]坐标标注", "NO\..*编号", "TEXt", "-TEXT",
                          "F-废水-TEXT", "W-污水-TEXT", "YT-阳台雨-TEXT", "污水文字", "废水文字", "雨水文字", "凝结水文字",
                          "通气文字", "P-负一层消火栓标准", "P[-_]生活污水管线[-_]注释", "A[-_]INDEX",
                          "YCS[-_]通气管[-_]立管标注", "标注$", "编号$",
                          "ACS_PFG_BZ", "ACS_COM_BZ", "ACS_COM", "BZ", "暖通文字", "G-TABL", 'DM-供暖-标注'],  # "IDEN",
            "ignore_word": ["PUB", "标高", "红线", "流线", "坐标", "尺寸", "中线", "ELEV", "^TWT[-_]SYMB$", "FROM",
                            "FORM", "GRID", "A-COND-IDEN-TEXT", "LEVL", "LEVEL", "P[-_]FS[-_]EQPM[-_]TEXT",
                            "A[-_]DIM[-_]AXIS", "P[-_]WS[-_]EQPM.*TEXT", "A[-_]ANNO[-_]NOTE", "A[-_]ANNO[-_]DIMS",
                            "TWT_DIM", "CK-PCAP-DIMS"],
        },
        "engineering_work_table_line": {
            "layer_sub": ["HS-A-说明文字", '通用-轴网标注', "ANNO-TABS", "底框", "0-TTLB", "A-BORD", "TK",
                          "AAD-A1$0$AAD-FR-LINE", "图框线", "A-文字-功能", "PUB_TAB", "表"],
            "ignore_word": []
        },
        "fen_ji_shui_qi": {  # 分集水器
            "layer_sub": ["EQ-采暖分集水器", "M-HT-EQPM", "(采|供)暖-设备", "水暖设备", "DM-供暖-设备", "M-供暖-设备",
                          "H-Heat-Dev", "供暖-分集水器", ],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "temp_controller": {  # 地暖温度控制器
            "layer_sub": ["供暖-设备", "H-Heat-Dev", "DM-供暖-标注", "M-供暖-标注", "M-供暖-电动阀门", "M-供暖-设备",
                          "DM-供暖-设备"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"标注"}),
        },
    }

    BASIC_LAYERS = {
        "basic": ["wall", "border"],
        "indoor_segment": ["wall", "pillar", "segment", "segment_extra"],  # 去掉了 border
        # "indoor_first_floor_segment": ["wall", "pillar", "segment", "segment_extra", "segment_lobby_platform", "border"],
        "underground_segment": ["wall", "pillar", "segment"],  # 去掉了 border
        "building_segment": ["building", "door", "window"],
        # "second_third_segment": ["wall", "door", "window", "pillar", "segment", "border", "second_third_space"],
        # "indoor_access_segment": ["wall", "pillar", "segment", "border", "indoor_access"],
    }

    # 对于风管，可以合并，但不做分类，在后处理根据图层识别为空间
    # "bu_feng_guan", "pai_yan_jian_pai_feng_guan", "pai_feng_guan", "xin_feng_guan", "song_bu_feng_guan", "jia_ya_feng_guan",

    COMBINATION_EXCLUDE_LAYERS_INDOOR = [
        "wall", "segment", "pillar", "mentou", "wall_hatch", "hatch", "second_third_space", "pipe_barrier",
        "hatch_outline", "text_with_bound_vertex", "annotation_line", "lobby_platform_border", "segment_underground",
        "segment_extra", "text",
        "solid_wall_line", "non_solid_wall_line", "mleader",
        "wall_floor_line",
          "kong_tiao_shui_guan", "di_nuan_pan_guan", "feng_guan_fa_lan",
    ]  # hatch_outline-规则62，pillar_line 在LAYERS_WITH_SLOPE_LINE_REVISED中有

    COMBINATION_EXCLUDE_LAYERS_UNDERGROUND_AND_SITEPLAN = [
        "wall", "podao", "separator", "filling", "road", "car_lane", "hatch", "red_line", "red_line_sub",
        "building", "underground_building", "podao_extra", "podao_mark", "podao_edge", "overflow_level", "text",
        "hatch_outline", "text_with_bound_vertex", "annotation_line", "segment_underground",
        "segment", "segment_extra", "solid_wall_line", "non_solid_wall_line", "mleader",
        "kong_tiao_shui_guan", "di_nuan_pan_guan", "feng_guan_fa_lan",
    ]

    CLASSIFICATION_EXCLUDE_LAYERS = [
        "wall", "pillar", "special_pillar", "segment", "podao", "podao_extra", "separator", "filling",
        "pillar_line", "road", "car_lane", "red_line", "red_line_sub", "building", "elevation_handrail",
        "mentou", "underground_building", "wall_hatch", "podao_mark", "structure", "elevation_window_exclude",
        "hatch", "podao_edge", "pipe_barrier", "hatch_outline", "wall_line", "text_with_bound_vertex",
        "annotation_line", "lobby_platform_border", "segment_underground", "segment_extra",
        "text", "parking_contour_dict", "road_center_line", "solid_wall_line",
        "non_solid_wall_line", "mleader", "wall_floor_line",
        "pai_yan_jian_pai_feng_guan", "song_bu_feng_guan", "pai_feng_guan",
        "bu_feng_guan", "jia_ya_feng_guan", "kong_tiao_shui_guan", "di_nuan_pan_guan", "feng_guan_fa_lan", "xin_feng_guan"
    ]
    
    # 分图层打印配置
    INDOOR_DRAWING_PRINT_LAYER_SEPARATE_SET = {
        'set_1': ['door'],
        'set_2': ['window'],
        'set_3': ["air_conditioner"],
        'set_4': ["fen_ji_shui_qi", "temp_controller"],
    }

    # 不会用函数get_hyper_layer进行匹配的图层
    MATCH_EXCLUDE_LAYERS = ["podao_extra", "podao_mark", "podao_edge", "pipe_barrier"]

    # 存在斜线的图层，（需要对像素坐标进行特殊处理，确保能真实反映图纸上的线段走势） add by yanct01 2020-5-16
    # 处理结果，保存到一个新的逻辑层 ： 原图层名 + '_line'
    LAYERS_WITH_SLOPE_LINE_SUFFIX = '_line'
    LAYERS_WITH_SLOPE_LINE = ['wall', 'pillar', 'red_line', 'red_line_sub']
    LAYERS_WITH_SLOPE_LINE_REVISED = [x + '_line' for x in LAYERS_WITH_SLOPE_LINE]
    # 对于线型是虚线的墙线，单独保存
    DASH_LINE_SUFFIX = '_dash'
    DASH_LINE_REVISED = [x + '_dash' for x in LAYERS_WITH_SLOPE_LINE_REVISED]

    # "暖通构件" 与 "图层" 的对应关系
    HVAC_ENTITY_LAYER_MAP = {
        "150°防火阀": ["fang_huo_fa_150"],
        "280°排烟防火阀": ["pai_yan_fang_huo_fa_280"],
        "70°防火阀": ["fang_huo_fa_70"],
        "CO探测器": ["co_tan_ce_qi"],
        "下送风口": ["xia_song_feng_kou"],
        "侧墙补风口": ["ce_qiang_bu_feng_kou"],
        "侧送加压风口": ["ce_song_jia_ya_feng_kou"],
        "侧送排烟兼排风口": ["ce_song_pai_yan_jian_pai_feng_kou"],
        "全热交换器": ["quan_re_jiao_huan_qi"],
        "内衬金属风管": ["nei_chen_jin_shu_feng_guan"],
        "分体空调": ["fen_ti_kong_tiao"],
        "分集水器": ["fen_ji_shui_qi"],
        "加压风机": ["jia_ya_feng_ji"],
        "压差传感器": ["ya_cha_chuan_gan_qi"],
        "壁式轴流风机": ['bi_shi_zhou_liu_feng_ji'],
        "多叶风口": ["duo_ye_feng_kou"],
        "战时排风机": ["zhan_shi_pai_feng_ji"],
        "战时送风机": ["zhan_shi_song_feng_ji"],
        "手动开启装置": ["shou_dong_kai_qi_zhuang_zhi"],
        "排烟兼排风机": ["pai_yan_jian_pai_feng_ji"],
        "排烟风机": ["pai_yan_feng_ji"],
        "排风机": ["pai_feng_ji"],
        "新风机": ["xin_feng_ji"],
        "止回阀": ["zhi_hui_fa"],
        "毛巾暖气架": ["mao_jin_nuan_qi_jia"],
        "水管套管": ["shui_guan_tao_guan"],
        "泄压阀": ["xie_ya_fa"],
        "消声器": ["xiao_sheng_qi"],
        "燃气壁挂炉": ["ran_qi_bi_hua_lu"],
        "电动风阀": ["dian_dong_feng_fa"],
        "空调回风口": ["kong_tiao_hui_feng_kou"],
        "诱导风机": ["you_dao_feng_ji"],
        "送补风机": ["song_bu_feng_ji"],
        "风机盘管": ["feng_ji_pan_guan"],
        "风管上下翻": "feng_guan_shang_xia_fan",
    }
