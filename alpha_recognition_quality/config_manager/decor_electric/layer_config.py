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
        
        "device": {  # 通用的 "设备" 图层，但排除了其他已定义设备的关键字，且过滤了"插座"、"电视"、"楼控"这些目前不关注的设备
            "layer_sub": ["EQUP", "EQUIP", "设备", "EQPM", "EQMT", "ELEC[-_]图块", "E[-_]SYSM[-_]DEVS", "E[-_]L[-_]控制", "断路器"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["厨", "卫", "消火栓", "喷淋", "地漏", "TOLT", "KICH", "PLUM",  # 非电气设备
                                                          "PUMB", "DRAI", "SMAL", "MOVE", "FIXD", "MECH", "空调",  # 非电气设备
                                                          "消防", "FIRE", "安防", "XF",  # 已定义
                                                          "照明", "灯", "LIGH", "LIGHTING",  # 已定义
                                                          "广播", "BROADCAST", "BORADCAST", "NURS",  # 已定义
                                                          "箱柜", "BOX", "QDXK", "CABINET", "BIN", "POW", "动力", "强电", "电力",  # 已定义
                                                          "开关", "ELEMENT", "E-COMP",  # 已定义
                                                          "通讯", "COMM", "电话", "TEL",  # 已定义
                                                          "插座", "SOCK", "电视", "楼控",  # 不关注
                                                          "PARK", "CAR", "车", "car", "PRKG", "快充", "慢充", "无障碍",
                                                          "泊位", "pkng", "che", "设备机房", "D-设备-符号", "给水设备",
                                                          "建筑设备", "XHS", "给排水设备",
                                                          ],
        },
        "device_light": {  # 照明设备（包含 灯）
            "layer_sub": ["灯", "DE[_-]设备[_-]动力", "EQUIP[-_]照明"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ['导线', 'WIRE'],
        },
        "device_box": {  # 箱柜设备（包含配电箱、动力设备）
            "layer_sub": ["(EQUP|EQUIP|设备|EQPM|EQMT).*(箱柜|BOX|QDXK|CABINET|BIN|POW|动力|强电|电力|POWR|强电设备|强电平面|QD|HLVO)",
                          "(箱柜|BOX|QDXK|CABINET|BIN|POW|动力|强电|电力|POWR|强电设备|强电平面|QD|HLVO).*(EQUP|EQUIP|设备|EQPM|EQMT)",
                          "BPM", "Q强电图块", "E-TEXT-PLAN", "EQUIP-箱柜-户箱"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["XHS", "WIRE", "导线"],
        },
        "device_switch": {  # 开关（注意：在 "照明设备" 中也存在开关）
            "layer_sub": ["开关", "E-COMP", "POW", "D块", "SB", "WIRE-1-X", "CORE", "SYSTEM", "E[-_]EQUIP", "Q强电图块",
                          "E[-_]SY[-_]E", "E[-_]元件设备", "E[-_]SYST[-_]SWIT[-_]WIRE", "EL[-_]SYS", "^SYST$", "DQ", "dq1",
                          "WZ", "设备", "EQUIP[-_]照明"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["插座", "消防", "KT", "ACS"],
        },  # 有些开关在 WIRE-1-X 图层，通过对图元进行判断找出可能的开关图元
        "door": {  # 门
            "layer_sub": ["WINDOW", "DOOR", "门", "D&W", "W&D", "WIN", "DOWI"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立面门窗", "人防", "0-DOOR\.T", "WINDOW[-_]BLIN", "开启范围"],
        },
        "window": {  # 窗户
            "layer_sub": ["WINDOW", "WIN", "窗", "DRWD", "WIND", "Window", "D&W", "W&D", "L-玻璃", "DOWI", "dowi",
                          "0A-B-GLAZ", "百叶", "CHUANG"],  # 0A-B-GLAZ-255679
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立面门窗", "WINDOW[-_]BLIN", "0A[-_]B[-_]GLAZ[-_]OPEN"],
        },  # GLAZ-255679
        "wall": {  # 墙
            "layer_sub": ["wall", "墙", "侧壁", "0[-_]结构", "0[-_]现浇混凝土", "CONC", "WAL", "STRU", "W[-_]LINE",
                          "^C[-_]1$", "C-L", "W-L"],  # STRU-249183 & 249178
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"线", "LINE"}) +
                           ["COLS", "墙柱", "挡墙", "外墙轮廓", "STRU[-_]MATE", "P[-_]S[-_]CASI[-_]CONC",
                            "集水坑", "HOLE", "^A-WALL-INSL$", "A_SIGN_STRU", "降板线", "P[-_]结构孔洞[-_]穿墙"],
        },  # 经业务确定，对"wall"构件，忽略关键字中删除"线"，1530 - wall-虚线
        "pillar": {  # 柱子
            "layer_sub": ["柱", "COLU", "COLUMN", "COLS", "S-Col", "S-Col_hatch", "S-WC", "CLOS"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["柱帽", "填充"],
        },
        "wall_hatch": {
            "layer_sub": ["填充", "HATCH"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "axis_net": {
            "layer_sub": ["标注", "轴线", "axis"],
            "ignore_word": ["电气标注"],
        },
        "segment": {  # 住宅平面空间识别图层
            "layer_sub": ["FLOR", "栏杆", "BALCONY", "HANDRAIL", "阳台", "Rail",
                          "HRAL", "blcn", "0425-致逸结构", "surface", "SURFACE",
                          "外包石材", "HEAT", "SILL", "空调板", "OVER", "Hdrl",  # Hdrl-248189
                          "0A-P-ROOF", "AE-FNSH", "A-VISI", "HANDRA", "饰线"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"LINE", "线"}) + [
                "SPCL", "OVHD", "FURN", "SPCL", "OVHD", "FURN", "BORD", "FLUE", "FLOR-PLAN", "GRND", "TPTN", "IDEN",
                "LEVL", "SHFT", "SIGH", "WDWK", "PATT", "CASE", "GRID", "FTMT", "STAIR", "MOVE", "家具", "Fixt",
                "A-Flor-Path", "A-FLOR-FURN", "AE-FLOR", "A[-_]FLOR[-_]AIRC", "A-FLOR-PARK", "A-FLOR-EVTR", "A-FLOR-STR",
                "DRAN", "P-FLOR", "A-FLOR.*边缘", "A-FLOR-STAR", "FLOR-EVTR", "FLOR-STAIR", "S-FLOR_ZM", "A-FLOR-LOOK",
                "A-FLOR-DRAI", "A-FLOR-SANI"]
        },  # FLOR-HRAL - 阳台的边界，A-FLOR-STR-256817，0A-P-ROOF-DRAN-255679，STRS-RAIL阳台边界-255679
        "segment_extra": {  # 住宅平面空间分割需要用到但不常用的图层, 若广泛测试后没有问题可以放到segment中
            "layer_sub": ["0S-C-LINE", "0S-CC-LINE", "A-LIN", "^造型线$", "A_HDWR", "AR_LINE"],
            # A-LIN-249066中的阳台边界；造型线-248189；A_HDWR-1372阳台边界；A-Detl-Thin-是雨棚投影线，先删除
            "ignore_word": [],
        },
        "annotation_line": {  # 引线图层
            "layer_sub": ["DIM", "IDEN", "ANNO", "SYMB", "LEAD", "0[-_]坐标标注", "NO\..*编号", "TEXt", "-TEXT",
                          "F-废水-TEXT", "W-污水-TEXT", "YT-阳台雨-TEXT", "污水文字", "废水文字", "雨水文字", "凝结水文字",
                          "通气文字", "P-负一层消火栓标准", "A[-_]INDEX", "电气标注"],
            "ignore_word": ["PUB", "标高", "红线", "流线", "坐标", "尺寸", "中线", "ELEV", "^TWT[-_]SYMB$", "FROM",
                            "FORM", "GRID", "A-COND-IDEN-TEXT", "LEVL", "LEVEL", "P[-_]FS[-_]EQPM[-_]TEXT",
                            "A[-_]DIM[-_]AXIS", "A[-_]ANNO[-_]NOTE", "A[-_]ANNO[-_]DIMS"],
        },
        "dash_border": {  # 虚线框
            "layer_sub": ["DOTLN", "电气文字"],
            "ignore_word": [],
        },
        "building": {  # 总平图的空间轮廓的图层
            "layer_sub": [
                'DESG设计建筑', '建筑首层', '建筑轮廓', 'ROOF-WALL', '外墙轮廓', 'BULD-BMAX', '空墅', 'BUID', '商业轮廓线',
                '设计建筑', 'BLDG-FACILIT', 'Wall', 'WALL', '屋顶轮廓', 'SITE-BLDG', 'OUTD-BUID', 'COLUMN', 'WINDOW',
                "WIN", 'A-Wind', 'A-Blcn', 'PLAN_建筑基底轮', 'JZW_Close', 'AUDIT_I_12', '总图外墙', '箱变', '建筑标准层轮廓',
                '建筑屋顶平面', 'DOOR_FIRE', '建构筑物轮廓线', '建筑标准层', '^0-建筑$', '规划建筑', '现状建筑', 'P-BULD-BMAX',
                '住宅建筑', 'A_HDWR(配件)', 'A_FLOR[（(]边缘[)）]', 'BD-主体', '新建建筑', 'A-EQPM-MECH', '建筑主轮廓',
                'Z_0_EXST[（(]现有建筑[)）]', 'G_COL', 'Z-0-ZBW', '00-共用-建筑轮廓加粗', '^总图$', '^轮廓$', '3T_WOOD',
            ],  # 云效250244的燃气调压箱，云效250537的住宅，云效249538的住宅，云效249538的住宅，'1*F'去掉
            "ignore_word": [
                "CONC", "DIM", "HATCH", "LANDSCAPE", "ELEV", "HIGH", "NUMB", "人防范围", "地下构筑物", "挡土墙", "用地红线",
                "景观", "TEXT", "YARD", "HATH", "COOR", "坐标", "AXIS", "HACH", "填充", "尺寸", "DIMS", "AXIS", "编号",
                "标号", "名", "NAME", "AD-NUMB", "尺寸", "道", "增补", "VALVE", "LINE", "IDEN", "窗沿", "DIM", "家具",
                "索引", "UDBD", "LIMT", "STAR", "DWALL", "WALL_JG", "PARAPET", "WINDOW[-_]BLIN"],
        },
        "distribution_cabinet": {  # 配电柜
            "layer_sub": ["设备框", "DQ", "EQPM.*DBOX", "设备.*箱体", "配电", "E[-_]EQPM[-_]DBOX", "B[-_]变电所设备",
                          "D[-_]设备[-_]箱体", "HDWR.*配件", "EES[-_]设备动力", "TEL[-_]CABINET", "D[-_]E[-_]Eqpm.*强电设备",
                          "EQUIP[-_]动力", "TEL[-_]CABINET", "POWR[-_]电力大设备[-_]E", "照明平面设备层", "EQUIP[-_]箱柜",
                          "AE[-_]EQPM", "E[-_]WIRE","电设备","TEL_柜","POWER","强电桥架", "DIM_SYMB"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"DIM"}) + ['D[-_]DQ'], #去掉DIM关键字去匹配含有DIM_SYMB的图层
        },
        # "socket": {  # 原插座
        #     "layer_sub": ["D[-_]E[-_]EQPM.*强电设备", "EQUIP[-_]插座", "E[-_]EQUIP[-_]QD", "0E[-_]EQUIP[-_]SOCKET",
        #                   "Q强电图块", "0E[-_]EQUIP[-_]LIGHTING", "E[-_]TEXT[-_]PLAN", "E[-_]HELETPLAN[-_]EQUIP",
        #                   "设备.*插座", "EQUIP[-_]动力", "E[-_]LIGT[-_]EQPM", "E[-_]插座设备", "D[-_]设备[-_]插座",
        #                   "强电.*插座","电气设备","E-UNIV-NOTE","SOCKET"],
        #     "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["弱电"],
        # },
        "socket": {  # bgy插座
            "layer_sub": ["设备.*插座", "D[-_]设备[-_]插座", "强电.*插座","电气设备","E-UNIV-NOTE", "SOCKET", "EQUIP[-_]插座"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["弱电"],
        },
        "weak_socket": {  # bgy弱电插座
            "layer_sub": ["设备.*插座", "弱电.*插座","电气设备","E-UNIV-NOTE","SOCKET"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["强电"],
        },  
        # TODO: 细分的灯具和之前的灯具有什么关系？
        "common_lamp": {  # 普通灯
            "layer_sub": ["EQUIP[-_]照明", "C[-_]天花灯具", "0E[-_]EQUIP[-_]LIGHTING", "D[-_]E[-_]EQPM.*强电设备",
                          "0E[-_]EQUIP[-_]LIGHTING", "A[-_]天花灯具", "E[-_]EQUIP[-_]QD", "E[-_]EQUIP[-_]QD",
                          "E[-_]EQUIP[-_]QD", "RCP.*LIGHT", "E[-_]EQMT[-_]LIGHTING[-_]E", "E[-_]EQMT[-_]LIGHTING[-_]E",
                          "LITE[-_]照明设备[-_]E", "Q强电图块", "F[-_]HELETPLAN[-_]EQUIP", "天花灯"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "single_tube_lamp": {  # 单管灯
            "layer_sub": ["0E[-_]EQUIP[-_]LIGHTING", "D[-_]E[-_]EQPM.*强电设备", "EQUIP[-_]照明", "E[-_]EQUIP[-_]QD",
                          "E[-_]EQMT[-_]LIGHTING[-_]E", "D[-_]设备[-_]普通照明","EQUIP-应急","电气设备"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "double_tube_lamp": {  # 双管灯
            "layer_sub": ["0E[-_]EQUIP[-_]LIGHTING", "EQUIP[-_]照明", "D[-_]E[-_]EQPM.*强电设备",
                          "E[-_]EQMT[-_]LIGHTING[-_]E","EQUIP-应急","电气设备"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "triple_tube_lamp": {  # 三管灯
            "layer_sub": ["EQUIP[-_]照明","EQUIP-应急","电气设备"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "emergency_single_tube_lamp": {  # 应急单管灯
            "layer_sub": ["0E[-_]EQUIP[-_]LIGHTING", "D[-_]E[-_]EQPM.*强电设备", "E[-_]EQUIP[-_]QD", "EQUIP[-_]照明","EQUIP-应急","电气设备"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "emergency_double_tube_lamp": {  # 应急双管灯
            "layer_sub": ["D[-_]E[-_]EQPM.*强电设备", "E[-_]EQUIP[-_]QD", "0E[-_]EQUIP[-_]LIGHTING","EQUIP-应急","电气设备"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "emergency_triple_tube_lamp": {  # 应急三管灯
            "layer_sub": ["0E[-_]EQUIP[-_]LIGHTING","EQUIP-应急","电气设备"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "a_model_emergency_lamp": {  # A型应急照明灯
            "layer_sub": ["EQUIP[-_]照明", "0E[-_]EQUIP[-_]LIGHTING", "D[-_]E[-_]EQPM.*强电设备",
                          "E[-_]EQMT[-_]LIGHTING[-_]E", "Q强电图块", "0E[-_]EQUIP[-_]LIGHTING", "F[-_]HELETPLAN[-_]EQUIP","EQUIP-应急","电气设备"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "button": {  # 按钮
            "layer_sub": ["LVTRY", "D[-_]E[-_]EQPM.*强电设备", "EQUIP[-_]照明", "E[-_]EQUIP", "0E[-_]EQUIP[-_]FIRE",
                          "E[-_]EQMT[-_]FIRE[-_]E", "GEN[-_]通用平面标注[-_]E", "R弱电图块", "0E[-_]EQUIP[-_]LIGHTING",
                          "EQUIP[-_]动力", "E[-_]POWE[-_]EQPM", "EQUIP[-_]动力", "T[-_]CTCC[-_]EQPM",
                          "YHD[-_]EQUIP[-_]通讯", "E[-_]POWER[-_]EQPM", "配电", "D[-_]电箱[-_]ACjlm", "LEB", "Socket.*Ca"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "equipotential_junction_plate": {  # 等电位连接板
            "layer_sub": ["EQUIP[-_]箱柜", "D[-_]E[-_]EQPM.*强电设备", "D[-_]E[-_]Eqpm.*强电设备",
                          "E[-_]LITE[-_]EQPM", "E[-_]E[-_]BOX", "0E[-_]EQUIP[-_]SOCKET","电气设备","RS-应急照明配电箱"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "load_switch": {  # 负荷开关
            "layer_sub": ["电气设备", "ELEMENT", "Q[-_]文字", "BXT", "E[-_]COMPONENT[-_]E", "SYS[-_]元件[-_]E", "Q强电图块",
                          "PD","电-强电设备-系统","ZM", "D-设备-系统元件"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        # TODO: 插座细分
        "information_socket": {  # 信息插座
            "layer_sub": ["D[-_]强弱电", "SOCKET", "CA", "EQUIP[-_]通讯", "插座", "T[-_]CTCC[-_]EQPM",
                          "E[-_]GCS[-_]DEVC", "Z[-_]SOCK","弱电插座","000-弱电"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "telephone_socket": {  # 电话插座
            "layer_sub": ["插座", "A[-_]强弱电点位", "EQUIP[-_]通讯", "T[-_]CTCC[-_]EQPM", "E[-_]GCS[-_]DEVC",
                          "Z[-_]SOCK","弱电插座","000-弱电"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ['WIRE'],
        },
        "television_socket": {  # 电视插座
            "layer_sub": ["插座", "A[-_]强弱电点位", "Z[-_]SOCK", "EQUIP[-_]通讯", "T[-_]CTCC[-_]EQPM",
                          "E[-_]GCS[-_]DEVC", "Z[-_]SOCK", "弱电插座", "000-弱电"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ['WIRE'],
        },  
        "arrow": {  # 箭头 
            "layer_sub": ["DIM_SYMB", "A-ANNO-SYMB", "0A-A-SYMB", "A-Anno-Dims", "建-箭头", "A-Index(建筑索引线剖切号线)",
                          "A-3-Symb", "A-TEXT", "G-ANNO-INDX", "A-ANNO-IDEN", "A-FLOR-STRS", "E-TEXT", "箭头", "坡向线"],
            "ignore_word": ["PUB", "标高", "红线", "流线", "坐标", "尺寸", "中线", "ELEV", "^TWT[-_]SYMB$", "FROM",
                            "FORM", "GRID", "A-COND-IDEN-TEXT", "LEVL", "LEVEL", "P[-_]FS[-_]EQPM[-_]TEXT",
                            "A[-_]DIM[-_]AXIS", "A[-_]ANNO[-_]NOTE", "A[-_]ANNO[-_]DIMS"],
        },
        "weak_electric_box":{ # 弱电箱，多媒体配线箱
            "layer_sub": ["设备", '箱柜'],
            "ignore_word": ["导线", "WIRE"],
        },
        "strong_electric_box": { # 强电箱
            "layer_sub": ["设备", '箱柜'],
            "ignore_word": ["导线", "WIRE"],
        },
        "visual_intercom": {     #可视对讲
            "layer_sub": ["通讯", 'EQUIP[-_]通讯', 'EQUIP[-_]箱柜', "EQUIP", "Pm-弱电"],
            "ignore_word": BASIC_IGNORE_WORDS['basic'],
        }
    }

    BASIC_LAYERS = {
        "basic": ["wall", "axis_net"],
        "indoor_segment": ["wall", "pillar", "segment", "segment_extra"],  # 去掉了 border
        # "indoor_first_floor_segment": ["wall", "pillar", "segment", "segment_extra", "segment_lobby_platform", "border"],
        "underground_segment": ["wall", "pillar", "segment"],  # 去掉了 border
        "building_segment": ["building", "door", "window"],
        # "second_third_segment": ["wall", "door", "window", "pillar", "segment", "border", "second_third_space"],
        # "indoor_access_segment": ["wall", "pillar", "segment", "border", "indoor_access"],
    }

    COMBINATION_EXCLUDE_LAYERS_INDOOR = [
        "wall", "segment", "pillar", "mentou", "wall_hatch", "hatch", "second_third_space", "pipe_barrier",
        "hatch_outline", "wire", "jieshandai", "annotation_line", "lobby_platform_border",
        "segment_underground", "segment_extra", "text_with_bound_vertex", "text", "solid_wall_line",
        "non_solid_wall_line", "mleader",
    ]  # hatch_outline-规则62，pillar_line 在LAYERS_WITH_SLOPE_LINE_REVISED中有

    # COMBINATION_EXCLUDE_LAYERS_UNDERGROUND_AND_SITEPLAN = [
    #     "wall", "podao", "separator", "filling", "road", "car_lane", "hatch", "red_line", "red_line_sub",
    #     "building", "underground_building", "podao_extra", "podao_mark", "podao_edge", "hatch_outline", "wire",
    #     "annotation_line", "jieshandai", "segment_underground", "text_with_bound_vertex", "text", "segment_extra",
    #     "segment", "solid_wall_line", "non_solid_wall_line", "mleader"
    # ]

    CLASSIFICATION_EXCLUDE_LAYERS = [
        "wall", "pillar", "special_pillar", "segment", "podao", "podao_extra", "separator", "filling",
        "pillar_line", "road", "car_lane", "red_line", "red_line_sub", "building", "elevation_handrail",
        "mentou", "underground_building", "wall_hatch", "podao_mark", "structure", "elevation_window_exclude",
        "hatch", "podao_edge", "pipe_barrier", "hatch_outline", "wall_line", "wire", "wire_line", #"yinxiaxian",
        "jieshandai", "annotation_line", "lobby_platform_border", "segment_underground", "segment_extra",
        "text_with_bound_vertex", "text", "road_center_line", "solid_wall_line", "non_solid_wall_line",
        "mleader", "cabinet_contour_dict", 'transformer_contour_dict', 'dash_border',
    ]

    # 分图层打印配置
    INDOOR_DRAWING_PRINT_LAYER_SEPARATE_SET = {
        'set_1': ['pipe', 'floor_drain', 'door', 'elevator_door', 'window', 'air_conditioner'],
        'set_2': ['floor_drain_mix', 'air_conditioner_mix', 'fire_hydrant', 'elevator_box'],
        # 'set_3': ['device', 'device_fire', 'device_light', 'device_broadcast', 'device_box', 'device_switch',
        #           'device_communication', 'yinxiaxian', 'surge_protector', 'transformer', 'socket', 'button',
        #           'fire_resistant_shutter_controller', 'fire_proof_door_monitor', 'distribution_cabinet',
        #           'floor_indicator_light', 'common_lamp', 'single_tube_lamp', 'double_tube_lamp', 'triple_tube_lamp',
        #           'emergency_single_tube_lamp', 'emergency_double_tube_lamp', 'emergency_triple_tube_lamp',
        #           'a_model_emergency_lamp', 'equipotential_junction_plate', 'residual_current_circuit_breaker',
        #           'load_switch', 'thermorelay', 'contactor', 'electricity_meter', 'circuit_breaker',
        #           'integrated_circuit_breaker', 'information_socket', 'telephone_socket', 'television_socket',
        #           'fire_hydrant_button', 'fuse_protector'],
        'set_3': ['device', 'device_fire', 'device_box', 'device_switch', 'socket', 'weak_socket',
                  'weak_electric_box', 'strong_electric_box', 'visual_intercom'],
        'set_4': ['window', 'elevator_door', 'door', 'emergency_door', 'wall', 'pillar', 'elevation_window'],
        # 'set_5': ['floor_drain_mix', 'air_conditioner_mix', 'fire_hydrant', 'elevator_box', 'pipe', 'floor_drain',
        #           'air_conditioner', 'elevator_stair', 'washbasin', 'closestool', 'diamond_bath'],
    }

    # 不会用函数get_hyper_layer进行匹配的图层
    MATCH_EXCLUDE_LAYERS = ["podao_extra", "podao_mark", "podao_edge", "pipe_barrier"]

    # 存在斜线的图层，（需要对像素坐标进行特殊处理，确保能真实反映图纸上的线段走势） add by yanct01 2020-5-16
    # 处理结果，保存到一个新的逻辑层 ： 原图层名 + '_line'
    LAYERS_WITH_SLOPE_LINE_SUFFIX = '_line'
    LAYERS_WITH_SLOPE_LINE = ['wall', 'pillar', 'red_line', 'red_line_sub', "wire"]
    LAYERS_WITH_SLOPE_LINE_REVISED = [x + '_line' for x in LAYERS_WITH_SLOPE_LINE]
    # 对于线型是虚线的墙线，单独保存
    DASH_LINE_SUFFIX = '_dash'
    DASH_LINE_REVISED = [x + '_dash' for x in LAYERS_WITH_SLOPE_LINE_REVISED]

    # "电气设备" 与 "图层" 的对应关系
    DEVICE_ENTITY_LAYER_MAP = {
        "灯具": ["device", "device_light", "device_box"],
        "平面图开关": ["device", "device_switch", "device_light", "device_box", "surge_protector"],  # 将不涉及和电线等图层混合的开关图层从device_switch中删除
        "插座": ["socket"],
        "弱电插座": ["weak_socket"],
        "强电箱": ["strong_electric_box"],
        "弱电箱": ["weak_electric_box"],
        "箱柜": ["device_box"],
        # "电话网络电视接口": ["information_socket", "telephone_socket", "television_socket"],
        "等电位连接板": ["equipotential_junction_plate"],
        "普通灯": ["common_lamp", "device", "device_light", "device_box"],
        "单管灯": ["single_tube_lamp", "device", "device_light", "device_box"],
        "双管灯": ["double_tube_lamp", "device", "device_light", "device_box"],
        "三管灯": ["triple_tube_lamp", "device", "device_light", "device_box"],
        "应急单管灯": ["emergency_single_tube_lamp", "device", "device_light", "device_box"],
        "应急双管灯": ["emergency_double_tube_lamp", "device", "device_light", "device_box"],
        "应急三管灯": ["emergency_triple_tube_lamp", "device", "device_light", "device_box"],
        "A型应急照明灯": ["a_model_emergency_lamp", "device", "device_light", "device_box"],
        # "电话": ["device", "device_fire", "device_communication"],
        "信息插座": ["information_socket"],
        "电话插座": ["telephone_socket"],
        "电视插座": ["television_socket"],
        "疏散照明灯具": ["device", "device_light", "device_box"],
        "楼层标志灯": ["floor_indicator_light", "device", "device_light", "device_box"],

        "灯光疏散指示标志": ["device", "device_light", "device_box"],
        "可视对讲": ['visual_intercom'],
        # "专设引下线": ["yinxiaxian"],
        # "电线": ["wire"],
        # "配电柜": ["distribution_cabinet", "transformer"],
        # "照明分支回路": ["device", "device_light", "device_box", "common_lamp", "single_tube_lamp", "double_tube_lamp",
        #            "triple_tube_lamp", "a_model_emergency_lamp", "emergency_single_tube_lamp",
        #            "emergency_double_tube_lamp", "emergency_triple_tube_lamp", "wire"],
        # "配电箱子图": ["wire", "circuit_breaker", "integrated_circuit_breaker", "residual_current_circuit_breaker",
        #           "electricity_meter", "fuse_protector", "thermorelay"],
    }
