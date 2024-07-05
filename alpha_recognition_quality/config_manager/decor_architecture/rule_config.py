from enum import Enum

# from rule_engine.single_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig


class RuleConfig(Enum):
    VANKE_RULES = {

        DrawingType.DECORATION_PLAN_LAYOUT: ["1603017", "1603020", "1603014", "1603012", "1103046", "1603019",
                                             "1603010", "1603013", "1603022", "1603021", "1603018", "1603059",
                                             "1603060", "1603049", "1603052", "1603053", "1603054", "1603055",
                                             "1603056", "1603057", "1603058", "1603061", "1603062", "1603064",
                                             "1603065", "1603066", "1603067", "1603079", "1603080", "1603081",
                                             "1603082", "1603042", "1603023", "1603027", "1603030", "1603033",
                                             "1603034", "1603039", "1603040", "1603041", "1603042", "1603043",
                                             "1603044", "1603045", "1603046", "1603047", "1603048", "1603088",
                                             "1603090", "1603092", "1603069", "1603070", "1603071", "1603072",
                                             "1603038", "1603037", "1603036", "1603094", "1603004", "1603006",
                                             "1603025", "1603024", "1603031", "1603026", "1603032", "1603028",
                                             "1603074", "1603075", "1603076", "1603077",
                                             ],
        DrawingType.DECORATION_PLASTER_DETAIL: ["1603017", "1603020"],
        DrawingType.DECORATION_SANITARY_SCHEDULE: ["1603017", "1603020", "1603018", "1603059", "1603060",
                                                   "1603061", "1603047", "1603048", "1603062", "1603064", "1603065",
                                                   "1603066", "1603067"],
        DrawingType.DECORATION_MATERIAL_SCHEDULE: ["1603019", "1603021", "1603043", "1603052", "1603053", "1603023",
                                                   "1603054", "1603055", "1603049", "1603027", "1603030", "1603033",
                                                   "1603034", "1603042", "1603044", "1603045", "1603046", "1603047",
                                                   "1603048", "1603044", "1603045", "1603046", "1603037", "1603038",
                                                   "1603088", "1603090", "1603092"],

        DrawingType.DECORATION_EQUIPMENT_SCHEDULE: ["1603014", "1603069", '1603070', '1603071', '1603072'],
        DrawingType.DECORATION_LIGHTING_SCHEDULE: ["1603079", "1603080",
                                                   "1603081", "1603082"],
        DrawingType.DECORATION_METAL_SCHEDULE: ["1603056", "1603057", "1603058", "1603039", "1603040", "1603041",
                                                "1603047", "1603048"],
        DrawingType.DECORATION_DOOR_SCHEDULE: ["1603036"],
        DrawingType.DECORATION_GROUND_MATERIAL: ['1603024', '1603025', '1603026', '1603028'],
        DrawingType.DECORATION_CEILING_LAYOUT: ['1603031', '1603032'],
        DrawingType.DECORATION_KITCHEN_ELEVATION: ['1603026'],
        DrawingType.DECORATION_BATHROOM_ELEVATION: ['1603026'],
    }

    INDOOR_FIRST_FLOOR_NO_SPACE_RULE = []

    SPECIAL_CHEKCPOINT_ID_DICT = {

    }

    # 规则详情
    # REF: https://www.kdocs.cn/p/51356796370?from=docs&source=docsWeb
    CONFIGURATION = {
        "1103046": {
            "name": "平开窗执手安装高度，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603010": {
            "name": "货量和板房是否在乳胶漆品牌、型号等存在货板不一致",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603012": {
            "name": "货量和板房是否在净水装置品牌、型号等存在货板不一致",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603013": {
            "name": "热水器、壁挂炉的的平面位置，板房与货量是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603014": {
            "name": "货量和板房是否在净水装置品牌、型号等存在货板不一致",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603017": {
            "name": "石膏线尺寸、规格、型号，板房与货量是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", "chu_wei",
                                                                          "plaster_line"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603018": {
            "name": "货量和板房是否在乳胶漆品牌、型号等存在货板不一致",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603019": {
            "name": "货量和板房是否在乳胶漆品牌、型号等存在货板不一致",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603020": {
            "name": "防水面板品牌、型号、位置，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", "chu_wei", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603021": {
            "name": "不锈钢品牌、型号、规格，板房与货量是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },

        "1603023": {
            "name": "地面铺贴材料，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603027": {
            "name": "窗台、凸窗台材料，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603030": {
            "name": "天花材料，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603033": {
            "name": "墙体的材料，板房与货量是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603034": {
            "name": "墙体的型号，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603039": {
            "name": "门锁、门拉手、铰链、插销、门镜、门合页、吊轨、门吸、地弹簧等五金的品牌，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603040": {
            "name": "门锁、门拉手、铰链、插销、门镜、门合页、穿线盒、吊轨、门吸、地弹簧等五金的材料型号，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603041": {
            "name": "门锁、门拉手、铰链、插销、门镜、门合页、穿线盒、吊轨、门吸、地弹簧等五金的规格尺寸，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603042": {
            "name": "卫生间及厨房（西厨）不锈钢收口条，板房货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603043": {
            "name": "踢脚线的材料，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603044": {
            "name": "踢脚线的颜色，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603045": {
            "name": "踢脚线的尺寸，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603046": {
            "name": "踢脚线的型号，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603047": {
            "name": "鞋柜、浴室柜、镜柜、橱柜、衣柜、洗衣柜的品牌，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603048": {
            "name": "鞋柜、浴室柜、镜柜、橱柜、衣柜、洗衣柜的材料型号，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603049": {
            "name": "鞋柜、浴室柜、镜柜、橱柜、衣柜、洗衣柜的饰面材料，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603052": {
            "name": "橱柜台面的材质，板房与货量是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603053": {
            "name": "橱柜台面的型号，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603054": {
            "name": "橱柜台面的规格，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603055": {
            "name": "橱柜台面的品牌，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603056": {
            "name": "路轨、铰链等五金的品牌，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603057": {
            "name": "路轨、铰链等五金的材料型号，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603058": {
            "name": "路轨、铰链等五金的规格尺寸，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603059": {
            "name": "浴缸、马桶、智能马桶、蹲便器、洗脸盆、花洒、龙头、厨房水盆等的品牌，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603060": {
            "name": "浴缸、马桶、智能马桶、蹲便器、洗脸盆、花洒、龙头、厨房水盆等的材料型号，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603061": {
            "name": "浴缸、马桶、智能马桶、蹲便器、洗脸盆、花洒、龙头、厨房水盆等的规格尺寸，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603062": {
            "name": "浴缸、马桶、智能马桶、蹲便器、花洒、龙头、厨房水盆等的平面位置，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603064": {
            "name": "马桶刷支架、毛巾架、纸巾架、置物架、地漏、马桶清洁喷头、阳台晾衣架、淋浴屏的品牌，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603065": {
            "name": "马桶刷支架、毛巾架、纸巾架、地漏、马桶清洁喷头、阳台晾衣架、淋浴屏的材料型号，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603066": {
            "name": "马桶刷支架、毛巾架、纸巾架、置物架、地漏、马桶清洁喷头、阳台晾衣架、淋浴屏的规格尺寸，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603067": {
            "name": "马桶刷支架、毛巾架、纸巾架、置物架、地漏、马桶清洁喷头、阳台晾衣架、淋浴屏的平面位置，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", "annotation_line"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603069": {
            "name": "抽油烟机，燃气灶、拉篮、空调、蒸烤机、消毒柜、洗碗机、衣柜鞋柜除湿消毒器等的品牌，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603070": {
            "name": "抽油烟机，燃气灶、拉篮、冰箱、空调、洗衣机、蒸烤机、消毒柜、洗碗机、衣柜鞋柜除湿消毒器等的材料型号，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603071": {
            "name": "抽油烟机，燃气灶、拉篮、冰箱、空调、洗衣机、蒸烤机、消毒柜、洗碗机、衣柜鞋柜除湿消毒器等的规格尺寸，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603072": {
            "name": "抽油烟机，燃气灶、拉篮、冰箱、空调、洗衣机、蒸烤机、消毒柜、洗碗机等的平面位置，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603024": {
            "name": "地面铺贴尺寸，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", "annotation",
                                                                          "annotation_line"],
            "operation": ["text_information"],
        },
        "1603025": {
            "name": "地砖填缝材质与颜色，板房、货量及交付标准是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["text_information"],
        },
        "1603026": {
            "name": "地面起铺点位置及方向，货板是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", "limian", "floor_pavin"],
            "operation": ["combination", "segmentation"],
        },
        "1603028": {
            "name": "窗台、凸窗台尺寸，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603029": {
            "name": "窗台起铺点位置及方向，货板是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", "limian", "floor_pavin"],
            "operation": ["combination", "segmentation"],
        },
        "1603031": {
            "name": "天花吊顶位置，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", "elevation_mark",
                                                                          "annotation_line"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603032": {
            "name": "天花吊顶造型与尺寸，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", "elevation_mark",
                                                                          "annotation_line", "tian_hua"],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603035": {
            "name": "墙体铺贴方式，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603036": {
            "name": "房间门、厨房门、卫生间门等的品牌，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603037": {
            "name": "房间门、厨房门、卫生间门等的材料型号，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603038": {
            "name": "房间门、厨房门、卫生间门等的规格尺寸，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603050": {
            "name": "鞋柜、浴室柜（含洗脸盆）、镜柜、橱柜（中西厨）、衣柜、洗衣柜等的平面位置，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603051": {
            "name": "浴室柜的安装高度，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603063": {
            "name": "浴缸、马桶、智能马桶、蹲便器、洗脸盆、花洒、厨房水盆的数量，板房与货量是否一致",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603068": {
            "name": "毛巾架、纸巾架、重力挂钩的安装高度，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603074": {
            "name": "排气扇、新风、厨房凉霸、浴室浴霸的品牌，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603075": {
            "name": "排气扇、厨房凉霸、浴室浴霸规格尺寸，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603076": {
            "name": "排气扇、厨房凉霸、浴室浴霸、的材料型号，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603077": {
            "name": "排气扇、厨房凉霸、浴室浴霸、净水器等的平面位置，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603084": {
            "name": "鞋柜、浴室柜、镜柜、橱柜的规格尺寸，板房与货量是否一致？橱柜的规格尺寸，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603088": {
            "name": "电梯门套材料、规格，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603089": {
            "name": "电梯门套款式，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603090": {
            "name": "集成铝扣板规格、颜色、品牌，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603091": {
            "name": "电梯按钮的位置，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603092": {
            "name": "门夹砖（石）品牌、材料、型号、规格，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
        "1603093": {
            "name": "感应灯、消防应急灯品牌、型号、功率、光通量、光束角、色温、尺寸、开孔、是否可调角度，板房与货量是否一致？",
            "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe", ],
            "operation": ["combination", "segmentation", "classification"],
        },
    }

# for i in RuleConfig.VANKE_RULES.value.keys():
#     RuleConfig.VANKE_RULES.value[i] = []
