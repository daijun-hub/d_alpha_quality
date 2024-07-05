from enum import auto, Enum

class SpaceBaseType(Enum):

    BASE = auto()                       # 基础类型
    SITEPLAN_PIELD = auto()             # 总图场地范围
    INDOOR_FUNCTIONAL_SPACE = auto()    # 室内功能空间
    OUTDOOR_SUPPORT_SPACE = auto()      # 室外辅助空间
    PIELD_AREA = auto()                 # 场地范围
    FIRE_PREVENTION_ZONE = auto()       # 消防分区
    SYSTEM_LOCATION = auto()            # 系统所在范围
    OTHERS = auto()                     # 无父类

