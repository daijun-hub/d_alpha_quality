# -*- coding: utf-8 -*-

from enum import Enum

# from rule_engine.multi_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig
from ..multiple_border_pipeline_config import MultiBorderPipelineType


class MultiBorderRuleConfig(Enum):
    CONFIGURATION = {
        # 515020: {
        #     'name': '机房内应设置储油间， 其总储存量不应超过1m³, 并应采取相应的防火措施',
        #     'type': MultiBorderPipelineType.TYPE_C,
        #     'borders': {
        #         (DrawingType.GENERATOR_ROOM_DAYANG, DrawingType.DIANQI): {
        #             'major_drawing': True,
        #             'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"],
        #             'operations': ['combination', 'classification', 'segmentation', 'text_information'],
        #         }
        #     },
        # },
    }