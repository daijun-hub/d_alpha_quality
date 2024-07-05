from enum import Enum
from ...config import getenv

# TODO: 套内空间的构件检测是建筑和给排水专业共用模型，每次模型迭代之后，需要将建筑和给排水专业的构件检测配置和构件检测代码同步修改


class DetectType(Enum):
    # ENUM = MODEL_NAME
    PLUMBING_SYSTEM_ENTITY = "vanke_plumbing_entity_det_system"
    INDOOR_WASHROOM = "vanke_indoor_entity_det_wash"
    INDOOR_KITCHEN = "vanke_indoor_entity_det_kitc"
    INDOOR_BALCONY = "vanke_indoor_entity_det_balc"
    INDOOR_LIVINGROOM = "vanke_indoor_entity_det_livr"


class DetectConfig:
    MODEL_CLASS = {
        DetectType.PLUMBING_SYSTEM_ENTITY: [
            "check_point",  # 检查口
            "rain_well",  # 雨水井
            "system_dilou",  # 系统地漏
            "butterfly_valve",  # 蝶阀
            "stop_valve",  # 截止阀
            "system_sprayer",  # 喷头-系统
            "water_meter",  # 水表
            "clean_hole",  # 清扫口
            "sluice_valve",  # 闸阀
            "pump_connector",  # 水泵接合器
            "reducing_valve",  # 减压阀
            "casing",  # 套管
            "flow_indicator",  # 水流指示器
            "signal_valve",  # 信号阀
            "exhaust_valve",  # 排气阀
        ],
        DetectType.INDOOR_KITCHEN: [
            "sink",
            "cooktop",
            "refrigerator",
        ],
        DetectType.INDOOR_WASHROOM: [
            "drain",
            "toilet",
            "washbasin",
            "shower",
            "pipe",
            "washer",
            "bathtub",
        ],
        DetectType.INDOOR_BALCONY: [
            "drain",
            "pipe",
            "washer",
            "washbasin",
        ],
        DetectType.INDOOR_LIVINGROOM: [
            "washer",
            "washbasin",
            "drain",
            "refrigerator",
            "cooktop",
            "sink",
            "pipe",
        ],
    }

    LABEL_MAP = {  # 检测标签和分类标签之前的映射
        DetectType.PLUMBING_SYSTEM_ENTITY: {
            "butterfly_valve": 'butterfly_valve',
            "check_point": 'check_point',
            "reducing_valve": 'reducing_valve',
            "stop_valve": 'stop_valve',
            "water_test_epuip_end_system": 'water_test_epuip_end_system',
            "exhaust_valve": 'exhaust_valve',
            "system_sprayer": 'system_sprayer',
            "clean_hole": 'clean_hole',
            "pump_connector": 'pump_connector',
            "water_meter": 'water_meter',
            "flow_indicator": 'flow_indicator',
            "system_alarm_valve": 'system_alarm_valve',
            "signal_valve": 'signal_valve',
            "casing": 'casing',
            "system_dilou": 'system_dilou',
            "fire_hydrants_plumbing": 'fire_hydrants_plumbing',
            "hydrant_hpipe": 'hydrant_hpipe',
            "pressure_meter": 'pressure_meter',
            "rain_well": 'rain_well',
            "sluice_valve": 'sluice_valve',
        },
        DetectType.INDOOR_KITCHEN: {
            "wardrobe": "wardrobe",  # 柜子（含衣柜、储物柜）
            "sink": "sink",  # 洗涤槽
            "pipe": "pipe",  # 立管
            "refrigerator": "fridge",
            "cooktop": "stove",
            "air_conditioner_internal_machine": "air_conditioner_ins",  # 空调内机
            "drain": "dilou",
            "washbasin": "washbasin",  # 洗手池
            "washer": "washer",  # 洗衣机
            "chair": "chair",  # 椅子
            "table": "table",  # 桌子
            "light": "lamps",  # 普通灯
            "sofa": "sofa",  # 沙发
            "tv": "tv",  # 电视
            "coffee_table": "coffee_table",  # 茶几
            "fire_hydrant": "xiaohuoshuan",
        },
        DetectType.INDOOR_WASHROOM: {
            "drain": "dilou",  # 地漏
            "shower": "shower",  # 洗浴器
            "toilet": "closestool",  # 便器
            "washer": "washer",  # 洗衣机
            "wardrobe": "wardrobe",  # 柜子（含衣柜、储物柜）
            "washbasin": "washbasin",  # 洗手池
            "pipe": "pipe",  # 立管
            "bathtub": "bathtub",  # 浴缸
            "sink": "sink",  # 洗涤槽
            "fire_hydrant": "xiaohuoshuan",  # 消火栓
            "air_conditioner_internal_machine": "air_conditioner_ins",  # 空调内机
            "table": "table",  # 桌子
            "chair": "chair",  # 椅子
            "tv": "tv",  # 电视
            "coffee_table": "coffee_table",  # 茶几
            "sofa": "sofa",  # 沙发
            "light": "lamps",  # 普通灯
            "bed": "bed",  # 床
            "refrigerator": "fridge",  # 冰箱
            "lightstand": "lightstand",  # 床头柜
        },
        DetectType.INDOOR_BALCONY: {
            "drain": "dilou",  # 地漏
            "washer": "washer",  # 洗衣机
            "washbasin": "washbasin",  # 洗手池
            "pipe": "pipe",  # 立管
        },
        DetectType.INDOOR_LIVINGROOM: {
            "drain": "dilou",
            "washer": "washer",
            "washbasin": "washbasin",
            "pipe": "pipe",
            "refrigerator": "fridge",
            "cooktop": "stove",
            "sink": "sink",
        },
    }

    SCORE_THRESHOLD = {  # NMS置信度阈值
        DetectType.PLUMBING_SYSTEM_ENTITY: 0.5,
        DetectType.INDOOR_KITCHEN: 0.2,
        DetectType.INDOOR_WASHROOM: 0.5,
        DetectType.INDOOR_BALCONY: 0.4,
        DetectType.INDOOR_LIVINGROOM: 0.35,
    }

    MODEL_URL_SUFFIX = {  # 模型url后缀
        DetectType.PLUMBING_SYSTEM_ENTITY: "/api/v1/pinshi/detection",
        DetectType.INDOOR_KITCHEN: "/api/v1/pinshi/detection",
        DetectType.INDOOR_WASHROOM: "/api/v1/pinshi/detection",
        DetectType.INDOOR_BALCONY: "/api/v1/pinshi/detection",
        DetectType.INDOOR_LIVINGROOM: "/api/v1/pinshi/detection",
    }

    MODEL_URL = {
        "prd": {
            DetectType.PLUMBING_SYSTEM_ENTITY: getenv("detection_plumbing_system", "http://124.71.149.69:9006"),
            DetectType.INDOOR_KITCHEN: getenv("detection_indoor_kitchen", "http://123.60.40.81:9003"),
            DetectType.INDOOR_WASHROOM: getenv("detection_indoor_washroom", "http://123.60.40.81:9007"),
            DetectType.INDOOR_BALCONY: getenv("detection_indoor_balcony", "http://123.60.40.81:9001"),
            DetectType.INDOOR_LIVINGROOM: getenv("detection_indoor_livingroom", "http://123.60.40.81:9004"),
        },
        "pre": {
            DetectType.PLUMBING_SYSTEM_ENTITY: getenv("detection_plumbing_system", "http://124.71.149.69:9006"),
            DetectType.INDOOR_KITCHEN: getenv("detection_indoor_kitchen", "http://123.60.40.81:9003"),
            DetectType.INDOOR_WASHROOM: getenv("detection_indoor_washroom", "http://123.60.40.81:9007"),
            DetectType.INDOOR_BALCONY: getenv("detection_indoor_balcony", "http://123.60.40.81:9001"),
            DetectType.INDOOR_LIVINGROOM: getenv("detection_indoor_livingroom", "http://123.60.40.81:9004"),
        },
        "test": {
            DetectType.PLUMBING_SYSTEM_ENTITY: getenv("detection_plumbing_system", "http://124.71.149.69:9006"),
            DetectType.INDOOR_KITCHEN: getenv("detection_indoor_kitchen", "http://123.60.40.81:9003"),
            DetectType.INDOOR_WASHROOM: getenv("detection_indoor_washroom", "http://123.60.40.81:9007"),
            DetectType.INDOOR_BALCONY: getenv("detection_indoor_balcony", "http://123.60.40.81:9001"),
            DetectType.INDOOR_LIVINGROOM: getenv("detection_indoor_livingroom", "http://123.60.40.81:9004"),
        },
        "dev": {
            DetectType.PLUMBING_SYSTEM_ENTITY: getenv("detection_plumbing_system", "http://124.71.149.69:9006"),
            DetectType.INDOOR_KITCHEN: getenv("detection_indoor_kitchen", "http://123.60.40.81:9003"),
            DetectType.INDOOR_WASHROOM: getenv("detection_indoor_washroom", "http://123.60.40.81:9007"),
            DetectType.INDOOR_BALCONY: getenv("detection_indoor_balcony", "http://123.60.40.81:9001"),
            DetectType.INDOOR_LIVINGROOM: getenv("detection_indoor_livingroom", "http://123.60.40.81:9004"),
        },
        "bgy_dev": {
            DetectType.PLUMBING_SYSTEM_ENTITY: getenv("detection_plumbing_system", "http://124.71.149.69:9006"),
            DetectType.INDOOR_KITCHEN: getenv("detection_indoor_kitchen", "http://123.60.40.81:9003"),
            DetectType.INDOOR_WASHROOM: getenv("detection_indoor_washroom", "http://123.60.40.81:9007"),
            DetectType.INDOOR_BALCONY: getenv("detection_indoor_balcony", "http://123.60.40.81:9001"),
            DetectType.INDOOR_LIVINGROOM: getenv("detection_indoor_livingroom", "http://123.60.40.81:9004"),
        }
    }
