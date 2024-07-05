# -*- coding: utf-8 -*-

from enum import Enum

# from rule_engine.single_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig


class RuleConfig(Enum):
    # 万科审核规则列表
    VANKE_RULES = {
        DrawingType.HVAC_DESIGN: ["1402014", "1402024"],
        DrawingType.B_HVAC_DESIGN: [],
        DrawingType.MATERIAL_LIST: ["1402009"],
        DrawingType.B_MATERIAL_LIST: [],
        DrawingType.B_VENTILATION: [],
        DrawingType.B_ROOF_VENTILATION: [2, '1402005'],
        DrawingType.B_HVAC_WATER: [9],
        DrawingType.B_BOILER_ROOM: [],
        DrawingType.B_REFRIGERATION_ROOM: [],
        DrawingType.T_HVAC: [3],
        DrawingType.T_1F_HEATING_VENTILATION: [1],
        DrawingType.T_HEATING_VENTILATION: [1],
        DrawingType.T_AIR_PRE_CAVITATION: [6],
        DrawingType.HEATING_SYSTEM: [8],
        DrawingType.T_RF_HEATING_VENTILATION: [1],
        DrawingType.T_1F_AIR: [5, "1402027", "1404001"],
        DrawingType.T_AIR: [5, "1402027", "1404001"],
        DrawingType.AIR_SYSTEM: [],
        DrawingType.SMOKE_SYSTEM: [7],
        DrawingType.INSTALL_DAYANG: [],
        DrawingType.CIVIL_AIR_DEFENSE_DESIGN: [],
        DrawingType.CIVIL_AIR_DEFENSE_MATERIAL_LIST: [],
        DrawingType.CIVIL_AIR_DEFENSE_B_VENTILATION: [4],
        DrawingType.IGNORE: [],
    }

    # 规则详情
    # REF: https://www.kdocs.cn/p/51356796370?from=docs&source=docsWeb
    CONFIGURATION = {
        1: {'name': '地上采暖通风平面--对象开发',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net"] + \
                      [ "pai_feng_ji", "pai_yan_feng_ji", "jia_ya_feng_ji", "duo_ye_feng_kou", "shou_dong_kai_qi_zhuang_zhi",
                        "nei_chen_jin_shu_feng_guan", "pai_yan_fang_huo_fa_280", "fang_huo_fa_70", "zhi_hui_fa", "xie_ya_fa",
                        "dian_dong_feng_fa", 'bi_shi_zhou_liu_feng_ji', "ce_song_jia_ya_feng_kou", "fen_ji_shui_qi", #"di_nuan_pan_guan",
                        "mao_jin_nuan_qi_jia", "fang_huo_fa_150", "ran_qi_bi_gua_lu",
                      ],
            'operation': ['combination', 'classification', "segmentation", "text_information"]
        },
        2: {'name': '地下车库通风平面图--对象开发',
            'entity': # LayerConfig.BASIC_LAYERS.value["indoor_segment"]  + \
                      # ["pai_yan_jian_pai_feng_guan", "song_bu_feng_ji", "pai_feng_guan", "bu_feng_guan", "jia_ya_feng_guan",] + \
                      ["fang_huo_fa_70", "fang_huo_fa_150", "pai_yan_fang_huo_fa_280",
                        "xia_song_feng_kou",
                        "annotation_line", "song_bu_feng_ji",
                       "fen_ti_kong_tiao",  "feng_ji_pan_guan",
                        "shui_guan_tao_guan", "co_tan_ce_qi",  "ce_qiang_bu_feng_kou",  "ce_song_jia_ya_feng_kou",
                        "ce_song_pai_yan_jian_pai_feng_kou",  "quan_re_jiao_huan_qi",   "nei_chen_jin_shu_feng_guan",
                        "fen_ji_shui_qi",  "jia_ya_feng_ji",  "ya_cha_chuan_gan_qi",  'bi_shi_zhou_liu_feng_ji', "duo_ye_feng_kou",
                        "zhan_shi_pai_feng_ji",  "zhan_shi_song_feng_ji",  "shou_dong_kai_qi_zhuang_zhi",  "pai_yan_jian_pai_feng_ji",
                        "pai_yan_feng_ji",  "pai_feng_ji",  "xin_feng_ji",  "zhi_hui_fa", "mao_jin_nuan_qi_jia", "xie_ya_fa",
                        "xiao_sheng_qi", "ran_qi_bi_gua_lu",  "dian_dong_feng_fa", "kong_tiao_hui_feng_kou",
                        "you_dao_feng_ji",  "feng_guan_shang_xia_fan",
                       ],
            'operation': ['combination', 'classification', "segmentation", "text_information"]
            },
        3: {'name': '地上采暖通风平面--对象开发',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net"] + \
                      ["pai_feng_ji", "pai_yan_feng_ji", "jia_ya_feng_ji", "duo_ye_feng_kou",
                       "shou_dong_kai_qi_zhuang_zhi",
                       "nei_chen_jin_shu_feng_guan", "pai_yan_fang_huo_fa_280", "fang_huo_fa_70", "zhi_hui_fa",
                       "xie_ya_fa", "dian_dong_feng_fa", 'bi_shi_zhou_liu_feng_ji', "ce_song_jia_ya_feng_kou", "fen_ji_shui_qi",
                       # "di_nuan_pan_guan",
                       "mao_jin_nuan_qi_jia", "fang_huo_fa_150", "ran_qi_bi_gua_lu", "fen_ti_kong_tiao",
                       "feng_guan_fa_lan", "xia_song_feng_kou",
                       "pai_yan_jian_pai_feng_guan", "song_bu_feng_guan", "pai_feng_guan", "bu_feng_guan",
                       "jia_ya_feng_guan", "xin_feng_ji"
                       ],
            'operation': ['combination', 'classification', "segmentation", "text_information"]
            },
        4: {
            'name': '地下室战时通风平面图--对象开发',
            'entity': #LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net"] + \
                      ["zhan_shi_song_feng_ji", "zhan_shipai_feng_ji"] +\
                      ["pai_feng_ji", "pai_yan_feng_ji", "jia_ya_feng_ji", "duo_ye_feng_kou",
                       "shou_dong_kai_qi_zhuang_zhi",
                       "nei_chen_jin_shu_feng_guan", "pai_yan_fang_huo_fa_280", "fang_huo_fa_70", "zhi_hui_fa",
                       "xie_ya_fa", "ce_song_pai_yan_jian_pai_feng_kou",
                       "dian_dong_feng_fa", 'bi_shi_zhou_liu_feng_ji', "ce_song_jia_ya_feng_kou", "fen_ji_shui_qi",
                       # "di_nuan_pan_guan",
                       "mao_jin_nuan_qi_jia", "fang_huo_fa_150", "ran_qi_bi_gua_lu", "fen_ti_kong_tiao",
                       "feng_guan_fa_lan", "xia_song_feng_kou",
                       "pai_yan_jian_pai_feng_guan", "song_bu_feng_guan", "pai_feng_guan", "bu_feng_guan",
                       "jia_ya_feng_guan", "xin_feng_ji", "xiao_sheng_qi",
                       ],
            'operation': ['combination', 'classification', "segmentation", "text_information"]
        },
        5: {'name': '空调平面图--对象开发',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net"] + \
                      ["pai_yan_jian_pai_feng_guan", "song_bu_feng_ji", "pai_feng_guan", "bu_feng_guan", "jia_ya_feng_guan",] + \
                      [ "fang_huo_fa_150", "pai_yan_fang_huo_fa_280", "fang_huo_fa_70", "co_tan_ce_qi",
                        "xia_song_feng_kou",   "ce_qiang_bu_feng_kou",  "ce_song_jia_ya_feng_kou", "ce_song_pai_yan_jian_pai_feng_kou",
                        "quan_re_jiao_huan_qi", "nei_chen_jin_shu_feng_guan",  "fen_ti_kong_tiao", "fen_ji_shui_qi",
                        "jia_ya_feng_ji", "ya_cha_chuan_gan_qi",  'bi_shi_zhou_liu_feng_ji', "duo_ye_feng_kou",
                        "zhan_shi_pai_feng_ji", "zhan_shi_song_feng_ji", "shou_dong_kai_qi_zhuang_zhi",
                        "pai_yan_jian_pai_feng_ji",  "pai_yan_feng_ji",  "pai_feng_ji", "xin_feng_ji",  "zhi_hui_fa",
                        "mao_jin_nuan_qi_jia",  "shui_guan_tao_guan",  "xie_ya_fa",  "xiao_sheng_qi",  "ran_qi_bi_gua_lu",
                        "dian_dong_feng_fa",  "kong_tiao_hui_feng_kou",   "you_dao_feng_ji",   "song_bu_feng_ji",  # 送补风机
                        "feng_ji_pan_guan",  "feng_guan_shang_xia_fan",
                        "road",  # 普通道路边线 - 不包含车道中心线
                        "fire_road",  # 消防道路边线
                        "car_lane",  # 地下车库车道线
                        "road_center_line",  # 道路中心线(+xingchexian)
                       ] + \
                      ["feng_guan_fa_lan", "shui_guan_tao_guan", "feng_ji_pan_guan"] + \
                      ["quan_re_jiao_huan_qi", "xin_feng_ji", "feng_ji_pan_guan", "fen_ti_kong_tiao", "kong_tiao_hui_feng_kou"],
            'operation': ['combination', 'classification', "segmentation", "text_information"]
        },
        6: {'name': '预留洞口平面图--对象开发',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net", "annotation_line"] + \
                      ["shui_guan_tao_guan", "kong_tiao_hui_feng_kou"],
            'operation': ['combination', 'classification', "segmentation", "text_information"]
        },
        7: {
            'name': '防排烟系统图--对象开发',
            'entity': # LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net"] + \
                    [
                    "fang_huo_fa_70", "fang_huo_fa_150", "pai_yan_fang_huo_fa_280",
                    "song_bu_feng_ji", "xia_song_feng_kou", "fen_ti_kong_tiao", "feng_ji_pan_guan",
                    "shui_guan_tao_guan", "co_tan_ce_qi", "ce_qiang_bu_feng_kou",  "ce_song_jia_ya_feng_kou",
                    "ce_song_pai_yan_jian_pai_feng_kou",  "quan_re_jiao_huan_qi", "nei_chen_jin_shu_feng_guan",
                    "fen_ji_shui_qi",  "jia_ya_feng_ji",  "ya_cha_chuan_gan_qi",  'bi_shi_zhou_liu_feng_ji',
                    "duo_ye_feng_kou", "zhan_shi_pai_feng_ji",  "zhan_shi_song_feng_ji",  "shou_dong_kai_qi_zhuang_zhi",
                    "pai_yan_jian_pai_feng_ji",  "pai_yan_feng_ji",  "pai_feng_ji",  "xin_feng_ji",
                    "zhi_hui_fa",  "mao_jin_nuan_qi_jia",  "xie_ya_fa",
                    "xiao_sheng_qi",  "ran_qi_bi_gua_lu",  "dian_dong_feng_fa",
                    "kong_tiao_hui_feng_kou",  "you_dao_feng_ji",  "feng_guan_shang_xia_fan",
                    ],
            'operation': ['combination', 'classification', "segmentation", "text_information"]
        },
        8: {'name': '采暖系统图--对象开发',
            'entity':  # LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net"] + \
                    ["fang_huo_fa_70", "fang_huo_fa_150", "pai_yan_fang_huo_fa_280",
                    "song_bu_feng_ji", "xia_song_feng_kou", "fen_ti_kong_tiao", "feng_ji_pan_guan",
                    "shui_guan_tao_guan", "co_tan_ce_qi", "ce_qiang_bu_feng_kou",  "ce_song_jia_ya_feng_kou",
                    "ce_song_pai_yan_jian_pai_feng_kou",   "quan_re_jiao_huan_qi",   "nei_chen_jin_shu_feng_guan",  "fen_ji_shui_qi",
                    "jia_ya_feng_ji",  "ya_cha_chuan_gan_qi",  'bi_shi_zhou_liu_feng_ji',  "duo_ye_feng_kou",  "zhan_shi_pai_feng_ji",
                    "zhan_shi_song_feng_ji",  "shou_dong_kai_qi_zhuang_zhi",  "pai_yan_jian_pai_feng_ji",  "pai_yan_feng_ji",
                    "pai_feng_ji",  "xin_feng_ji",  "zhi_hui_fa",  "mao_jin_nuan_qi_jia",  "xie_ya_fa",  "xiao_sheng_qi",  "ran_qi_bi_gua_lu",
                    "dian_dong_feng_fa",  "kong_tiao_hui_feng_kou",  "you_dao_feng_ji",  "feng_guan_shang_xia_fan",
                ],
            'operation': ['combination', 'classification', "segmentation", "text_information"]
        },
        9: {'name': '地下车库暖通水管平面图--对象开发',
            'entity':  # LayerConfig.BASIC_LAYERS.value["indoor_segment"]  + \
                       # ["pai_yan_jian_pai_feng_guan", "song_bu_feng_ji", "pai_feng_guan", "bu_feng_guan", "jia_ya_feng_guan",] + \
                    [
                    "elevation_mark", "fang_huo_fa_70", "fang_huo_fa_150", "pai_yan_fang_huo_fa_280",
                    "song_bu_feng_ji", "xia_song_feng_kou", "fen_ti_kong_tiao", "feng_ji_pan_guan",
                    "shui_guan_tao_guan", "co_tan_ce_qi",  "ce_qiang_bu_feng_kou",  "ce_song_jia_ya_feng_kou",
                    "ce_song_pai_yan_jian_pai_feng_kou",  "quan_re_jiao_huan_qi",   "nei_chen_jin_shu_feng_guan",  "fen_ji_shui_qi",
                    "jia_ya_feng_ji",  "ya_cha_chuan_gan_qi",  'bi_shi_zhou_liu_feng_ji',  "duo_ye_feng_kou",   "zhan_shi_pai_feng_ji",
                    "zhan_shi_song_feng_ji",   "shou_dong_kai_qi_zhuang_zhi",   "pai_yan_jian_pai_feng_ji",  "pai_yan_feng_ji",
                    "pai_feng_ji",  "xin_feng_ji",  "zhi_hui_fa",  "mao_jin_nuan_qi_jia",  "xie_ya_fa",  "xiao_sheng_qi",
                    "ran_qi_bi_gua_lu",  "dian_dong_feng_fa",  "kong_tiao_hui_feng_kou",  "you_dao_feng_ji",  "feng_guan_shang_xia_fan",
                ],
            'operation': ['combination', 'classification', "segmentation", "text_information"]
        },

        "1402005": {
            'name': '风管宜在车位尾端安装，禁止地库车道上空平行安装',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net", 'pai_yan_jian_pai_feng_guan',
                                                                          'song_bu_feng_ji', 'pai_feng_guan', "car_lane", "road_center_line"],
            'operation': ['combination', 'classification', "segmentation", "text_information"]
        },

        "1402009": {
            'name': '电梯机房设置通风系统，其通风量需根据电梯机房发热量计算，并按每台电梯通风量不小于1000m3/h选择通风机',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net"],
            'operation': ['combination', 'classification', "segmentation", "text_information"]
        },

        "1402014": {
            'name': '当采用生活热水及采暖两用燃气壁挂炉时，采暖末端供水温度控制在35℃～45℃，供回水温差不宜大于10℃。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net"],
            'operation': ["text_information"]
        },

        "1402024": {
            'name': '地暖管保温板厚度不小于10mm。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net"],
            'operation': ["text_information"]
        },

        "1402027": {
            'name': '设置户式集中空调系统时，当条件允许，回风口和检修口应合并设置，回风口宽度不小于300mm，不另设单独检修口。'
                    '当回风口和检修口分别设置时，回风口最小净宽度为200mm，检修口尺寸为350x350。且送风口采用双层可调百叶，回风口采用可拆单层百叶（带过滤网）',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "axis-net"] +
                      ["kong_tiao_hui_feng_kou", "duo_ye_feng_kou", "ce_qiang_bu_feng_kou", "ce_song_jia_ya_feng_kou", "ce_song_pai_yan_jian_pai_feng_kou", "xia_song_feng_kou", "duo_ye_feng_kou"],
            'operation': ['combination', 'classification', "segmentation",]
        },

        "1404001": {
            'name': '新风系统取风口设置不合理，易吸入浊气。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["xin_feng_guan", "pai_feng_guan"],
            'operation': ['combination', 'classification', "segmentation", "text_information"]
        },

    }