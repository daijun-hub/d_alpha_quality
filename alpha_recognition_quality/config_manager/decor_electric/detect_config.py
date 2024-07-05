from enum import Enum
from ...config import getenv


class DetectType(Enum):
    # ENUM = MODEL_NAME
    PEIDIANXIANG_SYSTEM_PEIDIANXIANGZITU = "vanke_electric_space_det_pdxzt"
    PEIDIANXIANG_SYSTEM_ENTITY = "electric_pdx_chuxianhuilu"
    # PEIDIANXIANG_SYSTEM_ENTITY = "vanke_electric_entity_det_pdxxt"
    ZHAOMING_ENTITY = "decor_elec_indoor_entity_det_all_room"
    # INDOOR_KITCHEN = "decor_arch_indoor_entity_det_kitc"
    # INDOOR_BALCONY = "decor_arch_indoor_entity_det_balc"


class DetectConfig:
    MODEL_CLASS = {
        DetectType.PEIDIANXIANG_SYSTEM_PEIDIANXIANGZITU: [
            "background",  # 背景
            "peidianxiangzitu",  # 配电箱子图
        ],
        DetectType.PEIDIANXIANG_SYSTEM_ENTITY: [
            "circuit_breaker",
            "electricity_meter",
            "peidianxiang_outlet_branch",
            "switch_double",
            "contactor",
            "thermorelay",
            "load_switch",
            "residual_current_circuit_breaker",
            "surge_protector",
            "Isolation_switch",
            "Integrated_circuit_breaker",

        ],
        # DetectType.ZHAOMING_ENTITY: [
        #     "socket",  # 插座
        #     "flat_switch",  # 平面图开关
        #     "phone", # 可视对讲
        #     "strong_electric_box", # 强电箱
        #     "weak_electric_box", # 弱电箱
        #     "equipotential_junction_plate", # 等电位
        # ],
        DetectType.ZHAOMING_ENTITY: [
            "socket", # cha zuo, 0
            'flat_switch', # kai guan, 1
            "visual_intercom", # ke shi dui jiang, 2
            'strong_electric_box', # qiang dian xiang, 3
            'weak_electric_box', # ruo dian xiang, 4
            'equipotential_junction_plate', # deng dian wei, 5
            # "flat_switch",
            # "emergency_single_tube_lamp",
            # "distribution_box",
            # "socket",
            # "single_tube_lamp",
            # "lamps",
            # "double_tube_lamp",
            # "evacuation_signs",
            # "emergency_lighting",
            # "floor_indicator_light",
            # "emergency_double_tube_lamp",
            # "yinxiaxian",
            # "broadcast",
            # "smoke",
            # "light_alarm",
            # "fire_button",
            # "button",
        ]
        # DetectType.INDOOR_KITCHEN: [
        #     "gas_meter",  # 燃气表
        #     "heater",  # 热水器
        # ],
        # DetectType.INDOOR_BALCONY: [
        #     "gas_meter",
        #     "heater",
        # ],
    }

    LABEL_MAP = {  # 检测标签和分类标签之前的映射
        # DetectType.ZHAOMING_ENTITY: {
        #     "flat_switch": "flat_switch",
        #     "socket": "socket",
        #     "phone": "phone",
        #     "strong_electric_box": "strong_electric_box",
        #     "weak_electric_box": "weak_electric_box",
        #     "equipotential_junction_plate": "equipotential_junction_plate",
        # },
        DetectType.ZHAOMING_ENTITY: {
            "socket": "socket",  # cha zuo, 0
            'flat_switch': 'flat_switch',  # kai guan, 1
            "visual_intercom": "visual_intercom",  # ke shi dui jiang, 2
            'strong_electric_box': 'strong_electric_box',  # qiang dian xiang, 3
            'weak_electric_box': 'weak_electric_box',  # ruo dian xiang, 4
            'equipotential_junction_plate': 'equipotential_junction_plate',  # deng dian wei, 5
            # "flat_switch": "flat_switch",
            # "emergency_single_tube_lamp": "emergency_single_tube_lamp",
            # "distribution_box": "distribution_box",
            # "socket": "socket",
            # "single_tube_lamp": "single_tube_lamp",
            # "lamps": "lamps",
            # "double_tube_lamp": "double_tube_lamp",
            # "evacuation_signs": "evacuation_signs",
            # "emergency_lighting": "emergency_lighting",
            # "floor_indicator_light": "floor_indicator_light",
            # "emergency_double_tube_lamp": "emergency_double_tube_lamp",
            # "yinxiaxian": "yinxiaxian",
            # "broadcast": "broadcast",
            # "smoke": "smoke",
            # "light_alarm": "light_alarm",
            # "fire_button": "fire_button",
            # "button": "button",
        },
        DetectType.PEIDIANXIANG_SYSTEM_ENTITY: {
            "circuit_breaker": "circuit_breaker",
            "electricity_meter": "electricity_meter",
            "peidianxiang_outlet_branch": "peidianxiang_outlet_branch",
            "switch_double": "switch_double",
            "contactor": "contactor",
            "thermorelay": "thermorelay",
            "load_switch": "load_switch",
            "residual_current_circuit_breaker": "residual_current_circuit_breaker",
            "surge_protector": "surge_protector",
            "Isolation_switch": "isolation_switch",
            "Integrated_circuit_breaker": "integrated_circuit_breaker",

        },
        # DetectType.INDOOR_KITCHEN: {
        #     "gas_meter": "others",  # 燃气表
        #     "heater": "heater",  # 热水器
        # },
        # DetectType.INDOOR_BALCONY: {
        #     "gas_meter": "others",  # 燃气表
        #     "heater": "heater",  # 热水器
        # },
    }

    SCORE_THRESHOLD = {  # NMS置信度阈值
        DetectType.PEIDIANXIANG_SYSTEM_PEIDIANXIANGZITU: 0.2,
        DetectType.PEIDIANXIANG_SYSTEM_ENTITY: 0.5,
        DetectType.ZHAOMING_ENTITY: 0.5,
        # DetectType.INDOOR_BALCONY: 0.4,
        # DetectType.INDOOR_KITCHEN: 0.2,
    }

    MODEL_URL_SUFFIX = {  # 模型url后缀
        # DetectType.PEIDIANXIANG_SYSTEM_PEIDIANXIANGZITU: "/api/v1/pinshi/detection_yolo",
        DetectType.PEIDIANXIANG_SYSTEM_PEIDIANXIANGZITU: "/api/v1/pinshi/detection",
        DetectType.PEIDIANXIANG_SYSTEM_ENTITY: "/api/v1/pinshi/detection",
        DetectType.ZHAOMING_ENTITY: "/api/v1/pinshi/detection",
        # DetectType.INDOOR_KITCHEN: "/api/v1/pinshi/detection",
        # DetectType.INDOOR_BALCONY: "/api/v1/pinshi/detection",
    }

    MODEL_URL = {
        "prd": {
            DetectType.PEIDIANXIANG_SYSTEM_PEIDIANXIANGZITU: getenv("detection_peidianxiangzitu", "http://124.71.149.69:9005"),
            DetectType.PEIDIANXIANG_SYSTEM_ENTITY: getenv("detection_peidianxiang_entity", "http://124.71.161.45:9002"),
            DetectType.ZHAOMING_ENTITY: getenv("detection_zhaoming", "http://124.71.149.69:9002")
        },
        "pre": {
            DetectType.PEIDIANXIANG_SYSTEM_PEIDIANXIANGZITU: getenv("detection_peidianxiangzitu", "http://124.71.149.69:9005"),
            DetectType.PEIDIANXIANG_SYSTEM_ENTITY: getenv("detection_peidianxiang_entity", "http://124.71.161.45:9002"),
            DetectType.ZHAOMING_ENTITY: getenv("detection_zhaoming", "http://124.71.149.69:9002")
        },
        "test": {
            DetectType.PEIDIANXIANG_SYSTEM_PEIDIANXIANGZITU: getenv("detection_peidianxiangzitu", "http://124.71.149.69:9005"),
            DetectType.PEIDIANXIANG_SYSTEM_ENTITY: getenv("detection_peidianxiang_entity", "http://124.71.161.45:9002"),
            DetectType.ZHAOMING_ENTITY: getenv("detection_zhaoming", "http://124.71.149.69:9002")
        },
        "dev": {
            DetectType.PEIDIANXIANG_SYSTEM_PEIDIANXIANGZITU: getenv("detection_peidianxiangzitu", "http://124.71.149.69:9005"),
            DetectType.PEIDIANXIANG_SYSTEM_ENTITY: getenv("detection_peidianxiang_entity", "http://124.71.161.45:9002"),
            DetectType.ZHAOMING_ENTITY: getenv("detection_zhaoming", "http://124.71.149.69:9002")
        },
        "bgy_dev": {
            DetectType.PEIDIANXIANG_SYSTEM_PEIDIANXIANGZITU: getenv("detection_peidianxiangzitu",
                                                                    "http://124.71.149.69:9005"),
            DetectType.PEIDIANXIANG_SYSTEM_ENTITY: getenv("detection_peidianxiang_entity", "http://124.71.161.45:9002"),
            DetectType.ZHAOMING_ENTITY: getenv("detection_zhaoming", "http://124.71.161.45:7000"),
            # DetectType.INDOOR_KITCHEN: getenv("detection_indoor_kitchen", "http://124.70.184.163:9110"),
            # DetectType.INDOOR_BALCONY: getenv("detection_indoor_balcony", "http://124.71.158.131:32040"),
        }
    }
