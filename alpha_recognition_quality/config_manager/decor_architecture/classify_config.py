from enum import Enum
from ...config import getenv

class ClassifyType(Enum):
    # ENUM = MODEL_NAME
    INDOOR = "indoor"
    UNDERGROUND = "underground"


class ClassifyConfig:

    MODEL_CLASS = {
        ClassifyType.INDOOR: [
            "others",
            "mailbox",              # 信报箱
            "fridge",               # 冰箱
            "washroom_paifengjing", # 卫生间排风井
            "kitchen_exhaust_pipe", # 厨房排烟管道
            "dilou",                # 地漏
            "zhexianchuang",        # 折线窗
            "paiqikou",             # 排气口
            "paishuikou",           # 排水口
            "tuila_door",           # 推拉门
            "door",                 # 平开门
            "elevation_symbol",     # 标高符号
            "stair",                # 楼梯
            "washbasin",		    # 洗手池
            "shower",               # 洗浴器
            "sink",                 # 洗涤槽
            "washer",			    # 洗衣机
            "xiaohuoshuan",         # 消火栓
            "stove",                # 炉灶
            "elevator_box",         # 电梯厢
            "baiye",                # 百叶窗
            "air_conditioner",      # 空调
            "window",               # 窗户
            "pipe",                 # 立管
            "limianchuang",         # 立面窗
            "guanjingmen",          # 设备管井门
            "diamond_bath",         # 钻石淋浴
            "menlianchuang",        # 门联窗
            "reserved_hole",        # 预留孔洞
            "closestool",           # 马桶
            "apron",                # 散水
        ],
        ClassifyType.UNDERGROUND: [
            "others",
            "renfang_door",     # 人防门
            "cd_parking",       # 充电停车位
            "juanlianmen",      # 卷帘门
            "gutter",           # 排水沟
            "wza_cd_parking",   # 无障碍充电停车位
            "wza_parking",      # 无障碍非充电停车位
            "door",             # 门
            "louti",            # 楼梯
            "shuijing",         # 水井
            "fire_hydrants",    # 消火栓
            "elevator_door",    # 电梯门
            "baiye",            # 百叶
            "window",           # 窗户
            "pipe",             # 立管
            "guanjingmen",      # 设备管井门
            "menlianchuang",    # 门联窗
            "famen",            # 阀门
            "water_pit",        # 集水坑
            "normal_parking",   # 非充电停车位
        ],
    }

    MODEL_URL = {
        "prd": {
            ClassifyType.INDOOR: getenv("classification_indoor", "http://124.71.158.131:31864"),
            ClassifyType.UNDERGROUND: getenv("classification_underground", "http://121.36.197.103:8508")
        },
        "pre": {
            ClassifyType.INDOOR: getenv("classification_indoor", "http://124.71.158.131:31864"),
            ClassifyType.UNDERGROUND: getenv("classification_underground", "http://121.36.197.103:8508")
        },
        "test": {
            ClassifyType.INDOOR: getenv("classification_indoor", "http://124.71.158.131:31864"),
            ClassifyType.UNDERGROUND: getenv("classification_underground", "http://124.71.161.45:8508")
        },
        "dev": {
            ClassifyType.INDOOR: getenv("classification_indoor", "http://124.71.158.131:31864"), # http://124.71.158.131:30776 http://124.71.158.131:31864
            ClassifyType.UNDERGROUND: getenv("classification_underground", "http://124.71.161.45:8508")
        },
        "bgy_dev": {
            ClassifyType.INDOOR: getenv("classification_indoor", "http://124.71.161.45:8509"),
            ClassifyType.UNDERGROUND: getenv("classification_underground", "http://124.70.184.163:8502")
        }
    }
