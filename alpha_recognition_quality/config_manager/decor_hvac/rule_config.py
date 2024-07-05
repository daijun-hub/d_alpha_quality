# -*- coding: utf-8 -*-

from enum import Enum

# from rule_engine.single_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig


class RuleConfig(Enum):
    # 万科审核规则列表
    VANKE_RULES = {
        DrawingType.DECORATION_HVAC_VENTILATION_PLAN: ["1603015", "1603022", '1603083', "1603078"],
        DrawingType.DECORATION_HEATING_DESCRIPTION: ["1603022", '1603083'], # "1603022"
        DrawingType.HEATING_PLAN: ["1"],
        DrawingType.IGNORE: [],
    }

    # 规则详情
    # REF: https://www.kdocs.cn/p/51356796370?from=docs&source=docsWeb
    CONFIGURATION = {
        # "1603022": {
        #     'name': '货量区和板房的地暖系统控制方式是否一致（分户控制和分室控制）',
        #     'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"],
        #     'operation': ["text_information"]
        # },
        "1603015":{
            'name': '板房和货量采用的空调系统形式（中央空调、分体空调）是否存在货板不一致',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["air_conditioner", "door", "window", "fen_ji_shui_qi", "temp_controller", "annotation_line"],
            'operation': ['combination', 'classification', "segmentation", "text_information"]
        },
        "1603078": {
            'name': '地暖温度控制器、分集水器的平面位置，货板是否一致',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ["fen_ji_shui_qi", "door", "window", "temp_controller", "annotation_line"],
            'operation': ['combination', 'classification', "segmentation", "text_information"]
        },
        # "1402009": {
        #     'name': '电梯机房设置通风系统，其通风量需根据电梯机房发热量计算，并按每台电梯通风量不小于1000m3/h选择通风机',
        #     'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net"],
        #     'operation': ['combination', 'classification', "segmentation", "text_information"]
        # },
        #
        # "1402014": {
        #     'name': '当采用生活热水及采暖两用燃气壁挂炉时，采暖末端供水温度控制在35℃～45℃，供回水温差不宜大于10℃。',
        #     'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net"],
        #     'operation': ["text_information"]
        # },
        #
        # "1402024": {
        #     'name': '地暖管保温板厚度不小于10mm。',
        #     'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net"],
        #     'operation': ["text_information"]
        # },
        #
        # "1402027": {
        #     'name': '设置户式集中空调系统时，当条件允许，回风口和检修口应合并设置，回风口宽度不小于300mm，不另设单独检修口。'
        #             '当回风口和检修口分别设置时，回风口最小净宽度为200mm，检修口尺寸为350x350。且送风口采用双层可调百叶，回风口采用可拆单层百叶（带过滤网）',
        #     'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net"] +
        #               ["kong_tiao_hui_feng_kou", "duo_ye_feng_kou", "ce_qiang_bu_feng_kou", "ce_song_jia_ya_feng_kou", "ce_song_pai_yan_jian_pai_feng_kou", "xia_song_feng_kou", "duo_ye_feng_kou"],
        #     'operation': ['combination', 'classification', "segmentation",]
        # },
        #
        # "1404001": {
        #     'name': '新风系统取风口设置不合理，易吸入浊气。',
        #     'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["xin_feng_guan", "pai_feng_guan"],
        #     'operation': ['combination', 'classification', "segmentation", "text_information"]
        # },

    }

# for i in RuleConfig.VANKE_RULES.value.keys():
#     RuleConfig.VANKE_RULES.value[i] = []