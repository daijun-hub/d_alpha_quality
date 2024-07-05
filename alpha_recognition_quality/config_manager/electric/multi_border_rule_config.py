# -*- coding: utf-8 -*-

from enum import Enum

# from rule_engine.multi_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig
from ..multiple_border_pipeline_config import MultiBorderPipelineType


class MultiBorderRuleConfig(Enum):
    CONFIGURATION = {
        "1502007": {
            'name': '负荷等级是否正确',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.QIANGDIAN_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1502006": {
            'name': '电气用房正上方不应有用水房间。与用水房间或潮湿场所毗邻建议做双墙。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.ZHAOMING_FIRST_FLOOR, DrawingType.ZHAOMING): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
                (DrawingType.ZHAOMING_FIRST_FLOOR, DrawingType.ZHAOMING): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"],
                    'operations': ['combination', 'classification', 'segmentation'],
                },

            },
        },
        "1502010": {
            'name': '电缆型号选型应合理（消防/无联动功能）采用阻zr',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.HUOZAI_AUTO_SYSTEM, DrawingType.XIAOFANG_DESIGN, DrawingType.XIAOFANG,
                 DrawingType.XIAOFANG_FIRST_FLOOR): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1502011": {
            'name': '双电源切换箱应设置在消防水泵房、消防电梯机房、消防风机/末端切换消控室及各防火分区的配电小间内',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["basic"] +
                                LayerConfig.BASIC_LAYERS.value["indoor_segment"],
                    'operations': ['combination', 'segmentation', 'classification', 'text_information'],
                },
                (DrawingType.PEIDIAN_PEIDIANXIANG_SYSTEM,): {
                    'major_drawing': True,
                    'entities': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["系统图双切开关"] + ['wire'],
                    'operations': ["combination", "classification"],
                },
            },
        },
        "1502019": {
            'name': '供电电源描述应清楚',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                },
            },
        },
        "1502022": {
            'name': '电梯是否有自动平层功能',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                },
                (DrawingType.PEIDIAN_PEIDIANXIANG_SYSTEM,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ["combination", "classification"],
                },
            },
        },
        "1502023": {
            'name': '消防配电箱箱体应有标识',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                },
                (DrawingType.PEIDIAN_PEIDIANXIANG_SYSTEM,): {
                    'major_drawing': True,
                    'entities':  LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["系统图双切开关"] + ['wire'],
                    'operations': ["combination", "classification"],
                },
            },
        },
        "1502028": {
            'name': '防雷接地接地测试端子应避开建筑主要出、入口。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["basic"] +
                                LayerConfig.BASIC_LAYERS.value["indoor_segment"],
                    'operations': ['combination', 'segmentation', 'classification', 'text_information'],
                },
                (DrawingType.NON_ROOF_FANGLEI,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["basic"] +
                                LayerConfig.BASIC_LAYERS.value["indoor_segment"],
                    'operations': ['combination', 'segmentation', 'classification', 'text_information'],
                },
            },
        },
        "1503001": {
            'name': '碧桂园电气开关数量比对',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.DIANQI,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"] +
                                LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["平面图开关"],
                    'operations': ['combination', 'classification', 'segmentation', 'text_information'],
                },
                (DrawingType.DIANQI,): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"] +
                                LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["平面图开关"],
                    'operations': ['combination', 'classification', 'segmentation', 'text_information'],
                }
            },
        },
        "1503002": {
            'name': '碧桂园电气插座数量比对',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.DIANQI,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"] +
                                LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["插座"],
                    'operations': ['combination', 'classification', 'segmentation', 'text_information'],
                },
                (DrawingType.DIANQI,): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"] +
                                LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["插座"],
                    'operations': ['combination', 'classification', 'segmentation', 'text_information'],
                }
            },
        },

        "1500037": {
            'name': '高度超过100m的建筑中，除消防控制室内设置的控制器外，每台控制器直接控制的火灾探测器、手动报警按钮和模块等设备不应跨越避难层。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1500042": {
            'name': '火灾自动报警系统应设置火灾声光警报器，并应在确认火灾后启动建筑内的所有火灾声光警报器',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1500047": {
            'name': '消防控制室、消防水泵房、自备发电机房、配电室、防排烟机房以及发生火灾时仍需正常工作的消防设备房应设置备用照明，其作业面的最低照度不应低于正常照明的照度',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.QIANGDIAN_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1500050": {
            'name': '防火卷帘下降至距楼板面1.8m处、下降到楼板面的动作信号和防火卷帘控制器直接连接的感烟、感温火灾探测器的报警信号，应反馈至消防联动控制器。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501010: {
            'name': '每台警报器覆盖的楼层不应超过3层，且首层明显部位应设置用于直接启动火灾声警报器的手动火灾报警按钮',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.XIAOFANG, DrawingType.XIAOFANG_FIRST_FLOOR, DrawingType.XIAOFANG_UNDERGROUND): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + \
                                LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["火灾自动报警按钮"] + \
                                LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["光警报器"],
                    'operations': ['combination', 'segmentation', 'classification'],
                }
            },
        },
        501011: {
            'name': '高度超过100m的建筑中，除消防控制室内设置的控制器外，每台控制器直接控制的火灾探测器、手动报警按钮和模块等设备不应跨越避难层。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501012: {
            'name': '本报警区域内的模块不应控制其他报警区域的设备。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501013: {
            'name': '火灾自动报警系统应设置交流电源和蓄电池备用电源。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501014: {
            'name': '火灾自动报警系统的供电线路、消防联动控制线路应采用耐火铜芯电线电缆，报警总线、消防应急广播和消防专用电话等传输线路应采用阻燃或阻燃耐火电线电缆。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501015: {
            'name': '消火栓泵的动作信号应反馈至消防联动控制器。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501016: {
            'name': '',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501017: {
            'name': '壁挂扬声器的底边距地面高度应大于2.2m。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501018: {
            'name': '',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501019: {
            'name': '消防专用电话网络应为独立的消防通信系统',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501020: {
            'name': '模块严禁设置在配电(控制)柜(箱)内。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501021: {
            'name': '消防控制室应有相应的竣工图纸、各分系统控制逻辑关系说明、设备使用说明书、系统操作规程、应急预案、值班制度、维护保养制度及值班记录等文件资料',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501022: {
            'name': '消防控制室内严禁穿过与消防设施无关的电气线路及管路',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501023: {
            'name': '消防联动控制器应能按设定的控制逻辑向各相关的受控设备发出联动控制信号，并接受相关设备的联动反馈信号',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501024: {
            'name': '各受控设备接口的特性参数应与消防联动控制器发出的联动控制信号相匹配。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501025: {
            'name': '消防水泵、防烟和排烟风机的控制设备，除应采用联动控制方式外，还应在消防控制室设置手动直接控制装置。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501026: {
            'name': '需要火灾自动报警系统联动控制的消防设备，其联动触发信号应采用两个独立的报警触发装置报警信号的"与"逻辑组合。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501027: {
            'name': '火灾自动报警系统应设置火灾声光警报器，并应在确认火灾后启动建筑内的所有火灾声光警报器',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501028: {
            'name': '火灾声警报器设置带有语音提示功能时，应同时设置语音同步器',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501029: {
            'name': '同一建筑内设置多个火灾声警报器时，火灾自动报警系统应能同时启动和停止所有火灾声警报器工作',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501030: {
            'name': '消防应急广播与普通广播或背景音乐广播合用时，应具有强制切入消防应急广播的功能',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501031: {
            'name': '不同电压等级的线缆不应穿入同一根保护管内，当合用同一线槽时，线槽内应有隔板分隔',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information']
                }
            },
        },
        501032: {
            'name': '',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501036: {
            'name': '线路暗敷设时，应采用金属管、可挠(金属)电气导管或B1级以上的刚性塑料管保护，并应敷设在不燃烧体的结构层内，且保护层厚度不宜小于30mm；线路明敷设时，应采用金属管、可挠(金属)电气导管或金属封闭线槽保护。矿物绝缘类不燃性电缆可直接明敷',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501038: {
            'name': '线路暗敷设时，应采用金属管、可挠(金属)电气导管或B1级以上的刚性塑料管保护，并应敷设在不燃烧体的结构层内，且保护层厚度不宜小于30mm；线路明敷设时，应采用金属管、可挠(金属)电气导管或金属封闭线槽保护。矿物绝缘类不燃性电缆可直接明敷',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                },
                (DrawingType.XIAOFANG, DrawingType.XIAOFANG_FIRST_FLOOR, DrawingType.XIAOFANG_UNDERGROUND): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + \
                                LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["火灾自动报警按钮"] + \
                                ["door", "window"],
                    'operations': ['combination', 'segmentation', 'classification'],
                }
            },
        },
        501043: {
            'name': '任一台火灾报警控制器所连接的火灾探测器、手动火灾报警按钮和模块等设备总数和地址总数，均不应超过3200点，其中每一总线回路连接设备的总数不宜超过200点，且应留有不少于额定容量10%的余量；任一台消防联动控制器地址总数或火灾报警控制器(联动型)所控制的各类模块总数不应超过1600点，每一联动总线回路连接设备的总数不宜超过100点，且应留有不少于额定容量10%的余量。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501044: {
            'name': '',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501045: {
            'name': '',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501046: {
            'name': '火灾声警报器单次发出火灾警报时间宜为8s~20s，同时设有消防应急广播时，火灾声警报应与消防应急广播交替循环播放',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501047: {
            'name': '消防应急广播的单次语音播放时间宜为10s~30s，应与火灾声警报器分时交替工作，可采取1次火灾声警报器播放、1次或2次消防应急广播播放的交替工作方式循环播放',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501048: {
            'name': '疏散通道上设置的防火卷帘的联动控制设计，应符合下列规定:1 联动控制方式，防火分区内任两只独立的感烟火灾探测器或任一只专门用于联动防火卷帘的感烟火灾探测器的报警信号应联动控制防火卷帘下降至距楼板面1.8m处:任一只专门用于联动防火卷帘的感温火灾探测器的报警信号应联动控制防火卷帘下降到楼板面；在卷帘的任一侧距卷帘纵深O.5m～5m内应设置不少于2只专门用于联动防火卷帘的感温火灾探测器',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501049: {
            'name': '防火卷帘下降至距楼板面1.8m处、下降到楼板面的动作信号和防火卷帘控制器直接连接的感烟、感温火灾探测器的报警信号，应反馈至消防联动控制器。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501050: {
            'name': '未集中设置的模块附近应有尺寸不小于100mm×100mm的标识。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        501051: {
            'name': '应设置防火门系统的联动控制设计',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.HUOZAI_AUTO_SYSTEM): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': [],
                }
            },
        },
        504001: {
            'name': '火灾自动报警系统应设置交流电源和蓄电池备用电源。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.QIANGDIAN_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        504002:  {
            'name': '抗震设防烈度为6度及6度以上地区的建筑机电工程必须进行抗震设计。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.QIANGDIAN_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        505001: {
            'name': '消防控制室 、消防水泵房、防烟和排烟风机房的消防用电设备及消防电梯等的供电，应在其配电线路的最末一级配电箱处设置自动切换装置',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.QIANGDIAN_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                },
                (DrawingType.PEIDIAN_PEIDIANXIANG_SYSTEM, ): {
                    'major_drawing': True,
                    'entities': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["系统图双切开关"] + ['wire'],
                    'operations': ["combination", "classification"],
                },
            },
        },
        505002: {
            'name': '除本规范第 10.1.1 和 10.1.2 条外的建筑物、储罐（区〉和堆场等的消防用电，可按三级负荷供电。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.QIANGDIAN_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        505003: {
            'name': '下列建筑物的消防用电应按一级负荷供电。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.QIANGDIAN_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        505004: {
            'name': '二类高层建筑 二级负荷',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.QIANGDIAN_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        505005: {
            'name': '应急照明和灯光疏散指示标志的备用电源的连续供电时间应不小于30min',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.QIANGDIAN_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        505006: {
            'name': '开关、插座和照明灯具靠近可燃物时，应采取隔热、散热等防火措施',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.QIANGDIAN_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        505007: {
            'name': '除建筑高度小于 27m 的住宅建筑外,民用建筑、厂房和丙类仓库的下列部位应设置疏散照明',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                },
                (DrawingType.ZHAOMING, DrawingType.ZHAOMING_FIRST_FLOOR, DrawingType.ZHAOMING_UNDERGROUND): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["疏散照明灯具"] +
                                ["elevator_box", "elevator_stair", "door", "window", "elevator_door", ],
                    'operations': ['classification', 'combination', 'segmentation'],
                },
            },
        },
        505008: {
            'name': '消防控制室、消防水泵房、自备发电机房、配电室、防排烟机房以及发生火灾时仍需正常工作的消防设备房应设置备用照明，其作业面的最低照度不应低于正常照明的照度',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.QIANGDIAN_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        505009: {
            'name': '公共建筑、建筑高度大于54m的住宅建筑、高层厂房（库房）和甲、乙、丙类单、多层厂房，应设置灯光疏散指示标志，并应符合下列规定：1 应设置在安全出口和人员密集的场所的疏散门的正上方；2 应设置在疏散走道及其转角处距地面高度1.0m以下的墙面或地面上。灯光疏散指示标志的间距不应大于20m；对于袋形走道，不应大于10m；在走道转角区，不应大于1.0m。',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ZHAOMING, DrawingType.ZHAOMING_FIRST_FLOOR, DrawingType.ZHAOMING_UNDERGROUND): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["basic"] +
                                LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["灯光疏散指示标志"] +
                                ["door", "window"],
                    'operations': ["combination", "segmentation", "classification"],
                }
            },
        },
        # 506001: {
        #     'name': '专设引下线不应少于2根，并应沿建筑物四周和内庭院四周均匀对称布置，其间距沿周长计算不应大于18m。当建筑物的跨度较大，\
        #             无法在跨距中间设引下线时，应在跨距两端设引下线并减小其他引下线的间距，专设引下线的平均间距不应大于18m。',
        #     'type': MultiBorderPipelineType.TYPE_C,
        #     'borders': {
        #         (DrawingType.DIANQI_DESIGN,): {
        #             'major_drawing': True,
        #             'entities': [],
        #             'operations': ['text_information'],
        #         },
        #         (DrawingType.FANGLEI, ): {
        #             'major_drawing': True,
        #             'entities': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["接闪带"] +
        #                         LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["专设引下线"],
        #             'operations': ['combination', 'classification', 'segmentation'],
        #         }
        #     },
        # },
        # 506002: {
        #     'name': '在可能发生对地闪击的地区，预计雷击次数大于0．25次／a的住宅。应划为第二类防雷建筑物',
        #     'type': MultiBorderPipelineType.TYPE_C,
        #     'borders': {
        #         (DrawingType.DIANQI_DESIGN, DrawingType.FANGLEI): {
        #             'major_drawing': True,
        #             'entities': [],
        #             'operations': ['text_information'],
        #         }
        #     },
        # },
        # 506003: {
        #     'name': '在可能发生对地闪击的地区，预计雷击次数大于等于0．05次／a小于等于0．25次／a的住宅。应划为第三类防雷建筑物',
        #     'type': MultiBorderPipelineType.TYPE_C,
        #     'borders': {
        #         (DrawingType.DIANQI_DESIGN, DrawingType.FANGLEI): {
        #             'major_drawing': True,
        #             'entities': [],
        #             'operations': ['text_information'],
        #         }
        #     },
        # },
        # 506006: {
        #     'name': '三类防雷建筑专设引下线不应少于2根，其间距沿周长计算不应大于25m。',
        #     'type': MultiBorderPipelineType.TYPE_C,
        #     'borders': {
        #         # (DrawingType.DIANQI_DESIGN,): {
        #         #     'major_drawing': True,
        #         #     'entities': [],
        #         #     'operations': ['text_information'],
        #         # },
        #         (DrawingType.FANGLEI, ): {
        #             'major_drawing': True,
        #             'entities': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["接闪带"] +
        #                         LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["专设引下线"],
        #             'operations': ['combination', 'classification', 'segmentation'],
        #         }
        #     },
        # },
        508001: {
            'name': '插座的形式和安装要求应符合下列规定：6 在住宅和儿童专用的活动场所应采用带保护门的插座。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.QIANGDIAN_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        509001: {
            'name': '无障碍厕所的无障碍设计应符合下列规定：10 在坐便器旁的墙面上应设高400mm~500mm的救助呼叫按钮。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        510001: {
            'name': '消防水泵控制柜在平时应使消防水泵处于自动启泵状态。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        510002: {
            'name': '消防水泵应能手动启停和自动启动。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },

        510003: {
            'name': '消防水泵不应设置自动停泵的控制功能，停泵应由具有管理权限的工作人员根据火灾扑救情况确定。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        510004: {
            'name': '消防控制柜或控制盘应设置专用线路连接的手动直接启泵按钮。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        510005: {
            'name': '消防水泵控制柜设置在专用消防水泵控制室时，其防护等级不应低于IP30；与消防水泵设置在同一空间时，其防护等级不应低于IP55。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        510006: {
            'name': '在高温潮湿环境下，消防水泵控制柜内应设置自动防潮除湿的装置。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        510007: {
            'name': '消防水泵控制柜应设置机械应急启泵功能，并应保证在控制柜内的控制线路发生故障时由有管理权限的人员在紧急时启动消防水泵',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        511002: {
            'name': '住宅套内的电源插座与照明，应分路配电。安装在1．8m及以下的插座均应采用安全型插座。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.QIANGDIAN_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        511003: {
            'name': '水、暖、电、气管线穿过楼板和墙体时，孔洞周边应采取密封隔声措施。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.QIANGDIAN_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        512003: {
            'name': '套内安装在1．80m及以下的插座均应采用安全型插座',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.QIANGDIAN_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        512004: {
            'name': '当发生火警时，疏散通道上和出入口处的门禁应能集中解锁或能从内部手动解锁。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.XIAOFANG_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        513001: {
            'name': '应急照明控制器的主电源应由消防电源供电；控制器的自带蓄电池电源应至少使控制器在主电源中断后工作3h。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN, DrawingType.QIANGDIAN_DESIGN): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        514001: {
            'name': '每套住宅应设置自恢复式过、欠电压保护电器',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.PEIDIAN_PEIDIANXIANG_SYSTEM,): {
                    'major_drawing': True,
                    'entities': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["系统图单刀开关"] + ["wire"],
                    'operations': ["combination", "classification"],
                }
            },
        },
        514002: {
            'name': '高层住宅建筑中明敷的线缆应选用低烟、低毒的阻燃类线缆',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                },
                (DrawingType.PEIDIAN_PEIDIANXIANG_SYSTEM,): {
                    'major_drawing': True,
                    'entities': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["系统图单刀开关"] + ["wire"],
                    'operations': ["combination", "classification"],
                }
            },
        },
        514003: {
            'name': '设置在住宅建筑内的变压器，应选择干式、气体绝缘或非可燃性液体绝缘的变压器',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        506008: {
            'name': '固定在建筑物上的节日彩灯、航空障碍信号灯及其他用电设备和线路应根据建筑物的防雷类别采取相应的防止闪电电涌侵入的措施',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.PEIDIAN_MAIN_ROUTE_SYSTEM,): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value["basic"] +
                                LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱"],
                    'operations': ["combination", "segmentation", "classification"],
                },
                (DrawingType.PEIDIAN_PEIDIANXIANG_SYSTEM,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["basic"] +
                                LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["浪涌保护器"],
                    'operations': ["combination", "classification"],
                }
            },
        },
        514006: {
            'name': '当配变电所设在住宅建筑内时，配变电所不应设在住户的正上方、正下方、贴邻和住宅建筑疏散出口的两侧，不宜设在住宅建筑地下的最底层。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["basic"] +
                                LayerConfig.BASIC_LAYERS.value["indoor_segment"],
                    'operations': ['combination', 'segmentation', 'classification', 'text_information'],
                }
            },
        },
        513006: {
            'name': '设置消防控制室的场所应选择集中控制型系统',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.XIAOFANG_FIRST_FLOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window"],
                    'operations': ["combination", "segmentation"],
                },
                (DrawingType.EMERGENCY_ILLUMINATION_SYSTEM,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        515022: {
            'name': '竖井大小除应满足布线间隔及端子箱、 配电箱布置所必 需尺寸外， 进人竖井宜在箱体前留有不小于0.8m的操作距离。 当建筑物平面受限制时， 可利用公共走道满足操作距离的要求， 但竖井的进深不应小于0. 6m。 ',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DIANQI, DrawingType.ZHAOMING_FIRST_FLOOR, DrawingType.ZHAOMING): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                LayerConfig.BASIC_LAYERS.value["basic"] + ["door", "window"] +
                                LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱"],
                    'operations': ["combination", "segmentation", "classification"],
                },
                (DrawingType.DIANJING_DAYANG,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                LayerConfig.BASIC_LAYERS.value["basic"] + ["door", "window"] +
                                LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱"],
                    'operations': ["combination", "segmentation", "classification"],
                }
            },
        },
        515007: {
            'name': '竖井内应设电气照明及单相三孔电源插座--获取与照明平面图同一子项的电气平面图',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.ZHAOMING_FIRST_FLOOR, DrawingType.ZHAOMING, DrawingType.ZHAOMING_UNDERGROUND,
                 DrawingType.DIANQI): {
                    'major_drawing': True,
                    'entities': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["普通灯"] +
                                LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["单管灯"] +
                                LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["双管灯"] +
                                LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["插座"],
                    'operations': ["combination", "classification"],
                }
            },
        },
        515020: {
            'name': '机房内应设置储油间， 其总储存量不应超过1m³, 并应采取相应的防火措施',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.GENERATOR_ROOM_DAYANG, DrawingType.DIANQI): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"],
                    'operations': ['combination', 'classification', 'segmentation', 'text_information'],
                }
            },
        },
    }