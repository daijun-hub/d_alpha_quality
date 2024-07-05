# -*- coding: utf-8 -*-

from enum import Enum
from .drawing_config import DrawingType


class DrawingTypeConfig(Enum):
        STR = {

            DrawingType.GENERAL_DESCRIPTION: {
                'entities': [],
                'operations': []

            },  # "结构设计总说明"
            DrawingType.PILE_DESCRIPTION: {
                'entities': [],
                'operations': []

            },  # "桩设计说明"
            DrawingType.WALL_COLUMN_GRAPH: {
                'entities': ['wall', 'pillar', 'wall_hatch', 'axis_net', 'axis_grid', 'annotation_line',
                             'arrow', 'other_layers'],
                'operations': ['combination']

            },  # "住宅墙柱平法施工图"
            DrawingType.WALL_COLUMN_DETAILS: {
                'entities': ['wall', 'pillar', 'wall_hatch', 'axis_net', 'axis_grid', 'annotation_line',
                             'arrow', 'other_layers'],
                'operations': ['combination']

            },  # "住宅墙柱详图"
            DrawingType.BEAM_GRAPH: {
                'entities': ['pillar', 'beam', 'axis_net', 'axis_grid', 'annotation_line', 'other_layers'],
                'operations': ['combination']

            },  # "住宅梁平法施工图"
            DrawingType.STRUCTURE_GRAPH: {
                'entities': ['pillar', 'beam', 'wall', 'axis_net', 'axis_grid', 'other_layers'],  # 识别slab
                'operations': ['combination']

            },  # "住宅结构平面图"
            DrawingType.SLAB_GRAPH: {
                'entities': ['pillar', 'beam', 'wall', 'axis_net', 'axis_grid', 'other_layers'],  # 识别slab
                'operations': ['combination']

            },  # "住宅板平法施工图"
            DrawingType.BASEMENT_WALL_COLUMN_GRAPH: {
                'entities': ['pillar', 'wall', 'axis_net', 'axis_grid', 'other_layers'],
                'operations': ['combination']

            },  # "地下室墙柱平法施工图"
            DrawingType.BASEMENT_WALL_COLUMN_DETAILS: {
                'entities': ['axis_net', 'axis_grid', 'other_layers'],
                'operations': []

            },  # "地下室墙柱详图"
            DrawingType.BASEMENT_BEAM_GRAPH: {
                'entities': ['pillar', 'beam', 'axis_net', 'axis_grid', 'other_layers'],
                'operations': ['combination']

            },  # "地下室梁平法施工图"
            DrawingType.BASEMENT_SLAB_GRAPH: {
                'entities': ['pillar', 'wall', 'beam', 'axis_net', 'axis_grid', 'other_layers'],  # 识别slab
                'operations': ['combination']

            },  # "地下室板平法施工图"
            DrawingType.BASEMENT_STRUCTURE_GRAPH: {
                'entities': ['wall', 'beam', 'axis_net', 'axis_grid', 'other_layers'],  # 识别slab
                'operations': ['combination']

            },  # "地下室结构平面图"
            DrawingType.PILE_GRAPH: {
                'entities': [],
                'operations': []

            },  # "桩位平面布置图"
            DrawingType.BOLT_GRAPH: {
                'entities': [],
                'operations': []

            },  # "锚杆平面布置图"
            DrawingType.BASIC_GRAPH: {
                'entities': ['pillar'],
                'operations': ['combination']

            },  # "基础平面布置图"
            DrawingType.PLATFORM_GRAPH: {
                'entities': [],
                'operations': []

            },  # "承台平面布置图"
            DrawingType.BASE_STRUCTURE_DETAILS: {
                'entities': [],
                'operations': []

            },  # "基础详图"
            DrawingType.STAIR_STRUCTURE_DETAILS: {
                'entities': [],
                'operations': []

            },  # "楼梯详图"
            DrawingType.WALL_STRUCTURE_DETAILS: {
                'entities': [],
                'operations': []

            },  # "墙身详图"
            DrawingType.BICYCLE_RAMP_STRUCTURE_DETAILS: {
                'entities': [],
                'operations': []

            },  # "机动车坡道详图"
            DrawingType.CAR_RAMP_STRUCTURE_DETAILS: {
                'entities': [],
                'operations': []

            },
            # "人防详图"
            DrawingType.CIVIL_AIR_DEFENSE_DETAILS: {
                'entities': [],
                'operations':[]
            },
            DrawingType.IGNORE: {
                'entities': [],
                'operations': []

            },

        }
