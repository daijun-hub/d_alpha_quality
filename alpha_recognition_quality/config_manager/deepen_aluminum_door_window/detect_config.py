from enum import Enum
from ...config import getenv

# TODO: 套内空间的构件检测是建筑和给排水专业共用模型，每次模型迭代之后，需要将建筑和给排水专业的构件检测配置和构件检测代码同步修改


class DetectType(Enum):
    # ENUM = MODEL_NAME
    INDOOR_WASHROOM = "vanke_indoor_entity_det_wash"
    INDOOR_KITCHEN = "vanke_indoor_entity_det_kitc"
    INDOOR_BALCONY = "vanke_indoor_entity_det_balc"
    INDOOR_LIVINGROOM = "vanke_indoor_entity_det_livr"
    INDOOR_BEDROOM = "zhonghai_indoor_entity_det_bdr"


class DetectConfig:
    MODEL_CLASS = {
        DetectType.INDOOR_KITCHEN: [
            # "wardrobe",  # 柜子（含衣柜、储物柜）
            # "sink",  # 洗涤槽
            # "pipe",  # 立管
            # "refrigerator",
            # "cooktop",
            # "air_conditioner_internal_machine",  # 空调内机
            # "drain",
            # "washbasin",  # 洗手池
            # "washer",  # 洗衣机
            # "chair",   # 椅子
            # "table",  # 桌子
            # "light",  # 普通灯
            # "sofa",  # 沙发
            # "tv",    # 电视
            # "coffee_table",  # 茶几
            # "fire_hydrant",
            "sink",
            "cooktop",
            "refrigerator",
            "heater",
            "exhaust_pipe",
        ],
        DetectType.INDOOR_WASHROOM: [
            # "drain",        # 地漏
            # "shower",       # 洗浴器
            # "toilet",   # 便器
            # "washer",  # 洗衣机
            # "wardrobe",  # 柜子（含衣柜、储物柜）
            # "washbasin",    # 洗手池
            # "pipe",  # 立管
            # "bathtub",  # 浴缸
            # "sink",         # 洗涤槽
            # "fire_hydrant",  # 消火栓
            # "air_conditioner_internal_machine",  # 空调内机
            # "table",        # 桌子
            # "chair",        # 椅子
            # "tv",           # 电视
            # "coffee_table", # 茶几
            # "sofa",         # 沙发
            # "light",        # 普通灯
            # "bed",          # 床
            # "refrigerator",       # 冰箱
            # "lightstand",   # 床头柜
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
        DetectType.INDOOR_BEDROOM: [
            "table",
            "chair",
            "bed",
            "wardrobe",
            "light",
            "lightstand",
            "air_conditioner_internal_machine",
            "tv",
            "air_conditioner_outside_machine",
            "sofa",
            "pipe",
            "fire_hydrant",
            "sink",
            "cooktop",
            "refrigerator",
            "washbasin",
            "washer",
            "shower",
            "toilet",
            "coffee_table",
            "drain",
        ],
    }

    LABEL_MAP = {  # 检测标签和分类标签之前的映射
        DetectType.INDOOR_KITCHEN: {
            "wardrobe": "wardrobe",     # 柜子（含衣柜、储物柜）
            "sink": "sink",             # 洗涤槽
            "pipe": "pipe",             # 立管
            "refrigerator": "fridge",
            "cooktop": "stove",
            "air_conditioner_internal_machine": "air_conditioner_ins",  # 空调内机
            "drain": "dilou",
            "washbasin": "washbasin",   # 洗手池
            "washer": "washer",         # 洗衣机
            "chair": "chair",           # 椅子
            "table": "table",           # 桌子
            "light": "lamps",           # 普通灯
            "sofa": "sofa",             # 沙发
            "tv": "tv",                 # 电视
            "coffee_table": "coffee_table",  # 茶几
            "fire_hydrant": "xiaohuoshuan",
            "heater": "heater",         #热水器
            "exhaust_pipe": "kitchen_exhaust_pipe", #厨房排烟管
        },
        DetectType.INDOOR_WASHROOM: {
            "drain": "dilou",               # 地漏
            "shower": "shower",             # 洗浴器
            "toilet": "closestool",         # 便器
            "washer": "washer",             # 洗衣机
            "wardrobe": "wardrobe",         # 柜子（含衣柜、储物柜）
            "washbasin": "washbasin",       # 洗手池
            "pipe": "pipe",                 # 立管
            "bathtub": "bathtub",           # 浴缸
            "sink": "sink",                 # 洗涤槽
            "fire_hydrant": "xiaohuoshuan", # 消火栓
            "air_conditioner_internal_machine": "air_conditioner_ins",  # 空调内机
            "table": "table",               # 桌子
            "chair": "chair",               # 椅子
            "tv": "tv",                     # 电视
            "coffee_table": "coffee_table", # 茶几
            "sofa": "sofa",                 # 沙发
            "light": "lamps",               # 普通灯
            "bed": "bed",                   # 床
            "refrigerator": "fridge",       # 冰箱
            "lightstand": "lightstand",     # 床头柜
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
        DetectType.INDOOR_BEDROOM: {
            "drain": "dilou", # 地漏
            "washer": "washer", # 洗衣机
            "washbasin": "washbasin", # 洗手盆
            "pipe": "pipe", # 立管
            "refrigerator": "fridge", # 冰箱
            "cooktop": "stove", # 炉灶
            "sink": "sink", # 洗涤槽/洗菜盆

            "table": "table", # 桌
            "chair": "chair", # 椅子
            "bed": "bed", # 床
            "wardrobe": "wardrobe", # 柜子
            "light": "light", # 灯
            "lightstand": "lightstand", # 床头柜
            "air_conditioner_internal_machine": "air_conditioner_internal_machine", # 空调内机
            "tv": "tv", # 电视
            "air_conditioner_outside_machine": "air_conditioner_outside_machine", # 空调外机
            "sofa": "sofa", # 沙发
            "fire_hydrant": "fire_hydrant", # 消火栓
            "shower": "shower", # 淋浴器
            "toilet": "toilet", # 马桶(便器/大便器)
            "coffee_table": "coffee_table", # 茶几
        },
    }

    SCORE_THRESHOLD = {  # NMS置信度阈值
        DetectType.INDOOR_KITCHEN: 0.2,
        DetectType.INDOOR_WASHROOM: 0.5,
        DetectType.INDOOR_BALCONY: 0.4,
        DetectType.INDOOR_LIVINGROOM: 0.35,
        DetectType.INDOOR_BEDROOM: 0.4,
    }

    MODEL_URL_SUFFIX = {  # 模型url后缀
        DetectType.INDOOR_KITCHEN: "/api/v1/pinshi/detection",
        DetectType.INDOOR_WASHROOM: "/api/v1/pinshi/detection",
        DetectType.INDOOR_BALCONY: "/api/v1/pinshi/detection",
        DetectType.INDOOR_LIVINGROOM: "/api/v1/pinshi/detection",
        DetectType.INDOOR_BEDROOM: "/api/v1/pinshi/detection",
    }

    MODEL_URL = {
        "prd": {
            DetectType.INDOOR_KITCHEN: getenv("detection_indoor_kitchen", "http://123.60.40.81:9003"),
            DetectType.INDOOR_WASHROOM: getenv("detection_indoor_washroom", "http://123.60.40.81:9007"),
            DetectType.INDOOR_BALCONY: getenv("detection_indoor_balcony", "http://123.60.40.81:9001"),
            DetectType.INDOOR_LIVINGROOM: getenv("detection_indoor_livingroom", "http://123.60.40.81:9004"),
            DetectType.INDOOR_BEDROOM: getenv("detection_indoor_bedroom", "http://121.36.197.103:9008"),
        },
        "pre": {
            DetectType.INDOOR_KITCHEN: getenv("detection_indoor_kitchen", "http://123.60.40.81:9003"),
            DetectType.INDOOR_WASHROOM: getenv("detection_indoor_washroom", "http://123.60.40.81:9007"),
            DetectType.INDOOR_BALCONY: getenv("detection_indoor_balcony", "http://123.60.40.81:9001"),
            DetectType.INDOOR_LIVINGROOM: getenv("detection_indoor_livingroom", "http://123.60.40.81:9004"),
            DetectType.INDOOR_BEDROOM: getenv("detection_indoor_bedroom", "http://121.36.197.103:9008"),
        },
        "test": {
            DetectType.INDOOR_KITCHEN: getenv("detection_indoor_kitchen", "http://123.60.40.81:9003"),
            DetectType.INDOOR_WASHROOM: getenv("detection_indoor_washroom", "http://123.60.40.81:9007"),
            DetectType.INDOOR_BALCONY: getenv("detection_indoor_balcony", "http://123.60.40.81:9001"),
            DetectType.INDOOR_LIVINGROOM: getenv("detection_indoor_livingroom", "http://123.60.40.81:9004"),
            DetectType.INDOOR_BEDROOM: getenv("detection_indoor_bedroom", "http://121.36.197.103:9008"),
        },
        "dev": {
            DetectType.INDOOR_KITCHEN: getenv("detection_indoor_kitchen", "http://124.71.158.131:30366"),
            DetectType.INDOOR_WASHROOM: getenv("detection_indoor_washroom", "http://124.71.158.131:31095"),
            DetectType.INDOOR_BALCONY: getenv("detection_indoor_balcony", "http://123.60.40.81:9001"),
            DetectType.INDOOR_LIVINGROOM: getenv("detection_indoor_livingroom", "http://123.60.40.81:9004"),
            DetectType.INDOOR_BEDROOM: getenv("detection_indoor_bedroom", "http://121.36.197.103:9008"),
        },
        "bgy_dev": {
            DetectType.INDOOR_KITCHEN: getenv("detection_indoor_kitchen", "http://123.60.40.81:9003"),
            DetectType.INDOOR_WASHROOM: getenv("detection_indoor_washroom", "http://123.60.40.81:9007"),
            DetectType.INDOOR_BALCONY: getenv("detection_indoor_balcony", "http://123.60.40.81:9001"),
            DetectType.INDOOR_LIVINGROOM: getenv("detection_indoor_livingroom", "http://123.60.40.81:9004"),
            DetectType.INDOOR_BEDROOM: getenv("detection_indoor_bedroom", "http://121.36.197.103:9008"),
        }
    }
