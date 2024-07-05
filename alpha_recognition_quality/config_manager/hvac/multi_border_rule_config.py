# -*- coding: utf-8 -*-

from enum import Enum

# from rule_engine.multi_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig
from ..multiple_border_pipeline_config import MultiBorderPipelineType


class MultiBorderRuleConfig(Enum):
    CONFIGURATION = {
        "1402001": {
            'name': '采暖管选材满足压力要求，不提高管材级别。楼栋内采暖立管采用镀锌钢管（DN＞80采用无缝钢管）；'
                    '当采用分户供暖时，供水干管采用PPR管；采暖户内管：地暖采用PE-RT管。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.HVAC_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1402002": {
            'name': '消防电梯前室不宜顶面设置加压风口，特殊情况除外，则梁上翻，满足前室吊顶后净高2.4米以上',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.SMOKE_SYSTEM,): {
                    'major_drawing': False,
                    'entities': ['annotation_line', 'elevation_symbol'],
                    'operations': ['combination', 'classification'],
                },
                (DrawingType.T_HEATING_VENTILATION,): {
                    'major_drawing': True,
                    'entities': ['annotation_line', 'elevation_symbol'],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
            },
        },
        "1402007": {
            'name': '空调冷凝水管：PVC-U管，外墙干挂石材内暗敷时采用HDPE管保温管厚度及选材满足要求即可',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.HVAC_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1402008": {
            'name': '冷媒管、冷凝水管、住宅多联机风管保温材料采用难燃B1级发泡橡塑保温。室内采暖主管道保温宜采用难燃B1级发泡橡塑或离心玻璃棉保温材料。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.HVAC_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1402013": {
            'name': '采暖热源：当有市政热源时，优先考虑采用市政热源，当无市政热源是采用燃气壁挂炉',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.HVAC_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        "1402017": {
            'name': '屋顶风机房高度宜小于2.2米，减少机房面积。且加压机房优先设置在地下室',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.T_RF_HEATING_VENTILATION,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net"] +
                                ['annotation_line', 'elevation_symbol'],
                    'operations': ['combination', 'classification', "segmentation", "text_information"],
                },
                (DrawingType.SMOKE_SYSTEM, ): {
                    'major_drawing': True,
                    'entities':  ['annotation_line', 'elevation_symbol'],
                    'operations': ["text_information"],
                },
            },
        },
    }

