# -*- coding: utf-8 -*-

from enum import Enum

# from rule_engine.single_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig


class RuleConfig(Enum):
    VANKE_RULES = {
        # 给排水系统图
        # 给水系统子图
        DrawingType.WATER_SUPPLY_SYSTEM_SUB: ['1603007', '1603009'],

        # 热水系统子图
        DrawingType.HOT_WATER_SUPPLY_SYSTEM_SUB: ['1603007'],

        # 给排水平面图
        DrawingType.WATER_SUPPLY_DRAIN_PLAN: ['1603008', '1603009'],

        # 卫生间立面图
        # 装修给排水设计说明
        DrawingType.DECORATION_PLUMBING_DESCRIPTION: ['1603009'],
    }

    # 规则详情
    # REF: https://www.kdocs.cn/p/51356796370?from=docs&source=docsWeb
    CONFIGURATION = {
        '1603008': {
            'name': '找到对应图例，审查尺寸标注数值',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['window', 'door'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        '1603007': {
            'name': '找到对应图例，审查尺寸标注数值',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['window', 'door'],
            'operation': ['combination', 'segmentation', 'classification'],
        },
        '1603009': {
            'name': '找到对应图例，审查尺寸标注数值',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['window', 'door'],
            'operation': ['combination', 'segmentation', 'classification'],
        },

    }

# for i in RuleConfig.VANKE_RULES.value.keys():
#     RuleConfig.VANKE_RULES.value[i] = []
