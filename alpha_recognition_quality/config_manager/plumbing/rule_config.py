# -*- coding: utf-8 -*-

from enum import Enum

# from rule_engine.single_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig


class RuleConfig(Enum):
    # 万科审核规则列表
    VANKE_RULES = {
        # 给排水平面图
        DrawingType.TOWER_WATER_SUPPLY: [301005, 301004, 303034, 303036, 302001, 305010, 305012, 308004,
                                         305013, "1302009", "1302010", "1302015", "1300030", "1302012", "1300031",
                                         "1300040", "1303004", "1303002", "1303001", "1303003", "1303005"],  # 塔楼给水平面图
        DrawingType.TOWER_WATER_DRAIN: [301005, 301004, 301007, 301008, 302001, 302002, 303020, 303021, 303029, 303003,
                                        302007, 303004, 303013, 303040, 303043, "1302009", "1302010", "1300026",
                                        "1302012", "1303001", "1303002", "1303003", "1303004", "1303005"],  # 塔楼排水平面图

        DrawingType.WUMIAN_WATER_SUPPLY: [],  # 屋面给水平面图
        # 屋面排水平面图
        DrawingType.WUMIAN_WATER_DRAIN: [303003, 303028, 307004, 303040, ],
        DrawingType.WUDING_WATER_SUPPLY: [],  # 屋顶给水平面图
        DrawingType.WUDING_WATER_DRAIN: [303003],  # 屋顶排水平面图
        DrawingType.UNDERGROUND_WATER_SUPPLY: [303023, 303032, 303034, 303042, 305010, 303005, 303007, 312001,
                                               305012, 308004, 308009, 305013, "1302017", "1302015", "1300028",
                                               "1300027", "1300031", "1300030", "1300040", "1300046", "1304001"],
        # 地下室给水平面图
        # 地下室排水平面图
        DrawingType.UNDERGROUND_WATER_DRAIN: [303003, 303023, 312001, 303013, 303040, 305022, 303043, "1302017",
                                              "1300026", "1304001"],
        # 喷淋平面图
        DrawingType.SPRINKLER: ["1302012"],  # 喷淋平面图
        # 地下室喷淋平面图
        DrawingType.UNDERGROUND_SPRINKLER: [306001, 306002, 306003, 306006, "1300029"],
        # 给排水系统图
        # 地上给水系统图
        DrawingType.INDOOR_WATER_SUPPLY_SYSTEM: [305014, 305018, 302004, 301010, 305021, "1300004", "1300018",
                                                 "1302011", "1300032"],
        # 地上排水系统图
        DrawingType.INDOOR_WATER_DRAIN_SYSTEM: [303039, 305014, 303025, 303009, 303046, 303027, "1302013", "1302011",
                                                "1300032", "1302016", "1300043"],

        # 地下室给水系统图
        DrawingType.UNDERGROUND_WATER_SUPPLY_SYSTEM: [305014, "1300032"],
        # 地下室排水系统图
        DrawingType.UNDERGROUND_WATER_DRAIN_SYSTEM: [305014, "1300032"],
        # 地下室喷淋系统图
        DrawingType.UNDERGROUND_SPRINKLER_SYSTEM: [305014, "1300032"],
        # 地下室消火栓系统图
        DrawingType.UNDERGROUND_FIRE_HYDRANT_SYSTEM: [305014, "1300032"],
        # 给排水设计说明
        DrawingType.GEIPAISHUI_DESIGN: ["1302014"],  # 给排水设计说明
        # 给排水总图
        DrawingType.WATER_SUPPLY_SITE_PLAN: [305008],  # 给水总图
        DrawingType.WATER_DRAIN_SITE_PLAN: [303012, 303037, 303011],  # 排水总图
        # 大样图
        DrawingType.PUMP_DAYANG: [303003],  # 水泵房大样图
        # 户型大样图
        DrawingType.GEIPAISHUI_HUXING_DAYANG: [303019, 303022, 303024, "1300007", "1302009", "1300037"],
        # 雨水回收大样图
        DrawingType.RAINWATER_RECLAIM_DAYANG: [307002, 307006, "1302018"],
        # 11.1添加图纸类型
        DrawingType.OUTDOOR_GEIPAISHUI_DESIGN: [],  # 室外给排水设计说明
        DrawingType.TOWER_FIRST_FLOOR_SUPPLY: [301004, "1302015"],  # 塔楼首层给水平面图
        DrawingType.TOWER_FIRST_FLOOR_DRAIN: [301004, 303045],  # 塔楼首层排水平面图
        # 塔楼二层给水平面图
        DrawingType.TOWER_SECOND_FLOOR_SUPPLY: [301004, 301005, "1302015", "1300030", "1303004", "1303002", "1303001",
                                                "1303003", "1303005"],
        # 塔楼二层排水平面图
        DrawingType.TOWER_SECOND_FLOOR_DRAIN: [301004, 301005, "1300026", "1303004", "1303002", "1303001", "1303003",
                                               "1303005"],
        DrawingType.GAS_EXTINGUISH: [],  # 气体灭火图
        # 2.22添加图纸类型
        DrawingType.TOWER_BINAN_SUPPLY: ["1302015"],  # 塔楼避难层给水平面图
        DrawingType.TOWER_BINAN_DRAIN: [],  # 塔楼避难层排水平面图
    }

    # 规则详情
    # REF: https://www.kdocs.cn/p/51356796370?from=docs&source=docsWeb
    CONFIGURATION = {

        "1300032": {
            'name': '消防给水系统管道的最高点处宜设置自动排气阀。',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["排气阀"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["消火栓横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["喷淋横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["废水横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["排气阀门"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['消火栓-给排水'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['雨水井'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['减压阀'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["套管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['检查口'],
            'operation': ["combination", "segmentation", "classification"],
        },

        "1300030": {
            'name': '给水管道不得敷设在烟道、风道、电梯井',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["给水横管"] +
                      ['hydrant_hpipe', 'sprinkler_hpipe', 'inflow_hpipe', 'window', 'door', 'annotation_line'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'],
            'operation': ['combination', 'segmentation', 'classification'],
        },

        "1300026": {
            'name': '排水管道不得穿越下列场所：1. 卧室、客房、病房和宿舍等人员居住的房间；2. 生活饮用水池（箱）上方',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      ['window', 'door'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["排水横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["所有立管"],
            'operation': ["combination", "segmentation", "classification"],
        },

        "1300028": {
            'name': '消防水泵房应符合下列规定：附设在建筑物内的消防水泵房，不应设置在地下三层及以下，或室内地面与室外出入口地坪高差大于10m的地下楼层',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      ['window', 'door'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["标高构件"],
            'operation': ["combination", "segmentation", "classification"],
        },

        "1302015": {
            'name': '消防电梯前室应设置室内消火栓，并应计入消火栓使用数量',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      ["fire_hydrant", "elevator_box", "door", "window", ],
            'operation': ["combination", "segmentation", "classification"],
        },

        "1302017": {
            'name': '排水管穿越地下室外墙或地下构筑物的墙壁处，应采取防水措施',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["排水横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["套管"] +
                      LayerConfig.BASIC_LAYERS.value['underground_segment'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["消火栓"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["减压阀"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["集水坑"] +
                      ["sleeve", 'window', 'door'],
            'operation': ['combination', 'segmentation', 'classification'],

        },

        "1300007": {
            'name': '大便器排水管最小管径不得小于100mm',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["所有立管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["地漏"],
            'operation': ["text_information"],
        },
        "1300018": {
            'name': '室内消火栓栓口压力和消防水枪充实水柱，应符合下列规定: 消火栓栓口动压力不应大于 0.50MPa ；当大于 0.70MPa 时必须设置减压装置',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["消火栓横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["消火栓-给排水"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["标高构件"],
            'operation': ['combination', 'classification', 'text_information'],
        },
        "1300027": {
            'name': '生活用水水池（箱）应符合下列规定：2.建筑物内的水池（箱）应设置在专用房间内; 3.建筑物内的水池（箱）不应毗邻配变电所',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ['window', 'door', 'tank'],
            'operation': ['combination', 'segmentation', 'classification']
        },
        "1300029": {
            'name': '配水管两侧每根配水支管控制的标准流量洒水喷头数量，轻危险级、中危险级场所不应超过8只',
            'entity': LayerConfig.BASIC_LAYERS.value['underground_segment'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["喷头"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["喷淋横管"] +
                      ['window', 'door'],
            'operation': ["combination", "segmentation", "classification"],
        },
        "1300031": {
            'name': '消防电梯前室应设置室内消火栓',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      ["fire_hydrant", "elevator_box", "door", "window", ],
            'operation': ["combination", "segmentation", "classification"],
        },
        "1300037": {
            'name': '冷水管、热水管平行时，热水管在上；卫生器具同时连接冷水管和热水管时，冷水管在右侧。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["生活给水横管"] +
                      ["door", "window"],
            'operation': ["combination", "segmentation", "classification"],
        },
        "1300040": {
            'name': '建筑室内消火栓的设置位置应满足火灾扑救要求。',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      ["fire_hydrant", "elevator_stair", "door", "window", "parking"],
            'operation': ["combination", "segmentation", "classification"],
        },
        "1300043": {
            'name': '生活排水管道的立管顶端应设置伸顶通气管',
            'entity': LayerConfig.BASIC_LAYERS.value['basic'] + ['ventilation_cap', 'sewage_hpipe', 'waste_hpipe'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        "1300046": {
            'name': '建筑物内的生活饮用水水池（箱）体，应采用独立结构形式，不得利用建筑物的本体结构作为水池（箱）的壁板、底板及顶盖',
            'entity': LayerConfig.BASIC_LAYERS.value['underground_segment'] +
                      ["tank", "window", "door"],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        # 301003: {
        #     'name': '住宅应设室内给水排水系统',
        #     'entity': ["vpipe", "annotation_line"],
        #     'operation': ['combination', 'classification']
        # },
        "1300004": {
            'name': '套内用水点供水压力不宜大于0．20MPa，且不应小于用水器具要求的最低压力',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["生活给水横管"] +
                      ['valve', 'window', 'door'],
            'operation': ['combination', 'segmentation', 'classification'],
        },

        "1302013": {
            'name': '凝结水支管管径不大于De32',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["空调冷凝水横管"] +
                      ["dilou"],
            'operation': ['combination', 'segmentation', 'classification'],
        },

        "1302011": {
            'name': '消火栓系统：合理设置管径、住宅立管及干管不小于DN100',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["消火栓横管"] +
                      ["fire_hydrant", "valve", "exhaust_valve",
                       "pressure_meter", "ventilation_cap"],
            'operation': ['combination', 'segmentation', 'classification'],

        },
        "1302010": {
            'name': '与建筑专业配合，合理设置管井位置，尽量避免设置于楼梯休息平台',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["elevator_stair", "elevator_box"],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        "1302009": {
            'name': '厨房和卫生间的排水立管应分别设置，厨房布置应考虑立管布置位置；如有条件，厨房废水可与生活阳台洗衣机废水合用排水立管',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["所有立管"] + ['furniture', 'kitchen_toilet'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["废水横管"],
            'operation': ["text_information"],
        },
        "1302012": {
            'name': '水泵房、变配电所（室）、开闭站、配电间、强弱电间等房间不得设置自动喷淋系统',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["sprayer", "sprinkler_hpipe", "sprinkler_vpipe"],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        "1302014": {
            'name': '给水管道不宜穿越变形缝。当必须穿越时，应设置补偿管道伸缩和剪切变形的装置。',
            'entity': [],
            'operation': ['text_information'],
        },
        "1302018": {
            'name': '供水管道和补水管道上应设水表计量装置',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["水表"],
            'operation': ['combination', 'classification']
        },
        "1304001": {
            'name': "地下室无取水点，物业无法冲洗地面",
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['faucet'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        "1303001": {
            "name": "卫生间立管数量货板是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["pipe", 'sewage_hpipe', 'waste_hpipe'],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1303003": {
            "name": "污水立管位置，板房与货量是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["pipe", 'sewage_hpipe', 'waste_hpipe'],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1303005": {
            "name": "阳台地漏位置，板房与货量是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["floor_drain"],
            "operation": ["combination", "segmentation", "classification"],
        },
        301004: {
            'name': '住宅的给水总立管、雨水立管、消防立管、采暖供回水总立管和电气、电信干线（管），不应布置在套内。公共功能的阀门、电气设备和用于总体调节和检修的部件，应设在共用部位',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["valve", "annotation_line", "window", "door", "fire_hydrant", "kitchen_exhaust_pipe"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['清扫口'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['套管'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['减压阀'],
            'operation': ['combination', 'classification', "segmentation"],
        },
        # 301005: {
        #     'name': '住宅的水表、电能表、热量表和燃气表的设置应便于管理。',
        #     'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment']+['door', 'window'] +
        #               LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'] +
        #               LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['水表'],
        #     'operation': ['combination', 'segmentation', 'classification'],
        # },
        301007: {
            'name': '厨房和卫生间的排水立管应分别设置。排水管道不得穿越卧室。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"]
                      + LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['排水横管']
                      + LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管']
                      + ["door", "annotation_line", "window"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        301008: {
            'name': '设有淋浴器和洗衣机的部位应设置地漏。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"]
                      + LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['系统地漏']
                      + ["door", "kitchen_toilet", "furniture", "window"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        # 301009: {
        #     'name': '',
        #     'entity': [],
        #     'operation': [],
        # },
        302001: {
            'name': '下列设施不应设置在住宅套内，应设置在共用空间内：1 公共功能的管道，包括给水总立管、消防立管、雨水立管、采暖（空调）供回水总立管和配电和弱电干线（管）等，设置在开敞式阳台的雨水立管除外；2 公共的管道阀门、电气设备和用于总体调节和检修的部件，户内排水立管检修口除外；3 采暖管沟和电缆沟的检查孔。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["door", "valve", "annotation_line", "window"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'],
            'operation': ['combination', 'segmentation', 'classification']
        },
        # 302003: {
        #     'name': '',
        #     'entity': [],
        #     'operation': [],
        # },
        # 302006: {
        #     'name': '',
        #     'entity': [],
        #     'operation': [],
        # },
        302007: {
            'name': '排水立管不应设置在卧室内',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ['window', 'door', 'annotation_line'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        # 303001: {
        #     'name': '从生活饮用水管网向下列水池（箱）补水时应符合下列规定：1 向消防等其他非供生活饮用的贮水池（箱）补水时，其进水管口最低点高出溢流边缘的空气间隙不应小于150mm； 2 向中水、雨水回用水等回用水系统的贮水池（箱）补水时，其进水管口最低点高出溢流边缘的空气间隙不应小于进水管管径的2．5倍，且不应小于150mm。',
        #     'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + \
        #               LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["给水横管"] + \
        #               ["annotation_line"],
        #     'operation': ['combination', 'segmentation', 'classification']
        # },
        # 303002: {
        #     'name': '生活饮用水水池（箱）应设置消毒装置',
        #     'entity': [],
        #     'operation': []
        # },
        303003: {
            'name': '排水管道不得穿越卧室和水箱',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["排水横管"] +
                      ['tank', 'window', 'door', 'annotation_line'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['减压阀'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        303004: {
            'name': '住宅厨房间的废水不得与卫生间的污水合用一根立管',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ['window', 'door', 'annotation_line'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        303005: {
            'name': '雨水供水管道应与生活饮用水管道分开设置，严禁回用雨水进入生活饮用水给水系统',
            'entity': LayerConfig.BASIC_LAYERS.value['underground_segment'] +
                      ['window', 'door'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["雨水横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["生活给水横管"],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        303007: {
            'name': '生活用水水池（箱）应符合下列规定：2.建筑物内的水池（箱）应设置在专用房间内; 3.建筑物内的水池（箱）不应毗邻配变电所',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ['window', 'door', 'tank'],
            'operation': ['combination', 'segmentation', 'classification']
        },
        303009: {
            'name': '生活排水管道应按下列规定设置检查口',
            'entity': ["sewage_hpipe", "waste_hpipe", "inspection_hole", "elevation_symbol"],
            'operation': ['classification', 'combination', 'segmentation'],
        },
        303012: {
            'name': '化粪池应设通气管，通气管排出口设置位置应满足安全、环保要求；',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["通气横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["所有立管"] +
                      ["annotation_line", "building", 'window', 'door'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        303013: {
            'name': '下列场所不应布置雨水管道：1 生产工艺或卫生有特殊要求的生产厂房、车间；  2 贮存食品、贵重商品库房；3 通风小室、电气机房和电梯机房',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["雨水横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["雨水立管"] +
                      ["annotation_line", 'window', 'door'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        303020: {
            'name': '地漏应设置在有设备和地面排水的下列场所:\n卫生间、盥洗室、淋浴间、洗衣机',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["洗衣机"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["地漏"] +
                      ["door", "kitchen_toilet", 'window'],
            'operation': ["combination", "segmentation", "classification"],
        },
        303021: {
            'name': '地漏应设置在易溅水的器具或冲洗水嘴附近',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ['kitchen_toilet', 'floor_drain', 'window', 'door'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        303023: {
            'name': '排水管穿越地下室外墙或地下构筑物的墙壁处，应采取防水措施',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["排水横管"] +
                      LayerConfig.BASIC_LAYERS.value['underground_segment'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["消火栓"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["减压阀"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["集水坑"] +
                      ["sleeve", 'window', 'door'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        303025: {
            'name': '建筑物内排出管最小管径不得小于50mm',
            'entity': ["sewage_hpipe", "waste_hpipe", "rain_hpipe", "condensate_hpipe"],
            'operation': ['classification', 'combination', 'segmentation'],
        },
        303029: {
            'name': '居住建筑设置雨水内排水系统时，除敞开式阳台外应设在公共部位的管道井内',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ['window', 'door', 'annotation_line'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        303032: {
            'name': '建筑物内的生活饮用水水池（箱）体，应采用独立结构形式，不得利用建筑物的本体结构作为水池（箱）的壁板、底板及顶盖',
            'entity': LayerConfig.BASIC_LAYERS.value['underground_segment'] +
                      ["tank", "window", "door"],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        303034: {
            'name': '室内给水管道布置应符合下列规定： 1 不得穿越变配电房、电梯机房、通信机房',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["生活给水横管"] +
                      ['hydrant_hpipe', 'sprinkler_hpipe', 'window', 'door', 'annotation_line'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        # 303035: {
        #     'name': '小区生活排水与雨水排水系统应采用分流制',
        #     'entity': LayerConfig.BASIC_LAYERS.value['basic'] +
        #               LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['污水横管'] +
        #               LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['雨水横管'] +
        #               LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'],
        #     'operation': [],
        # },
        303036: {
            'name': '给水管道不得敷设在烟道、风道、电梯井',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["生活给水横管"] +
                      ['hydrant_hpipe', 'sprinkler_hpipe', 'inflow_hpipe', 'window', 'door', 'annotation_line'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        303040: {
            'name': '室内排水管道布置应符合下列规定：3 排水管道不得敷设在食品和贵重商品仓库、通风小室、电气机房和电梯机房内；4 排水管道不得穿过变形缝、烟道',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["排水横管"] +
                      ['window', 'door', 'annotation_line'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        303042: {
            'name': '给水管道不得敷设在烟道、风道、电梯井',
            'entity': LayerConfig.BASIC_LAYERS.value["underground_segment"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["生活给水横管"] +
                      ['hydrant_hpipe', 'sprinkler_hpipe', 'inflow_hpipe', 'window', 'door', 'annotation_line'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        303043: {
            'name': '除土建专业允许外，雨水管道不得敷设在结构柱内',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["雨水横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["所有立管"] +
                      ['pillar', 'window', 'door'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        303039: {
            'name': '生活排水管道的立管顶端应设置伸顶通气管',
            'entity': LayerConfig.BASIC_LAYERS.value['basic'] + ['ventilation_cap', 'sewage_hpipe', 'waste_hpipe'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        303046: {
            'name': '下列构筑物和设备的排水管与生活排水管道系统应采取间接排水的方式：蒸发式冷却器、空调设备冷凝水的排水；',
            'entity': LayerConfig.BASIC_LAYERS.value['basic'] + ['condensate_hpipe', 'well', 'elevation_symbol'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        305008: {
            'name': '水泵接合器距室外消火栓的距离不宜小于 15m ，并不宜大于 40m',
            'entity': LayerConfig.BASIC_LAYERS.value['basic'] +
                      ['building'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["室外消火栓-总图"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["消火栓"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["水泵接合器"],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        303037: {
            'name': '室外生活排水管道下列位置应设置检查井',
            'entity': LayerConfig.BASIC_LAYERS.value['basic'] +
                      ['building', 'well'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['排水横管'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        305010: {
            'name': '消防电梯前室应设置室内消火栓',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      ["fire_hydrant", "elevator_box", "door", "window", ],
            'operation': ["combination", "segmentation", "classification"],
        },
        305012: {
            'name': '建筑室内消火栓的设置位置应满足火灾扑救要求。',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      ["fire_hydrant", "elevator_stair", "door", "window", "parking"],
            'operation': ["combination", "segmentation", "classification"],
        },
        305014: {
            'name': '消防给水系统管道的最高点处宜设置自动排气阀。',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["排气阀"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["消火栓横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["喷淋横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["废水横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["排气阀门"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['消火栓-给排水'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['雨水井'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['减压阀'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["套管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['检查口'],
            'operation': ["combination", "segmentation", "classification"],
        },
        305018: {
            'name': '设有室内消火栓的建筑应设置带有压力表的试验消火栓，其设置位置应符合规定',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['消火栓横管'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['消火栓'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['消火栓-给排水'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['压力表'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['标高构件'] +
                      ["annotation_line"],
            'operation': ["combination", "segmentation", "classification"]
        },
        305022: {
            'name': '消防给水系统试验装置处应设置专用排水设施，排水管径应符合下列规定:报警阀处的排水立管宜为 DN100 ；减压阀处的压力试验排水管道直径应根据减压阀流量确定，但不应小于 DN100',
            'entity': LayerConfig.BASIC_LAYERS.value['underground_segment'] +
                      ["floor_drain", "valve", "hydrant_hpipe",
                       "sprinkler_hpipe", "window", "door"],
            'operation': ["combination", "segmentation", "classification"]
        },
        306003: {
            'name': '配水管两侧每根配水支管控制的标准流量洒水喷头数量，轻危险级、中危险级场所不应超过8只',
            'entity': LayerConfig.BASIC_LAYERS.value['underground_segment'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["喷头"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["喷淋横管"] +
                      ['window', 'door'],
            'operation': ["combination", "segmentation", "classification"],
        },
        306002: {
            'name': '当水流指示器入口前设置控制阀时，应采用信号阀。',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["喷淋横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["水流指示器"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["信号阀"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["喷头"],
            'operation': ['combination', 'classification'],
        },
        # 307001: {
        #     'name': '当采用生活饮用水补水时，应采取防止生活饮用水被污染的措施，并符合下列规定：清水池(箱)内的自来水补水管出水口应高于清水池(箱)内溢流水位，其间距不得小于2．5倍补水管管径，且不应小于150mm；',
        #     'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + \
        #               LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["给水横管"] + \
        #               ["annotation_line"],
        #     'operation': ['combination', 'segmentation', 'classification']
        # },
        307002: {
            'name': '生活饮用水水池（箱）应设置消毒装置',
            'entity': [],
            'operation': []
        },
        307004: {
            'name': '屋面雨水收集系统应独立设置',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      ["annotation_line", 'window', 'door'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'],
            'operation': ["combination", "segmentation", "classification"]
        },
        307006: {
            'name': '供水管道和补水管道上应设水表计量装置',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["水表"],
            'operation': ['combination', 'classification']
        },
        312001: {
            'name': '地下室或地下构筑物外墙有管道穿过的，应采取防水措施。对有严格防水要求的建筑物，必须采用柔性防水套管',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["排水横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["给水横管"] +
                      # 'window', 'door',LayerConfig.BASIC_LAYERS.value['underground_segment'] +
                      ["sleeve", "wall_hatch", "kitchen_exhaust_pipe"],
            'operation': ["combination", "classification"],
        },
        # 313001: {
        #     'name': '',
        #     'entity': [],
        #     'operation': [],
        # },
        # 313002: {
        #     'name': '',
        #     'entity': [],
        #     'operation': [],
        # },
        302002: {
            'name': '厨房和卫生间的排水立管应分别设置。排水管道不得穿越卧室。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['排水横管'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'] +
                      ["door", "annotation_line", 'window'],
            'operation': ['combination', 'segmentation', 'classification']
        },
        303011: {
            'name': '小区生活排水管道平面布置应符合下列规定：管道中心线据建筑物外墙的距离不宜小于3m',
            'entity': ['wall', 'well', 'building'],
            'operation': ["combination", "segmentation", "classification"],
        },
        303019: {
            'name': '冷水管、热水管平行时，热水管在上；卫生器具同时连接冷水管和热水管时，冷水管在右侧。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["生活给水横管"] +
                      ["door", "window"],
            'operation': ["combination", "segmentation", "classification"],
        },
        303022: {
            'name': '淋浴室内地漏的排水负荷，可按表4．3．9确定',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["排水横管"] + ['door', 'window'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        308004: {
            'name': '灭火器应设置在位置明显和便于取用的地点，且不得影响安全疏散',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["灭火器"] +
                      ["door", "window"],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        301005: {
            'name': '住宅的水表、电能表、热量表和燃气表的设置应便于管理',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ['window', 'door'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["水表"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["套管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["减压阀"],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        301010: {
            'name': '生活给水系统应充分利用城镇给水管网的水压直接供水。',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["给水横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["标高构件"],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        303024: {
            'name': '大便器排水管最小管径不得小于100mm',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["所有立管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["地漏"],
            'operation': ["text_information"],
        },
        303027: {
            'name': '单根排水立管的排出管宜与排水立管相同管径',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["污水横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["废水横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["标高构件"],
            'operation': ['combination', 'classification', 'text_information'],
        },
        306001: {
            'name': '每个防火分区、每个楼层均应设水流指示器。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ['window', 'door', 'fire_compartment_sketch_contour'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["水流指示器"],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        306006: {
            'name': '每个报警阀组控制的最不利点洒水喷头处应设末端试水装置，其他防火分区、楼层均应设直径为25mm的试水阀',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ['window', 'door', 'fire_compartment_sketch_contour'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["末端试水装置-平面"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["截止阀"],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        302004: {
            'name': '套内用水点供水压力不宜大于0．20MPa，且不应小于用水器具要求的最低压力',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["生活给水横管"] +
                      ['valve', 'window', 'door'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        308009: {
            'name': '灭火器设置点的位置和数量应根据灭火器的最大保护距离确定，并应保证最不利点至少在1具灭火器的保护范围内。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ['window', 'door', 'annotation_line', 'fire_hydrant',
                       'fire_compartment_sketch_contour'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        305013: {
            'name': '请校核室内消火栓的布置间距',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ['window', 'door', 'fire_hydrant', 'fire_compartment_sketch_contour'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        305021: {
            'name': '室内消火栓栓口压力和消防水枪充实水柱，应符合下列规定: 消火栓栓口动压力不应大于 0.50MPa ；当大于 0.70MPa 时必须设置减压装置',
            'entity': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["消火栓横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["消火栓-给排水"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["标高构件"],
            'operation': ['combination', 'classification', 'text_information'],
        },
        303045: {
            'name': '当排水立管底部或排出管上的清扫口至室外检查井中心的最大长度大于表4．6．3-1的规定时，应在排出管上设清扫口；',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      ['window', 'door'] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["污水横管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["地漏"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["清扫口"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["套管"] +
                      LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["废水横管"],
            'operation': ['combination', 'segmentation', 'classification'],
        },

    }
