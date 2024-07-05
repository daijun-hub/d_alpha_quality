from enum import auto, Enum


class EntityBaseType(Enum):

    BASE = auto()                       # 基础类型
    DOOR = auto()                       # 门
    WINDOW = auto()                     # 窗
    PILLAR = auto()                     # 柱
    PIELD = auto()                      # 场地
    KITCHEN_RESTROOM_OBJECT = auto()    # 厨卫设施
    PIPE = auto()                       # 管道
    FIRE_ALARM_DEVICE = auto()          # 火警设备
    MECHANICAL_DEVICE = auto()          # 机械设备
    HOUSEHOLD_APPLIANCE = auto()        # 家电
    HOLE = auto()                       # 孔洞
    HANDRAIL = auto()                   # 栏杆扶手
    STAIR = auto()                      # 楼梯
    DOOR_WITH_WINDOW = auto()           # 门连窗
    PARKING = auto()                    # 停车位
    PIPE_ACCESSORY = auto()             # 管道附件
    SPRINKLER = auto()                  # 喷头
    STRUCTURE_WALL = auto()             # 结构墙
    ILLUMINATION_DEVICE = auto()        # 照明设备
    ELECTRIC_DEVICE = auto()            # 电气设备
    ELECTRIC_EQUIPMENT = auto()         # 电气装置
    HVAC_DEVICE = auto()                # 暖通设备
    LAMP = auto()                       # 灯具
    DATA_DEVICE = auto()                # 数据设备
    WIRE = auto()                       # 导线
    PATTERN = auto()                    # 图案
    TEXT = auto()                       # 文字标注
    LINE = auto()                       # 线
    HATCH = auto()                      # 填充
    OTHERS = auto()                     # 无父类/未知父类

