# -*- coding: utf-8 -*-

from enum import Enum

# from rule_engine.multi_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig
from ..multiple_border_pipeline_config import MultiBorderPipelineType


class MultiBorderRuleConfig(Enum):
    CONFIGURATION = {
        "1302006": {
            'name': '建筑高度小于或等于 54m 且每单元设置一部疏散楼梯的住宅，采用1支消防水枪的1股充实水柱到达室内任何部位，不必采用2股水柱',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {

                (DrawingType.TOWER_WATER_SUPPLY,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window", "fire_hydrant",
                                                                                    "elevator_stair"],
                    'operations': ['combination', 'segmentation', 'classification'],
                },

                (DrawingType.TOWER_SECOND_FLOOR_SUPPLY,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window", "fire_hydrant",
                                                                                    "elevator_stair"],
                    'operations': ['combination', 'segmentation', 'classification'],
                }
            },
        },

        "1300002": {
            'name': '管道井、水泵房、风机房应采取有效的隔声措施，水泵、风机应采取减振措施',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                },
                (DrawingType.PUMP_DAYANG,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            }
        },
        "1302001": {
            'name': '灭火器选型，住宅：按A类轻危，选用MF/ABC2，最大保护距离25米。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1302002": {
            'name': '灭火器选型，机房、配电间：按E类中危，选用MF/ABC4，最大保护距离12米。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1302003": {
            'name': '除当地有特殊规定外，灭火器选型，地下汽车库：按B类中危，选用MF/ABC4，最大保护距离12米。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1302004": {
            'name': '除当地有特殊规定外，灭火器选型，非机动车库；按A类中危，选用MF/ABC3，最大保护距离20米。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1302007": {
            'name': '寒冷地区，屋顶试验消火栓设置在室内，避免设置保温措施。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                },
                (DrawingType.WUDING_WATER_SUPPLY,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window", "fire_hydrant",
                                                                                    "elevator_stair"],
                    'operations': ['combination', 'segmentation', 'classification'],
                },
                (DrawingType.WUMIAN_WATER_SUPPLY,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window", "fire_hydrant",
                                                                                    "elevator_stair"],
                    'operations': ['combination', 'segmentation', 'classification'],
                },

            },
        },

        # 品览规则
        "1300006": {
            'name': '给水管道穿越下列部位或接管时，应设置防水套管:1 穿越地下室或地下构筑物的外墙处；2 穿越屋面处；3 穿越钢筋混凝土水池（箱）的壁板或底板连接管道时',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1300010": {
            'name': '建筑屋面雨水排水工程应设置溢流孔口或溢流管系等溢流设施',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.WUMIAN_WATER_DRAIN, DrawingType.WUDING_WATER_DRAIN,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'] + ['overflow_hole'],
                    'operations': ['combination', 'classification'],
                }
            },
        },
        "1300012": {
            'name': '消防水泵控制柜在平时应使消防水泵处于自动启泵状态',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1300013": {
            'name': '消防水泵不应设置自动停泵的控制功能，停泵应由具有管理权限的工作人员根据火灾扑救情况确定',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1300015": {
            'name': '消防控制柜或控制盘应设置专用线路连接的手动直接启泵按钮',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1300016": {
            'name': '消防水泵控制柜设置在专用消防水泵控制室时，其防护等级不应低于IP30；与消防水泵设置在同一空间时，其防护等级不应低于IP55',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1300017": {
            'name': '消防水泵控制柜应设置机械应急启泵功能，并应保证在控制柜内的控制线路发生故障时由有管理权限的人员在紧急时启动消防水泵。机械应急启动时，应确保消防水泵在报警后 5.0min内正常工作。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        '1300022': {
            'name': '排水系统检查井应安装防坠落装置。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.OUTDOOR_GEIPAISHUI_DESIGN, DrawingType.WATER_SUPPLY_SITE_PLAN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                },
                # (DrawingType.WATER_SUPPLY_SITE_PLAN,): {
                #     'major_drawing': True,
                #     'entities': LayerConfig.BASIC_LAYERS.value['building_segment'] +
                #                 LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['水泵接合器'],
                #     'operations': ['combination', 'classification'],
                # }

            }
        },
        "1300025": {
            'name': '防护区应设置泄压口，七氟丙烷灭火系统的泄压口应位于防护区净高的2/3以上。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GAS_EXTINGUISH,): {
                    'major_drawing': True,
                    'entities': ["relief_valve", "relief_valve_and_hpipe"],
                    'operations': ['combination', 'classification'],
                }
            },
        },
        "1300036": {
            'name': '明设的给水立管穿越楼板时，应采取防水措施',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1300049": {
            'name': '从生活饮用水管网向下列水池（箱）补水时应符合下列规定：1 向消防等其他非供生活饮用的贮水池（箱）补水时，其进水管口最低点高出溢流边缘的空气间隙不应小于150mm； 2 向中水、雨水回用水等回用水系统的贮水池（箱）补水时，其进水管口最低点高出溢流边缘的空气间隙不应小于进水管管径的2．5倍，且不应小于150mm。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.PUMP_DAYANG,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["给水横管"] +
                                ["annotation_line", 'door', 'window'],
                    'operations': ['combination', 'segmentation', 'classification'],
                }
            },
        },
        "1300005": {
            'name': '无存水弯的卫生器具和无水封的地漏与生活排水管道连接时，在排水口以下应设存水弯；存水弯和有水封地漏的水封高度不应小于50mm',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1302008": {
            'name': '水井中应设置废水立管，每层设置1个DN50排水地漏。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.TOWER_WATER_SUPPLY, DrawingType.TOWER_WATER_DRAIN): {
                    'major_drawing': True,
                    # 'entities': ["waste_vpipe", "floor_drain", "annotation_line"],
                    'operations': ['classification', 'combination', 'segmentation'],

                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                ["waste_vpipe", "floor_drain", 'annotation_line', 'door', 'window'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'],
                },
                (DrawingType.INDOOR_WATER_DRAIN_SYSTEM, ): {
                    'major_drawing': True,
                    'entities': ["waste_hpipe", "system_floor_drain", "annotation_line"],
                    'operations': ['classification', 'combination'],
                }
            },
        },
        "1302016": {
            'name': '排水通气管的出口，设置在上人屋面时，应高出屋面或平台地面2．00m',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.INDOOR_WATER_DRAIN_SYSTEM,): {
                    'major_drawing': True,
                    'entities': ['ventilation_cap', 'sewage_hpipe', 'waste_hpipe'],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
                (DrawingType.WUMIAN_WATER_DRAIN, DrawingType.WUDING_WATER_DRAIN): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'elevator_stair', 'window'],
                    'operations': ['combination', 'classification', 'segmentation'],
                }
            },
        },
        301001: {
            'name': '水穿过楼板和墙体时，孔洞周边应采取密封隔声措施。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        301002: {
            'name': '水泵房应采取有效的隔声措施，水泵应采取减振措施。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                },
                (DrawingType.PUMP_DAYANG,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': [],
                }
            },
        },
        301003: {
            'name': '住宅应设室内给水排水系统',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.TOWER_WATER_SUPPLY,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                },
                (DrawingType.TOWER_WATER_DRAIN, ): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        301006: {
            'name': '室内采用临时高压消防给水系统时，高位消防水箱的高层民用建筑、总建筑面积大于 10000m2 且层数超过 2 层的公共建筑和其他重要建筑，必须设置高位消防水箱',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        301008: {
            'name': '',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        301009: {
            'name': '地下室、半地下室中卫生器具和地漏的排水管，不应与上部排水管连接。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR_WATER_DRAIN_SYSTEM,): {
                    'major_drawing': True,
                    'entities': ["sewage_hpipe", "waste_hpipe", 'annotation_line'],
                    'operations': ['classification', 'combination', 'segmentation'],
                },
                (DrawingType.UNDERGROUND_WATER_DRAIN,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                ["floor_drain", 'annotation_line', 'door', 'window'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'],
                    'operations': ['classification', 'combination', 'segmentation'],
                }
            },
        },
        302003: {
            'name': '地下室、半地下室中卫生器具和地漏的排水管，不应与上部排水管连接。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR_WATER_DRAIN_SYSTEM,): {
                    'major_drawing': True,
                    'entities': ["sewage_hpipe", "waste_hpipe", 'annotation_line', ],
                    'operations': ['classification', 'combination', 'segmentation'],
                },
                (DrawingType.UNDERGROUND_WATER_DRAIN,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                ["floor_drain", 'annotation_line', 'window', 'door'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'],
                    'operations': ['classification', 'combination', 'segmentation'],
                },
                (DrawingType.UNDERGROUND_WATER_DRAIN_SYSTEM,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': [],
                },
            },
        },
        302005: {
            'name': '无存水弯的卫生器具和无水封的地漏与生活排水管道连接时，在排水口以下应设存水弯；存水弯和有水封地漏的水封高度不应小于50mm',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        302006: {
            'name': '卫生器具和配件应采用节水型产品。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            }
        },
        302008: {
            'name': '排水通气管的出口，设置在上人屋面时，应高出屋面或平台地面2．00m',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.INDOOR_WATER_DRAIN_SYSTEM,): {
                    'major_drawing': True,
                    'entities': ['ventilation_cap', 'sewage_hpipe', 'waste_hpipe'],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
                (DrawingType.WUMIAN_WATER_DRAIN, DrawingType.WUDING_WATER_DRAIN): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'elevator_stair', 'window'],
                    'operations': ['combination', 'classification', 'segmentation'],
                }
            },
        },
        303001: {
            'name': '从生活饮用水管网向下列水池（箱）补水时应符合下列规定：1 向消防等其他非供生活饮用的贮水池（箱）补水时，其进水管口最低点高出溢流边缘的空气间隙不应小于150mm； 2 向中水、雨水回用水等回用水系统的贮水池（箱）补水时，其进水管口最低点高出溢流边缘的空气间隙不应小于进水管管径的2．5倍，且不应小于150mm。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.PUMP_DAYANG,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["给水横管"] +
                                ["annotation_line", 'door', 'window'],
                    'operations': ['combination', 'segmentation', 'classification'],
                }
            },
        },
        303002: {
            'name': '生活饮用水水池（箱）应设置消毒装置。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.PUMP_DAYANG,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': [],
                }
            },
        },
        303014: {
            'name': '生活饮用水系统的水质，应符合现行国家标准《生活饮用水卫生标准》GB 5749的规定',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        303015: {
            'name': '室内的给水管道，应选用耐腐蚀和安装连接方便可靠的管材，可采用不锈钢管、铜管、塑料给水管和金属塑料复合管及经防腐处理的钢管。高层建筑给水立管不宜采用塑料管',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        303016: {
            'name': '给水管道不宜穿越变形缝。当必须穿越时，应设置补偿管道伸缩和剪切变形的装置。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        303017: {
            'name': '给水管道穿越下列部位或接管时，应设置防水套管',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        303018: {
            'name': '明设的给水立管穿越楼板时，应采取防水措施',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        303023: {
            'name': '',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        303028: {
            'name': '屋面排水系统应设置雨水斗。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.WUMIAN_WATER_DRAIN, DrawingType.WUDING_WATER_DRAIN): {
                    'major_drawing': True,
                    'entities': ['rain_outlet'],
                    'operations': ['combination', 'classification'],
                }
            },
        },
        303031: {
            'name': '',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.TOWER_WATER_DRAIN,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['洗衣机'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['地漏'] +
                                ['door', 'window'],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
                (DrawingType.WUDING_WATER_DRAIN,): {
                    'major_drawing': True,
                    'entities': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['雨水斗'],
                    'operations': ['combination', 'classification'],
                },
            },
        },
        303033: {
            'name': '水封装置的水封深度不得小于50mm，严禁采用活动机械活瓣替代水封，严禁采用钟式结构地漏',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        303034: {
            'name': '',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        303036: {
            'name': '',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        303038: {
            'name': '卫生器具排水管段上不得重复设置水封',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        303039: {
            'name': '',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        303040: {
            'name': '室内排水管道布置应符合规定',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.UNDERGROUND_WATER_DRAIN, DrawingType.TOWER_WATER_DRAIN, DrawingType.WUMIAN_WATER_DRAIN,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["排水横管"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["通气横管"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["所有立管"] +
                                ["door", "window"],
                    'operations': ["combination", "segmentation", "classification"],
                }
            },
        },
        304001: {
            'name': '座便器一次性冲洗水量应小于6L',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        305001: {
            'name': '下列场所的室内消火栓给水系统应设置消防水泵接合器',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR_WATER_SUPPLY_SYSTEM,  DrawingType.INDOOR_WATER_DRAIN_SYSTEM, ): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["给水横管"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["水泵接合器"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["进水横管"],
                    'operations': ["combination", "classification"],
                },
                (DrawingType.UNDERGROUND_FIRE_HYDRANT_SYSTEM,
                 DrawingType.UNDERGROUND_WATER_SUPPLY_SYSTEM, ): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["给水横管"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["水泵接合器"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["进水横管"],
                    'operations': ["combination", "classification"],
                },
                (DrawingType.WATER_SUPPLY_SITE_PLAN, ): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["给水横管"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["水泵接合器"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["进水横管"],
                    'operations': ["combination", "classification"],
                },
            },
        },
        305002: {
            'name': '自动喷水灭火系统,应设置消防水泵接合器',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.WATER_SUPPLY_SITE_PLAN, ): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["喷淋横管"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["水泵接合器"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["废水横管"],
                    'operations': ["combination", "classification"],
                },
                (DrawingType.UNDERGROUND_SPRINKLER_SYSTEM, DrawingType.UNDERGROUND_WATER_SUPPLY_SYSTEM, ): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["喷淋横管"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["水泵接合器"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["废水横管"],
                    'operations': ["combination", "classification"],
                },
                (DrawingType.INDOOR_WATER_SUPPLY_SYSTEM,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["喷淋横管"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["水泵接合器"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["废水横管"],
                    'operations': ["combination", "classification"],
                },
            },
        },
        305003: {
            'name': '附设在建筑物内的消防水泵房，不应设置在地下三层及以下，或室内地面与室外出入口地坪高差大于10m的地下楼层。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.UNDERGROUND_WATER_SUPPLY, ): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                ['window', 'door'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["标高构件"],
                    'operations': ['combination', 'segmentation', 'classification']
                }
            }
        },
        305004: {
            'name': '室内采用临时高压消防给水系统时，高位消防水箱的高层民用建筑、总建筑面积大于 10000m2 且层数超过 2 层的公共建筑和其他重要建筑，必须设置高位消防水箱',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        305005: {
            'name': '设置室内消火栓的建筑，包括设备层在内的各层均应设置消火栓。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.TOWER_WATER_SUPPLY, DrawingType.UNDERGROUND_WATER_SUPPLY): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['消火栓'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['消火栓-给排水'] +
                                ['door', 'window', 'elevator_box', 'elevator_stair'],
                    'operations': ['combination', 'segmentation', 'classification'],
                }
            },
        },
        305006: {
            'name': '消防水泵控制柜在平时应使消防水泵处于自动启泵状态',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        305007: {
            'name': '消防水泵不应设置自动停泵的控制功能，停泵应由具有管理权限的工作人员根据火灾扑救情况确定',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        305009: {
            'name': '消防水泵应能手动启停和自动启动',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        305016: {
            'name': '消防控制柜或控制盘应设置专用线路连接的手动直接启泵按钮',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        305019: {
            'name': '消防水泵控制柜设置在专用消防水泵控制室时，其防护等级不应低于IP30；与消防水泵设置在同一空间时，其防护等级不应低于IP55',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        305020: {
            'name': '消防水泵控制柜应设置机械应急启泵功能，并应保证在控制柜内的控制线路发生故障时由有管理权限的人员在紧急时启动消防水泵。机械应急启动时，应确保消防水泵在报警后 5.0min内正常工作。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        305010: {
            'name': '',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        # 305014: {
        #     'name': '',
        #     'type': MultiBorderPipelineType.TYPE_C,
        #     'borders': {
        #         (DrawingType.GEIPAISHUI_DESIGN,): {
        #             'major_drawing': True,
        #             'entities': [],
        #             'operations': [],
        #         }
        #     },
        # },
        305015: {
            'name': '当高位消防水箱在屋顶露天设置时，水箱的人孔以及进出水管的阀门等应采取锁具或阀门箱等保护措施',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        305017: {
            'name': '',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        307001: {
            'name': '当采用生活饮用水补水时，应采取防止生活饮用水被污染的措施，并符合下列规定：清水池(箱)内的自来水补水管出水口应高于清水池(箱)内溢流水位，其间距不得小于2．5倍补水管管径，且不应小于150mm；',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.RAINWATER_RECLAIM_DAYANG,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["给水横管"] +
                                ["annotation_line", 'window', 'door'],
                    'operations': ['combination', 'segmentation', 'classification'],
                }
            },
        },
        308001: {
            'name': 'A类火灾场所应选择水型灭火器、磷酸铵盐干粉灭火器、泡沫灭火器或卤代烷灭火器。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        308002: {
            'name': 'B类火灾场所应选择泡沫灭火器、碳酸氢钠干粉灭火器、磷酸铵盐干粉灭火器、二氧化碳灭火器、灭B类火灾的水型灭火器或卤代烷灭火器。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        308003: {
            'name': 'E类火灾场所应选择磷酸铵盐干粉灭火器、碳酸氢钠干粉灭火器、卤代烷灭火器或二氧化碳灭火器，但不得选用装有金属喇叭喷筒的二氧化碳灭火器。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        # 308004: {
        #     'name': '灭火器应设置在位置明显和便于取用的地点，且不得影响安全疏散',
        #     'type': MultiBorderPipelineType.TYPE_A,
        #     'borders': {
        #         (DrawingType.TOWER_WATER_SUPPLY,): {
        #             'major_drawing': True,
        #             'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
        #                         LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["灭火器"] + ["door", "window"],
        #             'operations': ['combination', 'segmentation', 'classification']
        #         },
        #         (DrawingType.UNDERGROUND_WATER_SUPPLY,): {
        #             'major_drawing': True,
        #             'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
        #                         LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["灭火器"] + ["door", "window"],
        #             'operations': ['combination', 'segmentation', 'classification']
        #         },
        #     },
        # },
        308005: {
            'name': '设置在A类火灾场所的灭火器，其最大保护距离应符合表5．2．1的规定。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        308006: {
            'name': '设置在B、C类火灾场所的灭火器，其最大保护距离应符合表5．2．2的规定。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        308007: {
            'name': 'A类火灾场所灭火器的最低配置基准应符合表6.2.1的规定。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        308008: {
            'name': 'B、C类火灾场所灭火器的最低配置基准应符合表6．2．2的规定。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        308010: {
            'name': 'C类火灾场所应选择磷酸铵盐干粉灭火器、碳酸氢钠干粉灭火器、二氧化碳灭火器或卤代烷灭火器。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        308011: {
            'name': '',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        309001: {
            'name': '位于车行道的检查井，应采用具有足够承载力和稳定性良好的井盖与井座',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.OUTDOOR_GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                },
                (DrawingType.WATER_SUPPLY_SITE_PLAN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        309002: {
            'name': '排水系统检查井应安装防坠落装置。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.OUTDOOR_GEIPAISHUI_DESIGN, DrawingType.WATER_SUPPLY_SITE_PLAN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                },
                # (DrawingType.WATER_SUPPLY_SITE_PLAN,): {
                #     'major_drawing': True,
                #     'entities': LayerConfig.BASIC_LAYERS.value['building_segment'] +
                #                 LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['水泵接合器'],
                #     'operations': ['combination', 'classification'],
                # }
            },
        },
        310001: {
            'name': '高层住宅建筑的公共部位和公共建筑内应设置灭火器',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.INDOOR_WATER_SUPPLY_SYSTEM,): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.TOWER_WATER_SUPPLY,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["灭火器"] +
                                ['door', 'window'],
                    'operations': ['combination', 'classification', 'segmentation'],
                }
            },
        },
        310002: {
            'name': '自动喷水灭火系统以及下列建筑的室内消火栓给水系统应设置消防水泵接合器。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.UNDERGROUND_WATER_SUPPLY_SYSTEM, ): {
                    'major_drawing': True,
                    'entities': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['水泵接合器'],
                    'operations': ['combination', 'classification'],
                },
                (DrawingType.WATER_SUPPLY_SITE_PLAN,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['building_segment'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['水泵接合器'],
                    'operations': ['combination', 'classification'],
                },
                (DrawingType.INDOOR_WATER_SUPPLY_SYSTEM, ): {
                    'major_drawing': True,
                    'entities': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['水泵接合器'],
                    'operations': ['combination', 'classification'],
                },
                (DrawingType.UNDERGROUND_SPRINKLER_SYSTEM,): {
                    'major_drawing': True,
                    'entities': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['水泵接合器'],
                    'operations': ['combination', 'classification'],
                },
                (DrawingType.UNDERGROUND_FIRE_HYDRANT_SYSTEM,): {
                    'major_drawing': True,
                    'entities': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['水泵接合器'],
                    'operations': ['combination', 'classification'],
                },
            },
        },
        310003: {
            'name': '除本规范另有规定和不宜用水保护或灭火的场所外，下列高层民用建筑或场所应设置自动灭火系统，并宜采用自动喷水灭火系统：4 建筑高度大于l00m 的住宅建筑。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR_WATER_SUPPLY_SYSTEM, ): {
                    'major_drawing': True,
                    'entities': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["喷淋横管"]
                                + LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["喷头"]
                                + LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': ['combination', 'classification'],
                },
            },
        },
        310004: {
            'name': '消防水泵房和消防控制室应采取防水淹的技术措施',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        311001: {
            'name': '',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        311002: {
            'name': '除本规范另有规定外，汽车库应设置室内消火栓系统，其消防用水量应符合下列规定：1 Ⅰ、Ⅱ、Ⅲ类汽车库的用水量不应小于10L／s。2 Ⅳ类汽车库的用水量不应小于5L／s。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        311003: {
            'name': '除敞开式汽车库、屋面停车场外，下列汽车库、修车库应设置自动灭火系统',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        313001: {
            'name': '抗震设防烈度为6度及6度以上地区的建筑机电工程必须进行抗震设计。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        313002: {
            'name': '管道的布置与敷设应符合下列规定：管道穿过内墙或楼板时，应设置套管；套管与管道间的缝隙，应采用柔性防火材料封堵；',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        314001: {
            'name': '防护区应设置泄压口，七氟丙烷灭火系统的泄压口应位于防护区净高的2/3以上。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GAS_EXTINGUISH,): {
                    'major_drawing': True,
                    'entities': ["relief_valve", "relief_valve_and_hpipe"],
                    'operations': ['combination', 'classification'],
                }
            },
        },
        303010: {
            'name': '高出屋面的通气管设置应符合下列规定。',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.INDOOR_WATER_DRAIN_SYSTEM,): {
                    'major_drawing': True,
                    'entities': ['ventilation_cap', 'sewage_hpipe', 'waste_hpipe'],
                    'operations': ['combination', 'classification'],
                },
                # 机房排水和屋面排水一致，不需要单独配置
                (DrawingType.WUMIAN_WATER_DRAIN, DrawingType.WUDING_WATER_DRAIN): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                ['door', 'window', 'elevator_stair'],
                    'operations': ['combination', 'classification', 'segmentation'],
                }
            },
        },
        303013: {
            'name': '贮存食品、贵重商品库房、通风小室、电气机房和电梯机房不应布置雨水管道',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.UNDERGROUND_WATER_DRAIN, DrawingType.TOWER_WATER_DRAIN): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["雨水横管"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value["所有立管"] +
                                ['window', 'door'],
                    'operations': ['combination', 'classification', 'segmentation'],
                }
            },
        },
        303026: {
            'name': '多层住宅厨房间的立管管径不宜小于75mm。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR_WATER_DRAIN_SYSTEM,): {
                    'major_drawing': True,
                    'entities': ["annotation_line", "sewage_hpipe", "waste_hpipe"],
                    'operations': ['combination', 'segmentation', 'classification']
                },
                (DrawingType.TOWER_WATER_DRAIN,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                ['door', 'window', 'kitchen_toilet', "annotation_line"],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
                (DrawingType.GEIPAISHUI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        303035: {
            'name': '小区生活排水与雨水排水系统应采用分流制',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.WATER_DRAIN_SITE_PLAN,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['污水横管'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['雨水横管'] +
                                ["annotation_line"] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['所有立管'],
                    'operations': ['combination', 'classification'],
                }
            },
        },
        303044: {
            'name': '建筑屋面雨水排水工程应设置溢流孔口或溢流管系等溢流设施',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.WUMIAN_WATER_DRAIN, DrawingType.WUDING_WATER_DRAIN,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'] + ['overflow_hole'],
                    'operations': ['combination', 'classification'],
                }
            },
        },
        306005: {
            'name': '自动喷水灭火系统应有下列组件、配件和设施',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.UNDERGROUND_SPRINKLER_SYSTEM, DrawingType.UNDERGROUND_WATER_SUPPLY_SYSTEM,): {
                    'major_drawing': True,
                    'entities': LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['喷头系统'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['末端试水装置-平面'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['系统报警阀'] +
                                LayerConfig.GEIPAISHUI_ENTITY_LAYER_MAP.value['喷淋横管'],
                    'operations': ['combination', 'classification', 'text_information'],
                }
            },
        },
    }