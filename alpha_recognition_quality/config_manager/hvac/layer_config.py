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

        "elevator_box": {  # 电梯厢/楼梯
            "layer_sub": ["EVTR", "Stair", "STAIR", "Lift", "LIFT", "电梯", "楼梯", "梯", "FIT", "ELEV", "elevator", "STRS",
                          "EQPM", "STAR", "轿厢", "STR$", "^A_equipment$"],  # STR-电梯厢256817
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"LINE"}) + ["SMAL", "BALC", "ELEC", "LIHT", "CLNG",
                                                                                "FIRE", "HYDR", "KICH", "ASSI",
                                                                                "MECH", "PLOM", "TOLT", "PRKG",
                                                                                "SYMB", "RAIL", "CAR", "车"],
        },
        "elevator_stair": {  # 电梯厢/楼梯（住宅平面图）
            "layer_sub": ['EVTR', 'Stair', 'STAIR', 'Lift', 'LIFT', '电梯', '楼梯', '梯', 'FIT', 'ELEV', 'elevator', 'STRS',
                          'EQPM', 'STAR'],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"LINE"}) + ['SMAL', 'BALC', 'ELEC', 'LIHT', 'CLNG',
                                                                                'FIRE', 'HYDR', 'KICH', 'ASSI',
                                                                                'MECH', 'PLOM', 'TOLT', 'PRKG',
                                                                                'SYMB', "RAIL", "CAR", "车"],
        },
        # "air_conditioner": {  # 空调s
        #     "layer_sub": ["空调", "^空_$", "Aircontroe", "^AC$", "Aircondition", "EQPM[-_]MECH", "EQPM[-_]SMAL",
        #                   "M[-_]AC", "KT", "FLOR[-_]OVHD", "LA[-_]plan[-_]smal", "RS[-_]A", "^A[-_]AC$",
        #                   "A[-_]FLOR[-_]AIRC"],
        #     "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["洞", "孔", "水", "空调管", "标注$"],
        # },
        # "air_conditioner_mix": {  # 家具图层，含有空调的混合图层
        #     "layer_sub": ["家具", "FURN", "Furniture", "furn", "EQPM[-_]MOVE", "EQPM[-_]FIXD", "Fixt"],
        #     "ignore_word": list(set(BASIC_IGNORE_WORDS['basic']) - {'家具'}),
        # },
        "door": {  # 门
            "layer_sub": ["WINDOW", "DOOR", "门", "D&W", "W&D", "WIN", "DOWI"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立面门窗", "人防", "0-DOOR\.T", "WINDOW[-_]BLIN", "开启范围", "阀门"],
        },
        "window": {  # 窗户
            "layer_sub": ["WINDOW", "WIN", "窗", "DRWD", "WIND", "Window", "D&W", "W&D", "L[-_]玻璃", "DOWI", "dowi",
                          "0A[-_]B[-_]GLAZ", "百叶", "CHUANG"],  # 0A-B-GLAZ-255679
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立面门窗", "WINDOW[-_]BLIN", "0A[-_]B[-_]GLAZ[-_]OPEN", "窗帘", "人防"],
        },  # GLAZ-255679
        "elevator_door": {  # 电梯门
            "layer_sub": ["WINDOW", "WIN", "DOOR", "门", "DRWD"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立面门窗", "0-DOOR\.T", "WINDOW[-_]BLIN", "人防", "开启范围"],
        },
        "emergency_door": {  # 人防
            "layer_sub": ["WINDOW", "WIN", "door", "门", "人防"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] +
                           ["分区", "0-DOOR\.T", "WINDOW[-_]BLIN", "开启范围", "人防集水坑"],
        },  # 过滤人防分区
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
                          "0A[-_]P[-_]ROOF", "AE[-_]FNSH", "A[-_]VISI", "HANDRA"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + [
                "SPCL", "OVHD", "FURN", "SPCL", "OVHD", "FURN", "BORD", "FLUE", "FLOR[-_]PLAN", "GRND", "TPTN", "IDEN",
                "LEVL", "SHFT", "SIGH", "WDWK", "PATT", "CASE", "GRID", "FTMT", "STAIR", "MOVE", "家具", "Fixt",
                "A[-_]Flor[-_]Path", "A[-_]FLOR[-_]FURN", "AE[-_]FLOR", "A[-_]FLOR[-_]PARK", "A[-_]FLOR[-_]EVTR",
                "A[-_]FLOR[-_]STR", "DRAN", "P[-_]FLOR", "A-FLOR.*边缘", "A-FLOR-STAR", "FLOR-EVTR", "FLOR-STAIR",
                "S-FLOR_ZM", "A-FLOR-LOOK", "A-FLOR-DRAI", "A-FLOR-SANI", "A[-_]FLOR[-_]AIRC", "集水坑", "M-HEAT-(RT|SP)WT"]
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
        "lobby_platform_border": {  # 规则523、535中用到的大堂外的 "入口平台" 区域
            "layer_sub": ["^fit$", "A-P-FLOR"],
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
                          "ACS_PFG_BZ", "ACS_COM_BZ", "ACS_COM", "BZ", "暖通文字", "G-TABL"], #"IDEN",
            "ignore_word": ["PUB", "标高", "红线", "流线", "坐标", "尺寸", "中线", "ELEV", "^TWT[-_]SYMB$", "FROM",
                            "FORM", "GRID", "A-COND-IDEN-TEXT", "LEVL", "LEVEL", "P[-_]FS[-_]EQPM[-_]TEXT",
                            "A[-_]DIM[-_]AXIS", "P[-_]WS[-_]EQPM.*TEXT", "A[-_]ANNO[-_]NOTE", "A[-_]ANNO[-_]DIMS","TWT_DIM", "CK-PCAP-DIMS"],
        },
        "elevation_symbol": {  # 标高符号（目前主要使用的是建筑专业中的"标注"图层）
            "layer_sub": ["标高", "ELEV", "LEVL", "TWT[-_]TITLE", "TWT_DIM", "S－GG公共标注", "PUB_DIM", "层高线", "楼层线"],
            "ignore_word": ["^地面标高$"],
        },
        "parking": {  # 车位
            "layer_sub": ["PARK", "park", "车位", "Car", "CAR", "车", "car",
                          "AE-EQPM", "PRKG", "快充", "慢充", "无障碍", "泊位",
                          "pkng", "che", "A-Pkng-Vhel-Mini", "A-1-Pkng"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["轮廓", "DRIV", "CURB", "自行车", "绿地"],
        },
        "underground_building": {
            "layer_sub": ["JZW_地下车库轮廓线", "2-地下车库"],
            "ignore_word": []
        },
        "arrow": {  # 箭头
            "layer_sub": ["DIM", "SYMB", "ANNO", "符号标注", "AD-SIGN", "DIM[-_]SYMB", "A[-_]ANNO[-_]SYMB",
                          "0A[-_]A[-_]SYMB", "A[-_]Anno[-_]Dims", "箭头", "A[-_]Index.*建筑索引线剖切号线", "坡向线",
                          "A[-_]3[-_]Symb", "A[-_]TEXT", "G[-_]ANNO[-_]INDX", "A[-_]ANNO[-_]IDEN", "A[-_]FLOR[-_]STRS",
                          "A_SIGN_ARRO(上下行箭头线)", "A_SYMB_DRCT(坡向线)", "AD-SIGN", "A-INDEX", "A-注释-符号"],
            "ignore_word": ["PUB", "标高", "红线", "流线", "坐标", "尺寸", "中线", "ELEV", "^TWT[-_]SYMB$", "FROM",
                            "FORM", "GRID", "A-COND-IDEN-TEXT", "LEVL", "LEVEL", "P[-_]FS[-_]EQPM[-_]TEXT",
                            "A[-_]DIM[-_]AXIS", "A[-_]ANNO[-_]NOTE", "A[-_]ANNO[-_]DIMS"],
        },
        "kitchen_toilet": {  # 厨卫
            "layer_sub": ["厨卫", "LVTRY", "洁具", "FLOR[-_]SPCL", "FIXT", "SANR", "EQPM[-_]ASSI", "EQPM[-_]TOLT",
                          "Lavatory", "EQPM[-_]KICH", "^A[-_]SAN$", "标配部件[-_]厨房卫生", "EQPM[-_]TACC", "TPTN"],  # TPTN是洗浴器
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        # 阀门
        "fang_huo_fa_70": {  # 70°防火阀F
            "layer_sub": [ "DUCT-(加压)?(排|送|新|回)风阀门", "DUCT-(排风)?排烟阀门", "ACS_(P|S|F|R|J)(F|B)G_FM_F",  "H-BOST-VALV-F", "H-SUPA-VALV-F",
                          "TY-消防阀门", "N-消防-阀门", "VALV", "M.*SMOK.*DSDT", "M.*BOST.*DWDT", "M.*BOST.*DRSY", "M.*SMOK.*DRSY", "M.*FRES.*DSDT",
                          ], # "H-风管-阀门配件", "DUCT-送风管", "ACS_PFG_F2",
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["M-HEAT-VALV", "EXHS", "SUPA"],
        },
        "fang_huo_fa_150": {  # 150°防火阀
            "layer_sub": ["DUCT-排烟阀门",  "M.*EXHS.*D[SR][DS]Y", "M.*EXHS.*VALV"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "pai_yan_fang_huo_fa_280": {  # 280°排烟防火阀
            "layer_sub": ["ACS_FFG_FM", "ACS_(S|Y)FG_FM_F", "DUCT-加压送风阀门", "DUCT-排烟阀门", "DUCT-排风阀门", "设备",
                          "DUCT-回风阀门", "H-DUCT(排烟阀门)", "DUCT-排风排烟阀门", "DUCT-排烟管", "H-EXHS-VALV-F", "M.*SUPA.*VALV", "M.*SUPA.*DSDT",
                          "H-SMOK-VALV-X"], # "H-风管-阀门配件",
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "dian_dong_feng_fa": {  # 电动风阀
            "layer_sub": ["ACS_PFG_FM_E",  "DUCT-加压送风阀门", "DUCT-加压送风电动阀门", "DUCT-送风阀门", "DUCT-排风阀门", "DUCT-新风阀门", "DUCT-排烟阀门"
                          "M-通风-阀门",
                          ], #"ACS_PFG_FL",
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "xie_ya_fa": {  # 泄压阀
            "layer_sub": ["H-BOST-VALV-E", "ACS_JFG_FM_E", "ACS_YFG_FM", "DUCT-加压送风阀门", "M-通风-阀门", "N-消防-阀门", "DUCT-加压送风电动阀门", "DUCT-送风电动阀门"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "zhi_hui_fa": {  # 止回阀
            "layer_sub": ["DUCT-排烟阀门", "DUCT-加压送风阀门", "DUCT-送风阀门", "_M-DUCT-加压送风阀门", "H-EXHS-VALV", "ACS_JFG_FM", "_M-DUCT-排风阀门"
                          "H-TL(图例)",   "DUCT-排风排烟阀门", "M-餐饮-风管阀门", "H-SUPA-VALV", "H-BOST-VALV", "H-SMOK-VALV"
                          ], #"ACS_PFG_FL", "ACS_PFG_FM", "H-风管-阀门配件",
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },

        # 风口
        "ce_qiang_bu_feng_kou": { # 侧墙补风口
            "layer_sub": ["DUCT-送风风口"], #"ACS_SFG_FK",
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "ce_song_jia_ya_feng_kou": {  # 侧送加压风口
            "layer_sub": ["TYN3-消防-风口", "TYN2-空调-风口", "TY-消防风口", "TY-空调送风风口", "DUCT-加压送风风口", "ACS_JFG_FM_F",
                          "ACS_PFG_FM_F", "ACS_JFG_FM_F", "ACS_SFG_FK", "H-SUPA-PORT", "ACS-留洞", "DUCT-送风风口", "DUCT-回风风口", "通风风口"], # "ACS_PFG_F2", "通风", "DUCT-送风管",
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "ce_song_pai_yan_jian_pai_feng_kou": {  # 侧送排烟兼排风口
            "layer_sub": ["DUCT-排风风口", "H-EXHS-PORT", "ACS_YFG_FK", "ACS_PFG_FK", "_M-DUCT-排风风口", ""
                          "(DUCT-)?排风排烟风口", "DUCT-送风风口", "暖通-通风设备", "H-SUPA-PORT"
                          ], # , "ACS_SFG_FK", "H-风管-排烟管", "DUCT-回风风口"
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "xia_song_feng_kou": {  # 下送风口
            "layer_sub": ["ACS_JFG_FK", "ACS_YFG_FK", "ACS_PFG_FK", "H-EXHS-PORT", "DUCT-排风风口", "H-SUPA-PORT", "_M-DUCT-排风风口", "DUCT-.*送风风口",
                          "DUCT-加压送风风口", "DUCT-排烟风口", "H-TL(图例)", "DUCT-回风风口", "DUCT-排风排烟风口", "出、回风口", "ACS_YFG_F2", "M-DUST-PORT"
                          ], # "ACS_SFG_FK",
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "duo_ye_feng_kou": {  # 多叶风口
            "layer_sub": ["DUCT-排烟风口", "DUCT-回风风口", "DUCT-排风风口", "DUCT-加压送风风口", "H-TL(图例)", "DUCT-新风风口"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "kong_tiao_hui_feng_kou": {  # 空调回风口
            "layer_sub": ["ACS_HFG_FK", "DUCT-送风阀门", "2-出( |、)?回风口"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },

        # 风机
        "jia_ya_feng_ji": {  # 加压风机
            "layer_sub": ["H-OTHR-FLDS", "ACS_KT_SB", "M-TF-SB", "DUCT-加压送风管设备", "TY-消防管设备", "DUCT-送风管设备", "DUCT-排风管设备"
                          "_M-DUCT-加压送风管设备", "M-通风-风机", "TYN3-消防-设备", "N-消防-设备", "H-设备-风机", "M-BOST-EQPM"], #
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "pai_feng_ji": {  # 排风机
            "layer_sub": ["DUCT-排风管设备", "H-通风设备", "ACS_KT_SB", "ACS_SFG_SB", "ACS_OTHER_FM", "ACS-通风设备", "H-设备-风机",  "DUCT-排风排烟管设备",
                          "DUCT-新风管设备", "ACS_FFG_SB", "通风", "M-0"], # "H-风管-排烟风口",
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["管", "风口", "法兰"],
        },
        "pai_yan_feng_ji": {  # 排烟风机
            "layer_sub": ["U-ANNO-TTLB", "H-OTHR-FLDS", "DUCT-排风设备", "DUCT-排风管设备", "DUCT-排烟管设备", "DUCT-排风排烟管设备", "ACS-通风设备",
                          "H-设备-风机"], # "ACS_KT_SB",
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "pai_yan_jian_pai_feng_ji": {  # 排烟兼排风机
            "layer_sub": ["DUCT-排烟管设备", "DUCT-排风管设备", "H-通风设备", "ACS_KT_SB",  "ACS-通风设备",
                          "H-设备-风机", "H-设备-风机", "DUCT-排风排烟管设备"], # "M-EXHS-EQPM",
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "song_bu_feng_ji": {  # 送补风机
            "layer_sub": ["DUCT-送风管设备", "H-设备-风机", "ACS_KT_SB", "ACS_FFG_SB", "ACS_OTHER_FM", "H-通风设备",
                          "H-设备基础", "H-设备-风机 ", "DUCT-排烟阀门", "DUCT-排风管设备", "DUCT-排烟管设备", "ACS-通风设备", "风管、风口定位",
                          "H-设备-补风机", "M-.*-EQPM", "M-(SUPA|SMOK)-MARK",
                          ], # "ACS_COM",
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "xin_feng_ji": {  # 新风机
            "layer_sub": ["N-TG", "N_SB", "ACS_PFG_SB", "XFG"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "you_dao_feng_ji": {  # 诱导风机
            "layer_sub": ["诱导风机", "诱导器", "M-SB"], # "ACS_PFG_F2", "ACS_COM"
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "zhan_shi_pai_feng_ji": {  # 战时排风机
            "layer_sub": ["ACS_OTHER_FM", "M-EXHS-EQPM", "DUCT-送风管设备", "_M-DUCT-排风管设备", "H-设备-风机"], #"ACS_COM", "设备", "暖人防",
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "zhan_shi_song_feng_ji": {  # 战时送风机
            "layer_sub": ["M-ACDT-SADT-EQPM", "N-SB", "M-EXHS-EQPM", "人防设备", "民防_风_消防通风设备", "ACS_KT_SB", "NT-设备",
                          "_M-EQ-TA"], # "设备",
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        'bi_shi_zhou_liu_feng_ji': {  # 壁式轴流风机
            "layer_sub": ["ACS_KT_SB", "TY-空调排风管设备", "M-TF-SB", "DUCT-送风管设备", "M-通风-风机", "DUCT-排风管设备", "DUCT-排烟管", "TYN2-空调-设备"
                          "TY-空调排风阀门", "通风",
                          ], # "ACS_PFG_F2", "ACS_COM",
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["管", "风口", "法兰"],
        },

        # 风管
        "pai_yan_jian_pai_feng_guan": {  # 排烟兼排风管
            "layer_sub": ["DUCT-排烟管", "ACS_(Y|P)FG_F2", "H-EXHS-DSDP", "M-SMOK-DUCT"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "song_bu_feng_guan": {  # 送补风管
            "layer_sub": ["DUCT-送风管", "H-风管-排烟管", "H-EXHS-DSDP", "ACS_SBG_F2", "H-SUPA-DSDP"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "pai_feng_guan": {  # 排风管
            "layer_sub": ["DUCT-排风管", "ACS_YFG_F2", "H-EXHS-DSDP"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "bu_feng_guan": {  # 补风管
            "layer_sub": ["DUCT-送风管", "ACS_SBG_F2", "H-SUPA-DSDP"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "xin_feng_guan": {  # 新风管
            "layer_sub": ["DUCT-新风管", "XFG", "FFG"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "jia_ya_feng_guan": {  # 加压风管
            "layer_sub": ["ACS_JFG_F2", "DUCT-加压送风管"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "feng_guan_fa_lan": {  # 风管法兰
            "layer_sub": ["ACS_(P|F)FG_FL", "法兰", "FLAN", "DSDT"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },

        # 水管
        "kong_tiao_shui_guan": {  # 空调水管
            "layer_sub": ["PIPE-空冷（热）供水", "PIPE-空冷（热）供水", "TEXT-空冷热供水", "PIPE-暖供水", "PIPE-暖回水", "暖通干管", "PIPE-CUSTOM3",
                          "M-HEAT-SPWT", "M-HEAT-RTWT"
                          ],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "di_nuan_pan_guan": {  # 地暖盘管
            "layer_sub": ["PIPE-暖供水", "PIPE-地暖", "M-HEAT-(RT|SP)WT"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },

        "nei_chen_jin_shu_feng_guan": {  # 内衬金属风管
            "layer_sub": ["DUCT-加压送风管端线", "N-消防-风管", "EQ-采暖分集水器", "A-楼面-下部", "DUCT-排烟管立管", "DUCT-加压送风管立管"
                          "地下室风井", "S竖井"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "feng_ji_pan_guan": {  # 风机盘管
            "layer_sub": ["M-新风机", "CMDLJ_SNJ", "ACS_KT_SB", "ACS_DLJ_SNJ"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "fen_ji_shui_qi": {  # 分集水器
            "layer_sub": ["暖通_采暖_地热盘管", "EQ-采暖分集水器", "M-HT-EQPM", "M-采暖-设备"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "fen_ti_kong_tiao": {  # 分体空调
            "layer_sub": ["K空调室外机", "空调室外机", "K空调", "A-EQPM-MECH", "ACS_DLJ_SWJ", "A-Roof", "A-设备-电气", "A-楼面-电气", "C-空调"
                          "0-电气条件", "M-空调-设备", "A-Fixt", "UA-空调", "KT", "MHI VRF", "CMDLJ_SWJ", "空调"
                          ],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "feng_guan_shang_xia_fan": {  # 风管上下翻
            "layer_sub": ["DUCT-排风阀门", "DUCT-加压送风管", "DUCT-排风排烟管", "DUCT-排烟管", "DUCT-送风阀门"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "mao_jin_nuan_qi_jia": {  # 毛巾暖气架
            "layer_sub": ["TH-散热器"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "quan_re_jiao_huan_qi": {  # 全热交换器
            "layer_sub": ["ACS_DLJ_JHQ" ], # "M-新风机", "新风"
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "ran_qi_bi_hua_lu": { # 燃气壁挂炉
            "layer_sub": ["C厨具"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "shou_dong_kai_qi_zhuang_zhi": {  # 手动开启装置
            "layer_sub": ["H-标注-文字"], #, "ACS_PFG_BZ", "ACS_COM", "ACS_COM_BZ",
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "shui_guan_tao_guan": {  # 水管套管
            "layer_sub": ["M-SUPA-DIMS", "ACS_PFG_F2", "VALVE-暖供水", "VALVE_给水", "VALVE_消防",  "M-DK-STRU", "M-DK-ARCH", "M-VT-TG", "M-HEAT-VALV",
                          "M-采暖-管道-中区-供水阀门",  "给结构提条件", "TH-构件", "套管", "通风文字"
                          ], # "ac-穿墙套管", " -新风套管", "GPS-钢套管", "GPS-柔性防水套管", "H-给结构提条件",
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - set(["字"])),
        },
        "xiao_sheng_qi": {  # 消声器
            "layer_sub": [ "K_KT_FM", "M-VT-PARTS", "H-TL(图例)", "DUCT-加压送风阀门", "DUCT-排风排烟阀门", "DUCT-排烟阀门"
                          "DUCT-送风阀门", "DUCT-排风阀门", "H-DUCT(送风管)", "H-通风设备", "H-SUPA-VALV", "DUCT-排烟管设备"
                          ], # "H-风管-阀门配件", "BZ", "ACS_FFG_FM",
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "ya_cha_chuan_gan_qi": {  # 压差传感器
            "layer_sub": ["ACS_YFG_FM_F", "0-暖-电气条件", "M-COM_SB", "DUCT-加压送风管", "H-DOMW-VALV", "ACS_JFG_FM"], # "ACS_COM_BZ",
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "co_tan_ce_qi": {  # CO探测器
            "layer_sub": ["ACS_KT_SB", "U-ANNO-TTLB", "H-标注-文字", "0-电气条件", "CO报警器", "K_KT_FM", "H-CO监测装置"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "wall_floor_line": {  # 为了获取floor_line_list图元
            "layer_sub": [".*"],
            "ignore_word": []
        },
        "emergency_door": {  # 人防
            "layer_sub": ["WINDOW", "WIN", "door", "门", "人防"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] +
                           ["分区", "0-DOOR\.T", "WINDOW[-_]BLIN", "开启范围", "人防集水坑", "人防经济指标", "门套"],
        },  # 过滤人防分区
        "elevation_mark": { # 标高符号
            "layer_sub": ["A-Anno-Levl", "P-ROAD-ELEV", "DIM_ELEV", "标高", "GCD", "A[-_]SYMB[-_]LEVL.*相对标高",
                          "A[-_]ANNO[-_]IDEN[-_]LEVL", "DIM[-_]ELEV", "DIM[-_]ELEV[-_]标高标注",
                          "A[-_]ANNO[-_]IDEN[-_]TEXT", "0A[-_]A[-_]SYMB[-_]ELEV", "A[-_]Anno[-_]Levl",
                          "建[-_]标高", "A[-_]SYMB[-_]LEVL.*标高", "A[-_]Elv.*建筑标高", "A[-_]2[-_]Elev",
                          "IDEN[-_]LEVL", "A[-_]LEVEL", "G[-_]ANNO[-_]LEVL", "A[-_]DIM[-_]ELEV", "DIM[-_]ELEV",
                          "DIM[-_]ELEV[-_]标高标注", "A[-_]ANNO[-_]LEVL", "A[-_]SYMB[-_]LEVL.*标高", "A[-_]Elv.*建筑标高",
                          "G[-_]ANNO[-_]LEVL", "A[-_]ANNO[-_]IDEN[-_]LEVE", "FLOR-LEVL", "SYMB_标高_A", "AD-LEVL-HIGH",
                          "A-ANNO-LEVEL-DIMS-1", "A-DIN-ELEV", "A-注释-标高", "A-标高标注", "A-标注-标高", "标高", "C-标高", "b标高",
                          "A-Elv(建筑标高)", "A_N_DIM_ELEV"],
            "ignore_word": ["^地面标高$"]
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
        'set_1': ['door', 'elevator_door',  "zhi_hui_fa", "fen_ti_kong_tiao", "feng_ji_pan_guan", "fang_huo_fa_70"],
        'set_2': ['elevator_box', "ce_song_jia_ya_feng_kou", 'window', 'bi_shi_zhou_liu_feng_ji', "kong_tiao_hui_feng_kong", "xia_song_feng_kou"],
        'set_3': [],
        'set_4': [],
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
