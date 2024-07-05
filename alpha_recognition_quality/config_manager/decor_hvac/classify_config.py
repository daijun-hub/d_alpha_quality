# -*- coding: utf-8 -*-

from enum import Enum
from ...config import getenv


class ClassifyType(Enum):
    # ENUM = MODEL_NAME
    DECOR_HVAC = "decor_hvac_cls"


class ClassifyConfig:
    MODEL_CLASS = {
        ClassifyType.DECOR_HVAC: [
            "air_conditioner_ins_sep", # 分体式室内机
            "fen_ji_shui_qi",  # 分集水器
            "air_conditioner_out", # 室外机
            "tuila_door", # 推拉门
            "door", # 普通门
            "window", # 窗户
            "menlianchuang", # 门联窗
            "air_conditioner_ins_pipe", # 风管式室内机
        ],
    }

    # 通过图层、尺寸等后处理获取的构件如下：
    # 'overflow_hole'   溢流口
    # 'water_tank',    # 水箱
    # 'sprinkler'      # 喷头
    # 'check_well'     # 检查井

    MODEL_URL = {
        "prd": {
            ClassifyType.DECOR_HVAC: getenv("classification_hvac", "http://124.70.147.162:8507")  # model_name: hvac
        },
        "test": {
            ClassifyType.DECOR_HVAC: getenv("classification_hvac", "http://124.70.147.162:8507")
        },
        "pre": {
            ClassifyType.DECOR_HVAC: getenv("classification_hvac", "http://124.70.147.162:8507")
        },
        "dev": {
            ClassifyType.DECOR_HVAC: getenv("classification_hvac", "http://124.70.147.162:8507")
        },
        "bgy_dev": {
            ClassifyType.DECOR_HVAC: getenv("classification_hvac", "http://124.70.184.163:9220")
        }
    }

