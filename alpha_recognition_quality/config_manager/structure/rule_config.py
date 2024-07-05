# -*- coding: utf-8 -*-

from enum import Enum

# from rule_engine.single_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig


class RuleConfig(Enum):
    # 万科审核规则列表
    VANKE_RULES = {
        DrawingType.GENERAL_DESCRIPTION: [],
        DrawingType.PILE_DESCRIPTION: [],
        DrawingType.WALL_COLUMN_GRAPH: [],
        DrawingType.WALL_COLUMN_DETAILS: [],
        DrawingType.BEAM_GRAPH: ["1203001", "1203002"],
        DrawingType.STRUCTURE_GRAPH: ["1203003", "1203004"],
        DrawingType.SLAB_GRAPH: ["1203003", "1203004"],
        DrawingType.BASEMENT_WALL_COLUMN_GRAPH: [],
        DrawingType.BASEMENT_WALL_COLUMN_DETAILS: [],
        DrawingType.BASEMENT_BEAM_GRAPH: [],
        DrawingType.BASEMENT_SLAB_GRAPH: [],
        DrawingType.BASEMENT_STRUCTURE_GRAPH: [],
        DrawingType.PILE_GRAPH: [],
        DrawingType.BOLT_GRAPH: [],
        DrawingType.BASIC_GRAPH: [],
        DrawingType.PLATFORM_GRAPH: [],
        DrawingType.BASE_STRUCTURE_DETAILS: [],
        DrawingType.STAIR_STRUCTURE_DETAILS: [],
        DrawingType.WALL_STRUCTURE_DETAILS: [],
        DrawingType.BICYCLE_RAMP_STRUCTURE_DETAILS: [],
        DrawingType.CAR_RAMP_STRUCTURE_DETAILS: [],
        DrawingType.IGNORE: [],
    }

    # 规则详情
    # REF: https://www.kdocs.cn/p/51356796370?from=docs&source=docsWeb
    CONFIGURATION = {
        # 301003: {
        #     'name': '住宅应设室内给水排水系统',
        #     'entity': ["vpipe", "annotation_line"],
        #     'operation': ['combination', 'classification']
        # },
    }