# -*- coding: utf-8 -*-

from enum import Enum

# from rule_engine.multi_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig
from ..multiple_border_pipeline_config import MultiBorderPipelineType


class MultiBorderRuleConfig(Enum):
    CONFIGURATION = {}