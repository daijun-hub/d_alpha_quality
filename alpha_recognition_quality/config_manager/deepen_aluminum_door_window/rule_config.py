from enum import Enum

# from rule_engine.single_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig


class RuleConfig(Enum):
    # 万科审核规则列表
    VANKE_RULES = {
        DrawingType.DEEPEN_DOOR_WINDOW_DESCRIPTION: ["1103044", "1103045", "1103046", "1103047"],
    }

    INDOOR_FIRST_FLOOR_NO_SPACE_RULE = [101016, 101036, 101061]

    SPECIAL_CHEKCPOINT_ID_DICT = {
        101008: 10100800,
        101009: 10100901,
        101027: 10102700,
        101031: 10103101,
        101032: 10103202,
        101033: 10103303,
        101034: 10103404,
        101055: 10105500,
        101056: 10105601,
    }

    # 规则详情
    # REF: https://www.kdocs.cn/p/51356796370?from=docs&source=docsWeb
    CONFIGURATION = {
        # "1100001": {
        #     "name": "立管不应设置在窗户前。",
        #     "entity": LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "pipe"],
        #     "operation": ["combination", "segmentation", "classification"],
        # },
    }

# for i in RuleConfig.VANKE_RULES.value.keys():
#     RuleConfig.VANKE_RULES.value[i] = []
