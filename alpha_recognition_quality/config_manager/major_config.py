from enum import Enum


class MajorType(Enum):
    BUILDING = 1
    STRUCTURE = 2
    WATER_SUPPLY = 3
    HVAC = 4
    ELECTRIC = 5
    DECORATE = 6
    GARDENS = 7
    ROAD = 8


class MajorConfig(Enum):
    ARCHITECTURE = 'architecture'
    ELECTRIC = 'electric'
    PLUMBING = 'plumbing'
    HVAC = "hvac"
    STRUCTURE = "structure"
    DEEPEN_ALUMINUM_DOOR_WINDOW = "deepen_aluminum_door_window"


class Decor_MajorConfig(Enum):
    ARCHITECTURE = 'decor_architecture'
    ELECTRIC = 'decor_electric'
    PLUMBING = 'decor_plumbing'
    HVAC = "decor_hvac"



MAJOR_NAME_MAP = {
    "建筑": MajorConfig.ARCHITECTURE,
    "建方": MajorConfig.ARCHITECTURE,
    "建施": MajorConfig.ARCHITECTURE,
    "建": MajorConfig.ARCHITECTURE,
    "装施": MajorConfig.ARCHITECTURE,
    "电气": MajorConfig.ELECTRIC,
    "电施": MajorConfig.ELECTRIC,
    "装修电": MajorConfig.ELECTRIC,
    "给排水": MajorConfig.PLUMBING,
    "水施": MajorConfig.PLUMBING,
    "暖通": MajorConfig.HVAC,
    "暖施": MajorConfig.HVAC,
    "结构": MajorConfig.STRUCTURE,
    "门窗": MajorConfig.DEEPEN_ALUMINUM_DOOR_WINDOW,
    "铝门窗": MajorConfig.DEEPEN_ALUMINUM_DOOR_WINDOW,
}

Decor_MAJOR_NAME_MAP = {
    "建筑": Decor_MajorConfig.ARCHITECTURE,
    "建方": Decor_MajorConfig.ARCHITECTURE,
    "建施": Decor_MajorConfig.ARCHITECTURE,
    "建": Decor_MajorConfig.ARCHITECTURE,
    "装施": Decor_MajorConfig.ARCHITECTURE,
    "装修": Decor_MajorConfig.ARCHITECTURE,
    "硬装": Decor_MajorConfig.ARCHITECTURE,
    "电气": Decor_MajorConfig.ELECTRIC,
    "电施": Decor_MajorConfig.ELECTRIC,
    "装修电": Decor_MajorConfig.ELECTRIC,
    "装修电气": Decor_MajorConfig.ELECTRIC,
    "装施电": Decor_MajorConfig.ELECTRIC,
    "给排水": Decor_MajorConfig.PLUMBING,
    "水施": Decor_MajorConfig.PLUMBING,
    "暖通": Decor_MajorConfig.HVAC,
    "暖施": Decor_MajorConfig.HVAC,
    "装修水": Decor_MajorConfig.PLUMBING,
    "装施水": Decor_MajorConfig.PLUMBING,
    "装修暖": Decor_MajorConfig.HVAC,
    "装施暖": Decor_MajorConfig.HVAC,
    "装修暖通": Decor_MajorConfig.HVAC,
}
