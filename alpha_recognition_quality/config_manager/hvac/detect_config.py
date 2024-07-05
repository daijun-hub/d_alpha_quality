from enum import Enum
from ...config import getenv


class DetectType(Enum):
    # ENUM = MODEL_NAME
    PLUMBING_SYSTEM_ENTITY = "vanke_plumbing_entity_det_system"


class DetectConfig:
    MODEL_CLASS = {
        DetectType.PLUMBING_SYSTEM_ENTITY: [
            "check_point", # 检查口
            "rain_well",  # 雨水井
            "system_dilou",  # 系统地漏
            "butterfly_valve",  # 蝶阀
            "stop_valve",  # 截止阀
            "system_sprayer",  # 喷头-系统
            "water_meter",  # 水表
            "clean_hole",  # 清扫口
            "sluice_valve",  # 闸阀
            "pump_connector",  # 水泵接合器
            "reducing_valve", # 减压阀
            "casing",  # 套管
            "flow_indicator",  # 水流指示器
            "signal_valve",  # 信号阀
            "exhaust_valve",  # 排气阀
        ],
    }

    LABEL_MAP = {  # 检测标签和分类标签之前的映射
        DetectType.PLUMBING_SYSTEM_ENTITY: {
            "butterfly_valve":'butterfly_valve',
            "check_point":'check_point',
            "reducing_valve":'reducing_valve',
            "stop_valve":'stop_valve',
            "water_test_epuip_end_system":'water_test_epuip_end_system',
            "exhaust_valve":'exhaust_valve',
            "system_sprayer":'system_sprayer',
            "clean_hole":'clean_hole',
            "pump_connector":'pump_connector',
            "water_meter":'water_meter',
            "flow_indicator":'flow_indicator',
            "system_alarm_valve":'system_alarm_valve',
            "signal_valve":'signal_valve',
            "casing":'casing',
            "system_dilou":'system_dilou',
            "fire_hydrants_plumbing":'fire_hydrants_plumbing',
            "hydrant_hpipe":'hydrant_hpipe',
            "pressure_meter":'pressure_meter',
            "rain_well":'rain_well',
            "sluice_valve":'sluice_valve',
        },
    }

    SCORE_THRESHOLD = {  # NMS置信度阈值
        DetectType.PLUMBING_SYSTEM_ENTITY: 0.5,
    }

    MODEL_URL_SUFFIX = {  # 模型url后缀
        DetectType.PLUMBING_SYSTEM_ENTITY: "/api/v1/pinshi/detection",
    }

    MODEL_URL = {
        "prd": {
            DetectType.PLUMBING_SYSTEM_ENTITY: getenv("detection_plumbing_entity", "http://124.71.149.69:9006"),
        },
        "pre": {
            DetectType.PLUMBING_SYSTEM_ENTITY: getenv("detection_plumbing_entity", "http://124.71.149.69:9006"),
        },
        "test": {
            DetectType.PLUMBING_SYSTEM_ENTITY: getenv("detection_plumbing_entity", "http://124.71.149.69:9006"),
        },
        "dev": {
            DetectType.PLUMBING_SYSTEM_ENTITY: getenv("detection_plumbing_entity", "http://124.71.149.69:9006"),
        }
    }
