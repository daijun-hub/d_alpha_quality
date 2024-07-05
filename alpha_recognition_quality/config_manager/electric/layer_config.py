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
            "layer_sub": ["EQUP", "EQUIP", "设备", "EQPM", "EQMT", "ELEC[-_]图块", "E[-_]SYSM[-_]DEVS", "E[-_]L[-_]控制"],
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
        "device_fire": {  # 消防设备（包含 安防设备）
            "layer_sub": ["(EQUP|EQUIP|设备|EQPM|EQMT).*(消防|FIRE|安防|XF)",
                          "(消防|FIRE|安防|XF).*(EQUP|EQUIP|设备|EQPM|EQMT)"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "device_light": {  # 照明设备（包含 灯）
            "layer_sub": ["(EQUP|EQUIP|设备|EQPM|EQMT).*(照明|灯|LIGH|LIGHTING)",
                          "(照明|灯|LIGH|LIGHTING).*(EQUP|EQUIP|设备|EQPM|EQMT)",
                          "灯", "E[-_]HELETPLAN[-_]EQUIP", "EQUIP[-_]照明", "E[-_]LIGT[-_]EQPM", "E[-_]TEXT[-_]PLAN",
                          "C[-_]LAMP", "E[-_]LITE[-_]LITE", "E[-_]EQUIP", "DQ2", "E[-_]照明设备"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ['天花灯'],
        },
        "device_broadcast": {  # 广播设备
            "layer_sub": ["(EQUP|EQUIP|设备|EQPM|EQMT).*(广播|BROADCAST|BORADCAST|NURS|电讯)",
                          "(广播|BROADCAST|BORADCAST|NURS|电讯).*(EQUP|EQUIP|设备|EQPM|EQMT)"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "device_box": {  # 箱柜设备（包含配电箱、动力设备）
            "layer_sub": ["(EQUP|EQUIP|设备|EQPM|EQMT).*(箱柜|BOX|QDXK|CABINET|BIN|POW|动力|强电|电力|POWR|强电设备|强电平面|QD|HLVO)",
                          "(箱柜|BOX|QDXK|CABINET|BIN|POW|动力|强电|电力|POWR|强电设备|强电平面|QD|HLVO).*(EQUP|EQUIP|设备|EQPM|EQMT)",
                          "BPM", "Q强电图块", "E-TEXT-PLAN", "EQUIP-箱柜-户箱"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["XHS"],
        },
        "device_switch": {  # 开关（注意：在 "照明设备" 中也存在开关）
            "layer_sub": ["开关", "E-COMP", "POW", "D块", "SB", "WIRE-1-X", "CORE", "SYSTEM", "E[-_]EQUIP", "Q强电图块",
                          "E[-_]SY[-_]E", "E[-_]元件设备", "E[-_]SYST[-_]SWIT[-_]WIRE", "EL[-_]SYS", "^SYST$", "DQ", "dq1", "WZ"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["插座", "消防"],
        },  # 有些开关在 WIRE-1-X 图层，通过对图元进行判断找出可能的开关图元
        "device_communication": {  # 通讯设备（包含电话）
            "layer_sub": ["(EQUP|EQUIP|设备|EQPM|EQMT).*(通讯|COMM|电话|TEL)",
                          "(通讯|COMM|电话|TEL).*(EQUP|EQUIP|设备|EQPM|EQMT)"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "jieshandai": {  # 接闪带
            "layer_sub": ["避雷", "防雷线", "WIRE-避雷", "电-接地防雷-防雷线", "WIRE-BL", "强电.*线缆", "WIRE-LP", "D_E_WIRE",
                          "WIRE-LIGHTNING", "LTNG", "arrester", "LTN_WIRE", "WIRE-接地"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"线", "LINE"}),
        },
        "yinxiaxian": {  # 引下线
            "layer_sub": ["防雷-箭头", "LWIRE", "引下线", "GEN", "引线", "电-接地防雷-箭头", "WIRE-LWTRE", "EQPM", "强电设备",
                          "LEADWIRE", "LTNG", "电[-_]标注", "防雷引下线", "E-WIRE-LINE"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"线", "LINE"}),
        },
        "wire": {  # 电线
            "layer_sub": ["WIRE", "电线", "BUSW", "照明布线", "D线", "DX", "电力线路", "导线", "线缆", "线路",
                          "E[-_]L[-_]动力", "^ELINE$", "^EL$", "WIRE-1-X", "TH[-_]wire", "E[-_]WIRE"
                          "WIRE[-_]动力", "SYST", "0D[-_]LINE", "E[-_]L[-_]照明", "XITONG", "DQ[-_]DL", "电-电力干线"],  # BUSW-总线
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"线", "LINE"}) +
                           ["WIRE-1-X", "弱电", "防雷", "接地", "ELEMENT", "E[-_]SYST[-_]SWIT[-_]WIRE",
                            "^E[-_]WIRE[-_]PWLT$", "EL[-_]SYS", "LWIRE", "ELETXT", "TEL"],
        },  # 因为有些图纸中开关和电线都画在WIRE-1-X图层，所以这里避免图层冲突，而将WIRE-1-X进行过滤，然后通过尺寸判断是开关还是电线
        "elevator_box": {  # 电梯厢/楼梯
            "layer_sub": ["EVTR", "Stair", "STAIR", "Lift", "LIFT", "电梯", "楼梯", "梯", "FIT", "ELEV", "elevator", "STRS",
                          "EQPM", "STAR", "轿厢", "STR$"],  # STR-电梯厢256817
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"LINE"}) + ["SMAL", "BALC", "ELEC", "LIHT", "CLNG",
                                                                                "FIRE", "HYDR", "KICH", "ASSI",
                                                                                "MECH", "PLOM", "TOLT", "PRKG",
                                                                                "SYMB", "RAIL"],
        },
        "elevator_stair": {  # 电梯厢/楼梯（住宅平面图）
            "layer_sub": ['EVTR', 'Stair', 'STAIR', 'Lift', 'LIFT', '电梯', '楼梯', '梯', 'FIT', 'ELEV', 'elevator', 'STRS',
                          'EQPM', 'STAR'],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"LINE"}) + ['SMAL', 'BALC', 'ELEC', 'LIHT', 'CLNG',
                                                                                'FIRE', 'HYDR', 'KICH', 'ASSI',
                                                                                'MECH', 'PLOM', 'TOLT', 'PRKG',
                                                                                'SYMB', "RAIL"],
        },
        "air_conditioner": {  # 空调
            "layer_sub": ["空调", "^空_$", "Aircontroe", "^AC$", "Aircondition", "EQPM-MECH", "EQPM-SMAL", "M_AC", "KT",
                          "FLOR-OVHD", "LA-plan-smal", "RS-A", "^A-AC$", "A[-_]FLOR[-_]AIRC"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["洞", "孔", "水", "空调管"],
        },
        "air_conditioner_mix": {  # 家具图层，含有空调的混合图层
            "layer_sub": ["家具", "FURN", "Furniture", "furn", "EQPM-MOVE", "EQPM-FIXD", "Fixt", "FTMT[-_]MOVE",
                          "设备.*洗衣机", "设备.*冰箱", "A-FLOR-SANI"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS['basic']) - {'家具'}),
        },
        "door": {  # 门
            "layer_sub": ["WINDOW", "DOOR", "门", "D&W", "W&D", "WIN", "DOWI"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立面门窗", "人防", "0-DOOR\.T", "WINDOW[-_]BLIN", "开启范围"],
        },
        "window": {  # 窗户
            "layer_sub": ["WINDOW", "WIN", "窗", "DRWD", "WIND", "Window", "D&W", "W&D", "L-玻璃", "DOWI", "dowi",
                          "0A-B-GLAZ", "百叶", "CHUANG"],  # 0A-B-GLAZ-255679
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立面门窗", "WINDOW[-_]BLIN", "0A[-_]B[-_]GLAZ[-_]OPEN"],
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
            "layer_sub": ["建-标注", "建-轴线", "axis"],
            "ignore_word": [],
        },
        "beam": {
            "layer_sub": ["BEAM"],
            "ignore_word": []
        },
        "segment": {  # 住宅平面空间识别图层
            "layer_sub": ["FLOR", "栏杆", "BALCONY", "HANDRAIL", "阳台", "Rail",
                          "HRAL", "blcn", "0425-致逸结构", "surface", "SURFACE",
                          "外包石材", "HEAT", "SILL", "空调板", "OVER", "Hdrl",  # Hdrl-248189
                          "0A-P-ROOF", "AE-FNSH", "A-VISI", "HANDRA"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + [
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
        "segment_underground": {  # 地下室空间识别
            "layer_sub": ["wall", "pillar", "door", "栏", "HANDRAIL", "Rail", "HRAL",
                          "SYMB", "PD", "坡道", "车流线", "车道中线", "行车方向", "AE-DICH-STRU",
                          "地下室墙柱线", "FLOR", "CON", "TY", "WATER", "排水", "水沟", "水井", 
                          "水坑", "GUTT", "WELL", "GLASS", "Stair", "STAIR", "Hole", "SUMP",
                          "FZ", "水管井", "AE-STAR"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["TEXT", "AXIS", "字", "编号", "标号", "名", "NAME", "AD-NUMB",
                                                          "尺寸", "道", "增补", "VALVE", "IDEN", "窗沿", "家具", "索引",
                                                          "配件", "洞口", "GUTT", "SUMP", "PARK", "0-DOOR\.T"],
        },
        "lobby_platform_border": {  # 规则523、535中用到的大堂外的 "入口平台" 区域
            "layer_sub": ["^fit$", "A-P-FLOR"],
            "ignore_word": [],
        },
        "annotation_line": {  # 引线图层
            "layer_sub": ["DIM", "IDEN", "ANNO", "SYMB", "LEAD", "0[-_]坐标标注", "NO\..*编号", "TEXt", "-TEXT",
                          "F-废水-TEXT", "W-污水-TEXT", "YT-阳台雨-TEXT", "污水文字", "废水文字", "雨水文字", "凝结水文字",
                          "通气文字", "P-负一层消火栓标准", "A[-_]INDEX"],
            "ignore_word": ["PUB", "标高", "红线", "流线", "坐标", "尺寸", "中线", "ELEV", "^TWT[-_]SYMB$", "FROM",
                            "FORM", "GRID", "A-COND-IDEN-TEXT", "LEVL", "LEVEL", "P[-_]FS[-_]EQPM[-_]TEXT",
                            "A[-_]DIM[-_]AXIS", "A[-_]ANNO[-_]NOTE", "A[-_]ANNO[-_]DIMS"],
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
        # 1206新增电气图层
        "surge_protector": {  # 浪涌保护器
            "layer_sub": ["ELEMENT", "EQUIP[-_]照明", "D[-_]E[-_]EQPM.*强电设备", "TH[-_]WIRE",
                          "电[-_]强电平面[-_]线缆[-_]绿色0[-_]40", "E[-_]DIM[-_]系统", "SB", "E[-_]EQUIP[-_]QD",
                          "0E[-_]A[-_]ELEMENT", "E[-_]EQUIP[-_]动力", "Q强电图块", "LGT1", "E[-_]POWR[-_]DEVC",
                          "电气设备[-_]接地安全", "电气设备[-_]系统元件", "PD", "E-COMP", "EQUIP", "电气",
                          "E[-_]HELETSYSTEM[-_]EQUIP", "PD", "电-强电设备-系统","ZM"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["插座", "表格"],
        },
        "transformer": {  # 变压器
            "layer_sub": ["设备框", "配电", "E[-_]EQPM[-_]DBOX", "B[-_]变电所设备", "D[-_]设备[-_]箱体", "HDWR.*配件",
                          "EES[-_]设备动力", "TEL[-_]CABINET", "EQUIP[-_]箱柜", "AE[-_]EQPM", "强电桥架", "WIRE[-_]照明",
                          "TEL[-_]TEXT", "电设备", "0[-_]电气设备", "E[-_]UNIV[-_]NOTE", "E[-_]WIRE",
                          "D[-_]E[-_]Eqpm.*强电设备","电设备","电气文字","E-TEXT","E-WIRE"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "transformer_symbol": {  # 变压器符号
            "layer_sub": ["D[-_]E[-_]EQPM.*强电设备", "D[-_]E[-_]WIRE.*强电线缆", "E[-_]DIM[-_]系统", "SB",
                          "E[-_]EQUIP[-_]QD", "0E[-_]A[-_]ELEMENT", "E[-_]ELEMENT", "Q强电图块", "0E[-_]A[-_]ELEMENT",
                          "照明平面设备层", "EQUIP[-_]动力", "TEL[-_]TEXT", "GDXT", "EQPM[-_]PWLT", "DQ[-_]Wire","core","equip","ELEMENT","ELE-WIRE-照明"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "fire_hydrant": {  # 消火栓
            "layer_sub": ["0E[-_]EQUIP[-_]CABINET", "EQUIP[-_]消火栓", "S[-_]HYDT[-_]BOX.*消火栓箱", "EQUIP[-_]消火栓",
                          "0P[-_]ACC[-_]FH", "P[-_]HYDT[-_]BOXX", "EQUIP[-_]箱柜", "0P[-_]ACC[-_]FH", "EQUIP[-_]消防",
                          "XF[-_]消火栓[-_]W", "消火栓", "0E[-_]EQUIP[-_]CABINET", "EQUIP[-_]消火栓",
                          "S[-_]HYDT[-_]BOX.*消火栓箱", "0P[-_]ACC[-_]FH", "P[-_]Hydt[-_]Boxx", "EQUIP[-_]箱柜",
                          "FH", "A[-_]HOLE[-_]WALL","XF","A-fire","A-LD","GPS-消火栓","P-消火栓箱", "XHS"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["QJ"],
        },
        "fire_resistant_shutter_controller": {  # 防火卷帘控制器
            "layer_sub": ["D[-_]E[-_]EQPM.*强电设备", "EQUIP[-_]照明", "EQUIP[-_]箱柜", "0E[-_]EQUIP[-_]FIRE",
                          "EQUIP[-_]消防", "X消防图块", "EQUIP[-_]通讯", "0E[-_]EQUIP[-_]LIGHTING", "E-EQUIP",
                          "电[-_]强电箱柜", "0E[-_]EQUIP[-_]LIGHTING", "E[-_]PLAN[-_]POWR[-_]EQUIP",
                          "E[-_]POWR[-_]EQPM", "T[-_]EQUIP", "D[-_]电箱[-_]ACjlm", "0火灾报警[-_]3电", "电气标注",
                          "电-受控设备", "EL[-_]POWER[-_]EQUIP"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["户箱"],
        },
        "shutter_door": {  # 卷帘门，防火卷帘
            "layer_sub": ["0A[-_]B[-_]D&W", "A[-_]DOOR", "0A[-_]B[-_]D&W", "F防火卷帘", "WINDOW", "A4", "A[-_]DOOR.*门",
                          "A[-_]WIND", "DOOR[-_]FIRE", "A[-_]PM[-_]WINDOWOW", "A-Wind", "0E[-_]WIRE[-_]CONTROL",
                          "DOOR[-_]FIRE", "0E[-_]EQUIP[-_]FIRE", "卷帘", "E[-_]TELE[-_]CMTB", "S[-_]BEAM",
                          "A[-_]WIN", "AXR[-_]DK[-_]AP.*A[-_]DOWI", "^A[-_]DRWD$","防火JL","-p-卷帘"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "fire_proof_door_monitor": {  # 防火门监控器
            "layer_sub": ["D[-_]EM[-_]EQPM.*消防设备", "EQUIP-消防", "E[-_]LELETPLAN[-_]EQUIP", "T[-_]EQUP[-_]FIRE",
                          "T[-_]FIRE[-_]EQPM", "EQUIP[-_]箱柜", "E[-_]EQPM"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "distribution_cabinet": {  # 配电柜
            "layer_sub": ["设备框", "DQ", "EQPM.*DBOX", "设备.*箱体", "配电", "E[-_]EQPM[-_]DBOX", "B[-_]变电所设备",
                          "D[-_]设备[-_]箱体", "HDWR.*配件", "EES[-_]设备动力", "TEL[-_]CABINET", "D[-_]E[-_]Eqpm.*强电设备",
                          "EQUIP[-_]动力", "TEL[-_]CABINET", "POWR[-_]电力大设备[-_]E", "照明平面设备层", "EQUIP[-_]箱柜",
                          "AE[-_]EQPM", "E[-_]WIRE","电设备","TEL_柜","POWER","强电桥架", "DIM_SYMB"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - set(["DIM"])) + ['D[-_]DQ'], #去掉DIM关键字去匹配含有DIM_SYMB的图层
        },
        "socket": {  # 插座
            "layer_sub": ["D[-_]E[-_]EQPM.*强电设备", "EQUIP[-_]插座", "E[-_]EQUIP[-_]QD", "0E[-_]EQUIP[-_]SOCKET",
                          "Q强电图块", "0E[-_]EQUIP[-_]LIGHTING", "E[-_]TEXT[-_]PLAN", "E[-_]HELETPLAN[-_]EQUIP",
                          "设备.*插座", "EQUIP[-_]动力", "E[-_]LIGT[-_]EQPM", "E[-_]插座设备", "D[-_]设备[-_]插座",
                          "强电.*插座","电气设备","E-UNIV-NOTE","SOCKET"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["弱电"],
        },
        "floor_indicator_light": {  # 楼层标志灯
            "layer_sub": ["EQUIP[-_]照明", "D[-_]E[-_]EQPM.*强电设备", "0E[-_]EQUIP[-_]LIGHTING",
                          "E[-_]PLAN[-_]LIGH[-_]EQUI","EQUIP-应急","电气设备"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
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
            "layer_sub": ["EQUIP[-_]插座", "EQUIP[-_]箱柜", "0E[-_]EQUIP[-_]LIGHTING", "E[-_]EQMT[-_]BIN[-_]E",
                          "EQUIP[-_]照明", "D[-_]E[-_]EQPM.*强电设备", "SOCKET", "CA", "EQUIP", "D[-_]E[-_]Eqpm.*强电设备",
                          "E[-_]LITE[-_]EQPM", "E[-_]E[-_]BOX", "0E[-_]EQUIP[-_]SOCKET","电气设备","RS-应急照明配电箱"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "residual_current_circuit_breaker": {  # 漏电断路器
            "layer_sub": ["ELEMENT", "E[-_]POWR[-_]DEVC", "D[-_]E[-_]EQPM.*强电设备", "电[-_]强电平面[-_]线缆[-_]绿色0[-_]30",
                          "电[-_]强电平面[-_]线缆[-_]绿色0[-_]40", "电[-_]强电平面[-_]设备", "PD", "EQUIP[-_]照明",
                          "E[-_]COMPONENT[-_]E", "SYS[-_]元件[-_]E", "Q强电图块", "EQUIP[-_]照明", "TERM","PD","电-强电设备-系统",
                          "ZM", "D-设备-系统元件", "电[-_]强电元件", "DQ1", "MX"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "load_switch": {  # 负荷开关
            "layer_sub": ["电气设备", "ELEMENT", "Q[-_]文字", "BXT", "E[-_]COMPONENT[-_]E", "SYS[-_]元件[-_]E", "Q强电图块",
                          "PD","电-强电设备-系统","ZM", "D-设备-系统元件"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "thermorelay": {  # 热继电器
            "layer_sub": ["电气设备", "ELEMENT", "D[-_]E[-_]EQPM.*强电设备", "LIN1", "Q强电图块","PD","电-强电设备-系统","ZM", "D-设备-系统元件"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "contactor": {  # 接触器
            "layer_sub": ["电气设备", "ELEMENT", "D[-_]E[-_]EQPM.*强电设备", "BXT", "Q强电图块", "电气", "DIM[-_]照明",
                          "EQUIP[-_]照明","PD","电-强电设备-系统","ZM", "电-灯具开关插座"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "electricity_meter": {  # 电表
            "layer_sub": ["EQUIP", "0E[-_]WIRE[-_]LIGHTING", "E[-_]POWR[-_]DEVC", "电气设备[-_]系统元件", "ELEMENT",
                          "D[-_]E[-_]EQPM.*强电设备", "Q[-_]文字", "EQUIP[-_]动力", "E[-_]SYST[-_]POWR[-_]EQPM.*动力系统设备",
                          "POWR[-_]电力小设备[-_]E", "0E[-_]TEXT", "电气", "EQUIP[-_]箱柜", "E[-_]HELETSYSTEM[-_]EQUIP","PD","电-强电设备-系统","ZM",
                          "D-设备-系统元件", "电[-_]强电箱柜"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "circuit_breaker": {  # 断路器
            "layer_sub": ["ELEMENT", "E[-_]POWR[-_]DEVC", "电气设备[-_]系统元件", "D[-_]E[-_]EQPM.*强电设备", "Q[-_]文字",
                          "PD", "E[-_]HLVO[-_]EQPM", "EQUIP[-_]照明", "SYS[-_]元件[-_]E", "Q强电图块",
                          "F[-_]HELETSYSTEM[-_]EQUIP","PD","电-强电设备-系统","ZM", "D-设备-系统元件", "E[-_]断路器"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "integrated_circuit_breaker": {  # 一体式断路器
            "layer_sub": ["电[-_]强电平面[-_]线缆[-_]红色0[-_]4", "EQUIP[-_]通讯", "0E[-_]EQUIP[-_]LIGHTING",
                          "EQUIP[-_]照明","PD","电-强电设备-系统","ZM"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "information_socket": {  # 信息插座
            "layer_sub": ["D[-_]强弱电", "SOCKET", "CA", "EQUIP[-_]通讯", "插座", "T[-_]CTCC[-_]EQPM",
                          "E[-_]GCS[-_]DEVC", "Z[-_]SOCK","弱电插座","000-弱电"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "telephone_socket": {  # 电话插座
            "layer_sub": ["插座", "A[-_]强弱电点位", "EQUIP[-_]通讯", "T[-_]CTCC[-_]EQPM", "E[-_]GCS[-_]DEVC",
                          "Z[-_]SOCK","弱电插座","000-弱电"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "television_socket": {  # 电视插座
            "layer_sub": ["插座", "A[-_]强弱电点位", "Z[-_]SOCK", "EQUIP[-_]通讯", "T[-_]CTCC[-_]EQPM",
                          "E[-_]GCS[-_]DEVC", "Z[-_]SOCK","弱电插座","000-弱电"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "underground_building": {
            "layer_sub": ["JZW_地下车库轮廓线", "2-地下车库"],
            "ignore_word": [],
        },
        "fire_hydrant_button": {  # 消火栓按钮
            "layer_sub": ["EQUIP[-_]消防", "电[-_]强电平面[-_]设备"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "fuse_protector": {  # 熔断器
            "layer_sub": ["ELEMENT", "E[-_]POWR[-_]DEVC", "电气设备[-_]系统元件", "D[-_]E[-_]EQPM.*强电设备", "Q[-_]文字",
                          "PD", "E[-_]HLVO[-_]EQPM", "EQUIP[-_]照明", "SYS[-_]元件[-_]E", "Q强电图块",
                          "G[-_]HELETSYSTEM[-_]EQUIP", "PD", "电-强电设备-系统", "ZM"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "arrow": {  # 箭头 
            "layer_sub": ["DIM_SYMB", "A-ANNO-SYMB", "0A-A-SYMB", "A-Anno-Dims", "建-箭头", "A-Index(建筑索引线剖切号线)",
                          "A-3-Symb", "A-TEXT", "G-ANNO-INDX", "A-ANNO-IDEN", "A-FLOR-STRS", "E-TEXT", "箭头", "坡向线"],
            "ignore_word": ["PUB", "标高", "红线", "流线", "坐标", "尺寸", "中线", "ELEV", "^TWT[-_]SYMB$", "FROM",
                            "FORM", "GRID", "A-COND-IDEN-TEXT", "LEVL", "LEVEL", "P[-_]FS[-_]EQPM[-_]TEXT",
                            "A[-_]DIM[-_]AXIS", "A[-_]ANNO[-_]NOTE", "A[-_]ANNO[-_]DIMS"],
        },
        "podao_edge": {  # 坡道空间的边界线, 基本上是gutter和separator的图层, 去掉stair
            "layer_sub": ["TY", "WATER", "排水", "水沟", "水井", "水坑",
                          "GUTT", "WELL", "GLASS", "Hole", "SUMP", "FZ",
                          "水管井", "DICH-ARCH", "DICH-STRU", "FLOR", "CON", "S-PUB-WCOL"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["STAR", "BALC", "UNDR"],
        },
        "weak_electric_box":{ # 弱电箱，多媒体配线箱
            "layer_sub": ["DQ-JF-TL","EQUIP-通讯", "E-SYST-SWBD", "E-PDS-DEVC"],
            "ignore_word": [],
        },
        "strong_electric_box": {
            "layer_sub": ["EQUIP-箱柜","E-POWER-SWBD"],
            "ignore_word": [],
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
        "non_solid_wall_line", "mleader"
    ]  # hatch_outline-规则62，pillar_line 在LAYERS_WITH_SLOPE_LINE_REVISED中有

    COMBINATION_EXCLUDE_LAYERS_UNDERGROUND_AND_SITEPLAN = [
        "wall", "podao", "separator", "filling", "road", "car_lane", "hatch", "red_line", "red_line_sub",
        "building", "underground_building", "podao_extra", "podao_mark", "podao_edge", "hatch_outline", "wire",
        "annotation_line", "jieshandai", "segment_underground", "text_with_bound_vertex", "text", "segment_extra",
        "segment", "solid_wall_line", "non_solid_wall_line", "mleader"
    ]

    CLASSIFICATION_EXCLUDE_LAYERS = [
        "wall", "pillar", "special_pillar", "segment", "podao", "podao_extra", "separator", "filling",
        "pillar_line", "road", "car_lane", "red_line", "red_line_sub", "building", "elevation_handrail",
        "mentou", "underground_building", "wall_hatch", "podao_mark", "structure", "elevation_window_exclude",
        "hatch", "podao_edge", "pipe_barrier", "hatch_outline", "wall_line", "wire", "wire_line", #"yinxiaxian",
        "jieshandai", "annotation_line", "lobby_platform_border", "segment_underground", "segment_extra",
        "text_with_bound_vertex", "text", "road_center_line", "solid_wall_line", "non_solid_wall_line",
        "mleader", "cabinet_contour_dict", 'transformer_contour_dict'
    ]

    # 分图层打印配置
    INDOOR_DRAWING_PRINT_LAYER_SEPARATE_SET = {
        'set_1': ['pipe', 'floor_drain', 'door', 'elevator_door', 'window', 'air_conditioner'],
        'set_2': ['floor_drain_mix', 'air_conditioner_mix', 'fire_hydrant', 'elevator_box'],
        'set_3': ['device', 'device_fire', 'device_light', 'device_broadcast', 'device_box', 'device_switch',
                  'device_communication', 'yinxiaxian', 'surge_protector', 'transformer', 'socket', 'button',
                  'fire_resistant_shutter_controller', 'fire_proof_door_monitor', 'distribution_cabinet',
                  'floor_indicator_light', 'common_lamp', 'single_tube_lamp', 'double_tube_lamp', 'triple_tube_lamp',
                  'emergency_single_tube_lamp', 'emergency_double_tube_lamp', 'emergency_triple_tube_lamp',
                  'a_model_emergency_lamp', 'equipotential_junction_plate', 'residual_current_circuit_breaker',
                  'load_switch', 'thermorelay', 'contactor', 'electricity_meter', 'circuit_breaker',
                  'integrated_circuit_breaker', 'information_socket', 'telephone_socket', 'television_socket',
                  'fire_hydrant_button', 'fuse_protector'],
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
        "总线隔离器": ["device", "device_fire", "device_communication", "device_light"],
        "配电箱": ["device", "device_box"],
        "感烟探测器": ["device", "device_fire"],
        "感温探测器": ["device", "device_fire"],
        "光警报器": ["device", "device_fire"],  # 先不考虑 "光警报器" 出现在 "device_light" 中的情况
        "区域显示器": ["device", "device_fire", "device_box"],
        "火灾自动报警按钮": ["device", "device_fire"],
        "消防应急广播": ["device", "device_fire", "device_broadcast"],
        "电话": ["device", "device_fire", "device_communication"],
        "疏散照明灯具": ["device", "device_light", "device_box"],
        "灯光疏散指示标志": ["device", "device_light", "device_box"],
        "接闪带": ["jieshandai"],
        "专设引下线": ["yinxiaxian"],
        "系统图单刀开关": ["device", "device_switch", "device_light", "device_box", "surge_protector"],  # 将不涉及和电线等图层混合的开关图层从device_switch中删除
        "系统图双切开关": ["device", "device_switch", "device_light", "device_box", "surge_protector"],  # 将不涉及和电线等图层混合的开关图层从device_switch中删除
        "电线": ["wire"],
        "灯具": ["device", "device_light", "device_box"],
        "平面图开关": ["device", "device_switch", "device_light", "device_box", "surge_protector"],  # 将不涉及和电线等图层混合的开关图层从device_switch中删除
        # 1206新增电气图层
        "浪涌保护器": ["surge_protector", "device", "device_switch", "device_light", "device_box"],
        "变压器符号": ["transformer_symbol"],
        "消火栓": ["fire_hydrant"],
        "防火卷帘控制器": ["fire_resistant_shutter_controller"],
        "卷帘门": ["shutter_door"],
        "防火门监控器": ["fire_proof_door_monitor"],
        "变压器": ["transformer", "distribution_cabinet"],
        "配电柜": ["distribution_cabinet", "transformer"],
        "插座": ["socket"],
        "楼层标志灯": ["floor_indicator_light", "device", "device_light", "device_box"],
        "普通灯": ["common_lamp", "device", "device_light", "device_box"],
        "单管灯": ["single_tube_lamp", "device", "device_light", "device_box"],
        "双管灯": ["double_tube_lamp", "device", "device_light", "device_box"],
        "三管灯": ["triple_tube_lamp", "device", "device_light", "device_box"],
        "应急单管灯": ["emergency_single_tube_lamp", "device", "device_light", "device_box"],
        "应急双管灯": ["emergency_double_tube_lamp", "device", "device_light", "device_box"],
        "应急三管灯": ["emergency_triple_tube_lamp", "device", "device_light", "device_box"],
        "A型应急照明灯": ["a_model_emergency_lamp", "device", "device_light", "device_box"],
        "按钮": ["button"],
        "等电位连接板": ["equipotential_junction_plate"],
        "负荷开关": ["load_switch", "device", "device_switch", "device_light", "device_box"],
        "热继电器": ["thermorelay", "device", "device_switch", "device_light", "device_box"],
        "接触器": ["contactor", "device", "device_switch", "device_light", "device_box"],
        "电表": ["electricity_meter"],
        "断路器": ["circuit_breaker", "device", "device_switch", "device_light", "device_box"],
        "一体式断路器": ["integrated_circuit_breaker", "device", "device_switch", "device_light", "device_box"],
        "漏电断路器": ["residual_current_circuit_breaker", "device", "device_switch", "device_light", "device_box"],
        "信息插座": ["information_socket"],
        "电话插座": ["telephone_socket"],
        "电视插座": ["television_socket"],
        "消火栓按钮": ["fire_hydrant_button"],
        "熔断器": ["fuse_protector", "device", "device_switch", "device_light", "device_box"],
        "配电箱出线回路": ["wire", "circuit_breaker", "integrated_circuit_breaker", "residual_current_circuit_breaker",
                    "thermorelay", "load_switch", "fuse_protector", "surge_protector", "electricity_meter", "contactor",
                    "device", "device_switch", "device_light", "device_box"],
        "插座分支回路": ["socket", "wire", "device", "device_box"],
        "照明分支回路": ["device", "device_light", "device_box", "common_lamp", "single_tube_lamp", "double_tube_lamp",
                   "triple_tube_lamp", "a_model_emergency_lamp", "emergency_single_tube_lamp",
                   "emergency_double_tube_lamp", "emergency_triple_tube_lamp", "wire"],
        "配电箱子图": ["wire", "circuit_breaker", "integrated_circuit_breaker", "residual_current_circuit_breaker",
                  "electricity_meter", "fuse_protector", "thermorelay"],
    }
