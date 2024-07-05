from enum import Enum

# from rule_engine.single_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig


class RuleConfig(Enum):
    # 万科审核规则列表
    VANKE_RULES = {
        DrawingType.INDOOR: [105015, 105019, 103061, 101001, 101002, 101006, 101007, 101011, 101012, 101013, 101014, 101015, 101017, 101018,
                             101019, 101020, 101021, 101029, 101053, 106001, 104003, 103001, 104005, 103024, 103026,
                             101044, 101045, 101046, 101047, 101048, 101049, 104009, 101050, 101052, 101076, 101077, 102001, 102002, 102003, 102015, 102007, 119001, 119002, 119006, 119008, 119006,  # 万翼规则
                             104046, 104012, 104014, 103004, 103005, 103006, 103007, 103009, 103010, 107002, 105008, 113001, 104015, 104016, 104022, 103012, 103013,  # 万翼规则
                             103014, 103015, 103018, 103019, 104024, 106013, # 万翼规则
                             515, 104040, 103036, 103037, 103038, 106004, 106005, 103041, 103043,
                             103044, 103045, 103046, 103047, 106008, 103049, 103050, 107008, 103055,103062, 104050, 103080,
                             103050, 103078, 105017, 103066, 104020, 103067, 103078, 106015, 106016, 103071, 103074, 106029, 106030, 106030, 103060, 103063, 107014,
                             "1102010", "1102015", "1102016", "1105001", "1105002", "1105003", "1105004", "1105005",
                             "1100005", "1100006", "1100009", "1100002", "1100001", "1100011", "1100010", "1102014", "1102020", "1100028", "1102022", "1100019", "1100027", "1100034",
                             "1100053", "1104001", "1104049", "1104014", "1104010", "1104011", "1104018", "1104012", "1104041", "1104015",   #品览规则
                             "1104044", "1104019", "1103005", "1103010", "1103015", "1103020", "1103025", "1103032", "1103035","1104027", "1104038", "1104051", "1104054", "1104052", "1104013", "1104023", #中海规则
                             "1104037", "1104016", "1104017", "1104045", "1104004", "1103001", "1103003", "1103006", "1103007", "1103008",
                             "1103004", "1103009", "1103019", "1103024", "1103026", "1103027", "1103028", "1103014", "1103022",
                             "1103033", "1103036", "1103037", "1103029", "1103031", "1103039", "1103040", "1103011", "1103016", "1103002", "1103012",
                             "1103013", "1103018", "1103023", "1103030", "1103038", "1103041", "1103042",
                             "1103021", "1103017", "1103048", "1103034", "1103044", "1103045", "1103047", "1103046"],
        DrawingType.INDOOR_BATHROOM: [],
        DrawingType.UNDERGROUND: [111003, 101004, 101005, 101008, 101009, 101010, 101025, 101028, 101030, 101058, 101060, 108005,
                                  "1102002",     # 金茂规则
                                  119005, 104010, 104017, 103011,  # 万翼规则
                                  106001, 104001, 103025, 111001, 111002, 108002, 106007, 105017, 106015, 106016, 108004, 107014, 108010,
                                  "1100003", "1100004", "1100007", "1100008", "1102008", "1104043", "1104007", "1104008",
                                  "1100034","1100043", "1100047", #品览规则
                                  "1104006", "1104031", "1104055", "1104020", "1104005",
                                  "1104009", "1104036", "1104046"],  # (3, 9)
        # DrawingType.UNDERGROUND_BASEMENT: [37],
        DrawingType.PODAO: [101024, 101037, 101065, 108006, "1102005", "1102008", "1102026", "1104034", "1104021"],
        DrawingType.INDOOR_FIRST_FLOOR: [105015, 105019, 103061, 107011, 101001, 101002, 101006, 101007, 101011, 101012, 101013, 101014, 101015, 101016,
                                         101044, 101045, 101046, 101047, 101076, 101077, 102001, 102002, 102003, 102015, 102016, 102008, 102009, 119008,  # 万翼规则
                                         101017, 101019, 101020, 101021, 101029, 101036, 101052, 101053, 101061, 106001,
                                         104005, 104006, 104007, 104027, 514, 105004, 103026, 103036, 103037, 106004,
                                         119006, 119009, 104046, 104012, 104009, 103004, 103005, 103006, 103007, 103009, 103010,105001, 104022,  # 万翼规则
                                         105002, 107002, 105008, 113001, 103012, 103013, 103014, 103018, 103019, 104024, 103008,  # 万翼规则
                                         106005, 103039, 103041, 103045, 103046, 106008, 103049, 103050,
                                         103052, 104043, 107008, 103055, 105005, 105006, 101058, 103078, 105017,
                                         103066, 103067, 103078, 106015, 106016, 103077, 103071, 103074, 106029, 106030,
                                         103060, 103063, 105014, 107014, 103062, 104050, 103080, 103044, 103043,
                                         "1102010", "1102015", "1102016", "1105001", "1105004", "1105002",
                                         "1105003", "1105005", "1100005", "1100006", "1100009", "1100002", "1100001","1100010",
                                         "1102014", "1102020","1100028", "1102022", "1102023", "1100019", "1100027", "1102024",
                                         "1100029", "1100034", "1103005", "1103025", "1104001", "1104002", "1104049", "1104014", "1104010", "1104018",
                                         "1104011", "1104012", "1104041", "1104015", "1104044", "1104019", "1104033",
                                         "1104038", "1104051", "1104054", "1104026", "1104052", "1104013", "1104023", "1104016",
                                         "1104017", "1104027", "1104045", "1104028", "1104004", "1103001", "1103003", "1103006", "1103007", "1103004", "1103008", "1103009",
                                         "1103019", "1103024", "1103026", "1103028", "1103033", "1103036", "1103014", "1103022", "1103002",
                                         "1103029", "1103031", "1103039", "1103040", "1103011", "1103016", "1103021", "1103012", "1103017", "1103048", "1103034",
                                         "1103041", "1103042", "1103045", "1103047", "1103046", "1103038"],
        DrawingType.INDOOR_FIRST_FLOOR_NO_SPACE: [101016, 101036, 101061, 103055],
        DrawingType.SITE_PLAN_ROAD: [101022, 101026, 101035, 101054, 101057, 101059, 104002, 107003, 104028, 107005,
                                     102016, 118002, 108003,  # 万翼规则
                                     105007, 114001, 104038, 104039, 104051, 107016, 106017, 106019, 107009, 107010,
                                     104047, 108007, 104052],  # (23)
        DrawingType.SITE_PLAN_BUILDING: [101027, 101055, 101056, 104034, 104051, 107015,
                                         118001, 118003, 104013, 112001,  # 万翼规则
                                         107016, 104052, 108007, 106019],  # (31,32,33,34)
        DrawingType.ELEVATION: [101043, 101051, 104004, 107004, 102005, 103020, 103069],
        DrawingType.SIDE_ELEVATION: [101043, 101051, 104004, 107004, 102005, 103069],
        DrawingType.UNDERGROUND_DINGBAN: [101040],
        DrawingType.PUZHUANG: [101038],
        DrawingType.PAISHUI: [101039],
        DrawingType.INDOOR_FIRST_FLOOR_ACCESS: [101063, 514, 105005, 105006, 103080, 105014, 105015],
        DrawingType.SECOND_THIRD_FLOOR: [],
        DrawingType.WALL_DAYANG: [101041, 101062, 103002, 104025, 104026, 103021, 103022, 103023, 103056, 116001, 116002,
                                  101081, 101079, 101080, 107001, 107013, 103069,  # 万翼规则
                                  "1104032", "1104047" # 中海规则
                                  ],
        # DrawingType.STRUCTURE_DESIGN: [96, 97, 99, 101, 102, 108, 109, 129, 131, 132, 133, 130, 134, 149, 150, 151,
        #                                152, 153, 154, 155, 156, 157, 158, 172, 174],  # (102005, 87)
        DrawingType.SECTION: [104001, 119007, 119003, 104008, 104009, 103003, 119004, 104046, 104011, 103016, 103017],
        DrawingType.BUILDING_DESIGN: [104018, 104019, 104037, 112001],
        DrawingType.DINGCENG: [103005, 106013, 106031, 106030],
        DrawingType.STAIR_DAYANG: [105008, 104041, 103034, 103035, 107006, 107007, 103051, "1104029", "1104028", "1104030", "1104003", "1104004"],
        DrawingType.JIFANG: [106031],
        DrawingType.WUMIAN: [106013, 117001, 106031],
        DrawingType.XIAOFANG_SITE_PLAN: [106017, 106019, 107009],
        DrawingType.FIRST_FLOOR_SITE_PLAN: [106020],
        DrawingType.DOOR_WINDOW_DAYANG: ["1102021"],
        DrawingType.JIANZHU_HUXING_DAYANG: [105013],
        DrawingType.BINANCENG: [],
    }

    INDOOR_FIRST_FLOOR_NO_SPACE_RULE = [101016, 101036, 101061]

    SPECIAL_CHEKCPOINT_ID_DICT = {
        101008: 10100800,
        101009: 10100901,
        101027: 10102700,
        101031: 10103101,
        101032: 10103202,
        101033: 10103303,
        101034: 10103404,
        101055: 10105500,
        101056: 10105601,
    }

    # 规则详情
    # REF: https://www.kdocs.cn/p/51356796370?from=docs&source=docsWeb
    CONFIGURATION = {
        "1100001": {
            "name": "立管不应设置在窗户前。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1100002": {
            "name": "禁止公共电梯门正对入户门",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "elevator_door", "elevator_box"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1100004": {
            "name": "开启后的人防门、消防门及设备管井门不应挤占停车位",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["parking", "door", "emergency_door"],
            "operation": ["combination", "classification"],
        },
        "1100006": {
            "name": "平开门之间不应相互碰撞，入户门不应遮挡电梯门。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["door", "elevator_door", "elevator_box"],
            "operation": ["combination", "classification"],
        },
        "1100007": {
            "name": "一侧靠墙的停车位宽度不应小于2.7米。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["parking", "pillar"],
            "operation": ["combination", "classification"],
        },
        "1100009": {
            "name": "电梯不应与卧室、客厅紧邻布置",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1100010": {
            "name": "通往阳（露）台的门，土建净宽不应小于0.8m。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1100011": {
            "name": "当楼梯间设置采光窗时，采光窗洞口的窗地面积比不应低于1/12.",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["window", "elevator_box", "elevator_door"],
            "operation": ['combination', 'segmentation', 'classification'],
        },

        "1100019": {
            "name": "禁止公共电梯门正对入户门",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "elevator_door",
                                                                          "elevator_box"],
            "operation": ["combination", "segmentation", "classification"],
        },

        "1100027": {
            "name": "电梯不应与起居厅、居室贴临，必须贴临时应采取隔音措施",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1100054": {
            "name": "无障碍通道宽度≥1.2m。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.BASIC_LAYERS.value[
                "indoor_access_segment"] + ['door', 'window'],
            "operation": ["combination", "segmentation", "classification"],
        },

        "1100034": {
            "name": "疏散楼梯间应符合下列规定：\
                        1 楼梯间应能天然采光和自然通风，并宜靠外墙设置。靠外墙设置时，楼梯间、前室及合用前室外墙上的窗口与两侧门、窗、洞口最近边缘的水平距离不应小于1．0m。\
                        2 楼梯间内不应设置烧水间、可燃材料储藏室、垃圾道。\
                        3 楼梯间内不应有影响疏散的凸出物或其他障碍物。\
                        4 封闭楼梯间、防烟楼梯间及其前室，不应设置卷帘。\
                        5 楼梯间内不应设置甲、乙、丙类液体管道。\
                        6 封闭楼梯间、防烟楼梯间及其前室内禁止穿过或设置可燃气体管道。敞开楼梯间内不",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] +
                      LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["pipe", "door", "fire_hydrant", "window"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1100043": {
            "name": "直通住宅单元的地下楼、电梯间入口处应设置乙级防火门,严禁利用楼、电梯间为地下车库进行自然通风。",
            "entity": LayerConfig.BASIC_LAYERS.value['basic'] + ['door', 'window', 'parking',
                                                                 'elevator_box', 'elevator_door', 'emergency_door'],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        "1100047": {
            "name": "开启后的人防门、消防门及设备管井门不应挤占停车位",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["parking", "door", "emergency_door", "fire_hydrants"],
            "operation": ["combination", "classification"],
        },
        "1100053": {
            "name": "严禁公共电梯前室不与公共楼梯间连通。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"]
                      + ["elevator_door", "elevator_box"],
            "operation": ["combination", "segmentation", "classification"],
        },

        "1100005": {
            "name": "管井门和消火栓不应正对电梯门。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door", "elevator_door", "elevator_box", "fire_hydrant"],
            "operation": ["combination", "classification"],
        },
        "1102005": {
            "name": "地库单行弧形坡道净宽≮3.8米，对高端府系产品，不宜≮4.5米且坡道内圈半径不宜小于6米",
            "entity": ["wall", "pillar", "podao", "podao_extra", "separator",
                       "gutter", "filling", "podao_mark", "podao_edge", "window", "door"],
            "operation": ["combination", "segmentation"],
        },
        "1102008": {
            "name": "机动车库基地出入口应设置减速安全设置",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["elevation_mark"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1102020": {
            "name": "电梯井道不应与起居厅、居室贴临，必须贴临时应采取隔音措施",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104001": {
            "name": "阳台未考虑有组织排水，导致积水和渗漏",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["door", "window", "floor_drain"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104003": {
            "name": "公共楼梯踏步宽度高度设置过宽、过高或过窄、过低（宽度宜在250~300，高度宜在150~170），未充分考虑使用感受",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["stair_dayang_plan_stair", "stair_dayang_profile_stair"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104009": {
            "name": "地下室入户门前通道太窄，不方便物品搬运。",
            "entity": LayerConfig.BASIC_LAYERS.value["underground_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104012": {
            "name": "入户门或户内门扇尺寸设计较小（卫生间、阳台最小门洞尺寸应不小于800）造成大型家电无法入户",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["door", "window"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104013": {
            "name": "户型设计中，入户门或内门缺少门垛，或入户门门垛小于100.",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104011": {
            "name": "入户门同时存在内开或外开，造成业主投诉",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["door", "window"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104017": {
            "name": "判断卫生间排气孔洞前后两侧是否有立管",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["door", "window", "pipe", "yu_liu_kong_dong"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104016": {
            "name": "无窗的卫生间未设排气孔",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["window", "reserved_hole"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104023": {
            "name": "楼栋设计的凹槽宽度过小，施工难度较大",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["door", "window"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104032": {
            "name": "栏杆高度不足或设置的横向杆件、反坎易攀爬，存在安全隐患",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["dayang_handrail", "completion_surface"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104034": {
            "name": "地下非机动车坡道尺寸、坡度等未采用标准化设计",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["wall", "pillar", "podao", "podao_extra", "separator",
                                                                  "gutter", "filling", "podao_mark", "podao_edge"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104036": {
            "name": "地库排水沟位置设置不合理(建议明沟时设置在两排车位尾部中间，沿地库边墙；排水沟尽量贯通）",
            "entity": LayerConfig.BASIC_LAYERS.value["underground_segment"] + ["gutter"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104038": {
            "name": "厨房冰箱位置预留不足；改善户型，没有预留对开门冰箱位",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104044": {
            "name": "走廊和公共部位通道完成面净宽度不小于1.3m。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104047": {
            "name": "凸窗未按标准做法，窗扇上下未留反坎",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["dayang_handrail", "completion_surface"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104051": {
            "name": "立管不应遮挡墙面留洞。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["yu_liu_kong_dong"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104055": {
            "name": "地库柱网不应影响车门开启。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["pillar", "parking", "road", "fire_road"],
            "operation": ["combination", "classification"],
        },
        "1104049": {
            "name": "电梯门不应正对管道门、消火栓",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["door", "window", "elevator_door", "fire_hydrant"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1105001": {
            "name": "户门外开时，应避免相邻户门、防火门（不含管井门）间碰撞（开启线最小距离200mm",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["door", "window", "elevator_door", "elevator_box"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1105002": {
            "name": "入户门、前室防火门向电梯厅开启时不应遮挡电梯门",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "elevator_door", "elevator_box"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1105003": {
            "name": "电梯不应与卧室、客厅紧邻布置",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1105004": {
            "name": "核心筒管井门和消火栓应避免正对入户门，当不能避免时装修应设隐门",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["door", "elevator_door", "elevator_box", "fire_hydrant"],
            "operation": ["combination", "classification"],
        },
        "1104005": {
            "name": "地下车库结构、设备及设备管道，如结构柱、消火栓、风管等，影响车位使用或车门开启",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["parking", "fire_hydrant", "pillar"],
            "operation": ["combination", "classification"],
        },
        "1104015": {
            "name": "卫生间门直接开向客厅，存在视觉干扰",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104020": {
            "name": "当停车位一侧靠墙时，停车位宽度应≥2.8m",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["parking", "pillar"],
            "operation": ["combination", "classification"],
        },
        "1104043": {
            "name": "开启后的人防门、消防门及设备管井门不应挤占停车位",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["parking", "door", "emergency_door"],
            "operation": ["combination", "classification"],
        },
        "1102010": {
            "name": "上下水布置是否合理且避免洗衣机压住地漏",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "floor_drain",
                                                                          "air_conditioner_mix"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1102014": {
            "name": "入户门净宽度不应小于0.9米，土建门洞宽度不应小于1.05m,门垛不宜小于100",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1102015": {
            "name": "入户门不与室内卫生间正对",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1102022": {
            "name": "禁止入户门开启互相打架，或遮挡电梯门/疏散楼梯门。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["door", "elevator_door", "elevator_box"],
            "operation": ["combination", 'segmentation', "classification"],
        },

        "1102021": {
            "name": "门窗分格及开启扇大小是否合适，开启扇净宽度：650mm/700mm（不含安装间隙）",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "elevation_window_open_line"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1102023": {
            "name": "禁止入户门与消防箱门开启互相打架碰撞。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["door", "elevator_door", "elevator_box", "fire_hydrant"],
            "operation": ["combination", 'segmentation', "classification"],
        },
        "1102024": {
            "name": "入户门开启后不影响消防疏散宽度",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["door", "elevator_door", "elevator_box", "fire_hydrant"],
            "operation": ["combination", 'segmentation', "classification"],
        },
        "1102026": {
            "name": "地库坡道开口段上端应设置截水沟及防水挡板，坡道下端应设置排水沟，截/排水沟篦子材质宜采用不锈钢材质。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["wall", "pillar", "podao", "podao_extra", "separator",
                                                                  "gutter", "filling", "podao_mark", "podao_edge"],
            "operation": ["combination", 'segmentation', "classification"],
        },
        "1100028": {
            "name": "走廊和公共部位通道完成面净宽度不小于1.2m。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1100029": {
            "name": "住宅首层疏散外门的净通过尺寸不应小于1.1m(扣除门框宽度和门扇厚度，建议土建最小宽度不应小于1.25m)",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["door", "elevator_door", "elevator_box", "fire_hydrant"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1100051": {
            "name": "当柱子与车头平齐时，行车道宽度≥5.5米",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["pillar", "parking", "road", "fire_road"],
            "operation": ["combination", "classification"],
        },
        "1104002": {
            "name": "住宅区或楼栋出入口，未做无障碍设计",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["window", "door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104004": {
            "name": "楼梯间扶手栏杆安装位置不合适，影响楼梯疏散宽度。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door", "fire_hydrant"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104014": {
            "name": "卫生间窗洞开窗过高，未预留装修吊顶及安装暖风机的空间",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.BASIC_LAYERS.value["indoor_segment"] + [
                "window", "door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104010": {
            "name": "住宅区或楼栋出入口，未做无障碍设计",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.BASIC_LAYERS.value["indoor_segment"] + [
                "window", "door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104006": {
            "name": "机动车位没有满足标准尺寸2500×5100~5300",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["pillar", "parking", "road", "parking"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104031": {
            "name": "垂直相接的行车道，应预留5.0m缓冲区，详见附图。应尽量避免设置防火分区隔墙、人防单元隔墙、功能房间墙体等影响视线的障碍物",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["pillar", "parking", "road", "parking","car_lane"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104018": {
            "name": "公共外走廊无排水设计，雨水和清洁用水时均无法正常排水",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["floor_drain"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104046": {
            "name": "人防密闭通道在主要归家流线上，门洞尺寸过小",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door", "elevator_stair", "elevator_door", "window"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104054": {
            "name": "室外空调机位设置不当，机位的平面、立面尺寸不够",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["pipe"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104029": {
            "name": "楼梯间消防前室消火栓暗装未考虑墙厚，消火栓箱体穿透前室墙面",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door", "fire_hydrant"],
           "operation": ["combination", "segmentation", "classification"],
        },
        "1104027": {
            "name": "室内空调机位设置不当，空调正对床头，使用舒适感差",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.BASIC_LAYERS.value["indoor_segment"] + [
                "bed", "door", "window"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104041": {
            "name": "空调板上是否设置地漏",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.BASIC_LAYERS.value["indoor_segment"] + [
                "dilou"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104026": {
            "name": "单元大堂出入口设置的一步台阶容易踩空",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.BASIC_LAYERS.value["indoor_segment"] + [
                "stair", "podao"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104052": {
            "name": "落水管未做处理，明露在主立面",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.BASIC_LAYERS.value["indoor_segment"] + [
                "pipe", 'segment_extra'],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104037": {
            "name": "窗户固定扇和开启扇设置不合理，没有考虑后续实际使用（如开启扇唯一时，应尽量不设置在床头位置）",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.BASIC_LAYERS.value["indoor_segment"] + [
                "bed", 'window'],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104028": {
            "name": "首层下地下室处，开门后未设置缓冲平台，容易踏空摔倒",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.BASIC_LAYERS.value["indoor_segment"] + [
                "bed", 'window'],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1104030": {
            "name": "楼梯梁处净高不满足规范要求",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1103003": {
            "name": "墙体位置，板房与货量是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"],
            "operation": ["combination", "segmentation", "classification"],
        },

        "1103007": {
            "name": "入户门、室内门开启方向，板房与货量是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1103008": {
            "name": "入户门的防火等级，板房与货量是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1303001": {
            "name": "卫生间立管数量货板是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["pipe"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1303003": {
            "name": "污水立管位置，板房与货量是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["pipe"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1103027": {
            "name": "厨房、卫生间水管井大小，板房与货量是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1103037": {
            "name": "各功能空间的套内净轮廓，板房与货量是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1103045": {
            "name": "平开窗的执手做法及颜色，板房与货量是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1103047": {
            "name": "外露螺栓、螺钉、螺丝、五金件材质，板房与货量是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1103046": {
            "name": "平开窗执手安装高度，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"],
            "operation": [],
        },
        105015: {
            "name": "轮椅坡道的高度超过300mm且坡度大于1：20时，应在两侧设置扶手，坡道与休息平台的扶手应保持连贯",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "elevation_mark", "arrow",
                                                                          "plan_handrail"],
            "operation": ["combination", "classification", "segmentation"],
        },
        103061: {
            "name": "向外开启的户门不应妨碍公共交通及相邻户门开启",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door"],
            "operation": ["combination", "classification", "segmentation"],
        },
        111003: {
            "name": "汽车库、修车库、停车场设计防火规范",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.BASIC_LAYERS.value["stair_dayang"] + \
                      ["door", "window", 'elevator_stair', 'elevator_box'],
            "operation": ["combination", "classification", "segmentation"],
        },
        107011: {
            "name": "建筑物底层出入口处应采取措施防止室外地面雨水回流",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door", "elevate_biaogao", "elevation_mark", "annotation","annotation_line"],
            "operation": ["combination", "classification", "segmentation"],
        },
        101001: {
            "name": "立管不得设置在窗户范围内",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["window", "pipe"],
            "operation": ["combination", "classification"],
        },
        101002: {
            "name": "禁止电梯门正对户门",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "elevator_door", "elevator_box"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101003: {
            "name": "停车位数量",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["parking"],
            "operation": ["combination", "classification"],
        },
        101004: {
            "name": "所有设备、设施不应挤占停车位空间",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["parking", "fire_hydrant", "water_pit"],
            "operation": ["combination", "classification"],
        },
        101005: {
            "name": "开启后的人防门、消防门及设备管井门不应挤占停车位",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["parking", "door", "emergency_door"],
            "operation": ["combination", "classification"],
        },
        101006: {
            "name": "电梯门不正对管道井、消火栓",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["door", "elevator_door", "elevator_box", "fire_hydrant"],
            "operation": ["combination", "classification"],
        },
        101007: {
            "name": "入户门和消防门间不应相互碰撞，入户门开启后不应遮挡电梯门",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["door", "elevator_door", "elevator_box"],
            "operation": ["combination", "classification"],
        },
        101008: {
            "name": "当停车位一侧靠墙时，停车位宽度应≥2.7米",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["parking", "pillar"],
            "operation": ["combination", "classification"],
        },
        101009: {
            "name": "当停车位两侧靠墙时，停车位宽度应≥3米",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["parking", "pillar"],
            "operation": ["combination", "classification"],
        },
        101010: {
            "name": "当柱子与车头平齐时，行车道宽度≥5.5米",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["pillar", "parking", "road", "fire_road"],
            "operation": ["combination", "classification"],
        },
        101011: {
            "name": "电梯不应与卧室、客厅紧邻布置",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101012: {
            "name": "入户门净通过尺寸不应小于0.9米（扣除门框宽度和门扇厚度，建议土建最小宽度1.05米）",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101013: {
            "name": "入户门外不应明装管线",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "pipe", "pipe_barrier"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101014: {
            "name": "入户门不宜与室内卫生间门正对",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101015: {
            "name": "（厨房）当采用双扇推拉门时，门洞土建净宽不应小于1.6m；当采用平开门时，门洞土建净宽不应小于0.8m",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101016: {
            "name": "住宅首层疏散外门的净通过尺寸不应小于1.1m（扣除门框宽度和门扇厚度，建议土建最小宽度不应小于1.25m）；普通非电动开启的外门开启扇高度不应大于2.4m。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101017: {
            "name": "走廊和公共部位通道完成面净宽度不小于1.2m。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101018: {
            "name": "严禁公共电梯前室不与公共楼梯间连通。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"]
                      + ["elevator_door", "elevator_box"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101019: {
            "name": "通往阳（露）台的门，土建净宽不应小于0.8m。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101020: {
            "name": "① 阳（露）台、室外连廊的排水不得采用散排方式；② 排水立管应设置于阳（露）台内侧、靠近外墙处；③ 严禁外连廊、阳台、露台、空调板等设备平台地漏设置在内侧。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["floor_drain", "floor_drain_mix", "pipe", "door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101021: {
            "name": "立管不应遮挡空调排气口",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["pipe", "air_conditioner", "air_conditioner_mix"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101022: {
            "name": "应满足各地政府部门对自行车停车数量提出的要求，校核自行车停车数量",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"],
            "operation": [],
        },
        101023: {
            "name": "应满足各地政府部门对自行车停车数量提出的要求，校核电动自行车停车数量",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"],
            "operation": [],
        },
        101024: {
            "name": "地库单行弧形坡道，净宽≥4.5m，且坡道内圈半径≥6.0m",
            "entity": ["wall", "pillar", "podao", "podao_extra", "separator",
                       "gutter", "filling", "podao_mark", "podao_edge"],
            "operation": ["combination", "segmentation"],
        },
        101025: {
            "name": "严禁城市均价1.4倍及以上高层产品地下室停车库选用小柱网布局（五级及以上等级人防、五层及以下多层产品地下停车库不受此限制）。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["pillar", "parking"],
            "operation": ["combination", "classification"],
        },
        101026: {
            "name": "园区内地面停车采用“垂直”停方式时，车位前车行道宽度应≥5.5m，停车车位尺寸不应小于2.5*5.5米（宽*长）",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["parking", "road", "fire_road"],
            "operation": ["combination", "classification"],
        },
        101027: {
            "name": "小区住宅楼与公共设施之间距离超过阈值，且用绿植隔离",
            "entity": ["building", "red_line", "red_line_sub", "road_center_line", "road", "fire_road"],
            "operation": ["combination", "classification", "segmentation"],
        },
        101028: {
            "name": "充电停车位数量",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["parking"],
            "operation": ["combination", "classification"],
        },
        101029: {
            "name": "设置洗衣机的阳（露）台，应设置给水点、排水地漏；应预留600mm洗衣机位、拖把池、洗手盆位置）。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"]
                      + ["floor_drain", "floor_drain_mix"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101030: {
            "name": "垂直相接的行车道，应预留5.0m缓冲区，尽量避免设置防火分区隔墙、人防单元隔墙、功能房间墙体等影响视线的障碍物。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["car_lane"],
            "operation": [],
        },
        101035: {
            "name": "园区应至少设置2个人行出入口及2个车行出入口，主要车行出入口应至少为双车道，且其中一个道闸的净宽满足消防车通过的要求，即：宽度≥4.0m（一个车行出入口宽度≥4.0米）",
            "entity": ["border", "road", "red_line", "red_line_sub", "fire_road"],
            "operation": [],
        },
        101036: {
            "name": "首层及地下室大堂应满足无障碍设计要求",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation"]
        },
        101037: {
            "name": "室外至负一层的地库坡道，上端应设置截水沟，下端应设置排水沟。",
            "entity": ["wall", "pillar", "podao", "podao_extra", "separator",
                       "gutter", "filling", "podao_mark", "podao_edge"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101038: {
            "name": "严禁小区内的主要人行道宽度小于1.5m。容积率＞3住宅小区，应充分考虑人行道的使用流量，对于使用流量较大的人行道应适当放宽至2.5m，避免出现“排队出行”的情况发生。）",
            "entity": ['border', 'pave'],
            "operation": []
        },
        101039: {
            "name": "水表井、热力管井内地坪需做防水并设置地漏",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["floor_drain", "floor_drain_mix", "door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101040: {
            "name": "严禁项目地库顶板采用无梁楼盖结构形式。",
            "entity": ["pillar_cap"],
            "operation": [],
        },
        101041: {
            "name": "6层及以下的栏杆高度≥1.2m；6层以上的栏杆高度≥1.3m。栏杆高度统一从阳台地面找坡最高点至栏杆扶手顶端计算；",
            "entity": ["elevation_handrail", "elevation_window", "ketamian", "elevation_mark"],
            "operation": ["combination", "classification"]
        },
        101042: {
            "name": "单元入口门头立面高度不应高于二层住宅窗下口，以避免对二层住户的视线和采光遮挡）",
            "entity": ["elevation_window"],  # 此处先去掉 mentou
            "operation": ["combination", "classification"],
        },
        101043: {
            "name": "严禁为装饰效果而设置的横梁、飘板、连廊、外框、造型线脚等构件影响住宅的采光、通风、视线",
            "entity": ["elevation_window", "decoration"],
            "operation": ["combination", "classification"],
        },
        101044: {
            "name": "室外空调机位未紧邻该空调的使用房间",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["air_conditioner"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101045: {
            "name": "分体空调室外机固定空调位，净尺寸不满足要求",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"]
                      + ["air_conditioner", "pipe"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101046: {
            "name": "空调室外机对吹",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["air_conditioner"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101047: {
            "name": "空调室外机排风方向不在阳台外测",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["air_conditioner"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101048: {
            "name": "一字型干湿分离卫生间，短向净尺寸不应小于1.55m，长向净尺寸不应小于2.65m",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["washbasin"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101049: {
            "name": "一字型普通卫生间，长向净尺寸不小于2.45m, 长向开门短向净尺寸不小于1.50m, 短向开门短向净尺寸不小于1.55m",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101050: {
            "name": "方形设钻石形淋浴间的卫生间，短向净尺寸不小于1.8m, 长向净尺寸不小于2.05m",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["diamond_bath"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101051: {
            "name": "严禁外立面采用GRC或其它材质的空心装饰线条（角）；严禁在外墙外保温上直接粘贴各类面砖；严禁外墙及高于2m的景墙采用湿贴石材。",
            "entity": [],
            "operation": [],
        },
        101052: {
            "name": "严禁空调室内机、热水器、暖气片等有坠落隐患的设备、部品直接外挂在没有具体构造措施的轻钢龙骨、条板、轻质砌块等轻质隔墙上。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["air_conditioner", "air_conditioner_mix", 'wall_hatch', 'window'],
            "operation": ["combination", "segmentation", "classification"],
        },
        101053: {
            "name": "严禁后搭板及改造大堂、小院、车位等易导致极高验收风险和质量隐患的设计",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101054: {
            "name": "当货车不可到达单元入口时，应在总图中设置货车临停区，临停区与单元入口间的步行距离≤50m，货车临停车位尺寸≥4.0*8.0m。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["parking", "road", "building", "fire_road"],
            "operation": ["combination", "classification"],
        },
        101055: {
            "name": "水泵房和配电站不应设置在住宅投影面下方，设置在地上时也不应毗邻住宅",
            "entity": ["building", "underground_building"],
            "operation": [],
        },
        101056: {
            "name": "水泵房和配电站不应设置在住宅投影面下方，设置在地上时也不应毗邻住宅",
            "entity": ["building", "underground_building"],
            "operation": [],
        },
        101057: {
            "name": "园区高程：园区出入口高程应≥相邻市政路0.3m；应高于本小区排水的相邻市政道路0.3m；其他高于本园区的市政道路位置必须采取措施防止雨水倒灌。",
            "entity": ["border", "road", "red_line", "red_line_sub", "elevation_mark", "fire_road"],
            "operation": [],
        },
        101058: {
            "name": "园区内所有“有业主出入的”建筑出入口必须设置无障碍通道（地下车库）",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ['door', 'window'],
            "operation": ["segmentation"]
        },
        101059: {
            "name": "当货车可达单元入口时，在单元入口设置停放区域，停车位尺寸≥4.0*8.0m，行车道宽度≥4.0m，转弯半径≥8.0m。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["road", "building", "fire_road"],
            "operation": ["combination", "classification"],
        },
        101060: {
            "name": "当货车需要到达地下室单元入口附近时，行车道宽度≥4.0m，转弯半径≥8.0m。考虑到装卸要求，货车临时停车位尺寸≥4.0*8.0m。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["car_lane", "parking"],
            "operation": ["combination", "classification"],
        },
        101061: {
            "name": "当电梯前室设计为非封闭室内空间时，须设置必要的挡水防水措施，防止雨水飘入。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["floor_drain", "floor_drain_mix", "door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        101062: {
            "name": "严禁阳台、露台、空调板部位的墙体根部不设置防水反坎；反坎高度宜为200mm。",
            "entity": ["structure", "wall_hatch", "door", "window", "elevation_window"],  # issue 253514增加搜索门窗，去掉了"border"
            "operation": [],
        },
        101063: {
            "name": "无障碍通道宽度≥1.2m。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.BASIC_LAYERS.value[
                "indoor_access_segment"] + ['door', 'window'],
            "operation": ["combination", "segmentation", "classification"],
        },
        # 64: {
        #     "name": "直接对外的单元入户大堂应设置雨篷；挑出宽度≥1.5m；雨棚底高度不应低于3.0m。",
        #     "entity": LayerConfig.BASIC_LAYERS.value["basic"] +
        #               LayerConfig.BASIC_LAYERS.value["second_third_segment"] + ['annotation_line', 'door', 'window'],
        #     "operation": ["combination", "segmentation"],
        # },
        101065: {
            "name": "坡道前方4.5米内不得有视线遮挡。",
            "entity": ["wall", "pillar", "podao", "podao_extra", "separator",
                       "gutter", "filling", "podao_mark", "podao_edge"],
            "operation": ["combination", "segmentation"],
        },
        106001: {
            "name": "消防电梯应设置前室；前室短边不应小于2.4m；消防电梯前室不与剪刀梯共用前室合用时，前室面积不应小于6m²；消防电梯前室与剪刀梯共用前室合用时，前室面积不应小于12m²；前室不应开设规范允许外门窗洞；前室或合用前室的门应采用乙级防火门",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["elevator_door", "elevator_box", "door", "window"],
            "operation": ["combination", "segmentation", "classification"],
        },
        # 67.1: {
        #     "name": "机动车库内不能有修理车位, 机动车库楼梯间和电梯间要有门",
        #     "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["parking", "door"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        # 67.2: {
        #     "name": "过“车库”文本所在bbox平行于x轴的线段上一点画一条直线；判断直线是否于墙线/填充图层有交点",
        #     "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["pillar", "wall_hatch", "door"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        104001: {
            "name": "机动车库内不能有修理车位, 机动车库楼梯间和电梯间要有门；过“车库”文本所在bbox平行于x轴的线段上一点画一条直线；判断直线是否于墙线/填充图层有交点",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["pillar", "wall_hatch", "door", "parking"],
            "operation": ["combination", "segmentation", "classification"],
        },
        104002: {
            "name": "居住用地内应配套设置居民自行车、汽车的停车场地或停车库。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["parking", "road", "building", "fire_road"],
            "operation": ["combination", "segmentation", "classification"],
        },
        104003: {
            "name": "每套住宅应设卧室、起居室（厅）、厨房和卫生间等基本空间。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        103001: {
            "name": "住宅应按套型设计，每套住宅应设卧室、起居室（厅）、厨房和卫生间等基本功能空间",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        104004: {
            "name": "住宅建筑上下相邻套房开口部位间应设置高度不低于0．8m的窗槛墙或设置耐火极限不低于1．00h的不燃性实体挑檐，其出挑宽度不应小于0．5m，长度不应小于开口宽度。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["window",  "elevation_window"],
            "operation": ["combination", "classification"],
        },
        104005: {
            "name": "住宅建筑中竖井的设置规则",
            "entity": LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      ['elevator_box', 'pipe', 'door', 'emergency_door', 'podao_edge', 'gutter'],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        104006: {
            "name": "住宅建筑中设有管理人员室时，应设管理人员使用的卫生间",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] +
                      LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        106015: {
            "name": "疏散楼梯间应符合下列规定：\
                    1 楼梯间应能天然采光和自然通风，并宜靠外墙设置。靠外墙设置时，楼梯间、前室及合用前室外墙上的窗口与两侧门、窗、洞口最近边缘的水平距离不应小于1．0m。\
                    2 楼梯间内不应设置烧水间、可燃材料储藏室、垃圾道。\
                    3 楼梯间内不应有影响疏散的凸出物或其他障碍物。\
                    4 封闭楼梯间、防烟楼梯间及其前室，不应设置卷帘。\
                    5 楼梯间内不应设置甲、乙、丙类液体管道。\
                    6 封闭楼梯间、防烟楼梯间及其前室内禁止穿过或设置可燃气体管道。敞开楼梯间内不",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] +
                      LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["pipe", "door", "fire_hydrant", "window"],
            "operation": ["combination", "segmentation", "classification"],
        },
        106016: {
            "name": "建筑内的疏散门应符合下列规定",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"],
            "operation": ["combination", "segmentation", "classification"],
        },
        106019: {
            "name": "消防车登高操作场地应符合下列规定",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["door", "window", "extinguishing_ascend_field", "building",
                       "red_line", "red_line_sub", "fire_road", "road", "garage_exit", "garage_podao_exit"],
            "operation": ["segmentation"],
        },
        107010: {
            "name": "缓冲段应从车库出入口坡道起坡点算起，并应符合下列规定。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["red_line", "red_line_sub", "door", "window", "road", "fire_road",
                       "garage_exit", "garage_podao_exit"],
            "operation": ["combination", "segmentation", "classification"],
        },
        # 73.2: {
        #     "name": "住宅建筑中设有管理人员室时，应设管理人员使用的卫生间",
        #     "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        103002: {
            "name": "阳台栏板或栏杆净高，六层及六层以下不应低于1.05m；七层及七层以上不应低于1.10m",
            "entity": ["elevation_handrail"],
            "operation": ['combination', 'classification'],
        },
        103060: {
            "name": "面临走廊、共用上人屋面或凹口的窗，应避免视线干扰，向走廊开启的窗扇不应妨碍交通",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["window","wall"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        105014: {
            "name": "轮椅坡道宜设计成直线形、直角形或折返形",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["mailbox","wall", "elevator_door"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        107013: {
            "name": "当凸窗窗台高度低于或等于0．45m时，其防护高度从窗台面起算不应低于0．9m；当凸窗窗台高度高于0．45m时，其防护高度从窗台面起算不应低于0．6m",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["completion_surface", "dayang_handrail","elevation_window","elevation_handrail"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        107014: {
            "name": "当梯段改变方向时，扶手转向端处的平台最小宽度不应小于梯段净宽，并不得小于1.2m,直跑楼梯的中间平台宽度不应小于0.9m",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["wall","elevator_stair"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        104007: {
            "name": "建筑入口无障碍设计规则",
            "entity": LayerConfig.BASIC_LAYERS.value['basic'] + ['door', 'podao', 'pillar', 'wall', 'elevation_handrail'],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        107015: {
            "name": "除地下室、窗井、建筑入口的台阶、坡道、雨篷等以外，建(构)筑物的主体不得突出建筑控制线建造。",
            "entity": ["red_line", "building"],
            "operation": ['segmentation', ],
        },
        101076: {
            "name": "空调外机位的设置应考虑设备安装、检修和更换的便利性。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["air_conditioner"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        101077: {
            "name": "设置空调标准孔内径净尺寸=70mm",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["air_conditioner"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        101079: {
            "name": "空调板设有外装饰或反坎时，要控制外装饰或反坎的高度，不能遮挡空调室外机的排风口，并设置地漏。",
            "entity": ["wall_hatch", "air_conditioner"],
            "operation": ['combination', 'classification'],
        },
        118002: {
            "name": "甲、乙类物品运输车的汽车库、修车库、停车场与其他民用建筑的防火间距不应小于25m。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["building"],
            "operation": ["segmentation"],
        },
        101080: {
            "name": "空调室外机位百叶应向顺水方向倾斜，避免雨水进入，同时保证空调通风率。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["air_conditioner"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        101081: {
            "name": "空调板墙根设置混凝土反坎应高度≥200mm，空调板应设置3%的排水坡度。",
            "entity": ["wall_hatch", "air_conditioner"],
            "operation": ['combination', 'classification'],
        },
        102001: {
            "name": "禁止入户门开启互相打架，或遮挡电梯门/疏散楼梯门。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]
                      + ["door", "elevator_door", "elevator_box"],
            "operation": ["combination", 'segmentation', "classification"],
        },
        102002: {
            "name": "与电梯相邻的居住房间必须做隔音和防震措施。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        102003: {
            "name": "电梯前室必须与消防楼梯间联通",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"]
                      + ["elevator_door", "elevator_box"],
            "operation": ["combination", "segmentation", "classification"],
        },
        102015: {
            "name": "室内尺寸标准:1):单元门土建洞口净宽不小于1300mm;2):地上地下各常用归家动线公共走廊完成面净宽不小于1200mm;3)消防楼梯间及前室防火门、入户门土建洞口净宽不小于1100mm；4）户内卧室门、厨房门土建洞口净宽不小于900mm；5）户内卫生间门土建洞口净宽不小于800mm。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["elevator_door", "elevator_box"],
            "operation": ["combination", "segmentation", "classification"],
        },
        # 85.1: {
        #     "name": "室内尺寸标准:3)消防楼梯间及前室防火门、入户门土建洞口净宽不小于1100mm；4）户内卧室门、厨房门土建洞口净宽不小于900mm；5）户内卫生间门土建洞口净宽不小于800mm。",
        #     "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["elevator_door", "elevator_box"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        # 85.2: {
        #     "name": "地上地下各常用归家动线公共走廊完成面净宽不小于1200mm。",
        #     "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["elevator_door", "elevator_box"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        # 85.3: {
        #     "name": "单元门土建洞口净宽不小于1300mm",
        #     "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["elevator_door", "elevator_box"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        102005: {
            "name": "禁止为装饰效果而设置的横梁/飘窗等构件影响住宅的采光、通风、视线",
            "entity": ["elevation_window"],
            "operation": ["combination", "classification"],
        },
        102016: {
            "name": "1. 禁止首层室内标高低于室外标高 2. 禁止场地标高低于市政标高",
            "entity": [],
            "operation": [],
        },
        # 87.1: {
        #     "name": "禁止首层室内标高低于室外标高",
        #     "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        # 87.2: {
        #     "name": "禁止场地标高低于市政标高。",
        #     "entity": ["border", "road", "red_line", "red_line_sub", "elevation_mark"],
        #     "operation": ["combination", "segmentation"],
        # },
        102007: {
            "name": "禁止消防连廊设置在半层处。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        102008: {
            "name": "至少有一条从园区至地上单元口的归家动线应为无台阶设计；且地下车库至单元地下电梯厅的归家动线应为无台阶设计。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["elevator_door", "elevator_box"],
            "operation": ["combination", "segmentation", "classification"],
        },
        102009: {
            "name": "与设备用房贴邻居住房间必须做隔音防震措施。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["segmentation", "combination"],
        },
        118001: {
            "name": "建筑单体距离满足消防规范问题",
            "entity": ["building"],
            "operation": [],
        },
        92: {
            "name": "甲、乙类物品运输车的汽车库、修车库、停车场与其他民用建筑的防火间距不应小于25m。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["building"],
            "operation": ["segmentation"],
        },
        119001: {
            "name": "卧室使用面积不应小于6m2,兼起居的卧室使用面积不应小于9m2",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["segmentation", "combination"],
        },
        119002: {
            "name": "厨房的使用面积不应小于3.5m2。当套型内无封闭的厨房，仅设置炊事空间时，炊事空间使用面积不应小于2m2。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["segmentation", "combination"],
        },
        119006: {
            "name": "向外开启入户门不应妨碍公共交通和相邻入户门。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door"],
            "operation": ["combination", 'segmentation', "classification"],
        },
        119008: {
            "name": "#电梯井道及电梯机房、水泵机房、冷冻机房严禁紧邻卧室，布置不应紧邻卧室布置。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        119007: {
            "name": " 走廊的净宽不应小于1.20m。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        119003: {
            "name": "厨房、卫生间的室内净高不应低于2.20m",
            "entity": ['wall_hatch', 'wall'],
            "operation": [],
        },
        118003: {
            "name": "高层住宅建筑和山坡地边缘或河道、湖泊等岸边临空建造的其他高层民用建筑应至少沿建筑的一条长边设置消防车道；仅沿一个长边设置消防车道的高层建筑，该消防车道应与建筑的消防车登高操作面对应。",
            "entity": ["road", "building", "fire_road"],
            "operation": [],
        },
        106: {
            "name": "1.消防登高面与建筑之间不存在任何除裙房外的物体。裙房边与建筑塔楼投影边任意垂直距离不大于4米。2.对于超50米的建筑，消防登高面场地不小于20米*10米。3.登高面场地范围内结构荷载应按照相应规范设计。4.消防登高面坡度不大于3°，且任意一边据墙边（垂直建筑墙边）不得大于10米。",
            "entity": ["road", "building", "fire_road"],
            "operation": [],
        },
        119005: {
            "name": "卧室、起居室、厨房不应布置在地下室",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"],
            "operation": ["combination", 'segmentation', "classification"],
        },
        104008: {
            "name": "卧室、起居室（厅）的室内净高不应低于2．40m，局部净高不应低于2．10m，局部净高的面积不应大于室内使用面积的1/3。利用坡屋顶内空间作卧室、起居室（厅）时，其1/2使用面积的室内净高不应低于2．10m。",
            "entity": ['wall_hatch', 'wall'],
            "operation": [],
        },
        104046: {
            "name": " 1、走廊的净宽不应小于1.20m；2、走廊的净高不应小于2.00m。",
            "entity": [],
            "operation": [],
        },
        104009: {
            "name": " 走廊和公共部位通道的净宽不应小于1．20m，局部净高不应低于2．00m。 ",
            "entity": [],
            "operation": [],
        },
        104010: {
            "name": "住宅的卧室、起居室（厅）、厨房不应布置在地下室。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"],
            "operation": ["combination", 'segmentation', "classification"],
        },
        104011: {
            "name": "住宅地下自行车库净高不应低于2．00m",
            "entity": ['wall_hatch', 'wall'],
            "operation": [],
        },
        104012: {
            "name": '电梯不应与卧室、起居室紧邻布置，受条件限制需要紧邻布置时,必须应采取有效的隔声和减振措施。',
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },

        104013: {
            "name": "住宅建筑与相邻民用建筑之间的防火间距应符合表9．3．2的要求",
            "entity": ["building"],
            "operation": [],
        },
        104014: {
            "name": "楼梯间窗口与套房窗口最近边缘之间的水平间距不应小于1．0m。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"],
            "operation": ["combination", 'segmentation', "classification"],
        },
        103003: {
            "name": "卧室、起居室（厅）的室内净高不应低于2．40m，局部净高不应低于2．10m，且局部净高的室内面积不应大于室内使用面积的1/3。",
            "entity": ['wall_hatch', 'wall'],
            "operation": [],
        },
        103004: {
            "name": "安全出口应分散布置，两个安全出口的距离不应小于5m。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        # 119.2: {
        #     "name": "安全出口应分散布置，两个安全出口的距离不应小于5m。",
        #     "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        103005: {
            "name": "楼梯间及前室的门应向疏散方向开启。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        # 120.2: {
        #     "name": "楼梯间及前室的门应向疏散方向开启。",
        #     "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        103006: {
            "name": '电梯不应紧邻卧室布置，当受条件限制，电梯不得不紧邻兼起居的卧室布置时，应采取隔声、减振的构造措施。',
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },

        103007: {
            "name": "供轮椅通行走道和通道等公共走廊完成面净宽不小于1200mm。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["elevator_door", "elevator_box"],
            "operation": ["combination", "segmentation", "classification"],
        },
        103008: {
            "name": "住宅建筑应配套设置信报箱或智能信报箱。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["elevator_door", "elevator_box"],
            "operation": ["combination", "segmentation", "classification"],
        },
        103009: {
            "name": "卧室、起居室(厅)、厨房应有直接天然采光",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        103010: {
            "name": "卧室、起居室(厅)、厨房应有自然通风",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        119004: {
            "name": "卧室、起居室(厅)的室内净高不应低于2.60m，局部净高不应低于2.20m，局部净高的面积不应大于室内使用面积的1/3。住宅利用坡屋顶内空间作卧室、起居室时，室内净高不低于2.20m 的使用面积不应小于室内使用面积的1/2。",
            "entity": ['wall_hatch', 'wall'],
            "operation": [],
        },
        112001: {
            "name": "住区收集站与周围建筑物的间距不应小于5ｍ",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["building"],
            "operation": [],
        },
        105001: {
            "name": "无障碍出入口的轮椅坡道及平坡出入口的坡度应符合下列规定：1平坡出入口的地面坡度不应大于1:20，当场地条件比较好时，不宜大于1：30； 2 同时设置台阶和轮椅坡道的出入口，轮椅坡道的坡度应符合本规范第3．4节的有关规定。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        105002: {
            "name": "出入口的地面应平整、防滑;除平坡出入口外，在门完全开启的状态下，建筑物无障碍出入口的平台的净深度不应小于1.50m;建筑物无障碍出入口的门厅、过厅如设置两道门，门扇同时开启时两道门的间距不应小于1.50m",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        # 135.1: {
        #     "name": "出入口的地面应平整、防滑",
        #     "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        # 135.4: {
        #     "name": "除平坡出入口外，在门完全开启的状态下，建筑物无障碍出入口的平台的净深度不应小于1.50m",
        #     "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        # 135.5: {
        #     "name": "建筑物无障碍出入口的门厅、过厅如设置两道门，门扇同时开启时两道门的间距不应小于1.50m",
        #     "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        107001: {
            "name": "居住建筑临空外窗的窗台距楼地面净高低于0．9m 需要设置窗台设置栏杆",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["window"] + ['elevation_handrail'],
            "operation": ["combination", "segmentation", "classification"],
        },
        107002: {
            "name": "1 开向疏散走道及楼梯间的门扇开足后，不应影响走道及楼梯平台的疏散宽度；2 门的开启不应跨越变形缝；",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        108003: {
            "name": "基地主要出入口的宽度不应小于4m;相邻机动车库基地出入口之间的最小距离不应小于15m,且不应小于两出入口道路转弯半径之和。",
            "entity": ["border", "road", "red_line", "red_line_sub", "elevation_mark", 'garage', "fire_road"],
            "operation": [],
        },
        # 138.2: {
        #     "name": "机动车库基地出入口应具有通视条件。",
        #     "entity": ['wall_hatch', 'wall'],
        #     "operation": [],
        # },
        # 139.1: {
        #     "name": "扶手末端应向下延伸不小于100mm。",
        #     "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        105008: {
            "name": "栏杆式扶手应向下成弧形或延伸到地面上固定。",
            "entity": [],
            "operation": [],
        },
        113001: {
            "name": "外墙变形缝必须做防水处理。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        104015: {
            "name": "阳台地面构造应有排水措施。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        119009: {
            "name": "住宅建筑应配套设置信报箱或智能信报箱。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["elevator_door", "elevator_box"],
            "operation": ["combination", "segmentation", "classification"],
        },
        104016: {
            "name": "住宅建筑中相邻套房之间应采取防火分隔措施。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        104017: {
            "name": '当住宅建筑中的楼梯、电梯直通住宅楼层下部的汽车库时，楼梯、电梯在汽车库出入口部位应采取防火分隔措施.',
            "entity": LayerConfig.BASIC_LAYERS.value["underground_segment"] + ["elevator_door", "elevator_box"],
            "operation": ["combination", "segmentation", "classification"],
        },
        104018: {
            "name": "35层及35层以上的住宅建筑应设置火灾自动喷水灭火系统。",
            "entity": [],
            "operation": [],
        },
        104019: {
            "name": "35层及35层以上的住宅建筑应设置火灾自动报警系统。",
            "entity": [],
            "operation": [],
        },
        104022: {
            "name": " 走道和通道净宽不应小于1.20m。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        103011: {
            "name": "1. 卧室、起居室（厅）、厨房不应布置在地下室 2. 当布置在半地下室时，需要每间房有窗，并且有排水及相关安全防护的措施",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"],
            "operation": ["combination", "segmentation", "classification"],
        },
        # 160: {
        #     "name": "住宅地下室应采取有效防水措施。",
        #     "entity": [],
        #     "operation": [],
        # },
        # 单图框改为多图框审查
        103012: {
            "name": "无前室的卫生间的门不应直接开向起居室（厅）或厨房。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        103013: {
            "name": "卧室的使用面积应符合下列规定：1.双人卧室不应小于9m2；2.单人卧室不应小于5m2；3.兼起居的卧室不应小于12m2。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["segmentation", "combination"],
        },
        103014: {
            "name": "起居室（厅）的使用面积不应小于10m^2",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["segmentation", "combination"],
        },
        103015: {
            "name": "无直接采光的餐厅、过厅等，其使用面积不宜大于10m2。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        103016: {
            "name": "住宅层高宜为2．80m。",
            "entity": ['wall_hatch', 'wall'],
            "operation": [],
        },
        103017: {
            "name": "厨房、卫生间的室内净高不应低于2.20m",
            "entity": ['wall_hatch', 'wall'],
            "operation": [],
        },
        # 167.1: {
        #     "name": "各部位门洞的最小尺寸应符合表5．8．7的规定。",
        #     "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["elevator_door", "elevator_box"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        # 167.2: {
        #     "name": "单元门土建洞口净宽不小于1200mm",
        #     "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["elevator_door", "elevator_box"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        103018: {
            "name": "各部位门洞的最小尺寸应符合表5．8．7的规定。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["elevator_door", "elevator_box"],
            "operation": ["combination", "segmentation", "classification"],
        },
        106013: {
            "name": "建筑的楼梯间宜通至屋面，通向屋面的门或窗应向外开启",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        103019: {
            "name": "楼梯井净宽大于0．11m时，必须采取防止儿童攀滑的措施。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        104024: {
            "name": "卫生间应设置便器、洗浴器、洗面器等设施或预留位置；布置便器的卫生间的门不应直接开在厨房内。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["washbasin", "closestool"],
            "operation": ["combination", "segmentation", "classification"],
        },
        103020: {
            "name": "阳台栏杆设计必须采用防止儿童攀登的构造，栏杆的垂直杆件间净距不应大于0.11m，放置花盆处必须采取防坠落措施。",
            "entity": ["elevation_handrail", "elevation_window"],
            "operation": ["combination", "classification"]
        },
        104025: {
            "name": "外窗窗台应有防护设施. 阳台栏杆净高不应低于规范值.",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["elevation_handrail", "window","door", "elevation_window", "completion_surface"],
            "operation": ["combination"],
        },
        104026: {
            "name": "外廊、内天井及上人屋面等临空处栏杆净高，六层及六层以下不应低于1．05m；七层及七层以上不应低于1．10m。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["elevation_handrail", "completion_surface"],
            "operation": ["combination"],
        },
        104027: {
            "name": "楼梯间对外出口设置规则",
            "entity": LayerConfig.BASIC_LAYERS.value['basic'] + ['door', 'elevator_box'],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103021: {
            "name": "窗外没有阳台或平台的外窗，窗台距楼面、地面的净高低于0．90m时，应设置防护设施。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["window", "dayang_handrail"],
            "operation": ['combination', 'segmentation'],
        },
        103022: {
            "name": "楼梯间、电梯厅等共用部分的外窗，窗外没有阳台或平台，且窗台距楼面、地面的净高小于0．90m时，应设置防护设施。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["window", "dayang_handrail", "completion_surface"],
            "operation": ["combination", 'segmentation'],
        },
        103023: {
            "name": "外廊、内天井及上人屋面等临空处栏杆净高，六层及六层以下不应低于1．05m；七层及七层以上不应低于1．10m。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["elevation_handrail", "completion_surface"],
            "operation": ["combination"],
        },
        103024: {
            "name": "每套住宅应设置洗衣机的位置及条件。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        103025: {
            "name": "直通住宅单元的地下楼、电梯间入口处应设置乙级防火门,严禁利用楼、电梯间为地下车库进行自然通风。",
            "entity": LayerConfig.BASIC_LAYERS.value['basic'] + ['door', 'window', 'parking',
                                                                 'elevator_box', 'elevator_door', 'emergency_door'],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        107003: {
            "name": "除骑楼、建筑连接体、地铁相关设施及连接城市的管线、管沟、管廊等市政公共设施以外，建筑物及其附属的下列设施不应突出道路红线或用地红线建造",
            "entity": ["building", "border", "red_line", "red_line_sub"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        107004: {
            "name": "住宅、托儿所、幼儿园、中小学及其他少年儿童专用活动场所的栏杆必须采取防止攀爬的构造。当采用垂直杆件做栏杆时，其杆件净间距不应大于0．11m。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]+["elevation_handrail"],
            "operation": ["combination"],
        },
        111001: {
            "name": "电梯井、管道井、电缆井和楼梯间应分别独立设置。管道井、电缆井的井壁应采用不燃材料，且耐火极限不应低于1．00h；电梯井的井壁应采用不燃材料，且耐火极限不应低于2．00h。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door", "elevator_door", "elevator_box"],
            "operation": ["combination", "segmentation", "classification"],
        },
        111002: {
            "name": "地库管井门必须是甲乙丙级防火门",
            "entity": LayerConfig.BASIC_LAYERS.value["underground_segment"] + ["door", "parking"],
            "operation": ["combination", 'segmentation', "classification"],
        },
        104028: {
            "name": "住宅至道路边缘的最小距离，应符合表4．1．2的规定。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ['road', "fire_road"],
            "operation": [],
        },
        514: {
            "name": "无障碍通路应贯通，并应符合表4．3．3的规定",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.BASIC_LAYERS.value["indoor_access_segment"] + ["door","podao","arrow"],
            "operation": ["combination", 'segmentation'],
        },
        # 515: {
        #     "name": "",
        #     "entity": [],
        #     "operation": [],
        # },
        105004: {
            "name": "居住建筑(含电梯)无障碍设计",
            "entity": LayerConfig.BASIC_LAYERS.value['basic'] + ['elevator_box', 'door', 'podao'],
            "operation": ["combination", 'segmentation', "classification"],
        },
        107005: {
            "name": "中等城市、大城市的主干路交叉口，自道路红线交叉点起沿线70.0m范围内不应设置机动车出入口",
            "entity": ["road", "car_lane", "red_line", "red_line_sub", "road_center_line", "fire_road"],
            "operation": ["combination", "segmentation", "classification"],
        },
        103026: {
            "name": "候梯厅深度不应小于多台电梯中最大轿厢的深度，且不应小于1.50m",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "elevator_door", "elevator_box"],
            "operation": ["combination", 'segmentation', "classification"],
        },
        108002: {
            "name": "机动车道路转弯半径应根据通行车辆种类确定。微型、小型车道路转弯半径不应小于3.5m。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ['car_lane'],
            "operation": [],
        },
        114001: {
            "name": "住区相邻高速公路或快速路时，临道路一侧退后用地红线距离应大于15ｍ",
            "entity": ["road", "car_lane", "red_line", "red_line_sub", "fire_road"],
            "operation": ["combination", 'segmentation', "classification"],
        },
        105005: {
            "name": "坡道起点、终点和中间休息平台的水平长度不应小于1.5m",
            "entity": LayerConfig.BASIC_LAYERS.value['basic'] + ['podao', "arrow", "door"],
            "operation": ["combination", 'segmentation', "classification"],
        },
        105006: {
            "name": "坡道的最大高度和水平长度，应满足需求",
            "entity": ["wall", "pillar", "podao", "podao_extra", "separator", "gutter"],
            "operation": ["combination", 'segmentation', "classification"],
        },
        104034: {
            "name": "10层及10层以上的住宅建筑至少沿建筑的一个长边设置消防车道。",
            "entity": ["building", "road", "road_center_line", "border", "fire_road"],
            "operation": [],
        },
        104037: {
            "name": "",
            "entity": [],
            "operation": [],
        },
        104038: {
            "name": "",
            "entity": [],
            "operation": [],
        },
        104039: {
            "name": "",
            "entity": [],
            "operation": [],
        },
        104040: {
            "name": "卧室、起居室（厅）、厨房应设置外窗，窗地面积比不应小于1/7",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["window"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        104041: {
            "name": "楼梯梯段净宽不应小于1.10m。六层及六层以下住宅，一边设有栏杆的梯段净宽不应小于1.00m。楼梯踏步宽度不应小于0.26m，踏步高度不应大于0.175m。",
            "entity": LayerConfig.BASIC_LAYERS.value["stair_dayang"],
            "operation": [],
        },
        103034: {
            "name": "楼梯梯段净宽不应小于1．10m，不超过六层的住宅，一边设有栏杆的梯段净宽不应小于1．00m。",
            "entity": LayerConfig.BASIC_LAYERS.value["stair_dayang"] + ['elevator_door', "fire_hydrant"],
            "operation": [],
        },
        103035: {
            "name": "楼梯踏步宽度不应小于0．26m，踏步高度不应大于0．175m。扶手高度不应小于0．90m。楼梯水平段栏杆长度大于0．50m时，其扶手高度不应小于1．05m。",
            "entity": LayerConfig.BASIC_LAYERS.value["stair_dayang"],
            "operation": [],
        },
        107006: {
            "name": "楼梯平台上部及下部过道处的净高不应小于2．0m;梯段净高不应小于2．2m。",
            "entity": LayerConfig.BASIC_LAYERS.value["stair_dayang"],
            "operation": [],
        },
        107007: {
            "name": "栏杆扶手宽度要求;水平栏杆大于0.5m时候，栏杆高度 大于 1.05m 其他栏杆 0.9m",
            "entity": LayerConfig.BASIC_LAYERS.value['basic'] + ['elevation_handrail'],
            "operation": [],
        },
        103036: {
            "name": "建筑入口无障碍设计规则",
            "entity": LayerConfig.BASIC_LAYERS.value['basic'] + ['door', 'podao', 'pillar', 'wall',
                                                                 'elevation_handrail', 'plan_handrail'],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103037: {
            "name": "卧室、起居室（厅）、厨房应设置外窗，窗地面积比不应小于1/7",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["window"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103038: {
            "name": "规则568当楼梯间设置采光窗时，采光窗洞口的窗地面积比不应低于1/12.",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["window", "elevator_box", "elevator_door"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        106004: {
            "name": "住宅单元的疏散楼梯，当分散设置确有困难且任一户门至最近疏散楼梯间入口的距离不大于10m 时，可采用剪刀楼梯间",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ["combination", "segmentation", "classification"],
        },
        106005: {
            "name": "建筑内的安全出口应分散布置，每个住宅单元每层相邻两个安全出口最近边缘之间的水平距离不应小于5m",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"]+["door", "elevator_box", "segment"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        # 106006: {
        #     "name": "防烟楼梯间除应符合本规范第6．4．1条的规定, 还需符合其他规定",
        #     "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["pillar", "pipe"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        103039: {
            "name": "住宅设计应在方案设计阶段布置信报箱的位置。信报箱宜设置在住宅单元主要入口处",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103041: {
            "name": "套型设计时应减少直接开向起居厅的门的数量。起居室（厅）内布置家具的墙面直线长度宜大于3m",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        103043: {
            "name": "厨房宜布置在套内近入口处",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ['door', "window", "floor_drain_mix",
                                                                          "kitchen_exhaust_pipe"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103044: {
            "name": "单排厨房净宽1.5m;双排设备之间净距0.9m",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["window", "floor_drain_mix", "elevator_stair", "elevator_door"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103045: {
            "name": "每套住宅宜设阳台或平台",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103046: {
            "name": "套内入口过道净宽不宜小于1．20m；通往卧室、起居室（厅）的过道净宽不应小于1．00m；通往厨房、卫生间、贮藏室的过道净宽不应小于0．90m",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103047: {
            "name": "套内楼梯当一边临空时，梯段净宽不应小于0．75m；当两侧有墙时，墙面之间净宽不应小于0．90m，并应在其中一侧墙面设置扶手。",
            "entity": LayerConfig.BASIC_LAYERS.value['basic'] + ['door', 'elevator_stair', 'wall', 'elevation_handrail','window'],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103056: {
            "name": "窗台高度低于或等于0．45m时，防护高度从窗台面起算不应低于0．90m。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["window",
                                                                 "dayang_handrail",
                                                                 "completion_surface"],
            "operation": ['combination'],
        },
        106007: {
            "name": "地下车库防火规范",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        106008: {
            "name": "住宅建筑的户门、安全出口、疏散走道和疏散楼梯的各自总净宽度应经计算确定，且户门和安全出口的净宽度不应小于0．90m，疏散走道、疏散楼梯和首层疏散外门的净宽度不应小于1．10m。",
            "entity": LayerConfig.BASIC_LAYERS.value['basic'] + ['door', 'pillar', 'wall', "elevator_box",
                                                                 "elevator_door", 'elevation_handrail'],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        # 103048: {
        #     "name": "套型的使用面积应符合下列规定：1 由卧室、起居室（厅）、厨房和卫生间等组成的套型，其使用面积不应小于30m2； 2 由兼起居的卧室、厨房和卫生间等组成的最小套型，其使用面积不应小于22m2",
        #     "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
        103049: {
            "name": "每套住宅应设卫生间，应至少配置便器、洗浴器、洗面器三件卫生设备。三件卫生设备集中配置的卫生间的使用面积不应小于2．50m2",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door",
                                                                          "washbasin",
                                                                          "closestool",
                                                                          "diamond_bath",
                                                                          "floor_drain_mix"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103050: {
            "name": "卫生间可根据使用功能要求组合不同的设备。不同组合的空间使用面积规定",
            "entity": LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["washbasin", "closestool",
                                                                          "diamond_bath"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103051: {
            "name": "楼梯平台净宽不应小于楼梯梯段净宽，且不得小于1．20m。楼梯平台的结构下缘至人行通道的垂直高度不应低于2．00m。",
            "entity": LayerConfig.BASIC_LAYERS.value["stair_dayang"],
            "operation": ["combination", "segmentation", "classification"],
        },
        103052: {
          "name": "公共出入口台阶踏步宽度不宜小于0．30m，台阶踏步数不应少于2级，当高差不足2级时，应按坡道设置；台阶宽度大于1．80m时，两侧宜设置栏杆扶手",
          "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "stair_dayang_plan_stair", "elevation_handrail"],
          "operation": ['combination', 'segmentation', 'classification'],
         },
        104051: {
            "name": "住宅单元至少有一个可以通过机动车的出入口",
            "entity": ["building", "border", "road", "car_lane", "fire_road"],
            "operation": [],
        },
        104043: {
            "name": "住宅与附建公共用房的出入口应分开布置",
            "entity": LayerConfig.BASIC_LAYERS.value['basic'] + ['door', 'window'],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        107008: {
            'name': '建筑物与相邻建筑基地及其建筑物的关系应符合下列规定：紧贴建筑基地边界建造的建筑物不得向相邻建筑基地方向开设洞口、门、废气排除口及雨水排泄口。',
            "entity": LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'window'],
            "operation": [],
        },
        105007: {
            'name': '居住建筑应按每100套住房设置不少于2套无障碍住房。',
            "entity": [],
            "operation": [],
        },
        117001: {
            "name": "当屋面坡度大于20％时，绝热层、防水层、排(蓄)水层、种植土层等均应采取防滑措施",
            "entity": LayerConfig.BASIC_LAYERS.value['indoor_segment']+["building"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        116001: {
            "name": "非地下车库的窗户，高度小于900mm时，附近应设栏杆",
            "entity": LayerConfig.BASIC_LAYERS.value['stair_dayang'] +
                      ["elevation_handrail", "window", "door", "elevation_window"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        116002: {
            "name": "非地下空间的窗户，高度小于900mm时，附近应设栏杆，且栏杆高度需大于900mm",
            "entity": LayerConfig.BASIC_LAYERS.value['stair_dayang']+["elevation_handrail", "window","door", "elevation_window"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103055: {
            "name": "楼梯为剪刀梯时，楼梯平台的净宽不得小于1．30m",
            "entity": LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'elevator_box'],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103063: {
            "name": "设有单元安全防护门的住宅，信报箱的投递口应设置在门禁以外。当通往投递口的专用通道设置在室内时，通道净宽应不小于0．60m。",
            "entity": LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'mailbox'],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103066: {
            "name": "厨房应设置洗涤池、案台、炉灶及排油烟机、热水器等设施或为其预留位置",
            "entity": LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'window',
                                                                          'floor_drain_mix'],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        104020: {
            "name": "厨房应设置洗涤池、案台、炉灶及排油烟机、热水器等设施或为其预留位置",
            "entity": LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'window',
                                                                          'floor_drain_mix'],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103067: {
            "name": "厨房应按炊事操作流程布置",
            "entity": LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'window',
                                                                          'floor_drain_mix'],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103069: {
            "name": "七层及七层以上住宅和寒冷、严寒地区住宅宜采用实体栏板。",
            "entity": LayerConfig.BASIC_LAYERS.value['basic'] +
                      ["dayang_handrail", "elevation_handrail", "completion_surface", "wall"],
            "operation": ["combination", "classification"],
        },
        103071: {
            "name": "阳台应采取有组织排水措施",
            "entity": LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'window',
                                                                          'floor_drain', 'arrow'],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103077: {
            "name": "信报箱的设置不得降低住宅基本空间的天然采光和自然通风标准",
            "entity": LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'window',
                                                                          'mailbox'],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        103078: {
            "name": "厨房的共用排气道应与灶具位置相邻",
            "entity": LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'window',
                                                                          'kitchen_exhaust_pipe', "floor_drain_mix"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        105013: {
            "name": "无障碍住房及宿舍的其他规定：1 、单人卧室面积不应小于7．00m2，双人卧室面积不应小于10．50m2，兼起居室的卧室面积不应小于16．00m2，起居室面积不应小于14．00m2，厨房面积不应小于6．00m2；2 、设坐便器、洗浴器(浴盆或淋浴)、洗面盆三件卫生洁具的卫生间面积不应小于4．00m2；设坐便器、洗浴器二件卫生洁具的卫生间面积不应小于3．00m2；设坐便器、洗面盆二件卫生洁具的卫生间面积不应小于2．50m2；单设坐便器的卫生间面积不应小于2．00m2；轮椅坡道宜设计成直线形、直角形或折返形。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["window", "door", "washbasin", "closestool", "diamond_bath", "floor_drain_mix", "arrow",
                       "annotation_line"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        105017: {
            "name": "无障碍电梯的候梯厅应符合下列规定：1  候梯厅深度不宜小于1．50m，公共建筑及设置病床梯的候梯厅深度不宜小于1．80m；2  呼叫按钮高度为0．90m～1．10m；3  电梯门洞的净宽度不宜小于900mm；4  电梯出入口处宜设提示盲道；5  候梯厅应设电梯运行显示装置和抵达音响。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["window", "door"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        108004: {
            "name": "按管理方式，机动车库宜设置值班室、管理办公室、控制室、卫生间等辅助用房",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] +
                      LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["window", "door"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        108005: {
            "name": "地下三层及以下机动车库应设置乘客电梯，电梯的服务半径不宜大于60m。 ",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] +
                      LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["window", "door"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        106026: {
            "name": "建筑高度大于54m的住宅建筑，每户应有一间房间符合下列规定：1 应靠外墙设置，并应设置可开启外窗；2 内、外墙体的耐火极限不应低于1．00h，该房间的门宜采用乙级防火门，外窗的耐火完整性不宜低于1．00h。",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["window", "door"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        107016: {
            "name": "室外机动车停车场应符合下列规定： 1 停车场地应满足排水要求，排水坡度不应小于0.3％；",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["parking", "road", "building", "fire_road"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        106031: {
            "name": "机房上的门应采用甲级防火门",
            "entity": LayerConfig.BASIC_LAYERS.value["basic"] + ["door"],
            "operation": ["combination", "segmentation", "classification"],
        },
        103074: {
            "name": "套内楼梯的踏步宽度不应小于0.22m；高度不应大于0.20m",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["window", "door", "elevator_stair", "elevator_box"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        106029: {
            "name": "封闭楼梯间除应符合本规范第6．4．1条的规定外，尚应符合下列规定：1 不能自然通风或自然通风不能满足要求时，应设置机械加压送风系统或采用防烟楼梯间。2 除楼梯间的出入口和外窗外，楼梯间的墙上不应开设其他门、窗、洞口。3 高层建筑、人员密集的公共建筑、人员密集的多层丙类厂房、甲、乙类厂房，其封闭楼梯间的门应采用乙级防火门，并应向疏散方向开启；其他建筑，可采用双向弹簧门。4. 楼梯间的首层可将走道和门厅等包括在楼梯间内形成扩大的封闭楼梯间，但应采用乙级防火门等与其他走道和房间分隔。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["window", "door", "elevator_stair", "elevator_box"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        106030: {
            "name": "疏散用楼梯和疏散通道上的阶梯不宜采用螺旋楼梯和扇形踏步；确需采用时，踏步上、下两级所形成的平面角度不应大于10°",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["window", "door", "elevator_stair", "elevator_box"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        104047: {
            "name": "双车道道路的路面宽度不应小于6m；宅前路的路面宽度不应小于2．5m；当尽端式道路的长度大于120m时，应在尽端设置不小于12m×12m的回车场地",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["window", "door", "road_center_line", "road", "fire_road"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        104052: {
            "name": "地面水的排水系统，应根据地形特点设计，地面排水坡度不应小于0.2％",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["window", "door", "annotation_line", "red_line", "red_line_sub", "road_center_line", "road", "fire_road"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        106017: {
            "name": "消防车道的坡度不宜大于8％",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["window", "door", "road_center_line", "road", "fire_road", "red_line", "red_line_sub"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        107009: {
            "name": "单车道路宽不应小于4．0m，双车道路宽住宅区内不应小于6．0m,道路转弯半径不应小于3．0m，消防车道应满足消防车最小转弯半径要求, 尽端式道路长度大于120．0m时，应在尽端设置不小于12．0m×12．0m的回车场地",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["window", "door",  "red_line", "red_line_sub", "road_center_line", "road", "fire_road"],
            "operation": ['combination', 'segmentation', 'classification'],
        },
        108006: {
            "name": "坡道式出入口可采用单车道或双车道，坡道最小净宽应符合表4．2．10-1 的规定。",
            "entity": ["wall", "pillar", "podao", "podao_extra", "separator", "filling", "podao_mark", "podao_edge", "road_center_line", "car_lane"],
            "operation": ["combination", "segmentation"],
        },
        108010: {
            "name": "车库总平面内的道路、广场应有良好的排水系统，道路纵坡坡度不应小于0.2％",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["window", "door", "car_lane"],
            "operation": [],
        },
        108007: {
            "name": "车辆出入口的最小间距不应小于15m，并宜与基地内部道路相接通，当直接通向城市道路时，应符合本规范第3．1．6 条的规定。",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["window", "door", "garage_exit",
                                                                          "basement_contour", 'road', "red_line","garage_podao_exit"],
            "operation": ['segmentation'],
        },
        103062: {
            'name': '住户的公共出入口与附建公共用房的出入口应分开布置',
            'entity': ['door'],
            'operation': ['combination', 'classification', 'segmentation'],
        },
        104050: {
            'name': '住户的公共出入口与附建公共用房的出入口应分开布置',
            'entity': ['door'],
            'operation': ['combination', 'classification', 'segmentation'],
        },
        103080: {
            'name': '严寒、寒冷、夏热冬冷地区的厨房，应设置供厨房房间全面通风的自然通风设施。',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + LayerConfig.BASIC_LAYERS.value[
                'basic'] + ["door", "window"],
            'operation': ["combination", "classification", "segmentation"],
        },
        105019: {
            'name': '无障碍电梯的轿厢应符合下列规定',
            'entity': LayerConfig.BASIC_LAYERS.value['basic'] + LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      ['door', 'elevator_box', 'elevator_door', 'window', "kan_xian"],
            'operation': ["combination", "classification", "segmentation"],
        },
        106020: {
            'name': '建筑物与消防车登高操作场地相对应的范围内，应设置直通室外的楼梯或直通楼梯间的入口。',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      ['door', 'window', 'stair_dayang_plan_stair', 'elevator_box', 'elevator_stair', 'building',
                       'extinguishing_ascend_field', "road_center_line", "road", "fire_road"],
            'operation': ["combination", "classification", "segmentation"],
        },
    }
