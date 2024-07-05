# -*- coding: utf-8 -*-

from enum import Enum
from ...config import getenv


class ClassifyType(Enum):
    # ENUM = MODEL_NAME
    PLUMBING = "plumbing"


class ClassifyConfig:
    MODEL_CLASS = {
        ClassifyType.PLUMBING: [
            "others",
            "parking",  # 停车位
            "pressure_meter",  # 压力表
            "system_sprayer",  # 喷头_系统
            "dilou",  # 地漏
            "casing",  # 套管
            "intercepting_ditch",  # 截水沟
            "tuila_door",
            "door",
            "water_test_epuip_end_plan",  # 末端试水装置_平面
            "water_test_epuip_end_system",  # 末端试水装置_系统
            "elevation_symbol",  # 标高符号
            "check_point",  # 检查口
            "stair",  # 楼梯
            "pump_connector",  # 水泵接合器
            "water_meter",  # 水表
            "water_meter",  # 水表方形
            "washbasin",  # 洗手池
            "shower",  # 洗浴器
            "washer",  # 洗衣机
            "fire_hydrants",  # 消火栓
            "fire_hydrants_plumbing",  # 系统消火栓
            "clean_hole",  # 清扫口
            "fire_extinguisher",  # 灭火器
            "fire_extinguisher_fire_hydrants",  # 灭火器和消火栓
            "elevator_box",
            "window",
            "vpipe",  # 立管
            "system_dilou",  # 系统地漏
            "axis_mark",  # 轴标
            "vent_cap",  # 通气帽
            "vent_cap",  # 通气帽圆形
            "menlianchuang",
            "signal_valve",  # 阀门_信号阀
            "reducing_valve",  # 阀门_减压阀
            "alarm_valve",  # 阀门_平面报警阀
            "stop_valve",  # 阀门_截止阀
            "exhaust_valve",  # 阀门_排气阀
            "system_alarm_valve",  # 阀门_系统报警阀
            "butterfly_valve",  # 阀门_蝶阀
            "sluice_valve",  # 阀门_闸阀
            "water_pit",  # 集水坑
            "rain_well",  # 雨水井
            "rain_bucket_side",  # 雨水斗侧排
            "rain_bucket_side",  # 雨水斗侧排_方形
            "rain_bucket_full",  # 雨水斗全排
            "toilet",  # 马桶(便器)
        ],
    }

    # 通过图层、尺寸等后处理获取的构件如下：
    # 'overflow_hole'   溢流口
    # 'water_tank',    # 水箱
    # 'sprinkler'      # 喷头
    # 'check_well'     # 检查井

    MODEL_URL = {
        "prd": {
            ClassifyType.PLUMBING: getenv("classification_plumbing", "http://124.70.184.163:8505")
        },
        "test": {
            ClassifyType.PLUMBING: getenv("classification_plumbing", "http://124.70.184.163:8505")
        },
        "pre": {
            ClassifyType.PLUMBING: getenv("classification_plumbing", "http://124.70.184.163:8505")
        },
        "dev": {
            ClassifyType.PLUMBING: getenv("classification_plumbing", "http://124.70.184.163:8505")
        },
        "bgy_dev": {
            ClassifyType.PLUMBING: getenv("classification_plumbing", "http://124.70.184.163:8505")
        }
    }

