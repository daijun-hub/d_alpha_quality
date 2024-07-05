# -*- coding: utf-8 -*-

from .architecture.drawing_config import DrawingType as DrawingTypeArchi
from .plumbing.drawing_config import DrawingType as DrawingTypePlumbing
from .decor_electric.drawing_config import DrawingType as DrawingTypeDecorElectric
from .decor_architecture.drawing_config import DrawingType as DrawingTypeDecorArchi
from .decor_hvac.drawing_config import DrawingType as DrawingTypeDecorHvac

SpaceWithRelation = {
    DrawingTypeArchi.INDOOR: [
        "户", "阳台", "厨房", "卫生间", "电梯井", "走廊", "户内设备平台", "公区设备平台", "强弱电井", "洗衣房",
        "储藏间", "衣帽间", "家政间", "客餐厅", "书房", "玄关", "露台", "套内水管井", "厨房油烟井", "卫生间排风井",
        "设备阳台", "空调机位", "敞开楼梯间", "封闭楼梯间", "防烟楼梯间", "剪刀楼梯间", "独立前室", "合用前室",
        "消防电梯前室", "共用前室", "三合一前室", "弱电井", "强电井", "电表井", "主卧", "其他卧室", "楼梯间"
    ],
    DrawingTypeArchi.INDOOR_FIRST_FLOOR: [
        "户", "阳台", "厨房", "卫生间", "配电间", "电梯井", "走廊", "大堂", "门斗", "扩大独立前室", "扩大合用前室",
        "扩大三合一前室", "扩大消防电梯前室", "扩大封闭楼梯间", "户内设备平台", "公区设备平台", "强弱电井", "洗衣房", "储藏间",
        "衣帽间", "家政间", "客餐厅", "书房", "玄关", "露台", "套内水管井", "厨房油烟井", "卫生间排风井", "设备阳台", "空调机位",
        "敞开楼梯间", "封闭楼梯间", "防烟楼梯间", "剪刀楼梯间", "独立前室", "合用前室", "消防电梯前室", "共用前室", "三合一前室",
        "弱电井", "强电井", "电表井", "主卧", "其他卧室", "楼梯间"
    ],
    DrawingTypeArchi.UNDERGROUND: [
        "配电间", "排风机房", "加压机房", "电梯井", "强弱电井", "储藏间", "强电井", "电表井", "排烟机房", "楼梯间"
    ],
    DrawingTypeArchi.JIFANG: [
        "热水机房", "加压机房", "强弱电井", "露台", "弱电井",  "强电井", "排烟机房", "楼梯间"
    ],
    DrawingTypeArchi.DINGCENG: [
        "热水机房", "弱电井",
    ],
    DrawingTypeArchi.STAIR_DAYANG: [
        "敞开楼梯间", "封闭楼梯间", "防烟楼梯间", "剪刀楼梯间",
    ],
    DrawingTypePlumbing.TOWER_WATER_DRAIN: [
        '阳台', '户', '卫生间'
    ],
    DrawingTypePlumbing.TOWER_WATER_SUPPLY: [
        '阳台', '户', '卫生间'
    ],
    DrawingTypePlumbing.TOWER_SECOND_FLOOR_DRAIN: [
        '阳台', '户', '卫生间'
    ],
    DrawingTypePlumbing.TOWER_SECOND_FLOOR_SUPPLY: [
        '阳台', '户', '卫生间'
    ],
    DrawingTypeDecorElectric.DECORATION_ELECTRIC_PLAN:[
        '户', "厨房", "卫生间", "阳台", "客餐厅"
    ],
    DrawingTypeDecorArchi.DECORATION_PLAN_LAYOUT:[
        '户'
    ],
    DrawingTypeDecorHvac.DECORATION_HVAC_VENTILATION_PLAN:[
        '户'
    ],
    DrawingTypeDecorHvac.HEATING_PLAN:[
        '户'
    ],
}
