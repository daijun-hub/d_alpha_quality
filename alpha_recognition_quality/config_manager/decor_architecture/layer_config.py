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
                "tian_hua",
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
        "tian_hua": {  # 天花
            "layer_sub": ["C-CEIL", "D-天-天花造型"],
            "ignore_word": [],
        },
        "pipe": {  # 立管
            "layer_sub": ["VPIPE", "立管", "S_EQUIPMENT", "雨水", "冷凝管", "给水", "污水管", "消防管", "废水管", "EQPM-PLUM",
                          "EQUIP_\*水\*", "DRAI-EQPM", "EQPM-DRAI", "VERT_PIPE", "P-.{13}-L", "WATER", "排水", "^水$",
                          "水管", "0P-ACC-FD", "LG", "lg", "PUB_STRM", "封管井", "^A-SAN$", "EQPM-PUMB", "PIPE-RISR-WATR",
                          "A-DRAI", "P-SWER-SILO", "QN-N-燃气", "DSEW", "P-WAST-SILO", "^PL_污水$",
                          ],  # 封管井-#2107立管, A-SAN-#249066立管，出图中遇到的一些不规范图层："分水线", "立剖面看线", "OVER", "设备", "ROOF"
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"线"}) + ["雨水斗", "冷凝管方向"],
        },
        "pipe_barrier": {  # 规则13相关, 隔挡立管的图元, 汇总了door,elevator和window, 分割合并分类都不走
            "layer_sub": [
                "A_FLOR", "A_HDWR", "WINDOW", "Window", "WIN", "DOOR", "门",
                "DRWD", "D&W", "W&D", "窗", "L-玻璃", "DOWI", "dowi",
                "^外墙装饰线$"
            ],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"线"}) +
                           ["0-DOOR\.T", "WINDOW[-_]BLIN", "人防", "开启范围", "门套", "A[-_]EQPM[-_]WIND", "阀门"],
        },
        "window": {  # 窗户
            "layer_sub": ["WINDOW", "WIN", "窗", "DRWD", "WIND", "Window", "D&W", "W&D", "L-玻璃", "DOWI", "dowi",
                          "GLAZ", "百叶", "CHUANG"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立面门窗", "WINDOW[-_]BLIN", "0A[-_]B[-_]GLAZ[-_]OPEN",
                                                          "开启", "A[-_]EQPM[-_]WIND"],
        },  # GLAZ-255679
        "elevator_door": {  # 电梯门
            "layer_sub": ["WINDOW", "WIN", "DOOR", "门", "DRWD", "^YCJ[-_]电梯扶梯$", "WI"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立面门窗", "0-DOOR\.T", "WINDOW[-_]BLIN", "人防", "开启范围",
                                                          "门套", "A[-_]EQPM[-_]WIND", "阀门", "WIRE-照明", "WIRE-消防"],
        },
        "door": {  # 门
            "layer_sub": ["WINDOW", "DOOR", "门", "D&W", "W&D", "WIN", "DOWI", "DRWD", "A-DO_FIRE", "窗"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立面门窗", "人防", "0-DOOR\.T", "WINDOW[-_]BLIN",
                                                          "开启", "门套", "A[-_]EQPM[-_]WIND", "阀门", "窗帘"],
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
        "elevator_stair": {  # 电梯厢/楼梯（住宅平面图）
            "layer_sub": ['EVTR', 'Stair', 'STAIR', 'Lift', 'LIFT', '电梯', '楼梯', '梯', 'FIT', 'ELEV', 'elevator', 'STRS',
                          'EQPM', 'STAR'],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"LINE"}) +
                           ['SMAL', 'BALC', 'ELEC', 'LIHT', 'CLNG', 'FIRE', 'HYDR', 'KICH', 'ASSI', 'MECH', 'PLOM',
                            'TOLT', 'PRKG', 'SYMB', "RAIL", "^FIT$", "STAIR-栏杆", "CAR", "TACC", "洁具", "A[-_]EQPM",
                            "JACK"],
        },
        "parking": {  # 车位
            "layer_sub": ["PARK", "park", "车位", "Car", "CAR", "车", "car",
                          "AE-EQPM", "PRKG", "快充", "慢充", "无障碍", "泊位",
                          "pkng", "che", "A-Pkng-Vhel-Mini", "A-1-Pkng"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["轮廓", "DRIV", "CURB", "自行车", "绿地"],
        },
        "fire_hydrant": {  # 消火栓
            "layer_sub": ["消火栓", "消防箱", "消火箱", "消防", "XHS", "HYDT_BOX", "HYDT", "XHSX", "HYDRANT", "EQPM-FIRE", "HYDR",
                          "^0P-ACC-FH$", "^0P-EQUIP-FH$", "FHBX", "FIRE-FH", "灭火器", "消栓[-_]栓箱", "YCS[-_]消防管.*配件"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立管", "PIPE", "阀门", "风管", "法兰", "风口", "消防分析", "消防出口"],
        },
        "emergency_door": {  # 人防
            "layer_sub": ["WINDOW", "WIN", "door", "门", "人防"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ['人防-计入单体、非人防面积', "井"] +
                           ["分区", "0-DOOR\.T", "WINDOW[-_]BLIN", "开启范围", "人防集水坑", "人防经济指标", "门套", "A[-_]EQPM[-_]WIND",
                            "阀门"],
        },  # 过滤人防分区
        "wall": {  # 墙
            "layer_sub": ["wall", "墙", "侧壁", "0[-_]结构", "0[-_]现浇混凝土", "CONC", "WAL", "STRU", "W[-_]LINE",
                          "^C[-_]1$", "C[-_]L", "A[-_]WALL[-_]BRIK.*砌块墙", "A[-_]WALL[-_]BLOK", "WALL", "WALL[-_]墙",
                          "A[-_]WALL", "0A[-_]S[-_]WALL", "S[-_]WALL", "建[-_]墙[-_]砌块墙", "0A[-_]S[-_]WALL", "COLU",
                          "S[-_]WACO.*墙柱", "C[-_]L", "A[-_]Wall.*建筑墙", "A[-_]1[-_]Wall", "A[-_]WALL[-_]CONC",
                          "A[-_]1[-_]Wall", "S[-_]WC", "COLUMN", "G_COL（墙柱）", "剪力墙线", "WALL_填充墙_A", "COLUMN_结构柱墙",
                          "COLUMN", "A_COLUMN", "塔楼墙柱(C-L)", "S_WACO（墙柱）", "C-墙体", "C-墙柱", "B$0$A-WALL", "BY-WALL",
                          "A-墙体-砼墙", "AE-WALL", "HYP-WALL", "WALL-SHER", "^W[-_]L$", "^C[-_]T0$", '^_A-W$', "隔断$"
                          ],  # STRU-249183 & 249178，出图中遇到的一些不规范图层："建-立剖面看线", "屋顶", "屋面"
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"线", "LINE"}) +
                           ["COLS", "墙柱", "挡墙", "外墙轮廓", "STRU[-_]MATE", "P[-_]S[-_]CASI[-_]CONC",
                            "集水坑", "HOLE", "^A-WALL-INSL$", "A_SIGN_STRU", "降板线", "P[-_]结构孔洞[-_]穿墙",
                            "A-COLU-CONC-HATC", "GLAZ", "AE-STRU-HACH", "ST-WALL", "轴线", "分水线", '洞口', '墙洞口'  # "完成面",
                               , "C[-_]LITEDIM", "C-LEVEL"]

        },  # 经业务确定，对"wall"构件，忽略关键字中删除"线"，1530 - wall-虚线
        "pillar": {  # 柱子
            "layer_sub": ["柱", "COLU", "COLUMN", "COLS", "S-Col", "S-Col_hatch", "S-WC", "CLOS", "S_CL$"],
            # 华住图纸柱子图层添加S_CL
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["柱帽", "填充", "A-COLU-CONC-HATC", 'A-COLS-C-S'],
        },
        "pillar_cap": {  # 柱帽
            "layer_sub": ["柱帽", "Z帽"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "axis_net": {
            "layer_sub": ["建-标注", "建-轴线", "axis", "GRID", "DOTE", "轴网", "轴线", "轴号"],  # 邀测图纸轴网图层新加，且设计师描述DOTE、轴网为轴网常用图层
            "ignore_word": [],
        },
        "elevator_box": {  # 电梯厢/楼梯
            "layer_sub": ["EVTR", "Stair", "STAIR", "Lift", "LIFT", "电梯", "楼梯", "梯", "FIT", "ELEV", "elevator", "STRS",
                          "EQPM", "STAR", "轿厢", "STR$", "^A-平面-楼梯电梯、台阶坡道$"],  # STR-电梯厢256817，^FIT$-不是楼梯图层
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"LINE", "道"}) +
                           ["SMAL", "BALC", "ELEC", "LIHT", "CLNG", "FIRE", "HYDR", "KICH", "ASSI", "MECH", "PLOM",
                            "TOLT", "PRKG", "SYMB", "RAIL", "^FIT$", "STAIR-栏杆", "CAR", "TACC", "洁具", "A[-_]EQPM"],
            # STAIR-栏杆-阳台边界
        },
        "floor_drain": {  # 地漏
            "layer_sub": ["地漏", "drain", "板面留洞", "DRAI-FLDR", "DRAL-FLDR", "pipe-risr$", "^water-dl$", "^0P-ACC-FD$",
                          "^A-SAN$", "A-DRAN-SYMB", "SD_FS_PJ", "DL", "P-SEWR-MISC", "1WL", "DICH.*建筑沟"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },  # FUR-#2107地漏(没加), FLOOR-#1757地漏(没加), A-SAN-#249066地漏，"P-FLDN"也是地漏图层
        "floor_drain_mix": {  # 厨卫
            "layer_sub": ["厨.*卫", "LVTRY", "洁具", "FLOR[-_]SPCL", "FIXT", "SANR", "EQPM[-_]ASSI", "TOLT", "Lavatory",
                          "EQPM[-_]KICH", "标配部件[-_]厨房卫生", "EQPM[-_]TACC", "厨房卫生间", "卫生间", "FURN",
                          "MILL.*PLUMB", "Lavatery", "WC", "家具", "卫浴", "洁厨", "AUDIT[-_]I", "BATH", "TPTN", "FUR",
                          "A-FLOR-SANI", "厨房厕所", "厨具", "A[-_]EQPM", "厨房设备", "^A[-_]KICH[-_]DASH$", "CHUWEI",
                          "JIAJU", "厨柜", "A[-_]1[-_]LVTR$", "B[-_]04电器$", "B[-_]04洁具$", "B[-_]10五金$", "家俱$",
                          "^A[-_]SPCL$", "A-COLS-C-S"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ['^A[-_]EQPM[-_]MECH$', '^A[-_]EQPM[-_]WIND$'],
        },
        "bed": {  # 床
            "layer_sub": ["家具", "FURN", "Furniture", "furn", "EQPM-MOVE", "EQPM-FIXD", "Fixt", "FTMT[-_]MOVE]"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "segment": {  # 住宅平面空间识别图层
            "layer_sub": ["FLOR", "^FLOOR$", "0425-致逸结构", "外包石材", "HEAT", "SILL", "空调板", "OVER", "0A-P-ROOF", "AE-FNSH",
                          "A-VISI", "^A[-_]SURFACE$", "平面饰线", "P-饰线", "平面[-_]饰线", "墙柱"],  # "surface", "SURFACE",
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"LINE", "线"}) + [
                "SPCL", "OVHD", "FURN", "SPCL", "OVHD", "FURN", "BORD", "FLUE", "FLOR-PLAN", "GRND", "TPTN",
                "IDEN", "LEVL", "SHFT", "SIGH", "WDWK", "PATT", "CASE", "GRID", "FTMT", "FLOR-ABOV",
                "MOVE", "家具", "Fixt", "A-Flor-Path", "A-FLOR-FURN", "AE-FLOR", "FLOR-STRS", "A-FLOR-PARK",
                "A-FLOR-EVTR", "A-FLOR-STR", "DRAN", "P-FLOR", "A[-_]FLOR.*边缘", "A-FLOR-STAR", "FLOR-EVTR",
                "FLOR-STAIR", "S-FLOR_ZM", "A-FLOR-LOOK", "A-FLOR-DRAI", "A-FLOR-SANI", "A[-_]FLOR[-_]AIRC",
                "A-FLOR-UNDR", "J[-_]FLOR[-_]DICH.*建筑沟", "A-HOLE-FLOR", "A[-_]1[-_]FLOR"]
        },  # "^A-OVER$" 会用到空调板的边界
        # A-FLOR-STR-256817，0A-P-ROOF-DRAN-255679，FLOR-HRAL-阳台边界, A-FLOR-UNDR是阳台边界，Hdrl-248189，STRS-RAIL阳台边界-255679，STAIR-栏杆-阳台边界
        "segment_extra": {  # 住宅平面空间分割需要用到但不常用的图层, 若广泛测试后没有问题可以放到segment中
            "layer_sub": ["0S-C-LINE", "0S-CC-LINE", "A-LIN", "^造型线$", "AR_LINE", "仿木纹铝板$", "^建-材料-2$"],
            # A-LIN-249066中的阳台边界；造型线-248189；A_HDWR-1372阳台边界；A-Detl-Thin-是雨棚投影线，先删除
            "ignore_word": [],
        },
        "lobby_platform_border": {  # 规则523、535中用到的大堂外的 "入口平台" 区域
            "layer_sub": ["^fit$", "^A-P-FLOR$", "^AE-FLOR$"],
            "ignore_word": [],
        },
        "podao": {  # 不包含外壁圆弧的坡道分割线
            "layer_sub": [
                "栏", "HANDRAIL", "Rail", "HRAL", "PD", "坡道", "车流线", "车道中线", "行车方向", "AE-DICH-STRU",
                "地下室墙柱线", "A-Detl-Thin", "AE-STAR", "APRO"
            ],  # "SYMB"，"电梯扶梯",
            "ignore_word": [
                "TEXT", "AXIS", "字", "编号", "标号", "名", "NAME", "AD-NUMB", "尺寸", "增补", "VALVE", "IDEN",
                "窗沿", "家具", "索引", "配件", "洞口", "GUTT", "SUMP", "虚线", "STAIR-栏杆", "A-平面-楼梯电梯、台阶坡道"
            ],  # "道"
        },
        "separator": {  # 坡道外壁圆弧，该entity类别只走空间分割
            "layer_sub": ["FLOR", "CON", "BEAM"],
            "ignore_word": ["GUTT", "SUMP", "水井", "PARK", "虚线", "COLU"],
        },
        "podao_extra": {  # podao与car_lane的冲突图层
            "layer_sub": ["车流线", "车道中线"],
            "ignore_word": [],
        },
        "podao_mark": {  # 坡道识别辅助构件，该entity类别不走空间分割，合并及分类
            "layer_sub": ["DIM_SYMB", "A-ANNO-IDEN"],
            "ignore_word": [],
        },
        "podao_edge": {  # 坡道空间的边界线, 基本上是gutter和separator的图层, 去掉stair
            "layer_sub": ["TY", "WATER", "排水", "水沟", "水井", "水坑",
                          "GUTT", "WELL", "GLASS", "Hole", "SUMP", "FZ",
                          "水管井", "DICH-ARCH", "DICH-STRU", "FLOR", "CON"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["STAR", "BALC", "UNDR"],
        },
        "gutter": {  # 排水沟外框
            "layer_sub": ["TY", "WATER", "排水", "水沟", "水井", "水坑", "GUTT", "WELL", "GLASS", "Stair", "STAIR", "Hole",
                          "SUMP", "FZ", "水管井", "DICH-ARCH", "DICH-STRU", '[0-9][-_].*水沟', '.*截水沟', '.*排水沟', 'DRAI'],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["STAIR-栏杆", "集水坑"],
        },
        "filling": {  # 排水沟内部填充
            "layer_sub": ["hatch", "hatc", "HATH"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "air_conditioner": {  # 空调
            "layer_sub": ["空调", "^空_$", "Aircontroe", "^AC$", "Aircondition", "EQPM-MECH", "EQPM-SMAL", "M_AC", "KT",
                          "FLOR-OVHD", "LA-plan-smal", "RS-A", "^A-AC$", "A[-_]FLOR[-_]AIRC", "^A[-_]EQPM[-_]WIND$",
                          "AC"],  # A-EQ
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["洞", "孔", "水", "空调管"],
        },
        "air_conditioner_mix": {  # 含有空调的混合图层，仅用于识别空调，"家具"图层
            "layer_sub": ["家具", "FURN", "Furniture", "furn", "EQPM-MOVE", "EQPM-FIXD", "Fixt", "FTMT[-_]MOVE",
                          "设备.*洗衣机", "设备.*冰箱", "A-DETL", "M_EQUIPMENT"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS['basic']) - {'家具'}),
        },
        "road": {  # 普通道路边线 - 不包含车道中心线
            "layer_sub": ["ROAD", "车道", "道路", "车行道", "HHDZ-0-市政", "RD", "园区车型路", "ZR[-_]道路路沿线",
                          "G[-_]Road[-_]Cntr", "P[-_]ROAD", "road", "0[-_]道路", "d道路边线调", "b道路",
                          "P[-_]ROAD[-_]DRWY", "ROAD[-_]CITY", "0[-_]道路.*园区", "小区道路", "Z[-_]小区道路",
                          "P[-_]ROAD[-_]ELEV", "H07[-_]道路.*小区", "R[-_]车道", "LA[-_]MASTER.*PLAN[-_]ROAD",
                          "1[-_]车行道路", "RD", "A[-_]SITE[-_]ROAD", "Z[-_]0[-_]ROAD.*车行道", "B[-_]车行路",
                          "rd[-_]步行道", "G[-_]ROAD", "Z[-_]道路边线", "道路[-_]车行道", "道路[-_]楼间交通[-_]0.0",
                          "道路", "新道路", "01[-_]道路", "paodao", "HHDZ[-_]0[-_]道路边线", "小区路", "入户路",
                          "0[-_]景观[-_]RD", "主路", "LC-道路", "Z_0_ROAD(车行道)", "SITE-ROAD", "P-ROAD-WALK", "road-道路边线",
                          "C-道路", "隐形通道", "路缘线", "ROAD[-_]PAVE", "人行便道",
                          "总平面-道路(车行道)", "0 - 道路", "园区道路", "HYP - ROAD", "0 - 小区道路", "D道路", "ZPM - ROAD", "1 - 小区道路",
                          "D-道路边线", "0-道路-车行", "Z-车道", "A-道路", "D-道路线", "G-道路-规划-侧石线", "A_L_ROAD"],
            "ignore_word": ["Center", "流线", "坐标", "尺寸", "标注", "登高", "CURB", "CENT", "CNTR", "中线", "坡道", "标高", "红线",
                            "定位", "元素", "中心", "AXIS", "COORD", "铁路", "非机动车道", "设计道路", "ROAD[-_]DESN",
                            "SITE[-_]ROAD", "道路立交线"],
        },
        "fire_road": {  # 消防道路边线
            "layer_sub": ["消防扑救面", "消防路", "消防道路", "1[-_]消防道路", "00[-_]消防车道", "消防道路", "0[-_]消防流线",
                          "消防车道", "LA[-_]MASTER.*PLAN[-_]消防车道", "XFCD", "道路[-_]区内消防路", "1-box-19消防车道边线",
                          "0-消防车道", "消防车流线", "XG-消防通道", "Z-消防车道", "消防路", "交通-消防道路", "m_消防路", "X消防车道",
                          "Z[-_]FIRE[-_]ROAD"],
            "ignore_word": ["Center", "流线", "坐标", "尺寸", "标注", "登高", "CURB", "CENT", "CNTR", "中线", "坡道", "标高", "红线",
                            "定位", "元素", "中心", "AXIS", "COORD", "非机动车道", "设计道路", "ROAD[-_]DESN", "SITE[-_]ROAD",
                            "道路立交线"],
        },
        "road_center_line": {  # 道路中心线 - 规则528
            "layer_sub": ["路.*中心线", "RD.*中心线", "ROAD.*中心线", "路.*中线", "RD.*中线", "ROAD.*中线",  # 中心线类型
                          "园区车型路",
                          "ROAD.*AXIS", "RD.*AXIS",  # axis类型
                          "ROAD.*CENT", "RD.*CENT", "RD.*CNTR", "ROAD.*CNTR",  # center类型
                          "路.*流线", "流线.*路"],  # 流线类型
            "ignore_word": [],
        },
        "car_lane": {  # 地下车库车道线，规则30业务要求：获取车道线所在图层：模糊匹配（不区分大小写）含有“*车*线”、“车道”、“PARK-LINE”
            "layer_sub": ["AD-SIGN", "车.*线", "车道", "PARK-LINE", "G-Road-Cntr", "a-road-cent", "PRKG-DRIV",
                          "PARK-CURB", "A-Road-Curb", "PKNG-LINE", "0A[-_]P[-_]PKNG[-_]LINE", "车道", "C车行线",
                          "A[-_]SIGN[-_]CAR.*车流线", "CAR_LINE(车行线)", "A_CAR_轿车路线", "A_SIGN_CAR(车流线)", "G-ROAD-INTL",
                          "A-停车-标线", "A-PKNG-TURN", "0A-P-RKNG-TURN", "汽车线路", "PRKG-DRIV", "c车行方向"],  # "道路中心线" 暂时去掉
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"道", "线", "LINE"}) + ['虚线车道'],
        },
        "red_line": {  # 用地红线
            "layer_sub": ["用地红线", "0[-_]规设[-_]11.*规划用地界线", "HHDZ[-_]0[-_]用地红线", "D01征地范围红线", "用地范围",
                          "用地红线", "规划用地红线", "A[-_]用地红线", "G[-_]通用[-_]用地红线", "M[-_]用地红线[-_]REDL",
                          "^000辅助线$", "0G-SITE-PROP", "Z-用地红线", "Z_0_LTMT(用地红线)", "02HC-用地红线", "1-box-28用地红线", "用地界线",
                          "a用地红线", "PLAN_用地红线", "yzt_道路红线", "Z-净用地范围线", "总平面-用地红线", "01-01 用地红线", "A-用地红线",
                          "z-建设用地红线", "base—red道路红线", "G-用地-规划红线", "AA规划用地红线", "RD-道路红线", "JZD"],
            "ignore_word": ["DIM", "COOR", "OUTD", "标注"]
        },
        "red_line_sub": {  # 红线
            "layer_sub": ["红线", "LINE-RED", "LIMT", "REDL"],
            "ignore_word": ["DIM", "COOR", "OUTD", "用地"],
        },
        "building": {  # 总平图的空间轮廓的图层
            "layer_sub": [
                'DESG设计建筑', '建筑首层', '建筑轮廓', 'ROOF-WALL', '外墙', 'BULD-BMAX', '空墅', 'BUID', '商业轮廓线',
                '设计建筑', 'BLDG-FACILIT', 'Wall', 'WALL', '屋顶轮廓', 'SITE-BLDG', 'OUTD-BUID', 'COLUMN', 'WINDOW',
                "WIN", 'A-Wind', 'A-Blcn', 'PLAN_建筑基底轮', 'JZW_Close', 'AUDIT_I_12', '总图外墙', '箱变',
                '建筑标准层轮廓', '建筑屋顶平面', 'DOOR_FIRE', '建构筑物轮廓线', '建筑标准层', '^0-建筑$', '规划建筑',
                '现状建筑', 'P-BULD-BMAX', '住宅建筑', 'A_HDWR(配件)', 'A_FLOR[（(]边缘[)）]', 'BD-主体', '新建建筑',
                'A-EQPM-MECH', 'Z_0_EXST[（(]现有建筑[)）]', 'G_COL', 'Z-0-ZBW', '00-共用-建筑轮廓加粗',
                '^总图$', '^轮廓$', '3T_WOOD', '^0G-SITE$', '地下设备房', '建筑主轮廓', 'G-FLOR', "Z[-_]BUILDING", "A-SITE-BOTL"
            ],  # 总图 - 云效250244的燃气调压箱，轮廓 - 云效250537的住宅， 3T_WOOD - 云效249538的住宅，1*F - 云效249538的住宅
            "ignore_word": [
                "CONC", "DIM", "HATCH", "LANDSCAPE", "ELEV", "HIGH", "NUMB", "人防范围", "地下构筑物", "挡土墙",
                "用地红线", "景观", "TEXT", "YARD", "HATH", "COOR", "坐标", "AXIS", "HACH", "填充", "尺寸", "DIMS",
                "AXIS", "编号", "标号", "名", "NAME", "AD-NUMB", "尺寸", "道", "增补", "VALVE", "LINE", "IDEN",
                "窗沿", "DIM", "家具", "索引", "UDBD", "LIMT", "STAR", "DWALL", "WALL_JG", "PARAPET", "WINDOW[-_]BLIN",
                "^XG-地下建筑轮廓$", "Z[-_]WALL"
            ],
        },
        "underground_building": {
            "layer_sub": ["JZW_地下车库轮廓线", "2-地下车库"],
            "ignore_word": []
        },
        'washbasin': {
            'layer_sub': ['LVTRY', '洁具', 'FURN', 'Lavatery', '厨.*卫', 'AUDIT_I', 'A-FLOR-SPCL', 'WC', '家具', '卫浴', 'MASK',
                          '洁厨', 'TOLT', '卫生间'],
            'ignore_word': list(set(BASIC_IGNORE_WORDS['basic']) - {'家具'})
        },
        'closestool': {
            'layer_sub': ['LVTRY', '洁具', 'FURN', 'Lavatery', '厨.*卫', 'AUDIT_I', 'A-FLOR-SPCL', 'WC', '家具', '卫浴', '洁厨',
                          'TOLT', '卫生间'],
            'ignore_word': list(set(BASIC_IGNORE_WORDS['basic']) - {'家具'})
        },
        'diamond_bath': {
            'layer_sub': ['LVTRY', '洁具', 'FURN', 'Lavatery', '厨.*卫', 'AUDIT_I', 'A-FLOR-SPCL', '家具', '卫浴', '洁厨', 'TOLT',
                          '卫生间'],
            'ignore_word': list(set(BASIC_IGNORE_WORDS['basic']) - {'家具'})
        },
        "mentou": {  # 门头
            "layer_sub": [".*"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"线"}) +
                           ["DOTE", "填充", "wind", "LMW", "WIN", "A[-_]ELEV[-_]METL"],
        },
        "elevation_handrail": {  # 立面栏杆
            "layer_sub": ["栏杆", "HRAL", "handrail", "RAIL", "HDWR", "SC-LINE", "hdrl", "栏杆", "BALCONY", "HANDRAIL",
                          "阳台", "Rail", "HRAL", "blcn", "Hdrl", "HANDRA", "AE-HDWR", "护栏", "A_HDWR", "RALL"],
            # "STAIR"暂时去掉
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"LINE"}) + ["STAIR-栏杆", '^GX阳台$', '阳台排水'],
        },
        "dayang_handrail": {  # 剖面栏杆
            "layer_sub": ["栏杆", "handrail", "RAIL", "HDWR", "hdrl", "栏杆", "BALCONY", "HANDRAIL", "阳台", "Rail",
                          "HRAL", "blcn", "Hdrl", "HANDRA", "AE-HDWR", "护栏", "A_HDWR", "RALL", "BALOORY"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ['DIM', 'SYMB', '^GX阳台$', '阳台排水'],
        },
        "plan_handrail": {  # 平面栏杆（既用于空间分割，也用于构件）
            "layer_sub": ["扶手", "栏杆", "BALCONY", "HANDRAIL", "阳台", "Rail", "HRAL", "blcn", "Hdrl", "HANDRA",
                          "AE-HDWR", "护栏", "A_HDWR", "RALL"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ['^GX阳台$', '阳台排水'],
        },
        "pave": {  # 铺装
            "layer_sub": ["pave"],
            "ignore_word": ["PAVE-HATCH", "pavinghatch"],
        },
        "elevation_window": {  # 立面窗
            "layer_sub": ["wind", "lmw", "WIN", "窗户", "DRWD", "窗线", "窗边", "门窗", "D&W", "立面开启扇",
                          "A[-_]ELEV[-_]METL", "立面.*窗"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["sher", "WINDOW[-_]BLIN", "开启", "A[-_]EQPM[-_]WIND",
                                                          "A[-_]ELEV[-_]WIND[-_]GRAY"],
        },
        "elevation_window_open_line": {  # 立面窗开启线
            "layer_sub": ["门窗开启", "窗户开启", "立面-材料填充", "大样-填充", "^A[-_]ELEV[-_]RIP$", "^A[-_]SECT[-_]THIN$",
                          "A[-_]PATN[-_]MATE.*图案填充", "PUB_HATCH", "PUB-HATCH"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "elevation_mark": {
            "layer_sub": ["A-Anno-Levl", "P-ROAD-ELEV", "DIM_ELEV", "ELEV_DIM", "标高", "GCD", "A[-_]SYMB[-_]LEVL.*相对标高",
                          "A[-_]ANNO[-_]IDEN[-_]LEVL", "DIM[-_]ELEV", "DIM[-_]ELEV[-_]标高标注",
                          "A[-_]ANNO[-_]IDEN[-_]TEXT", "0A[-_]A[-_]SYMB[-_]ELEV", "A[-_]Anno[-_]Levl",
                          "建[-_]标高", "A[-_]SYMB[-_]LEVL.*标高", "A[-_]Elv.*建筑标高", "A[-_]2[-_]Elev",
                          "IDEN[-_]LEVL", "A[-_]LEVEL", "G[-_]ANNO[-_]LEVL", "A[-_]DIM[-_]ELEV", "DIM[-_]ELEV",
                          "DIM[-_]ELEV[-_]标高标注", "A[-_]ANNO[-_]LEVL", "A[-_]SYMB[-_]LEVL.*标高", "A[-_]Elv.*建筑标高",
                          "G[-_]ANNO[-_]LEVL", "A[-_]ANNO[-_]IDEN[-_]LEVE", "FLOR-LEVL", "SYMB_标高_A", "AD-LEVL-HIGH",
                          "A-ANNO-LEVEL-DIMS-1", "A-DIN-ELEV", "A-注释-标高", "A-标高标注", "A-标注-标高", "标高", "C-标高", "b标高",
                          "A-Elv(建筑标高)", "A_N_DIM_ELEV", "建-符号", "A-ELEVEL", "C-LEVEL", "D-天-天花标高"],
            "ignore_word": ["^地面标高$"]
        },
        "structure": {
            "layer_sub": ["stru", "结构", "墙", "column"],
            "ignore_word": []
        },
        "wall_hatch": {
            "layer_sub": ["填充", "HATCH", "C-H"],
            "ignore_word": []
        },
        # # ZZPM005 ZZPM006 Aircontroe, indoor_space地上二三层分割使用
        # "second_third_space": {
        #     "layer_sub": [".*"],
        #     "ignore_word": list(set(
        #         ['DIM', 'ANNO', 'AXIS', 'DOTE', 'TEXT', 'SYMB', 'SIGN', 'FURN', '家具', 'LVTRY', '厨', '卫', 'TOLT'] +
        #         ["空调", "AIRCONDITION", "空_", "A-EQPM-MECH", "AE-EQPM-SMAL", "M_AC", "KT-室外机"] +
        #         ['INDX', 'INDEX', "索引"] + ['251', 'HEVY', 'XD', 'HDWR'] +
        #         ['SY', '示意'] + ['TWT_LEAD', '穿孔']) - {'line', '看线'}),
        # },
        "second_third_space": {  # 雨棚边界图层
            "layer_sub": ["雨棚", "雨蓬", "雨篷", "腰线", "栏杆", "看线", "建-门窗", "建-墙-完成面", "附线", "WJ", "WINDOW",
                          "WALL", "S饰线", "SURFACE", "STAIR", "SEE", "S-BORDER", "ROOF", "线脚", "0A-O-HOLE",
                          "PUB_HATCH", "LINE", "A-P-FLOR$", "BEAM", "建-保温", "A-BALC", "_TCH_KEY", "一体板"],
            "ignore_word": ["WINDOW[-_]BLIN", "A-STAIR-电梯"],
        },
        "indoor_access": {
            "layer_sub": ["stair", "梯"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"线"}) + ["STAIR-栏杆"],
        },
        "elevation_window_exclude": {
            "layer_sub": ["涂料", "门窗开启线", "XD-LEVL-HIGH", "立面修改", "A_PATN_MATE", "HATCH-H", "^0$"],
            "ignore_word": []
        },
        "elevate_biaogao": {  # 立面标高（没找到，补充的）
            "layer_sub": ["标高", "DIM", "PUB_TEXT"],
            "ignore_word": []
        },
        'garage': {  # 车库
            "layer_sub": ["地下室", '铺装', '地库'],
            "ignore_word": ['INT', 'AXIS', 'UDBD', 'SLC']
        },
        "annotation": {  # 标注内容图层 云效 258480 楼梯大样截断线图层在其中
            "layer_sub": ["DIM", "SYMB", "ANNO", "INDX", "A-DETL-DAS"],  # 0A-DETL-DAS虽然不是截断线，但是可以作为外轮廓
            "ignore_word": ["ELEV"],  # 将标高的图层过滤
        },
        "stair_dayang_plan_stair": {  # 楼梯大样平面图楼梯直线图层
            "layer_sub": ["EVTR", "Stair", "STAIR", "Lift", "LIFT", "电梯", "楼梯", "梯", "FIT", "ELEV", "elevator", "STRS",
                          "EQPM", "STAR", "轿厢", "STR$"],  # STR-256817平面图楼梯
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"LINE"}) +
                           ["SMAL", "BALC", "ELEC", "LIHT", "CLNG", "FIRE", "HYDR", "MECH", "PLOM", "SYMB", "KICH",
                            "ASSI", "TOLT", "PRKG", "RAIL", "^FIT$", "STAIR-栏杆", "CAR", "TACC", "洁具", "A[-_]EQPM",
                            "剖梯.*虚", "JACK", "M-DUCT-AIRD-EQPM", "DIM", "A-ELEVEL"],
        },  # SYMB-ELEV标高三角
        "stair_dayang_profile_stair": {  # 楼梯大样剖面图楼梯直线图层
            "layer_sub": ["WALL", "STRS", "内墙面", "slab", "AE-SUFC", "DETL-THREAD", "COLS", "A-DETL-2", "ELVE.*OVER",
                          "ELVE.*LINE", "^A[-_]SURF$", "^面层$", "^WD$", "^C$"],
            "ignore_word": ["RAIL", "JACK"],
        },
        "yu_liu_kong_dong": {  # 预留孔洞图层 分类结果为reserved_hole
            "layer_sub": ["洞口", ".*留洞", "[0-9][-_].*洞", ".*孔洞", "空调孔"],
            "ignore_word": ["DOTE", "WALL", '.*管', 'WINDOW', '.*空调$'],
        },
        "annotation_line": {  # 引线图层、箭头图层
            "layer_sub": ["DIM", "IDEN", "ANNO", "SYMB", "LEAD", "0[-_]坐标标注", "NO\..*编号", "TEXt", "-TEXT",
                          "F-废水-TEXT", "W-污水-TEXT", "YT-阳台雨-TEXT", "污水文字", "废水文字", "雨水文字", "凝结水文字",
                          "通气文字", "P-负一层消火栓标准", "A[-_]INDEX", "DIM[-_]LEAD", "DIM[-_]IDEN",
                          "A[-_]ANNO[-_]IDEN[-_]TEXT", "A[-_]ANNO[-_]NOTE", "J[-_]YCBZ", "0A[-_]A[-_]SYMB[-_]INDE",
                          "建[-_]索引符号", "建[-_]引出", "[AJ][-_]INDX.*索引", "A[-_]HOLE[-_]NOTE.*留洞编号注释",
                          "A[-_]INDEX", "A[-_]Index.*建筑索引线剖切号线", "IDEN[-_]TEXT", "A[-_]3[-_]Lead",
                          "A[-_]标注[-_]引出", "A[-_]ANNO[-_]IDEN[-_]LEAD", "DIM_LEAD_引出标注", "A_DIM_LEAD",
                          "D_T_HoleConText（结构留洞标注）"
                          "J-索引标注", "J-引出标注", "0A-A-SYMB-INDE", "A-INDEX", "IDEN-TEXT", "A-ANNO-IDEN-INDX",
                          "A_INDX(索引)", "A-索引标注",
                          "A-引出标注", "A-N-DIM-LEAD", "J-符号", ".*符号$", "家具.*标注"],
            "ignore_word": ["PUB", "标高", "红线", "流线", "坐标", "尺寸", "中线", "ELEV", "^TWT[-_]SYMB$", "FROM",
                            "FORM", "GRID", "A-COND-IDEN-TEXT", "LEVL", "LEVEL", "P[-_]FS[-_]EQPM[-_]TEXT",
                            "A[-_]DIM[-_]AXIS", "A[-_]ANNO[-_]NOTE", "A[-_]ANNO[-_]DIMS"],
        },
        "engineering_work_table_line": {
            "layer_sub": ["HS-A-说明文字", '通用-轴网标注', "ANNO-TABS", "底框", "0-TTLB", "A-BORD", "TK",
                          "AAD-A1$0$AAD-FR-LINE", "图框线", "A-文字-功能", "PUB_TAB", "表"],
            "ignore_word": []
        },
        "filter_road_layer": {
            "layer_sub": ["挡土", "绿化", "绿地", "公共设施", "植被", "土质", "地貌", "LAND-GREEN", "看线", "patt",
                          "景观", "铺地", "BAD_LAYER", "A-Detl-Thin"],
            "ignore_word": []
        },
        "completion_surface": {  # 空间完成面图层，如果需要空间完成面，则需要配置该图层和墙图层；将之前的 dayang_space_completion 剖面空间完成面图层加到该图层中
            "layer_sub": ["AE-SUFC", "A[-_]FLOR.*边缘", "SURFACE", "建[-_]楼面", "P[-_]粉刷线", "F[-_]粉刷",
                          "S[-_]SURFACE", "A[-_]DETL[-_]THIN", "THREAD", "thread", "抹灰", "细线", "SURFACE[-_]粉刷",
                          "SURFACE[-_]保温层", "A-SURF", "D-SURFACE", "A_外饰面线_粉刷", "HYP-SURF-PAIN", "DETL-SURF",
                          "建-详-面层", "A-SECT-FLOR", "0A-S-WALL-FINI", "A_FINISH", "A_面层", "A-墙体-面层", "LA-SECT-室内-面层-涂料",
                          "建-GROUND", "面层线", "WY-抹灰", "J-抹灰线", "m抹灰线", "AREA", "详图粉刷面层", "A-DETL-LIN2"],
            "ignore_word": ['DIM', 'SYMB'],
        },
        "kan_xian": {  # 看线
            "layer_sub": ["建筑.*看线"],
            "ignore_word": [],
        },
        # "handrail_completion_surface": {  # 栏杆完成面图层
        #     "layer_sub": ["SURFACE", "建[-_]楼面", "P[-_]粉刷线", "F[-_]粉刷", "S[-_]SURFACE", "A[-_]DETL[-_]THIN",
        #                   "SURFACE[-_]粉刷"],
        #     "ignore_word": []
        # },
        # "window_completion_surface": {  # 窗户完成面图层
        #     "layer_sub": ["A[-_]FLOR.*边缘", "SURFACE", "建[-_]楼面", "P[-_]粉刷线", "F[-_]粉刷", "S[-_]SURFACE",
        #                   "A[-_]DETL[-_]THIN", "SURFACE[-_]保温层"],
        #     "ignore_word": []
        # },
        "decoration": {  # 装饰物图层，目前只用于规则43
            "layer_sub": ["穿孔铝板"],
            "ignore_word": []
        },
        "mailbox": {  # 信报箱
            "layer_sub": ["A[-_]HDWR.*配件", "A[-_]WALL[-_]METL", "信报箱", "AE[-_]FURN[-_]MOVE", "长厦安基标准家具",
                          "0A[-_]B[-_]WIND[-_]SHER", "P平[-_]FURN1", "A[-_]DETL[-_]WOOD", "A[-_]FURN", "FUR",
                          "A[-_]FLOR[-_]TPTN", "EQU[-_]固定家具[-_]A", "FURN", "A[-_]活动家具", "EQU[-_]活动家具[-_]A",
                          "家具", "AE[-_]ELEV[-_]2", "FURNITURE", "ETTERTA[-_]FURN", "A[-_]FLOR[-_]HRAL",
                          "0A[-_]O[-_]EQPM", "DIM[-_]LEAD", "P[-_]家具", "EQU[-_]固定家具_A", "活动家具",
                          "AE[-_]EQPM[-_]KICH", "AE[-_]EQPM", "LA[-_]PLAN[-_]FURN", "J[-_]活动家具",
                          "建[-_]家具[-_]固定家具", "A[-_]FLOR", "FURNITURE[-_]详图家具", "J[-_]家具线",
                          "AE[-_]FLOR", "A[-_]FLOR[-_]HRAL", "FURNITURE[-_]平面家具", "A3[-_]FLOR[-_]FTMT.*家具信报箱",
                          "A_FLOR_FTMT_MOVE(可移动式家具)", "F-家具", "A_FLOR_FTMT(家具)", "I-Furn", "J-固定家具",
                          "A_FLOR_FTMT_MOVE(可移动式家具)",
                          "A_信报箱", "ETTERTA-FURN", "A_FLOR_FTMT_FIXD(固定家具)", "C-信报箱", "P平-FURN1", "A-FURN", "BLOCK 家具",
                          "a-活动家具", "0-家具", "A-FURN-FIXD", "A-楼面-家具", "--活动家具", "0A-O-FURN", "A-家具",
                          "A_FLOR_FTMT_FIXD(固定家具)",
                          "J-建-平-家具"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "kitchen_exhaust_pipe": {  # 厨房排烟管道
            "layer_sub": ["AE-HOLE", "管道", "A[-_]FLOR[-_]SPCL", "A[-_]FLOR[-_]FLUE", "A[-_]烟道风道",
                          "AE[-_]EQPM[-_]TOLT", "FLUE", "A[-_]FIXT", "LVTRY", "洁具", "A[-_]OTHER", "PUB[-_]HATCH",
                          "建筑[-_]排气道", "EQU[-_]厨.*卫设备[-_]A", "通风道", "新风", "厨.*卫", "C厨厕", "排烟道",
                          "A[-_]STRU[-_]SLAB", "建[-_]平[-_]风道烟道", "厨.*卫设备[-_]A1", "011[-_]厨.*卫固定",
                          "EQU[-_]厨.*卫设备[-_]A", "排气道", "烟井管道", "P[-_]排烟道", "P[-_]洁具及厨具", "A[-_]洁厨具",
                          "烟道", "风道", "A[-_]EQPM[-_]CHAN", "Y烟风道", "M[-_]ventilation", "A[-_]洁厨具",
                          "EQU[-_]厨.*卫设备", "YD", "建[-_]洁具", "A[-_]风道", "管井", "A7烟气管道", "厨房设备",
                          "A-烟道", "EQU_厨卫设备", "EQUI-FLUE", "C-厨房设备", "A-厨卫器具", "C-厨卫", "建-平-风道烟道",
                          "排风道", "A-FURN-排风道", "QN-J-厨卫"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "basement_contour": {  # 地库轮廓
            "layer_sub": ["地下车库范围线", "Z[-_]地下室边线", "D[-_]地下室", "0[-_]地库轮廓", "Z[-_]地下室边线",
                          "地下车库", "D地下室轮廓线.*-1F", "地下室轮廓线", "d地下室", "地下室边线", "ZT[-_]PM[-_]地下室",
                          "地库范围", "F[-_]Ctrol[-_]line地下室控制线", "H15[-_]地下车库范围", "A[-_]SITE[-_]BASE",
                          "dikulunkuo", "GH地下车库范围线", "JZW[-_]地下车库轮廓线", "地下车库范围线", "02[-_]地库范围[-_]1",
                          "E[-_]地库轮廓线", "HS-A-轮廓线-地下室", "地库轮廓线", "-1F地下室边线", "BLDG-BASE", "ZT_地下室轮廓线", "地下室范围线",
                          "D 地下室边线", "a-地下室范围线", "Z-地下室边线", "-ZT-PM-地下室轮廓线", "0-地下室轮廓线", "地库边界", "A_SYMB_BOAD(地下室轮廓线)",
                          "D地下室轮廓线",
                          "01-地库轮廓线", "J-车库轮廓", "A-地下车库轮廓线", "D-地下范围线(-1F)", "GH地下车库范围线", "Z-建筑地下轮廓", "G-轮廓-规划-地下",
                          "车库边界线"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "extinguishing_ascend_field": {  # 消防登高场地
            "layer_sub": ["Z[-_]消防登高面", "0[-_]消防", "消防登高面", "登高场地", "HHDZ[-_]XF[-_]消防登高",
                          "H11[-_]消防登高场地", "ZX[-_]消防扑救示意", "Sy[-_]登高场地", "00[-_]消防登高场地", "A[-_]消防登高面",
                          "ZT[-_]XF[-_]消防登高", "地上[-_]消防登高场地", "0[-_]消防登高面", "33[-_]消防扑救场地",
                          "X[-_]消防扑救场地", "X[-_]消防登高场地", "P[-_]消防登高场地", "E[-_]消防登高面", "消防登高操作场地", "LC-消防登高场地",
                          "Z_FIRE_AREA(消防操作场地)", "消防扑救面", "0-消防登高场", "消防扑救", "消防操作场地", "A-FIRE-消防登高场地",
                          "消防车登高场地", "G-注释-消防登高场地", "G-FIRE", "A-登高面", "Z-FIRE-SITE(登高场地)", "G-FIRE-CLSF(消防登高场地)",
                          "X-消防扑救面", "0-道路-消防登高场", "扑救场地", "lf-消防扑救面", "YS消防扑救面", "GH消防救援场地", "交通-消防登高面",
                          "Z_FIRE_AREA(消防操作场地)", "0-消防场地", "ZPM-XF-消防扑救场地", "0-消防扑救场地", "A-Anno-Fire Protection Zone",
                          "总平面-消防登高场地", "Z-XF-登高场地", "A-SITE-FIRE", "^FIRE[-_]WORK$"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "fire_compartment_sketch_contour": {  # 防火分区示意图轮廓线
            "layer_sub": ["0A[-_]P[-_]FIRE", "防火分区", "轮廓", "分区线", "A[-_]ZP[-_]地下室轮廓",
                          "A[-_]AREA[-_]FIRE", "SPACE[-_]ALL"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
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
        "garage_exit": {  # 车库出入口范围
            "layer_sub": ["0A[-_]P[-_]RKNG[-_]STRP", "00[-_]出入口指示", "P[-_]ROAD[-_]DRWY", "LA[-_]MASTER.*PLAN[-_]ROAD",
                          "Z[-_]地下停车[-_]出入口", "D[-_]地下出入口", "地库出入口", "00[-_]共用[-_]地下车库出入口", "0-车库坡道", "AE-STAR",
                          "P-BUID-STAR", "w-入口车道", "LA-MASTER PLAN-地库出入口", "8-车库入口", "0-车库出入口", "地下车库入口"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "cut_off_line": {  # 截断线
            "layer_sub": ["DIM[-_]SYMB", "A[-_]ANNO[-_]IDEN", "DIM[-_]SYMB[-_]剖切标注", "SYMB_折断线及跑向_A", "0A-A-SYMB",
                          "A-注释-符号", "A_N_DIM_SYMB"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "garage_podao_exit": {  # 地库坡道出入口
            "layer_sub": [".*"],
            "ignore_word": ["DIM", "SYMB", "ANNO", "INDX", "A-DETL-DAS", "PARK", "park", "车位", "CAR", "AE-EQPM",
                            "PRKG", "快充", "慢充", "无障碍", "泊位", "pkng", "che", "A-Pkng-Vhel-Mini", "^车$",
                            "A-1-Pkng", "^0$"] +  # 车位图层
                           ["厨.*卫", "LVTRY", "洁具", "FLOR[-_]SPCL", "FIXT", "SANR", "EQPM[-_]ASSI", "TOLT", "Lavatory",
                            "EQPM[-_]KICH", "标配部件[-_]厨房卫生", "EQPM[-_]TACC", "厨房卫生间", "卫生间", "FURN",
                            "MILL.*PLUMB", "Lavatery", "WC", "家具", "卫浴", "洁厨", "AUDIT[-_]I", "BATH", "TPTN", "FUR",
                            "A-FLOR-SANI", "厨房厕所", "厨具", "A[-_]EQPM", "厨房设备"] +  # 厨卫图层
                           ["EVTR", "Stair", "STAIR", "Lift", "LIFT", "电梯", "楼梯", "梯", "FIT", "ELEV", "elevator",
                            "STRS",
                            "EQPM", "STAR", "轿厢", "STR$"] +  # 楼梯图层
                           ["栏杆", "HRAL", "handrail", "RAIL", "STAIR", "HDWR", "SC-LINE", "hdrl"] +  # 栏杆图层
                           ["WINDOW", "DOOR", "门", "D&W", "W&D", "WIN", "DOWI"] +  # 门图层
                           ["WINDOW", "WIN", "窗", "DRWD", "WIND", "Window", "D&W", "W&D", "L-玻璃", "DOWI", "dowi",
                            "GLAZ"] +  # 窗户图层
                           ["用地红线", "0[-_]规设[-_]11.*规划用地界线", "HHDZ[-_]0[-_]用地红线", "D01征地范围红线",
                            "用地红线", "规划用地红线", "A[-_]用地红线", "G[-_]通用[-_]用地红线", "M[-_]用地红线[-_]REDL",
                            "^000辅助线$"] + ["红线", "LINE-RED", "LIMT", "REDL"] +  # 用地红线图层
                           ["A[-_]AXIS[-_]CRCL.*轴线圈", "AXIS", "0A[-_]A[-_]GRID[-_]NOTE", "ACO[-_]AXIS[-_]NUMB",
                            "AL[-_]DIMS[-_]AXIS.*轴线标注", "AXIS[-_]轴号[-_]A", "A[-_]Grid[-_]Iden", "A[-_]AXIS",
                            "P[-_]BUID[-_]AXIS", "AXIS[-_]轴标", "AXIS[-_]轴号[-_]A", "P[-_]BUID[-_]AXIS",
                            "ACO[-_]AXIS[-_]NUMB", "AXIS[-_]轴标"] +  # 轴标图层
                           ["TY", "WATER", "排水", "水沟", "水井", "水坑", "GUTT", "WELL", "GLASS", "Stair", "STAIR", "Hole",
                            "SUMP", "FZ", "水管井", "DICH-ARCH", "DICH-STRU"] +  # 排水沟图层
                           ["DIM", "IDEN", "ANNO", "SYMB", "LEAD", "0[-_]坐标标注", "NO\..*编号", "TEXt", "-TEXT",
                            "F-废水-TEXT", "W-污水-TEXT", "YT-阳台雨-TEXT", "污水文字", "废水文字", "雨水文字", "凝结水文字",
                            "通气文字", "P-负一层消火栓标准", "A[-_]INDEX", "DIM[-_]LEAD", "DIM[-_]IDEN",
                            "A[-_]ANNO[-_]IDEN[-_]TEXT", "A[-_]ANNO[-_]NOTE", "J[-_]YCBZ", "0A[-_]A[-_]SYMB[-_]INDE",
                            "建[-_]索引符号", "建[-_]引出", "A[-_]INDX.*索引", "A[-_]HOLE[-_]NOTE.*留洞编号注释",
                            "A[-_]INDEX", "A[-_]Index.*建筑索引线剖切号线", "IDEN[-_]TEXT", "A[-_]3[-_]Lead",
                            "A[-_]标注[-_]引出", "A[-_]ANNO[-_]IDEN[-_]LEAD"] +  # 引线图层
                           ["VPIPE", "立管", "S_EQUIPMENT", "雨水", "冷凝管", "给水", "污水管", "消防管", "废水管", "EQPM-PLUM",
                            "EQUIP_\*水\*", "DRAI-EQPM", "EQPM-DRAI", "VERT_PIPE", "P-.{13}-L", "WATER", "排水", "^水$",
                            "水管", "0P-ACC-FD", "LG", "lg", "PUB_STRM", "封管井", "^A-SAN$", "EQPM-PUMB", "PIPE-RISR-WATR",
                            "A-DRAI", "P-SWER-SILO", "QN-N-燃气", "DSEW"] +  # 立管图层
                           ["填充", "HATCH", "C-H"] +  # 墙填充图层
                           ["DIM", "SYMB", "ANNO", "符号标注", "AD-SIGN", "DIM[-_]SYMB", "A[-_]ANNO[-_]SYMB",
                            "0A[-_]A[-_]SYMB", "A[-_]Anno[-_]Dims", "建[-_]箭头", "A[-_]Index.*建筑索引线剖切号线",
                            "A[-_]3[-_]Symb", "A[-_]TEXT", "G[-_]ANNO[-_]INDX", "A[-_]ANNO[-_]IDEN",
                            "A[-_]FLOR[-_]STRS"] +  # 箭头图层
                           ['DESG设计建筑', '建筑首层', '建筑轮廓', 'ROOF-WALL', '外墙轮廓', 'BULD-BMAX', '空墅', 'BUID',
                            '商业轮廓线', '设计建筑', 'BLDG-FACILIT', 'Wall', 'WALL', '屋顶轮廓', 'SITE-BLDG', 'OUTD-BUID',
                            'COLUMN', 'WINDOW', "WIN", 'A-Wind', 'A-Blcn', 'PLAN_建筑基底轮', 'JZW_Close', 'AUDIT_I_12',
                            '总图外墙', '箱变', '建筑标准层轮廓', '建筑屋顶平面', 'DOOR_FIRE', '建构筑物轮廓线', '建筑标准层',
                            '^0-建筑$', '规划建筑', '现状建筑', 'P-BULD-BMAX', '住宅建筑', 'A_HDWR(配件)',
                            'A_FLOR[（(]边缘[)）]', 'BD-主体', '新建建筑', 'A-EQPM-MECH', 'Z_0_EXST[（(]现有建筑[)）]',
                            'G_COL', 'Z-0-ZBW', '00-共用-建筑轮廓加粗', '^总图$', '^轮廓$', '3T_WOOD', '^0G-SITE$',
                            '地下设备房', '建筑主轮廓', 'G-FLOR', "Z[-_]BUILDING"] +  # 建筑轮廓图层
                           ["A-Anno-Levl", "P-ROAD-ELEV", "DIM_ELEV", "标高", "GCD", "A[-_]SYMB[-_]LEVL.*相对标高",
                            "A[-_]ANNO[-_]IDEN[-_]LEVL", "DIM[-_]ELEV", "DIM[-_]ELEV[-_]标高标注",
                            "A[-_]ANNO[-_]IDEN[-_]TEXT", "0A[-_]A[-_]SYMB[-_]ELEV", "A[-_]Anno[-_]Levl",
                            "建[-_]标高", "A[-_]SYMB[-_]LEVL.*标高", "A[-_]Elv.*建筑标高", "A[-_]2[-_]Elev",
                            "IDEN[-_]LEVL", "A[-_]LEVEL", "G[-_]ANNO[-_]LEVL", "A[-_]DIM[-_]ELEV", "DIM[-_]ELEV",
                            "DIM[-_]ELEV[-_]标高标注", "A[-_]ANNO[-_]LEVL", "A[-_]SYMB[-_]LEVL.*标高", "A[-_]Elv.*建筑标高",
                            "G[-_]ANNO[-_]LEVL", "A[-_]ANNO[-_]IDEN[-_]LEVE"] +  # 标高图层
                           ["雨棚", "雨蓬", "雨篷", "腰线", "栏杆", "看线", "建-门窗", "建-墙-完成面", "附线", "WJ", "WINDOW",
                            "WALL", "S饰线", "SURFACE", "STAIR", "SEE", "S-BORDER", "ROOF", "线脚", "0A-O-HOLE",
                            "PUB_HATCH", "LINE", "A-P-FLOR$", "BEAM", "建-保温", "A-BALC"] + ["功能用房"],  # 雨棚边界图层
        },  # 暂时过滤掉0图层
        "water_pit": {  # 集水坑
            "layer_sub": ["集水坑", "0P[-_]A[-_]DIM", "集水井", "SUMP", "S[-_]MINI[-_]EQPM.*小型设备", "TK", "P[-_]STRT",
                          "EQUIP[-_]污水", "P[-_]EQPM", "A[-_]DRAIN", "0P[-_]WELL[-_]WW", "EQPM[-_]PUMB",
                          "WELL[-_]WW", "RF[-_]坑", "P[-_]J[-_]EQPM", "AE-EQPM", "排水管", "排水组织",
                          "AE-DICH-STRU", "Bsmt_drain", "STELL"],  # "排水沟",
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["CARS", ],
        },
        "san_shui": {  # 散水
            "layer_sub": ["楼面-地面", "RAIL", "看线", "EVTR", ],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + [],
        },
        "chu_wei": {  # 热水器 燃气表
            "layer_sub": ["设备", "厨具", "FURN", "家具"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + [],
        },
        "plaster_line": {  # 石膏线
            "layer_sub": ["ED", "大样", "D-SECT"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["大样-填充", "REDL"] +
                           ['ED-ED4_DIM', 'E-ED4_DIM', 'E-ED7_INDEX', 'ED-ED5_TXT', 'D-SECT6_HATCH']
        },
        "limian": {
            "layer_sub": ["立面"],
            "ignore_word": []
        },
        "floor_pavin": {  # 地面铺贴
            "layer_sub": ["地面开线", "FLOORDIM", "地面标注"],
            "ignore_word": []
        }
    }

    BASIC_LAYERS = {
        "basic": ["wall", "axis_net"],  # 去掉了 border
        "indoor_segment": ["wall", "pillar", "segment", "segment_extra", "elevation_handrail", "dayang_handrail",
                           "plan_handrail"],  # 去掉了 border
        # 暂时删除 "indoor_first_floor_segment"，因为经过评估，"segment_lobby_platform" 不适合作为空间图层，可以直接在规则中使用
        # "indoor_first_floor_segment": ["wall", "pillar", "segment", "segment_extra", "segment_lobby_platform", "border"],
        "underground_segment": ["wall", "pillar", "segment", "segment_extra", "elevation_handrail", "dayang_handrail",
                                "plan_handrail"],  # 去掉了 border
        "building_segment": ["building", "door", "window"],
        "second_third_segment": ["wall", "pillar", "segment", "segment_extra", "second_third_space",
                                 "elevation_handrail", "dayang_handrail", "plan_handrail"],  # 去掉了 border
        "indoor_access_segment": ["wall", "pillar", "segment", "segment_extra", "indoor_access", "elevation_handrail",
                                  "dayang_handrail", "plan_handrail"],  # 去掉了 border
        "stair_dayang": ["wall", "pillar", "annotation", "stair_dayang_plan_stair", "stair_dayang_profile_stair",
                         "elevation_handrail", "plan_handrail"],  # 去掉了 border
        "elevation_shelter": ["decoration"],
    }

    COMBINATION_EXCLUDE_LAYERS_INDOOR = [
        "wall", "segment", "pillar", "mentou", "wall_hatch", "hatch", "second_third_space", "pipe_barrier",
        "hatch_outline", "annotation_line", "text_with_bound_vertex", "text", "lobby_platform_border", "segment_extra",
        "podao_edge", "decoration", "solid_wall_line", "non_solid_wall_line", "mleader", "elevation_window_open_line",
        "annotation", "axis_grid"
    ]  # hatch_outline-规则62，pillar_line在LAYERS_WITH_SLOPE_LINE_REVISED中有

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
        "elevation_window_open_line", "annotation", "axis_grid",
    ]

    # 分图层打印配置
    INDOOR_DRAWING_PRINT_LAYER_SEPARATE_SET = {
        'set_1': ['pipe', 'floor_drain', 'door', 'elevator_door', 'window', 'air_conditioner', "water_pit"],
        'set_2': ['floor_drain_mix', 'air_conditioner_mix', 'fire_hydrant', 'elevator_box', "parking"],
        'set_3': ['floor_drain_mix', 'air_conditioner_mix', 'fire_hydrant', 'elevator_box', 'pipe', 'floor_drain',
                  'air_conditioner', 'elevator_stair', 'washbasin', 'closestool', 'diamond_bath', "chu_wei"],
        # 'set_4': ['window', 'elevator_door', 'door', 'emergency_door', 'wall', 'pillar', 'elevation_window', 'chu_wei'],
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
