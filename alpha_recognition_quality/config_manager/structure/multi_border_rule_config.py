# -*- coding: utf-8 -*-

from enum import Enum

# from rule_engine.multi_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig
from ..multiple_border_pipeline_config import MultiBorderPipelineType


class MultiBorderRuleConfig(Enum):
    CONFIGURATION = {
        # "1402001": {
        #     'name': '采暖管选材满足压力要求，不提高管材级别。楼栋内采暖立管采用镀锌钢管（DN＞80采用无缝钢管）；'
        #             '当采用分户供暖时，供水干管采用PPR管；采暖户内管：地暖采用PE-RT管。',
        #     'type': MultiBorderPipelineType.TYPE_C,
        #     'borders': {
        #         (DrawingType.HVAC_DESIGN,): {
        #             'major_drawing': True,
        #             'entities': [],
        #             'operations': ['text_information'],
        #         }
        #     },
        # },
    }

