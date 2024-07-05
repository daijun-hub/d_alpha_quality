# -*- coding: utf-8 -*-

from enum import Enum
from ...config import getenv


class ClassifyType(Enum):
    # ENUM = MODEL_NAME
    ELECTRIC = "electric"
    ELECTRIC_DETAILED = "electric_detailed"


class ClassifyConfig:

    MODEL_CLASS = {
        ClassifyType.ELECTRIC: [
            "others",
            "light_alarm",                  # 光警报器
            "light_alarm_fire_button",      # 光警报器和火灾报警按钮组合
            "area_display",                 # 区域显示器
            "juanlianmen",                  # 卷帘门
            "transformer_symbols",          # 变压器符号
            "flat_switch",                  # 平面图开关
            "flat_switch_evacuation_signs", # 平面图开关和灯光疏散指示标志组合
            "flat_switch",                  # 平面图开关组合
            "yinxiaxian",                   # 引下线
            "temperature",                  # 感温探测器
            "smoke",                        # 感烟探测器
            "button",                       # 按钮
            "tuila_door",
            "socket",                       # 插座
            "door",
            "stair",
            "fire_hydrants",                # 消火栓
            "broadcast",                    # 消防应急广播
            "hydrant_button",               # 消防栓按钮
            "fire_button",                  # 火灾报警按钮
            "evacuation_signs",             # 灯光疏散指示标志      -----> 待细分类
            "lamps",                        # 灯具(正方形)         -----> 待细分类
            "lamps_flat_switch",            # 普通灯和平面图开关组合
            "lamps_evacuation_signs",       # 普通灯和疏散指示组合
            "lamps",                        # 灯具(长条形)         -----> 待细分类
            "thermorelay",                  # 热继电器
            "fuse_protector",               # 熔断器
            "elevator_box",
            "phone",                        # 电话
            "air_conditioner_ins",          # 空调内机
            "window",
            "switch_single",                # 系统图开关单刀        -----> 待细分类
            "switch_double",                # 系统图开关双切
            "distribution_box",             # 配电箱
            "menlianchuang",                # 门联窗
            "fire_resistant_shutter_controller",  # 防火卷帘控制器和按钮
            # "weak_electric_box",            # 弱电箱
            # "strong_electric_box",          # 强电箱
        ],
        ClassifyType.ELECTRIC_DETAILED: [
            "emergency_lighting",               # A型应急照明灯
            "others",
            "integrated_circuit_breaker",       # 一体式断路器
            "triple_tube_lamp",                 # 三管灯
            "single_tube_lamp",                 # 单管灯
            "double_tube_lamp",                 # 双管灯
            "emergency_triple_tube_lamp",       # 应急三管灯
            "emergency_single_tube_lamp",       # 应急单管灯
            "emergency_double_tube_lamp",       # 应急双管灯
            "contactor",                        # 接触器
            "circuit_breaker",                  # 断路器
            "lamps",                            # 普通灯
            "surge_protector",                  # 浪涌保护器
            "residual_current_circuit_breaker", # 漏电断路器
            "evacuation_signs",                 # 灯光疏散指示标志
            "load_switch",                      # 负荷开关
        ],
    }

    MODEL_URL = {
        "prd": {
            ClassifyType.ELECTRIC: getenv("classification_electric", "http://124.70.184.163:8503"),
            ClassifyType.ELECTRIC_DETAILED: getenv("classification_electric_detailed", "http://124.70.184.163:8504")
        },
        "pre": {
            ClassifyType.ELECTRIC: getenv("classification_electric", "http://124.70.184.163:8503"),
            ClassifyType.ELECTRIC_DETAILED: getenv("classification_electric_detailed", "http://124.70.184.163:8504")
        },
        "test": {
            ClassifyType.ELECTRIC: getenv("classification_electric", "http://124.70.184.163:8503"),
            ClassifyType.ELECTRIC_DETAILED: getenv("classification_electric_detailed", "http://124.70.184.163:8504")
        },
        "dev": {
            # ClassifyType.ELECTRIC: getenv("classification_electric", "http://124.70.184.163:8503"),
            ClassifyType.ELECTRIC: getenv("classification_electric", "http://124.71.158.131:30238"),
            ClassifyType.ELECTRIC_DETAILED: getenv("classification_electric_detailed", "http://124.70.184.163:8504")
        },
        "bgy_dev": {
            # ClassifyType.ELECTRIC: getenv("classification_electric", "http://124.70.184.163:8503"),
            ClassifyType.ELECTRIC: getenv("classification_electric", "http://124.70.184.163:8503"),
            ClassifyType.ELECTRIC_DETAILED: getenv("classification_electric_detailed", "http://124.70.184.163:8504")
        }
    }

