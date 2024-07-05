# -*- coding: utf-8 -*-

from enum import Enum

# from rule_engine.single_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig


class RuleConfig(Enum):
    # 万科审核规则列表
    VANKE_RULES = {
        DrawingType.DECORATION_ELECTRIC_PLAN: ["1502001", "1603001", "1603002",  "1603003", "1603004", "1603005", "1603006",
                                               "1603016", "1603011", "1603094"],
        DrawingType.DECORATION_PLUG_SWITCH_PLAN: [],
        DrawingType.DECORATION_ELECTRIC_EQUIPMENT_SCHEDULE: [],
        DrawingType.DECORATION_STRONG_ELECTRIC_SYSTEM: [],
    }

    # 规则详情
    # REF: https://www.kdocs.cn/p/51356796370?from=docs&source=docsWeb
    CONFIGURATION = {
        "1502001": {
            'name': '电缆大小选择应合理，不能过大选取',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + LayerConfig.BASIC_LAYERS.value['basic'] + 
            ['window', 'door', 'socket', 'annotation_line', 'device_light'] +
            ['device_switch', 'common_lamp', 'single_tube_lamp', 'double_tube_lamp', 'triple_tube_lamp', 'emergency_single_tube_lamp'] + 
            ['emergency_double_tube_lamp', 'emergency_triple_tube_lamp', 'a_model_emergency_lamp', 'equipotential_junction_plate'] + 
            ['button', 'load_switch', 'television_socket', 'telephone_socket', 'weak_electric_box', 'strong_electric_box'] + 
            LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["灯具"],
            # 'operation': ['combination', 'classification', 'text_information', 'segmentation']
            'operation': ['combination', 'classification', 'text_information', 'segmentation']
            # 'operation': []
        },
        "1603002": {
            'name': '强、弱电箱、可视对讲平面位置，板房与货量是否一致？',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + LayerConfig.BASIC_LAYERS.value['basic'] +
            ['visual_intercom', 'weak_electric_box', 'strong_electric_box'] +
            LayerConfig.DEVICE_ENTITY_LAYER_MAP.value['强电箱'] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value['弱电箱'] +
            LayerConfig.DEVICE_ENTITY_LAYER_MAP.value['可视对讲'],
            'operation': ['combination', 'classification', 'text_information', 'segmentation']
        },
        "1603011": {
            'name': '强、弱电箱、可视对讲平面位置，板房与货量是否一致？',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + LayerConfig.BASIC_LAYERS.value['basic'] +
                      ['visual_intercom', 'weak_electric_box', 'strong_electric_box'] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value['强电箱'] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value[
                          '弱电箱'] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value['可视对讲'],
            'operation': ['combination', 'classification', 'text_information', 'segmentation']
        },
        "1603004": {
            'name': '开关、插座、电话/网络/电视接口、等电位的数量，板房与货量是否一致？',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + LayerConfig.BASIC_LAYERS.value['basic'] +
                    LayerConfig.DEVICE_ENTITY_LAYER_MAP.value['平面图开关'] +
                    LayerConfig.DEVICE_ENTITY_LAYER_MAP.value['插座'] +
                    LayerConfig.DEVICE_ENTITY_LAYER_MAP.value['信息插座'] +
                    LayerConfig.DEVICE_ENTITY_LAYER_MAP.value['电话插座'] +
                    LayerConfig.DEVICE_ENTITY_LAYER_MAP.value['电视插座'] +
                    LayerConfig.DEVICE_ENTITY_LAYER_MAP.value['等电位连接板'] +
                    ['dash_border'],
            'operation': ['combination', 'classification', 'text_information', 'segmentation']
        },
        "1603094": {
            'name': '强电箱内控制回路数量，板房与货量区是否一致？',
            'entity': ['circuit'],
            'operation': ['combination', 'classification', 'text_information', 'segmentation']
        },
    }

# for i in RuleConfig.VANKE_RULES.value.keys():
#     RuleConfig.VANKE_RULES.value[i] = []
