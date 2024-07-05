# -*- coding: utf-8 -*-

from .architecture.drawing_config import DrawingType as DrawingTypeArchi
from .structure.drawing_config import DrawingType as DrawingTypeStr
from .decor_electric.drawing_config import DrawingType as DrawingTypeDecorElectric
from .decor_hvac.drawing_config import DrawingType as DrawingTypeDecorHvac

EntityWithCrossBorderAttributes = {
    DrawingTypeArchi.INDOOR: [
        "平面栏杆", "普通窗", "凸窗", "转角窗", "预留孔洞", "风井百叶",
    ],
    DrawingTypeArchi.INDOOR_FIRST_FLOOR: [
        "平面栏杆", "普通窗", "凸窗", "转角窗", "风井百叶",
    ],
    DrawingTypeArchi.WUMIAN: [
        "平面栏杆"
    ],
    DrawingTypeStr.WALL_COLUMN_GRAPH: [
        "结构暗柱", "结构墙身",
    ],
    DrawingTypeDecorElectric.DECORATION_ELECTRIC_PLAN: [
        "强电箱", "弱电箱", "可视对讲", "等电位连接板", "插座"
    ],

}

SpaceWithCrossBorderAttributes = {
    DrawingTypeArchi.INDOOR: [
        "户", "家政间", "洗衣房", "衣帽间", "储藏间", "厨房", "阳台", "客餐厅", "书房", "玄关", "露台", "主卧", "其他卧室",
    ],
    DrawingTypeArchi.INDOOR_FIRST_FLOOR: [
        "户", "家政间", "洗衣房", "衣帽间", "储藏间", "厨房", "阳台", "客餐厅", "书房", "玄关", "露台", "主卧", "其他卧室",
    ],
    DrawingTypeArchi.JIFANG: [
        "露台",
    ],
    DrawingTypeDecorHvac.DECORATION_HVAC_VENTILATION_PLAN: [
        "户",
    ],
}
