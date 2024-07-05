# -*- coding: utf-8 -*-

from enum import Enum


class LayerConfig(Enum):
    BASIC_IGNORE_WORDS = {
        "basic": [
            "TEXT",
            "DIMS",
            "AXIS",
            "字",
            "编号",
            "标号",
            "名",
            "NAME",
            "AD[-_]NUMB",
            "尺寸",
            "道",
            "线",
            "增补",
            "VALVE",
            "LINE",
            "IDEN",
            "窗沿",
            "DIM",
            "索引",
            "标注",
        ]
    }

    ENTITY_LAYER_DICT = {
        "border": {
            "layer_sub": [
                "图框",
                "SHET",
                "BORDER",
                "内框",
                "PLOT",
                "PUB[-_]TITLE",
                # "TK",  # 遇到有图框内的表格图层在TK，造成空间分割错误，暂时将TK注释掉
                "BOLDER",
                "^0+$",
                "^4$",
                "PLTW",
                "X[-_]Tlbk",
            ],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        # "给水横管" 类
        "cold_life_supply_hpipe": {  # 未明确是"热给水横管"的给水横管
            "layer_sub": ["PIPE[-_]给水", "PIPE[-_]HOWS", "PIPE[-_]WATS", "P[-_]WATS", "J.*[-_]PIPE", "PIPE[-_]CW",
                          "PIPE[-_]GS", "P[-_]DOWN[-_]PIPE", "管线低区给水", "W[-_]J给水管", "S-PIPE-GS",
                          "供水管", "给水", "P[-_]J[0-9]"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"线"}) +
                           ["VPIPE", "VERT[-_]PIPE", "P[-_]J1", "配件", "消火栓", "辅助", "给水设备"],
        },
        "hot_life_supply_hpipe": {  # 热给水横管
            "layer_sub": ["PIPE[-_]热给水", "PIPE[-_]热水", "P[-_]HOT", "RJ1[-_]PIPE", "PIPE[-_]HW", "PIPE[-_]RS"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] +
                           ["VPIPE", "VERT[-_]PIPE", "配件", "P-WSUP-HOTR-PIPE" "辅助"],
        },
        "hydrant_hpipe": {  # 消火栓横管
            "layer_sub": ["PIPE[-_]消防", "PIPE[-_]FFHW", "PIPE[-_]HYDT", "P[-_]HYDT", "PIPE[-_]FH", "P[-_]HYDR",
                          "消火栓给水管线", "PTP[-_]XH消火栓管低区", "YCS[-_]消防管", "PIPE[-_]消防中", "J[-_]G消栓[-_]管线"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"线"}) +
                           ["VPIPE", "BOX", "VERT[-_]PIPE", "配件", "辅助"],
        },
        "sprinkler_hpipe": {  # 喷淋横管
            "layer_sub": ["PIPE[-_]喷淋", "PIPE[-_]SPRW", "P[-_]HYDT", "PIPE[-_]S", "自喷管", "ZP[-_]PIPE", "P[-_]SPRL",
                          "管线喷淋", "喷洒管", "S喷淋", "喷管"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] +
                           ["VPIPE", "VERT[-_]PIPE", "自喷[-_]SPR", "HEAD", "W[-_]ZP自喷管", "配件", "辅助"],
        },
        "inflow_hpipe": {  # 进水横管
            "layer_sub": ["PIPE[-_]给水", "PIPE[-_]CW", "VPIPE[-_]市政", "WP[-_]G", "P[-_]WatS"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["WP[-_]G[-_]PJ", "配件", "辅助"],
        },
        # "排水横管" 类
        "sewage_hpipe": {  # 污水横管
            "layer_sub": ["PIPE[-_]污水", "PIPE[-_]LDRA", "PIPE[-_]PRSW", "PIPE[-_]SEWR", "P[-_]SEWR", "P[-_]SEWE",
                          "W[-_]PIPE", "PIPE[-_]SW", "W[-_]污水", "W[-_]污水[-_]SILO", "WP[-_]P", "S[-_]PIPE[-_]WS",
                          "-W污水管", "P-WS-PIPE", "S_DRAI_PIPI", "污水", "排污[-_]管线"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["VPIPE", "VERT[-_]PIPE", "配件", "水管_其他", "辅助"],
        },
        "waste_hpipe": {  # 废水横管
            "layer_sub": ["PIPE[-_]废水", "PIPE[-_]DSEW", "PIPE[-_]PRSW", "PIPE[-_]WAST", "P[-_]WAST", "PIPE[-_]WW",
                          "F[-_]废水", "F[-_]废水[-_]SILO", "PIPE[-_]压力废", "W[-_]DRAI[-_]DOME[-_]PIPE",
                          "WAST[-_]GRAV[-_]PIPE", "S-WASTE", "FS-PIPE", "-P-废水管", "S[-_]排水", "S[-_]废水立管",
                          "S_WAST_PRES_PIPE", "PIPE（压力废水管）", "废水管", "PIPE[-_]废水", "废水[-_]管线", "P[-_]WAST[-_]PIPE"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] +
                           ["VPIPE", "VERT[-_]PIPE", "S[-_]排水地漏", "废水管[-_]配件", "配件", "辅助", "VPIP"],
        },
        "rain_hpipe": {  # 雨水横管
            "layer_sub": ["PIPE[-_]雨水", "PIPE[-_]RAIN", "PIPE[-_]PRRW", "PIPE[-_]STOM", "P[-_]STOM", "Y[-_]PIPE",
                          "WP_P", "YT-阳台雨-SILO", "S-Y雨水管"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] +
                           ["VPIPE", "VERT[-_]PIPE", "标注[-_]立管", "P[-_]PS", "排水", "排污[-_]立管编号", "P[-_]WS",
                            "DIM[-_]凝结", "P[-_]YS", "P[-_]FS", "P[-_]J", "P[-_]JS", "配件", "辅助"],
        },
        "condensate_hpipe": {  # 空调冷凝水横管
            "layer_sub": ["PIPE[-_]凝结", "PIPE[-_]SCWA", "PIPE[-_]AIRR", "P[-_]AIRR", "KN[-_]PIPE", "W-KN空调冷凝水管",
                          "0P-PIPE-CO", "凝结水管", "PIPE[-_]凝结", "冷凝[-_]管线", "辅助", "WP[-_]KTN"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["VPIPE", "VERT[-_]PIPE", "配件", "辅助", "LG"],
        },
        # "其他横管" 类
        "ventilate_hpipe": {  # 通气横管
            "layer_sub": ["PIPE[-_]通气", "PIPE[-_]PGAS", "P[-_]PGAS"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["VPIPE", "VERT[-_]PIPE", "配件", "辅助"],
        },
        "life_supply_vpipe": {  # 生活给水立管
            "layer_sub": ["P-JS", "P[-_]VPIPE[-_]给水", "VPIPE[-_]给水", "VPIPE[-_]CW", "S[-_]VPIPE[-_]GS", "WATS[-_]ANNO",
                          "J[-_]L", "WP[-_]G[-_]LG", "P[-_]J[-_]VPIPE", "P[-_]给水管立管", "P[-_]WATE[-_]PIP",
                          "S[-_]给水", "SUPL[-_]VERT", "给水", "WATE[-_]VPIP", "给水", "给排水", "VPIPE[-_]CW",
                          "P[-_]J[-_]L", "W-WSUP-EQPM", "W-VPIPE-J", "W-VPIPE-FW", "WP_G", "W-DRAI-EQPM", "s_VPIPE给中",
                          "P-VERP-DSEW", "P-Pipe-Risr-Watr", "P-Pipe-Risr-Arch", "P-JS-VPIP-IDEN", "P-J1-VPIPE", "WP_P",
                          "水立管", "V-核心筒立管"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"IDEN", '标注'}) +
                           ["雨水斗", "编号", "NO\.", "^[^Vv]*PIPE", "^S-给水$", "P-雨水-EQPM", "S[-_]排水", "-P-废水管",
                            "P[-_]消防管[-_]PJ", "立管定位", "标注$", "污水立管", "废水立管", '^YCS_(.*)_配件$', "辅助", "给水设备"],
        },
        "sewage_vpipe": {  # 污水立管
            "layer_sub": ["P[-_]EQUIP[-_]污水", "VPIPE[-_]SW", "S[-_]VPIPE[-_]WS", "P[-_]W[-_]VPIPE", "SEWR[-_]PIPE"
                                                                                                    "P[-_]SEWE[-_]VPIP",
                          "DRAI[-_]VERT", "DRAI[-_]EQPM", "EQPM[-_]DRAI", "排水", "P[-_]SEWE",
                          "污水", "OP[-_]VPIPE[-_]SW", "P[-_]W[-_]VPIPE", "P[-_]SEWR", "P-WS-VPIP-IDEN",
                          "污水", "VPIPE[-_]PDS", "SEWE[-_]VPIP", "WS", "SW", "P[-_]P[-_]L", "P-YW-L", "P-W-VPIPE",
                          "W-VPIPE-SE", "W-VPIPE-F", "WP_P", "W-DRAI-EQPM", "W-DRAI-DOME-PIPE", "P-VERP-LDRA",
                          "P-Pipe-Risr-Watr", "P-Pipe-Risr-Arch", "GPS-给排水立管", "CKL标注", "W-VPIPE-W", "0YWL", "0PL",
                          "WS_污水立管_W", "P-SEWE-VPIP", "污水立管", "排污-立管", "生活污水-立管",
                          "DOMS[-_]VPIP"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"IDEN"}) +
                           ["雨水斗", "编号", "NO\.", "^[^Vv]*PIPE", "^S-给水$", "P-雨水-EQPM", "S[-_]排水", "-P-废水管",
                            "P[-_]消防管[-_]PJ", "排水地漏", "污水管_配件", "立管定位", "污水管[-_]其他$", "辅助"],
        },
        "waste_vpipe": {  # 废水立管
            "layer_sub": ["废水", "DRAI[-_]EQPM", "EQPM[-_]DRAI", "P[-_].*[-_]L", "排水", "P[-_]W[-_]VPIPE",
                          "VPIPE[-_]WW", "S[-_]VPIPE[-_]FS", "WP[-_]S[-_]LG", "P[-_]F[-_]]VPIPE", "P[-_]WAST[-_]VPIP",
                          "WASTE[-_]VERT", "F[-_]废水[-_]SILO", "P-FS-VPIP-IDEN", "WAST[-_]PIPE", "废水",
                          "VPIPE[-_]PDW", "Pipe[-_]Risr", "VPIPE[-_]压力废", "W-WSUP-EQPM", "W-DRAI-EQPM",
                          "S_WSD_VERT_PIPE（给排水立管）", "污水管、W-DRAI-DOME-PIPE", "P-YF-VPIPE", "P-F-VPIPE",
                          "W-VPIPE-WW", "W-VPIPE-F","P-VERP-DSEW", "P-FW-L", "GPS-给排水立管", "DIM_污水",
                          "CKL标注", "_污水标注", "VPIPE-压力污", "S_NON_VERT_PIPE（非立管）", "P-RAIN-VPIP",
                          "WP_P", "P-SEWE-VPIP", "0P-VPIPE-WW", "排废", "WAST[-_]VPIP"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"IDEN"}) +
                           ["雨水斗", "编号", "NO\.", "^[^Vv]*PIPE", "^S-给水$", "P-雨水-EQPM", "S[-_]排水", "-P-废水管",
                            "P[-_]消防管[-_]PJ", "排水地漏", "立管定位", "^P[-_]PS$", '^YCS_(.*)_配件$', "辅助",
                            "P[-_]WAST[-_]PIPE"],
        },
        "rain_vpipe": {  # 雨水立管
            "layer_sub": ["P-YS", "雨水", "PUB[-_]STRM", "RAIN[-_]EQPM", "P[-_]消防管[-_]PJ", "VPIPE[-_]压力雨", "VPIPE[-_]R",
                          "S[-_]VPIPE[-_]YS", "Y[-_]L", "WP[-_]Y[-_]LG", "P[-_]Y[-_]VPIPE", "P[-_]RAIN[-_]VPIP",
                          "RAIN[-_]VERT", "P-YS-VPIP-IDEN", "P-YS-VPIP+IDEN", "VPIPE[-_]雨水", "VPIPE[-_]Y",
                          "VPIPE[-_]PR", "雨水", "VPIPE[-_]R", "Z[-_]Eqmt", "P[-_]Y[-_]L", "S_WSD_VERT_PIPE（给排水立管）",
                          "W-RAIN-PIPE", "VPIPE-阳台雨", "VPIPE-压力雨", "VPIPE-凝结", "S_NON_VERT_PIPE（非立管",
                          "P-Y-VPIPE", "P-YS-VPIP-IDEN", "P-Pipe-Risr-Watr", "P-Pipe-Risr-Arch", "GPS-给排水立管",
                          "CKL标注", "A-ROOF-WATER", "W-DRAI-EQPM", "P-VERP-RAIN", "8号楼屋面构架平面图",
                          "VALVE_给水", "水立管", "WP_Y", "P-HAVC-VPIP", "0P-VPIPE-R", "8#水施-实施版"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"IDEN"}) +
                           ["雨水斗", "编号", "NO\.", "^[^Vv]*PIPE", "^S-给水$", "P-雨水-EQPM", "S[-_]排水", "-P-废水管",
                            "P[-_]消防管[-_]PJ", "立管定位", "废水立管", "VALVE_雨水", "辅助"],
        },
        "sprinkler_vpipe": {  # 喷淋立管
            "layer_sub": ["VPIPE[-_]S", "S[-_]VPIPE[-_]ZP", "ZP[-_]L", "喷淋", "HUDR[-_]VERT", "消防管",
                          "P[-_]ZP[-_]VPIP[-_]IDEN", "喷淋.*水管", "P[-_]SPRL", "VPIPE[-_]中水", "P[-_]P[-_]L",
                          "S[-_]VPIPE[-_]ZP", "喷淋", "VPIPE[-_]S", "Pipe[-_]Risr", "自喷", "P[-_]ZP[-_]L",
                          "S_SPRL_VERT_PIPE（自喷立管）", "P-ZP1-VPIPE", "W-WSUP-COOL-PIPE", "W-VPIPE-ZP1", "WP_P",
                          "W-FRPT-SPRL-EQPM", "W-FRPT-HYDT-EQPM", "S_WSD_VERT_PIPE（给排水立管）", "P-ZP-VPIP-IDEN",
                          "P-ZP-VPIPE", "AUDIT_I_191225164800-20", "VPIPE-其它"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"IDEN"}) +
                           ["雨水斗", "编号", "NO\.", "^[^Vv]*PIPE", "^S-给水$", "P-雨水-EQPM", "S[-_]排水", "-P-废水管",
                            "P[-_]消防管[-_]PJ", "阀门", "立管定位", '^YCS_(.*)_配件$', "辅助"],
        },
        "hydrant_vpipe": {  # 消火栓立管
            "layer_sub": ["VPIPE[-_]FH", "S[-_]VPIPE[-_]XF", "PIPE[-_]RISR", "X[-_]L", "WP[-_]F[-_]LG",
                          "P[-_]XH[-_]VPIPE", "P[-_]HYDR[-_]VPIP", "S[-_]消防", "HUDR[-_]VERT", "消防管",
                          "VPIPE[-_]消防", "P[-_]XH[-_]VPIPE", "消火栓立管", "OP[-_]VPIPE[-_]FH", "P-XH-VPIP-IDEN",
                          "P[-_]HYDT[-_]PIPE", "HYDR[-_]VERT", "P[-_]HYDT[-_]RISR", "VPIPE[-_]FH", "VPIPE[-_]XF",
                          "消防", "P[-_]X[-_]L", "0XL", "Pipe[-_]Risr", "W-VPIPE-X", "W-FRPT-HYDT-EQPM", "消防管",
                          "P-XH-PIPE-VALVE", "S_WSD_VERT_PIPE（给排水立管）", "W-FRPT-HYDT-EQPM", "消火栓管"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"IDEN"}) +
                           ["雨水斗", "编号", "NO\.", "^[^Vv]*PIPE", "^S-给水$", "P-雨水-EQPM", "S[-_]排水", "-P-废水管",
                            "P[-_]消防管[-_]PJ", "立管定位", '^YCS(.*)_配件$', "辅助"],
        },
        "condensate_vpipe": {  # 冷凝水立管
            "layer_sub": ["P[-_]L", "LN", "P-LN", "P[-_]VPIPE[-_]凝结", "VPIPE[-_]凝结", "VPIPE[-_]CO", "S[-_]VPIPE[-_]NS",
                          "WP[-_]KTN[-_]LG",
                          "P[-_]KN[-_]VPIPE", "P[-_]HAVC[-_]VPIP", "S[-_]空调冷凝水", "COND[-_]VERT", "冷凝管",
                          "P-NS-VPIP-IDEN", "0P[-_]VPIPE[-_]CO", "冷凝", "冷凝水", "凝结", "P[-_]Y[-_]L", "P-KN-VPIPE",
                          "W-VPIPE-N", "W-RAIN-PIPE", "W-DRAI-EQPM", "VPIPE-压力雨", "S_WSD_VERT_PIPE（给排水立管）",
                          "P-VERP-CONW", "P-Pipe-Risr-Watr", "P-Pipe-Risr-Arch", "P-NS-VPIP-IDEN", "GPS-给排水立管",
                          "A-ROOF-WATER"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"IDEN"}) +
                           ["雨水斗", "编号", "NO\.", "^[^Vv]*PIPE", "^S-给水$", "P-雨水-EQPM", "S[-_]排水", "-P-废水管",
                            "P[-_]消防管[-_]PJ", "立管定位", "辅助"],
        },
        "ventilate_vpipe": {  # 通气立管
            "layer_sub": ["P[-_]VPIPE[-_]其他", "VPIPE[-_]其他", "VPIPE[-_]通气", "S[-_]VPIPE[-_]TQ", "WP[-_]T[-_]LG",
                          "P[-_]通气管立管", "P[-_]VENT[-_]VPIP", "S[-_]通气管", "AERATE[-_]VERT", "P-TQ-VPIP-IDEN", "通气管"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"IDEN"}) +
                           ["雨水斗", "编号", "NO\.", "^[^Vv]*PIPE", "^S-给水$", "P-雨水-EQPM", "S[-_]排水", "-P-废水管",
                            "P[-_]消防管[-_]PJ", "立管定位", "辅助"],
        },
        "vpipe": {  # 其他立管，不知道具体用途的立管
            "layer_sub": ["P-PS", "HC[-_]GPS", "WP[-_]P[-_]LG", "P[-_]PIPE[-_]RISR", "WSD[-_]VERT[-_]PIPE",
                          "VPIPE", "立管", "S[-_]EQUIPMENT", "VERT[-_]PIPE", "WATER", "^水$", "水管", "LG",
                          "EQPM[-_]PLUM", "EQUIP[-_]水", "EQPM[-_]PUMB", "0P[-_]ACC[-_]FD", "^A[-_]SAN$",
                          "S_WSD_VERT_PIPE（给排水立管）", "S_NON_VERT_PIPE（非立管）", "P-T-VPIPE", "VPIPE-通气",
                          "VPIPE-中水", "GPS-给排水立管", "P-Pipe-Risr-Watr", "_通气标注", "VPIPE-污水", "P-Pipe-Risr-Arch",
                          "P-RH-L", "DIM_MODI", "通气管", "W-DRAI-EQPM", "VPIPE-其它", "S-TQ-通气立管", "P-VERP-VENT",
                          "P-TQ-VPIP-IDEN", "P-T-L", "P-E-VPIPE", "CKL标注", "W-FRPT-HYDT", "W-DRAI-VENT-PIPE", "CKL标注",
                          "000原始墙体", "VPIPE-热回水"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"IDEN", "标注"}) +
                           ["雨水斗", "编号", "NO\.", "^[^Vv]*PIPE", "^S-给水$", "P-雨水-EQPM", "S[-_]排水", "-P-废水管",
                            "P[-_]消防管[-_]PJ", "雨水", "通气", "TQ", "VENT", "凝结", "冷凝", "COND", "FH", "XF", "HYDR",
                            "消防", "消火栓", "HYDT", "HYDR", "喷淋", "SPRL", "Risr", "雨水", "RAIN", "雨", "YS", "废水",
                            "DRAI", "WAST", "污水", "SW", "WS", "SEWR", "SEWE", "给水", "GS", "立管定位",
                            "P[-_]PS", "排污[-_]立管编号", "P[-_]WS", "DIM[-_]凝结", "P[-_]YS", '^YCS_(.*)_配件$'
                                                                                        "P[-_]J", "P[-_]JS", "辅助"],
        },
        "well": {  # 检查井
            "layer_sub": ["WELL", "室外雨水井"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "inspection_hole": {  # 检查口
            "layer_sub": ["EQUIP[-_].*水", "W[-_]EQUIP", "S[-_]EQUIP[-_]WS", "P[-_]WS[-_]PIPE", "废水管[-_]配件"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"])) + ['^YCS_(.*)_配件$'],
        },
        "rain_outlet": {  # 雨水斗
            "layer_sub": ["EQUP[-_]RAIN", "RAIN[-_]MISC", "屋面排水", "Pope[-_]Risr", "雨水斗", "EQUIP[-_]污水",
                          "P-雨水-EQPM", "P[-_]YS", "S[-_]EQUIP[-_]WS"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "sprayer": {  # 喷头
            "layer_sub": ["PT", "P-PT", "SPRW[-_]NOZL", "SPRN[-_]EQPM", "SPRL[-_]HEAD", "EQUIP[-_]喷淋", "喷头",
                          "自喷[-_]SPR",
                          "0P[-_]ACC[-_]NOZ", "P[-_]ZPPT[-_]EQUIP", "P[-_]SPRL[-_]HEAD", "P[-_]PT"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "tank": {  # 水箱
            "layer_sub": ["WTAN", "给排水设备", "水箱", "WATS[-_]EQUP"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "pressure_meter": {  # 压力表
            "layer_sub": ["VALVE[-_]消防", "水[-_]消防[-_]消火栓[-_]标识", "P[-_]HYDT[-_]ANNO", "0P[-_]VALVE[-_]H",
                          "0P[-_]VALVE[-_]FH", "S[-_]VALVE[-_]XF", "H消防管道", "X[-_]消防高[-_]MISC"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"道", "VALVE"}),
        },
        "sleeve": {  # 套管
            "layer_sub": ["VALV", "EQUIP[-_]管件", "WP[-_]F[-_]OTH", "P[-_]S[-_]CASI[-_]CONC", "P[-_]FS[-_]EQPM[-_]TEXT",
                          "VALVE[-_]压力废", "W_FU", '^YCS_(.*)_配件$'],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"VALVE"}) + ['P[-_]ZP', 'VALVE[-_]喷淋',
                                                                                 'YCS_给水管_4区_配件'],
        },
        # "地漏" 类
        "floor_drain": {  # 地漏
            "layer_sub": ["地漏", "drain", "板面留洞", "DRAI[-_]FLDR", "DRAL[-_]FLDR", "pipe[-_]risr$", "^water[-_]dl$",
                          "^0P[-_]ACC[-_]FD$", "^A[-_]SAN$", "P[-_]FS[-_]FD", "DL", "污水管_配件", "P-PS", "P[-_]FLDR"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "system_floor_drain": {  # 系统地漏
            "layer_sub": ["EQUIP[-_].*水", "EQUIP[-_]SW"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "fire_hydrant": {  # 消火栓
            "layer_sub": ["消火栓", "消防箱", "消防[-_]FH", "XHS", "HYDT[-_]BOX", "HYDT", "XHSX", "HYDRANT", "EQPM[-_]FIRE",
                          "HYDR", "^0P[-_]ACC[-_]FH$", "^0P[-_]EQUIP[-_]FH$", "FHBX", "FIRE[-_]FH", "灭火器",
                          "EQUIP[-_]消防", "P[-_]MH[-_]FEXT", "P[-_]消防管[-_]PJ", "FHYD", "EQUIP[-_]XF", "0XG[-_]X",
                          "MHQ", "消火箱", "消栓[-_]栓箱", "YCS[-_]消防管.*配件"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"线"}) +
                           ["立管", "PIPE", "阀门", "风管", "法兰", "风口", "消火栓标准", '^YCS_(.*)_配件$', "给水管线"],
        },
        "pump_connector": {  # 水泵接合器
            "layer_sub": ["WPUM", "VALVE", "WP[-_]F[-_]PJ", "EQUIP[-_]消防", "0P-EQUIP-FH", "S-EQUIP_XF", "S-室外消防管",
                          "P-Hydt-Equp", "EQUIP_消防", "P-XH-EQUIP", "P-SITE-HYDR-EQPM", "P_OUTD_WS_DIMS(室外给水管标注)",
                          "P-消火栓给水管线-附件", "s-消防", "PIPE-消防高", "PIPE-喷淋高", "PIPE-消防", "PIPE-喷淋",
                          "S_HYDT_PIPE（消火栓管）", "P-HUDR-SILO", "W-FRPT-HYDT-EQPM", "P-X", "OP-PIPE-FH", "OP-EQUIP-FH",
                          "WP_F_PJ", "WP_SP", "P-XH-EQPM-TEXT", "OP-EQUIP-FH", "PIPE-喷淋高", "PIPE-消防高", "PIPE-消防",
                          "P-Totl-Hydt-Equp", "S-EQUIP-XF", "H消防管道", "X-消防-MISC", "PIPE-消防", "W-FRPT-HYDT-PIPE",
                          "P-EQUIP_消防", "P-WATE-VPIP", "S_HYDT_PIPE（消火栓管一区）", "S_HYDT_PIPE（消火栓管）"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"VALVE"}) + ["VALVE[-_]压力废", "VALVE_废水",
                                                                                 "VALVE_凝结"],
        },
        "valve": {  # 阀门
            "layer_sub": ["VALV", "阀件", "阀门", "EQUIP[-_]阀门", "EQUIP[-_]ZP", "VALV[-_]Sprl",
                          "VALVE_喷淋", "S_SPRL_EQPM（自喷设备）", "W-FRPT-SPRL-EQPM", "喷淋阀门", "0-阀门", "P-ZP-VALVE",
                          "P-SB-TWT", "SZ-WZ", "_自喷标注", "S_MINI_EQPM（小型设备）", "VALVE_废水"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"VALVE"}) + ["VALVE[-_]压力废", "VALVE_污水", "VALVE_凝结",
                                                                                 "VALVE_废水"],
        },
        "exhaust_valve": {  # 排气阀门
            "layer_sub": ["W[-_]ZP自喷管", "WP[-_]G[-_]PJ"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "ventilation_cap": {  # 通气帽
            "layer_sub": ["W[-_]EQUIP", "EQUIP[-_]污水", "EQUIP[-_]SW", "EQUIP_通气", "EQUIP_SW", "P_排水管", "EQUIP_排水",
                          "P[-_]SPRK", "S[-_]废水立管", "-P-废水管", "FHYD", "P[-_]FS", "W[-_]W污水标注", "S[-_]Y雨水文字",
                          "S[-_]F废水管", "S[-_]W污水管", "S[-_]EQUIP[-_]FS", "S[-_]EQUIP[-_]WS", "S[-_]EQUIP[-_]YS",
                          "P[-_]WS[-_]EQPM.*TEXT"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"TEXT"}),
        },
        "kitchen_toilet": {  # 厨卫
            "layer_sub": ["厨卫", "LVTRY", "洁具", "FLOR[-_]SPCL", "FIXT", "SANR", "EQPM[-_]ASSI", "EQPM[-_]TOLT",
                          "Lavatory", "EQPM[-_]KICH", "^A[-_]SAN$", "标配部件[-_]厨房卫生", "EQPM[-_]TACC", "TPTN"],  # TPTN是洗浴器
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "furniture": {  # 家具
            "layer_sub": ["家具", "FURN", "Furniture", "furn", "EQPM[-_]MOVE", "EQPM[-_]FIXD", "Fixt", "FTMT[-_]MOVE",
                          "设备.*洗衣机", "设备.*冰箱", "A-FLOR-SANI"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "flow_indicator": {  # 水流指示器
            "layer_sub": ["VALVE[-_]喷淋", "VALVE[-_]S", "WP[-_]L[-_]PJ", "ZP[-_]VALVE"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"VALVE"}),
        },
        "water_meter": {  # 水表
            "layer_sub": ["VALVE[-_]给水", "阀门", "S-GSW", "P[-_]生活给水管线[-_]附件", "WP[-_]G[-_]PJ", "J[-_]给水[-_]MISC",
                          "S[-_]水表"],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"VALVE"}),
        },
        "overflow_level": {  # 溢流水位
            "layer_sub": ["TWT[-_]消防", "WP[-_]G"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "elevator_box": {  # 电梯厢/楼梯
            "layer_sub": ["EVTR", "Stair", "STAIR", "Lift", "LIFT", "电梯", "楼梯", "梯", "FIT", "ELEV", "elevator", "STRS",
                          "EQPM", "STAR", "轿厢", "STR$", "^A_equipment$"],  # STR-电梯厢256817
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"LINE"}) + ["SMAL", "BALC", "ELEC", "LIHT", "CLNG",
                                                                                "FIRE", "HYDR", "KICH", "ASSI",
                                                                                "MECH", "PLOM", "TOLT", "PRKG",
                                                                                "SYMB", "RAIL", "CAR", "车"],
        },
        "elevator_stair": {  # 电梯厢/楼梯（住宅平面图）
            "layer_sub": ['EVTR', 'Stair', 'STAIR', 'Lift', 'LIFT', '电梯', '楼梯', '梯', 'FIT', 'ELEV', 'elevator', 'STRS',
                          'EQPM', 'STAR'],
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"LINE"}) + ['SMAL', 'BALC', 'ELEC', 'LIHT', 'CLNG',
                                                                                'FIRE', 'HYDR', 'KICH', 'ASSI',
                                                                                'MECH', 'PLOM', 'TOLT', 'PRKG',
                                                                                'SYMB', "RAIL", "CAR", "车"],
        },
        "air_conditioner": {  # 空调
            "layer_sub": ["空调", "^空_$", "Aircontroe", "^AC$", "Aircondition", "EQPM[-_]MECH", "EQPM[-_]SMAL",
                          "M[-_]AC", "KT", "FLOR[-_]OVHD", "LA[-_]plan[-_]smal", "RS[-_]A", "^A[-_]AC$",
                          "A[-_]FLOR[-_]AIRC"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["洞", "孔", "水", "空调管", "标注$"],
        },
        # "air_conditioner_mix": {  # 家具图层，含有空调的混合图层
        #     "layer_sub": ["家具", "FURN", "Furniture", "furn", "EQPM[-_]MOVE", "EQPM[-_]FIXD", "Fixt"],
        #     "ignore_word": list(set(BASIC_IGNORE_WORDS['basic']) - {'家具'}),
        # },
        "door": {  # 门
            "layer_sub": ["WINDOW", "DOOR", "门", "D&W", "W&D", "WIN", "DOWI"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立面门窗", "人防", "0-DOOR\.T", "WINDOW[-_]BLIN", "开启范围", "阀门"],
        },
        "window": {  # 窗户
            "layer_sub": ["WINDOW", "WIN", "窗", "DRWD", "WIND", "Window", "D&W", "W&D", "L[-_]玻璃", "DOWI", "dowi",
                          "0A[-_]B[-_]GLAZ", "百叶", "CHUANG"],  # 0A-B-GLAZ-255679
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立面门窗", "WINDOW[-_]BLIN", "0A[-_]B[-_]GLAZ[-_]OPEN"],
        },  # GLAZ-255679
        "elevator_door": {  # 电梯门
            "layer_sub": ["WINDOW", "WIN", "DOOR", "门", "DRWD"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["立面门窗", "0-DOOR\.T", "WINDOW[-_]BLIN", "人防", "开启范围"],
        },
        "emergency_door": {  # 人防
            "layer_sub": ["WINDOW", "WIN", "door", "门", "人防"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] +
                           ["分区", "0-DOOR\.T", "WINDOW[-_]BLIN", "开启范围", "人防集水坑"],
        },  # 过滤人防分区
        "wall": {  # 墙
            "layer_sub": ["wall", "墙", "侧壁", "0[-_]结构", "0[-_]现浇混凝土", "CONC", "WAL", "STRU", "W[-_]LINE",
                          "^C[-_]1$", "C-L"],  # STRU-249183 & 249178
            "ignore_word": list(set(BASIC_IGNORE_WORDS["basic"]) - {"线", "LINE"}) +
                           ["COLS", "墙柱", "挡墙", "外墙轮廓", "STRU[-_]MATE", "P[-_]S[-_]CASI[-_]CONC",
                            "集水坑", "HOLE", "^A-WALL-INSL$", "A_SIGN_STRU", "降板线", "P[-_]结构孔洞[-_]穿墙", "轴线"],
        },  # 经业务确定，对"wall"构件，忽略关键字中删除"线"，1530 - wall-虚线
        "pillar": {  # 柱子
            "layer_sub": ["柱", "COLU", "COLUMN", "COLS", "S[-_]Col", "S[-_]Col[-_]hatch", "S[-_]WC", "CLOS"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["柱帽", "填充"],
        },
        "wall_hatch": {
            "layer_sub": ["填充", "HATCH"],
            "ignore_word": []
        },
        "segment": {  # 住宅平面空间识别图层
            "layer_sub": ["FLOR", "栏杆", "BALCONY", "HANDRAIL", "阳台", "Rail",
                          "HRAL", "blcn", "0425[-_]致逸结构", "surface", "SURFACE",
                          "外包石材", "HEAT", "SILL", "空调板", "OVER", "Hdrl",
                          "0A[-_]P[-_]ROOF", "AE[-_]FNSH", "A[-_]VISI", "HANDRA"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + [
                "SPCL", "OVHD", "FURN", "SPCL", "OVHD", "FURN", "BORD", "FLUE", "FLOR[-_]PLAN", "GRND", "TPTN", "IDEN",
                "LEVL", "SHFT", "SIGH", "WDWK", "PATT", "CASE", "GRID", "FTMT", "STAIR", "MOVE", "家具", "Fixt",
                "A[-_]Flor[-_]Path", "A[-_]FLOR[-_]FURN", "AE[-_]FLOR", "A[-_]FLOR[-_]PARK", "A[-_]FLOR[-_]EVTR",
                "A[-_]FLOR[-_]STR", "DRAN", "P[-_]FLOR", "A-FLOR.*边缘", "A-FLOR-STAR", "FLOR-EVTR", "FLOR-STAIR",
                "S-FLOR_ZM", "A-FLOR-LOOK", "A-FLOR-DRAI", "A-FLOR-SANI", "A[-_]FLOR[-_]AIRC", "集水坑"]
        },  # FLOR-HRAL - 阳台的边界
        "segment_extra": {  # 住宅平面空间分割需要用到但不常用的图层, 若广泛测试后没有问题可以放到segment中
            "layer_sub": ["0S[-_]C[-_]LINE", "0S[-_]CC[-_]LINE", "A[-_]LIN", "^造型线$", "A[-_]HDWR",
                          "AR_LINE"],
            "ignore_word": [],
        },
        "segment_underground": {  # 地下室空间识别
            "layer_sub": ["wall", "pillar", "door", "栏", "HANDRAIL", "Rail", "HRAL",
                          "SYMB", "PD", "坡道", "车流线", "车道中线", "行车方向", "AE[-_]DICH[-_]STRU",
                          "地下室墙柱线", "FLOR", "CON", "TY", "WATER", "排水", "水沟", "水井",
                          "水坑", "GUTT", "WELL", "GLASS", "Stair", "STAIR", "Hole", "SUMP",
                          "FZ", "水管井", "AE[-_]STAR"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["TEXT", "AXIS", "字", "编号", "标号", "名", "NAME", "AD[-_]NUMB",
                                                          "尺寸", "道", "增补", "VALVE", "IDEN", "窗沿", "家具", "索引",
                                                          "配件", "洞口", "GUTT", "SUMP", "PARK", "0-DOOR\.T"],
        },
        "lobby_platform_border": {  # 规则523、535中用到的大堂外的 "入口平台" 区域
            "layer_sub": ["^fit$", "A-P-FLOR"],
            "ignore_word": [],
        },
        "annotation_line": {  # 引线图层
            "layer_sub": ["DIM", "IDEN", "ANNO", "SYMB", "LEAD", "0[-_]坐标标注", "NO\..*编号", "TEXt", "-TEXT",
                          "F-废水-TEXT", "W-污水-TEXT", "YT-阳台雨-TEXT", "污水文字", "废水文字", "雨水文字", "凝结水文字",
                          "通气文字", "P-负一层消火栓标准", "P[-_]生活污水管线[-_]注释", "A[-_]INDEX",
                          "YCS[-_]通气管[-_]立管标注", "标注$", "编号$"],
            "ignore_word": ["PUB", "标高", "红线", "流线", "坐标", "尺寸", "中线", "ELEV", "^TWT[-_]SYMB$", "FROM",
                            "FORM", "GRID", "A-COND-IDEN-TEXT", "LEVL", "LEVEL", "P[-_]FS[-_]EQPM[-_]TEXT",
                            "A[-_]DIM[-_]AXIS", "P[-_]WS[-_]EQPM.*TEXT", "A[-_]ANNO[-_]NOTE", "A[-_]ANNO[-_]DIMS",
                            "TWT_DIM"],
        },
        "elevation_symbol": {  # 标高符号（目前主要使用的是建筑专业中的"标注"图层）
            "layer_sub": ["标高", "ELEV", "LEVL", "TWT[-_]TITLE", "TWT_DIM", "S－GG公共标注", "PUB_DIM", "层高线", "楼层线"],
            "ignore_word": ["^地面标高$"],
        },
        "building": {  # 总平图的空间轮廓的图层
            "layer_sub": [
                'DESG设计建筑', '建筑首层', '建筑轮廓', 'ROOF-WALL', '外墙轮廓', 'BULD-BMAX', '空墅', 'BUID', '商业轮廓线',
                '设计建筑', 'BLDG-FACILIT', 'Wall', 'WALL', '屋顶轮廓', 'SITE-BLDG', 'OUTD-BUID', 'COLUMN', 'WINDOW',
                "WIN", 'A-Wind', 'A-Blcn', 'PLAN_建筑基底轮', 'JZW_Close', 'AUDIT_I_12', '总图外墙', '箱变', '建筑标准层轮廓',
                '建筑屋顶平面', 'DOOR_FIRE', '建构筑物轮廓线', '建筑标准层', '^0-建筑$', '规划建筑', '现状建筑', 'P-BULD-BMAX',
                '住宅建筑', 'A_HDWR(配件)', 'A_FLOR[（(]边缘[)）]', 'BD-主体', '新建建筑', 'A-EQPM-MECH', '建筑主轮廓',
                'Z_0_EXST[（(]现有建筑[)）]', 'G_COL', 'Z-0-ZBW', '00-共用-建筑轮廓加粗', '^总图$', '^轮廓$', '3T_WOOD',
                'TWT[-_]室外',
            ],  # 云效250244的燃气调压箱，云效250537的住宅，云效249538的住宅，云效249538的住宅，'1*F'去掉
            "ignore_word": [
                "CONC", "DIM", "HATCH", "LANDSCAPE", "ELEV", "HIGH", "NUMB", "人防范围", "地下构筑物", "挡土墙", "用地红线",
                "景观", "TEXT", "YARD", "HATH", "COOR", "坐标", "AXIS", "HACH", "填充", "尺寸", "DIMS", "AXIS", "编号",
                "标号", "名", "NAME", "AD-NUMB", "尺寸", "道", "增补", "VALVE", "LINE", "IDEN", "窗沿", "DIM", "家具",
                "索引", "UDBD", "LIMT", "STAR", "DWALL", "WALL_JG", "PARAPET", "WINDOW[-_]BLIN"],
        },
        "road": {  # 道路边线 - 不包含车道中心线，另外消防车道的图层也包含这里面
            "layer_sub": ["ROAD", "车道", "道路", "车行道", "消防扑救面", "HHDZ-0-市政", "RD", "园区车型路", "消防路"],
            "ignore_word": ["Center", "流线", "坐标", "尺寸", "标注", "登高", "CURB", "CENT", "CNTR", "中线", "坡道",
                            "标高", "红线", "定位", "元素", "中心", "AXIS"],
        },
        "road_center_line": {  # 道路中心线 - 规则528
            "layer_sub": ["路.*中心线", "RD.*中心线", "ROAD.*中心线", "路.*中线", "RD.*中线", "ROAD.*中线",  # 中心线类型
                          "园区车型路",
                          "ROAD.*AXIS", "RD.*AXIS",  # axis类型
                          "ROAD.*CENT", "RD.*CENT", "RD.*CNTR", "ROAD.*CNTR",  # center类型
                          "路.*流线", "流线.*路"],  # 流线类型
            "ignore_word": [],
        },
        "parking": {  # 车位
            "layer_sub": ["PARK", "park", "车位", "Car", "CAR", "车", "car",
                          "AE-EQPM", "PRKG", "快充", "慢充", "无障碍", "泊位",
                          "pkng", "che", "A-Pkng-Vhel-Mini", "A-1-Pkng"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["轮廓", "DRIV", "CURB", "自行车", "绿地"],
        },
        # 1206新增给排水图层
        "water_test_epuip_end_plan": {  # 末端试水装置（平面）
            "layer_sub": ["W[-_]LGBH", "喷淋", "0P[-_]VALVE[-_]SS[-_]SPRL[-_]NOTE.*自喷文字说明", "柱帽",
                          "S[-_]SPRL[-_]PIPE.*自喷管", "VALVE[-_]废水", "给排水图层", "P[-_]VALVE[-_]废水",
                          "P[-_]SEWR[-_]VALVE", "P[-_]HYDT[-_]ANNO", "VALVE[-_]喷[-_]PIPE[-_]给水",
                          "VALVE", "WAST-VALV", "SPRL[-_]EQPM", "阀门", "VALVE_污水", "WW_F_PJ", "W-VALVE_ZP",
                          "W-FRPT-NOTE", "P-ZP-VALVE", "P-ZP-EQPM-TEXT", "CKL标注", "_自喷管径标注"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "water_test_epuip_end_system": {  # 末端试水装置（系统）
            "layer_sub": ["0P[-_]VALVE[-_]S", "S[-_]MINI[-_]EQPM.*小型设备", "P[-_]VALVE给水", "VALVE[-_]喷淋",
                          "VALVE[-_]消防", "P[-_]DOMW[-_]VALV", "HC[-_]F", "P[-_]SPRL[-_]PJ", "S[-_]GJ", "A8",
                          "P[-_]SPRI[-_]KLER", "P[-_]SPRN[-_]VALV", "P[-_]XF", "VALVE", "给水", "喷淋",
                          "-water", "市政阀门", "P-J-EQUIP", "_标注", "喷头", "WP_L", "S-ZP", "S_SPRL_EQPM（自喷设备）",
                          "S_SPRL（自喷喷头）", "P-ZP-PIPE", "P-VALVE_喷洒", "P-Sprl", "P-FE-FS-E", "LGBH_P", "FM",
                          "DLYQ2", "0s-水标注", "_消火栓标注", "0P-VALVE-CW", "EQUIP_阀门", "Equip", "S-辅助线", "Zp",
                          "GJ-阀门"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["地漏"],
        },
        "water_pit": {  # 集水坑
            "layer_sub": ["集水坑", "0P[-_]A[-_]DIM", "集水井", "SUMP", "S[-_]MINI[-_]EQPM.*小型设备", "TK", "P[-_]STRT",
                          "EQUIP[-_]污水", "P[-_]EQPM", "A[-_]DRAIN", "0P[-_]WELL[-_]WW", "EQPM[-_]PUMB",
                          "WELL[-_]WW", "RF[-_]坑", "P[-_]J[-_]EQPM", "AE-EQPM", "排水管", "排水组织", "排水沟",
                          "AE-DICH-STRU", "Bsmt_drain", "STELL"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["CARS", ],
        },
        "water_test_valve_end": {  # 末端试水阀
            "layer_sub": ["W[-_]FRPT[-_]SPRL[-_]EQPM", "0P[-_]VALVE[-_]S", "S[-_]SPRL[-_]NOTE.*自喷文字说明",
                          "0P[-_]VALVE[-_]S", "VALVE[-_]喷淋", "SSSSSSS", "S[-_]SPRL[-_]PIPE.*自喷管", "给排水图层",
                          "P[-_]WATS[-_]ANNO", "EQUIP[-_]污水", "P[-_]SEWR[-_]VALVE", "P[-_]WAST[-_]VALV",
                          "W-VALVE_ZP", "VPIPE-喷淋", "S_SPRL_EQPM（自喷设备）", "P-ZP-VALVE", "_自喷管径标注", "PIPE-废水",
                          "P-Wast-VALV"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "clean_hole": {  # 清扫口
            "layer_sub": ["EQUIP[-_]污水", "S[-_]DRAI[-_]PIPE.*污水管", "WS[-_]污水管线及标注[-_]W", "P[-_]VALVE[-_]污水",
                          "P[-_]SEWR[-_]ANNO", "0P[-_]VALVE[-_]SW", "0P[-_]EQUIP[-_]SW", "雨水", "P[-_]Y[-_]EQPM",
                          "VALVE_污水", "P-P", "P-EQUI-LDRA", "S-XXSB", "P-Sewr", "P-WS-EQPM+TEXT", "P-W-VALVE",
                          "VALVE_废水", "S_MINI_EQPM（小型设备）", "EQUIP_喷淋", "S_DRAI_FLDR（地漏）", "P-W-EQUIP",
                          "WP_P_PJ", "_污水标注", "水管[-_]其他"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["污水管_配件", 'VPIPE[-_]雨水'],
        },
        "overflow_hole": {  # 溢流口
            "layer_sub": ["LABEL[-_]PM", "P[-_]废水管", "A[-_]EQPM[-_]PLUM", "雨水", "SSSS", "0栏杆金属",
                          "P[-_]RAIN[-_]MISC", "屋面排水", "A[-_]EQPM[-_]PUMB", "水", "MINI[-_]EQPM", "P[-_]Stru",
                          "a[-_]LINE", "套管", "P[-_]Y[-_]EQPM", "S_WSD_VERT_PIPE（给排水立管）", "P-Y-DIM",
                          "S_WSD_CANNULA（给排水套管）", "排水、A_FLOR_DICH(建筑沟)", "0-C-屋面排水", "WINDOW",
                          "A-Detl-Thin", "W-RAIN-EQPM", "TWT_TEXT", "DRAI-FLOO", "溢流口", "WP_G", "W-DIM_Y",
                          "VPIPE-给水", "TWT_LEAD", "P-YS-EQPM-TEXT", "P-PIPE-RAIN", "MINI_EQPM（小型设备）",
                          "LVTRY、GPS-给排水标注", "EQUIP_雨水斗", "EQUIP_污水", "A-ROOF-SYMB", "A-FLOR-SYMB",
                          "AE-HOLE", "A_SYMB_DRCT(坡向线)", "AUDIT_I_190504173438-15", "wx_j", "SYMB_排水_A", "A-BALCONY",
                          "S_HOLE_BUIL（建筑留洞）", "WP_Y", "FLX00LP3_W10-10#t3", "EQUIP_给水", "平面-保温", "0P-ACC-RD:"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "fire_hydrants_outdoor_siteplan": {  # 室外消火栓（总图）
            "layer_sub": ["0P[-_]ACC[-_]FH", "P[-_]OUTD[-_]WS[-_]WELL.*室外给水阀门井", "EQUIP[-_]消防",
                          "P[-_]XH[-_]EQUIP", "P[-_]GEN[-_]FIT", "P[-_]HYDT[-_]BOXX", "P[-_]HYDR[-_]BOX", "P[-_]J",
                          "0P[-_]ACC[-_]FH", "EQUIP[-_]FH", "EQUIP[-_]XF", "给水", "消防", "消火栓", "P[-_]J",
                          "W-EQUIP_XHS", "P-XH-FHYD", "W-WSUP-EQPM", "W-FRPT-HYDT", "A-W-XH", "P-Totl-Hydt-Equp",
                          "P-XHS-EQUIP"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"] + ["消防登高场地"],
        },
        "rain_well": {  # 雨水井
            "layer_sub": ["W[-_]RAIN[-_]EQPM", "TWT[-_]IDEN", "雨水井", "P[-_]RAIN[-_]NOTE", "P[-_]Y[-_]J",
                          "TEXT[-_]雨水", "DIM[-_]雨水", "雨水", "DIM[-_]污水", "P[-_]Y[-_]J", "W-DIM_W、W_LGBH",
                          "W-DRAI-NOTE", "P-YS-EQPM-TEXT", "W-DRAI-EQPM", "P-Y-DIM", "CKL标住", "0SP、P-KN-DIM", "水字"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "system_sprayer": {  # 喷头系统
            "layer_sub": ["EQUIP[-_]喷淋", "W[-_]FRPT[-_]SPRL[-_]EQPM", "0P[-_]ACC[-_]NOZ", "文字", "X[-_]PL[-_]GJ",
                          "P[-_]SPRK[-_]HEAD", "P[-_]SPRL[-_]PJ", "喷头", "P[-_]SPRL[-_]ANNO", "A6", "P[-_]SPRI[-_]KLER",
                          "HC[-_]ZP[-_]S", "X[-_]PL[-_]GJ", "EQUIP[-_]ZP", "喷淋", "P[-_]ZP[-_]EQPM", "WP_L_PJ",
                          "W-FRPT-SPRL-EQPM", "P-ZP-SPRA", "P-ZPPT-EQUIP", "P-Sprl-Sprl", "P-FE-FS-E", "P-EQUIP_喷洒",
                          "LGBH_P", "L3", "FM", "BG", "0S-消防配件", "_消火栓标注", "-附件", "J-EL_104", "Equip", "S-辅助线",
                          "Zp", "P-WatS-Anno"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "underground_building": {
            "layer_sub": ["JZW_地下车库轮廓线", "2-地下车库"],
            "ignore_word": []
        },
        "fire_compartment_sketch_contour": {  # 防火分区示意图轮廓线
            "layer_sub": ["0A[-_]P[-_]FIRE", "防火分区", "轮廓", "分区线", "A[-_]ZP[-_]地下室轮廓",
                          "A[-_]AREA[-_]FIRE", "SPACE[-_]ALL", "AE[-_]FLOR", "分区[-_]防火", "SURFACE", "S-GG-图名图号",
                          "PUB_TAB", "P-01-JZ", "F-line", "FIRE-ZONE", "A-FLOR", "AD-AREA-OUTL", "P-标注",
                          "A_WALL_BRIK(砌块墙)", "A-Fire-Bdry", "-人防建筑区"],
            "ignore_word": BASIC_IGNORE_WORDS["basic"],
        },
        "arrow": {  # 箭头
            "layer_sub": ["DIM", "SYMB", "ANNO", "符号标注", "AD-SIGN", "DIM[-_]SYMB", "A[-_]ANNO[-_]SYMB",
                          "0A[-_]A[-_]SYMB", "A[-_]Anno[-_]Dims", "箭头", "A[-_]Index.*建筑索引线剖切号线", "坡向线",
                          "A[-_]3[-_]Symb", "A[-_]TEXT", "G[-_]ANNO[-_]INDX", "A[-_]ANNO[-_]IDEN", "A[-_]FLOR[-_]STRS",
                          "A_SIGN_ARRO(上下行箭头线)", "A_SYMB_DRCT(坡向线)", "AD-SIGN", "A-INDEX", "A-注释-符号"],
            "ignore_word": ["PUB", "标高", "红线", "流线", "坐标", "尺寸", "中线", "ELEV", "^TWT[-_]SYMB$", "FROM",
                            "FORM", "GRID", "A-COND-IDEN-TEXT", "LEVL", "LEVEL", "P[-_]FS[-_]EQPM[-_]TEXT",
                            "A[-_]DIM[-_]AXIS", "A[-_]ANNO[-_]NOTE", "A[-_]ANNO[-_]DIMS"],
        },
        "relief_valve": {  # 减压阀
            "layer_sub": ["^0[-_]给排水$", "^YCS[-_]喷洒管[-_]配件$"],
            "ignore_word": []
        },
        "relief_valve_and_hpipe": {  # 减压阀和生活给水横管混合图层
            "layer_sub": ["^P[-_]J[1-9]$"],
            "ignore_word": []
        },
        "alarm_valve_and_hpipe": {  # 报警阀和喷淋横管混合图层
            "layer_sub": ["^-其他立管$", "^VALVE[-_]喷淋$"],
            "ignore_word": []
        },
        "hpipe_vpipe_annotation": {  # 其他横管、立管、引注混合图层（其他混合）
            "layer_sub": ["标注[-_]立管", "P[-_]PS", "P[-_]FS", "排水"],
            "ignore_word": ["排水地漏"]
        },
        "wall_floor_line": {  # 为了获取floor_line_list图元
            "layer_sub": [".*"],
            "ignore_word": []
        },
        "faucet": {
            "layer_sub": ['EQUIP_给水', 'P-EQUIP-CW', '给水设备', 'Y_COMM_EQPM', 'P-DOMW-EQPM', 'P[-_]RC[-_]EQUP'],
            "ignore_word": []
        },

    }

    BASIC_LAYERS = {
        "basic": ["wall", "border"],
        "indoor_segment": ["wall", "pillar", "segment", "segment_extra"],  # 去掉了 border
        "underground_segment": ["wall", "pillar", "segment"],  # 去掉了 border
        "building_segment": ["building", "door", "window"],

    }

    COMBINATION_EXCLUDE_LAYERS_INDOOR = [
        "wall", "segment", "pillar", "mentou", "wall_hatch", "hatch", "second_third_space", "pipe_barrier",
        "hatch_outline", "text_with_bound_vertex", "annotation_line", "lobby_platform_border", "segment_underground",
        "segment_extra", "overflow_level", "text", "cold_life_supply_hpipe", "hot_life_supply_hpipe", "hydrant_hpipe",
        "sprinkler_hpipe", "inflow_hpipe", "sewage_hpipe", "waste_hpipe", "rain_hpipe", "condensate_hpipe",
        "ventilate_hpipe", "rain_recycle_supply_hpipe", "solid_wall_line", "non_solid_wall_line", "mleader",
        "waste_hpipe_short", "hydrant_hpipe_short", "sprinkler_hpipe_short", "cold_life_supply_hpipe_short",
        "sprinkler_hpipe_short", "wall_floor_line"
    ]

    COMBINATION_EXCLUDE_LAYERS_UNDERGROUND_AND_SITEPLAN = [
        "wall", "podao", "separator", "filling", "road", "car_lane", "hatch", "red_line", "red_line_sub",
        "building", "underground_building", "podao_extra", "podao_mark", "podao_edge", "overflow_level", "text",
        "hatch_outline", "text_with_bound_vertex", "annotation_line", "segment_underground", "inflow_hpipe",
        "cold_life_supply_hpipe", "hot_life_supply_hpipe", "hydrant_hpipe", "sprinkler_hpipe", "segment",
        "sewage_hpipe", "waste_hpipe", "rain_hpipe", "condensate_hpipe", "ventilate_hpipe", "segment_extra",
        "rain_recycle_supply_hpipe", "solid_wall_line", "non_solid_wall_line", "mleader",
        "waste_hpipe_short", "hydrant_hpipe_short", "sprinkler_hpipe_short", "cold_life_supply_hpipe_short",
        "sprinkler_hpipe_short", "wall_floor_line"
    ]

    CLASSIFICATION_EXCLUDE_LAYERS = [
        "wall", "pillar", "special_pillar", "segment", "podao", "podao_extra", "separator", "filling",
        "pillar_line", "road", "car_lane", "red_line", "red_line_sub", "building", "elevation_handrail",
        "mentou", "underground_building", "wall_hatch", "podao_mark", "structure", "elevation_window_exclude",
        "hatch", "podao_edge", "pipe_barrier", "hatch_outline", "wall_line", "text_with_bound_vertex",
        "annotation_line", "lobby_platform_border", "segment_underground", "segment_extra", "overflow_level",
        "text", "cold_life_supply_hpipe", "hot_life_supply_hpipe", "hydrant_hpipe", "sprinkler_hpipe",
        "inflow_hpipe", "sewage_hpipe", "waste_hpipe", "rain_hpipe", "condensate_hpipe", "ventilate_hpipe",
        "parking_contour_dict", "road_center_line", "rain_recycle_supply_hpipe", "solid_wall_line",
        "non_solid_wall_line", "mleader", "waste_hpipe_short", "hydrant_hpipe_short", "sprinkler_hpipe_short",
        "cold_life_supply_hpipe_short", "sprinkler_hpipe_short", "wall_floor_line"
    ]

    # 分图层打印配置
    INDOOR_DRAWING_PRINT_LAYER_SEPARATE_SET = {
        'set_1': ['vpipe', 'floor_drain', 'system_floor_drain', 'door', 'elevator_door', 'window', 'air_conditioner'],
        'set_2': ['floor_drain_mix', 'furniture', 'fire_hydrant', 'elevator_box', 'rain_outlet'],
        'set_3': ['vpipe', 'life_supply_vpipe', 'sewage_vpipe', 'waste_vpipe', 'rain_vpipe', 'sprinkler_vpipe',
                  'hydrant_vpipe', 'condensate_vpipe', 'floor_drain', 'ventilate_vpipe', 'fire_hydrant',
                  'kitchen_toilet', 'furniture', 'elevator_box', 'elevator_stair', 'air_conditioner'],
        'set_4': ['window', 'elevator_door', 'door', 'emergency_door', 'wall', 'pillar', 'elevation_window'],
    }

    # 不会用函数get_hyper_layer进行匹配的图层
    MATCH_EXCLUDE_LAYERS = ["podao_extra", "podao_mark", "podao_edge", "pipe_barrier"]

    # 存在斜线的图层，（需要对像素坐标进行特殊处理，确保能真实反映图纸上的线段走势） add by yanct01 2020-5-16
    # 处理结果，保存到一个新的逻辑层 ： 原图层名 + '_line'
    LAYERS_WITH_SLOPE_LINE_SUFFIX = '_line'
    LAYERS_WITH_SLOPE_LINE = ['wall', 'pillar', 'red_line', 'red_line_sub']
    LAYERS_WITH_SLOPE_LINE_REVISED = [x + '_line' for x in LAYERS_WITH_SLOPE_LINE]
    # 对于线型是虚线的墙线，单独保存
    DASH_LINE_SUFFIX = '_dash'
    DASH_LINE_REVISED = [x + '_dash' for x in LAYERS_WITH_SLOPE_LINE_REVISED]

    # "给排水构件" 与 "图层" 的对应关系
    GEIPAISHUI_ENTITY_LAYER_MAP = {
        # "排水横管" 类
        "排水横管": ["sewage_hpipe", "waste_hpipe", "rain_hpipe", "condensate_hpipe"],
        "污水横管": ["sewage_hpipe"],
        "废水横管": ["waste_hpipe"],
        "雨水横管": ["rain_hpipe"],
        "空调冷凝水横管": ["condensate_hpipe"],
        # "给水横管" 类
        "给水横管": ["cold_life_supply_hpipe", "hot_life_supply_hpipe", "hydrant_hpipe", "sprinkler_hpipe"],
        "生活给水横管": ["cold_life_supply_hpipe", "hot_life_supply_hpipe"],
        "冷水横管": ["cold_life_supply_hpipe"],
        "热水横管": ["hot_life_supply_hpipe"],
        "消火栓横管": ["hydrant_hpipe"],
        "喷淋横管": ["sprinkler_hpipe"],
        "进水横管": ["inflow_hpipe"],
        # "其他横管" 类
        "通气横管": ["ventilate_hpipe"],
        # "立管" 类
        "所有立管": ["vpipe", "life_supply_vpipe", "sewage_vpipe", "waste_vpipe", "rain_vpipe", "sprinkler_vpipe",
                 "hydrant_vpipe", "condensate_vpipe", "ventilate_vpipe", "hpipe_vpipe_annotation", "balcony_rain_vpipe"],
        "生活给水立管": ["life_supply_vpipe"],
        "污水立管": ["sewage_vpipe"],
        "废水立管": ["waste_vpipe"],
        "雨水立管": ["rain_vpipe", "balcony_rain_vpipe"],
        "喷淋立管": ["sprinkler_vpipe"],
        "消火栓立管": ["hydrant_vpipe"],
        "冷凝水立管": ["condensate_vpipe"],
        "通气立管": ["ventilate_vpipe"],
        "其他立管": ["vpipe"],
        "其他混合": ["hpipe_vpipe_annotation"],
        # "厨卫" 类
        "马桶": ["kitchen_toilet"],
        "淋浴器": ["kitchen_toilet"],
        "洗手盆": ["kitchen_toilet"],
        # "阀门" 类
        "排气阀": ["valve"],
        "报警阀": ["valve"],
        "系统报警阀": ["valve"],
        "信号阀": ["valve"],
        "阀门": ["valve"],
        "截止阀": ["valve"],
        "排气阀门": ["exhaust_valve"],
        # "消火栓" 类
        "灭火器": ["fire_hydrant"],
        "消火栓": ["fire_hydrant"],
        "消火栓-给排水": ["fire_hydrant"],
        # "雨水斗" 类
        "雨水斗侧排": ["rain_outlet"],
        "雨水斗全排": ["rain_outlet"],
        "雨水斗": ["rain_outlet"],
        # "地漏" 类
        "地漏": ["floor_drain"],
        "系统地漏": ["system_floor_drain"],
        # 其他类
        "水泵接合器": ["pump_connector"],
        "检查口": ["inspection_hole"],
        "检查井": ["well"],
        "通气帽": ["ventilation_cap"],
        "水箱": ["tank"],
        "水表": ["water_meter"],
        "压力表": ["pressure_meter"],
        "水流指示器": ["flow_indicator"],
        "喷头": ["sprayer"],
        "溢流水位": ["overflow_level"],
        "洗衣机": ["furniture"],
        "套管": ["sleeve"],
        "标高构件": ["elevation_symbol"],
        # 1206新增给排水图层
        "末端试水装置-平面": ["water_test_epuip_end_plan"],
        "末端试水装置-系统": ["water_test_epuip_end_system"],
        "集水坑": ["water_pit"],
        "末端试水阀": ["water_test_valve_end"],
        "清扫口": ["clean_hole"],
        "溢流口": ["overflow_hole"],
        "室外消火栓-总图": ["fire_hydrants_outdoor_siteplan"],
        "雨水井": ["rain_well"],
        "喷头系统": ["system_sprayer"],
        "减压阀": ["relief_valve", "relief_valve_and_hpipe"],
    }
