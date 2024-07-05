# -*- coding: utf-8 -*-

from enum import Enum

# from rule_engine.multi_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig
from ..multiple_border_pipeline_config import MultiBorderPipelineType


class MultiBorderRuleConfig(Enum):
    CONFIGURATION = {
        "1100012": {
            'name': '厨房的使用面积应符合下列规定：1 由卧室、起居室（厅）、厨房和卫生间等组成的住宅套型的厨房使用面积，不应小于4．0m2；2 由兼起居的卧室、厨房和卫生间等组成的住宅最小套型的厨房使用面积，不应小于3．5m2。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window"],
                    'operations': ["combination", "classification", "segmentation"],
                }
            },
        },
        "1100040": {
            'name': '直接对外的单元入户大堂应设置雨篷；挑出宽度≥1.5m；雨棚底高度不应低于3.0m。',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR,): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.BASIC_LAYERS.value[
                        'indoor_segment'] + ["door", "window"],
                    'operations': ["combination", "segmentation", "classification"],
                },
                (DrawingType.SECOND_THIRD_FLOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["basic"] +
                                LayerConfig.BASIC_LAYERS.value["second_third_segment"] + ['annotation_line', 'door',
                                                                                          'window'],
                    'operations': ["combination", "segmentation"],
                }
            },
        },
        "1100050": {
            'name': '高层建筑直通室外的安全出口上方，应设置挑出宽度不小于1.0m的防护挑檐。',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.SECOND_THIRD_FLOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
                (DrawingType.ELEVATION,): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'],
                    'operations': ['combination', 'classification'],
                },
            },
        },
        "1103001": {
            'name': '碧桂园墙厚度比对',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.INDOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"],
                    'operations': ['combination', 'classification', 'segmentation', 'text_information'],
                },
                (DrawingType.INDOOR,): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"],
                    'operations': ['combination', 'classification', 'segmentation', 'text_information'],
                }
            },
        },
        "1102001": {
            'name': '每个空间的窗地比不低于1/7',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window"],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
                (DrawingType.DOOR_WINDOW_DAYANG,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window", "elevation_window", "elevation_window_open_line"],
                    'operations': ['combination', 'classification'],
                },
            },
        },
        "1102003": {
            'name': '套内通风应满足要求.',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window"],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
                (DrawingType.DOOR_WINDOW_DAYANG,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window",
                                                                                    "elevation_window",
                                                                                    "elevation_window_open_line"],
                    'operations': ['combination', 'classification'],
                },
            },
        },
        "1102006": {
            'name': '地下设备用房和屋顶设备用房不能对住宅内造成不良影响。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window"],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
                (DrawingType.DINGCENG, DrawingType.UNDERGROUND, DrawingType.JIFANG): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window"],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
            },
        },
        "1102011": {
            'name': '屋顶电梯机房应考虑必要的排风设计，预留空调安装条件;电梯机房的位置是否合理，不宜布置在卧室等房间上部，否则应采取隔声减振措施。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window"],
                    'operations': ['combination', 'classification', 'segmentation', "text_information"],
                },
                (DrawingType.INDOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window"],
                    'operations': ['combination', 'classification', 'segmentation', "text_information"],
                },
                (DrawingType.JIFANG,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window"],
                    'operations': ['combination', 'classification', 'segmentation', "text_information"],
                },
            },
        },
        "1102009": {
            'name': '说明内容是否全面；应包括但不限于如下内容：项目概况、设计依据、采用的标准、规范和图集、设计范围、主要技术经济指标、总平面、标准层平面、外装修、内装修、墙体、防水、保温、幕墙门窗、电梯、消防、节能、无障碍、施工注意事项及其他',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ["text_information"],
                }
            },
        },

        "1102025": {
            'name': '厨房门联窗窗台应为1100mm高，可以避开后期厨房操作台和水龙头的影响',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DOOR_WINDOW_DAYANG, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "elevation_window_open_line"],
                    'operations': ["combination", "segmentation", "classification", "text_information"],
                }
            },
        },
        "1104022": {
            'name': '商铺门洞口高度偏低，不足2400，使用不便。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DOOR_WINDOW_DAYANG, DrawingType.INDOOR_FIRST_FLOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"],
                    'operations': ["combination", "segmentation", "classification", "text_information"],
                }
            },
        },
        "1104025": {
            'name': "大堂层高偏低，不满足标准化品质要求",
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"],
                    'operations': ["combination", "segmentation", "classification", "text_information"],
                },
                (DrawingType.SIDE_ELEVATION,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"],
                    'operations': ["combination", "segmentation", "classification", "text_information"],
                },
            },
        },
        "1104050": {
            'name': '商铺未统一设置空调机位导致空调安装混乱。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.SECOND_THIRD_FLOOR, DrawingType.DINGCENG): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"],
                    'operations': ["combination", "segmentation", "classification", "text_information"],
                }
            },
        },
        "1104040": {
            'name': '主要出入口处的雨棚未考虑有组织排水',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door"],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
                (DrawingType.SECOND_THIRD_FLOOR,): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['second_third_segment'] + ['annotation_line', 'door',
                                                                                          'window', "pipe",
                                                                                          "floor_drain"],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
            },
        },
        "1104048": {
            'name': '卫生间窗设计为内平开窗，且下部未设置固定扇，业主使用不便',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window"],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
                (DrawingType.DOOR_WINDOW_DAYANG,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window",
                                                                                    "elevation_window",
                                                                                    "elevation_window_open_line"],
                    'operations': ['combination', 'classification'],
                },
            },
        },
        "1104042": {
            'name': '供暖泵房或其他有震动及噪音的设备用房设置在紧邻住宅处',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"],
                    'operations': ["combination", "segmentation", "classification", "text_information"],
                },
                (DrawingType.UNDERGROUND,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"],
                    'operations': ["combination", "segmentation", "classification", "text_information"],
                },
            },
        },
        "1104053": {
            'name': '首层人行出入口上方未设置雨棚或雨棚尺度不适宜；物业用房、消防通道等人行处未设置雨棚，存在安全隐患。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.BASIC_LAYERS.value[
                        'indoor_segment'] + ["door", "window"],
                    'operations': ["combination", "segmentation", "classification"],
                },
                (DrawingType.SECOND_THIRD_FLOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["basic"] +
                                LayerConfig.BASIC_LAYERS.value["second_third_segment"] + ['annotation_line', 'door',
                                                                                          'window'],
                    'operations': ["combination", "segmentation", "classification"],
                },
                (DrawingType.INDOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["basic"] +
                                LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ['annotation_line', 'door',
                                                                                    'window'],
                    'operations': ["combination", "segmentation", "classification"],
                },
            }
        },
        "1104024": {
            'name': '上人屋面女儿墙高度不满足规范要求',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DINGCENG, DrawingType.JIFANG): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"],
                    'operations': ["combination", "segmentation", "classification", "text_information"],
                },
                (DrawingType.WALL_DAYANG,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["elevation_mark", "door", "window"],
                    'operations': ["combination", "segmentation", "classification", "text_information"],
                },
            },
        },
        103072: {
            'name': '当阳台设有洗衣设备时应符合下列规定：应设置专用给、排水管线及专用地漏，阳台楼、地面均应做防水。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN, DrawingType.ENGINEERING_WORK,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                },
                (DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + \
                                ["air_conditioner_mix", "floor_drain", 'washbasin', "floor_drain_mix"] + \
                                ['closestool', 'diamond_bath', "kitchen_exhaust_pipe"],
                    'operations': ['combination', "classification", "segmentation"],
                },
            },
        },
        103070: {
            'name': '顶层阳台应设雨罩，各套住宅之间毗连的阳台应设分户隔板',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.DINGCENG, DrawingType.INDOOR, DrawingType.WUMIAN): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
            },
        },
        105016: {
            'name': '轮椅坡道/无障碍坡道的坡面应平整、防滑、无反光。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        104025: {
            'name': '住宅屋面和外墙的内表面在室内温、湿度设计条件下不应出现结露。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        104026: {
            'name': '住宅屋面和外墙的内表面在室内温、湿度设计条件下不应出现结露。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        104030: {
            'name': '七层及七层以上住宅建筑入口平台宽度不应小于2．00m。',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR_FIRST_FLOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window",
                                                                                    "lobby_platform_border",
                                                                                    "elevator_box"],
                    'operations': ["combination", "segmentation", "classification"],
                }
            },
        },
        106002: {
            'name': '七层及七层以上住宅建筑入口平台宽度不应小于2．00m。',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", 'fire_hydrant'],
                    'operations': ["combination", "segmentation", "classification"],
                }
            },
        },
        104031: {
            'name': '七层以及七层以上的住宅或住户入口层楼面距室外设计地面的高度超过16m以上的住宅必须设置电梯',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + [
                        "elevator_box",
                        "elevator_door", ],
                    'operations': ["combination", "segmentation", "classification"],
                }
            },
        },
        104032: {
            'name': '住宅建筑应根据建筑的耐火等级、建筑层数、建筑面积、疏散距离等因素设置安全出口，并应符合下列要求',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["elevator_stair", "segment",
                                                                                    "elevator_box", "door"],
                    'operations': ["combination", 'segmentation', "classification"],
                }
            },
        },
        104033: {
            'name': '8层及8层以上的住宅建筑应设置室内消防给水设施',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR,  DrawingType.INDOOR_FIRST_FLOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["fire_hydrant"],
                    'operations': ["combination", "segmentation", "classification"],
                }
            },
        },
        104035: {
            "name": "12层及12层以上的住宅应设置消防电梯",
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION,DrawingType.SIDE_ELEVATION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["elevator_box"],
                    'operations': ['combination', 'segmentation', 'classification'],
                }
            },
        },
        104036: {
            'name': '七层及七层以上的住宅，应对下列部位进行无障碍设计：1 建筑入口；3 候梯厅 4 公共走道',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window", "elevator_box",
                                                                                    "elevator_door", "elevator_stair", "annotation_line", "elevation_mark"],
                    'operations': ['combination', 'classification', 'segmentation'],
                }
            },
        },
        104053: {
            'name': '住宅室内空气污染物的活度和浓度应符合表7.4.1的规定',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        103027: {
            'name': '十层以下的住宅建筑，当住宅单元任一层的建筑面积大于650m2，或任一套房的户门至安全出口的距离大于15m时，该住宅单元每层的安全出口不应少于2个。',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "elevator_stair"],
                    'operations': ["combination", "segmentation", "classification"],
                }
            },
        },
        103028: {
            'name': '十层及十层以上且不超过十八层的住宅建筑，当住宅单元任一层的建筑面积大于650m2，或任一套房的户门至安全出口的距离大于10m时，该住宅单元每层的安全出口不应少于2个。',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "elevator_stair"],
                    'operations': ["combination", "segmentation", "classification"],
                }
            },
        },
        103029: {
            'name': '十九层及十九层以上的住宅建筑，每层住宅单元的安全出口不应少于2个',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                   'major_drawing': True,
                   'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                   'operations': [],
                },
                (DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR): {
                   'major_drawing': True,
                   'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'window', 'elevator_stair'],
                   'operations': ['combination', 'segmentation', 'classification'],
                }
            },
        },
        103030: {
            'name': '七层及七层以上住宅或住户入口层楼面距室外设计地面的高度超过16m时, 必须设置电梯',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'window', 'elevator_stair'],
                    'operations': ['combination', 'segmentation', 'classification'],
                }
            },
        },
        103031: {
            'name': '七层及七层以上住宅建筑入口平台宽度不应小于2．00m，七层以下住宅建筑入口平台宽度不应小于1．50m。',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR_FIRST_FLOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window",
                                                                                    "lobby_platform_border",
                                                                                    "elevator_box"],
                    'operations': ["combination", "segmentation", "classification"],
                }
            },
        },
        106003: {
            'name': '建筑应设置消防电梯的规则',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'] + ['elevator_box'],
                    'operations': ['classification', 'combination', 'segmentation'],
                },
                (DrawingType.UNDERGROUND,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'] + ['elevator_box'],
                    'operations': ['classification', 'combination', 'segmentation'],
                }
            },
        },
        103032: {
            'name': '十二层及十二层以上的住宅，每栋楼设置电梯不应少于两台，其中应设置一台可容纳担架的电梯',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'window',
                                                                                    'elevator_stair', 'elevator_box'],
                    'operations': ['combination', 'segmentation', 'classification'],
                }
            },
        },
        103033: {
            'name': '七层及七层以上的住宅，应对下列部位进行无障碍设计：1 建筑入口；3 候梯厅 4 公共走道',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window", "elevator_box",
                                                                                    "elevator_door", "elevator_stair", "annotation_line", "elevation_mark"],
                    'operations': ['combination', 'classification', 'segmentation'],
                }
            },
        },
        109001: {
            'name': '七层及七层以上住宅建筑入口平台宽度不应小于2．00m，七层以下住宅建筑入口平台宽度不应小于1．50m。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN, DrawingType.ENGINEERING_WORK): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        109002: {
            'name': '住宅屋面和外墙的内表面在室内温、湿度设计条件下不应出现结露。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN, DrawingType.ENGINEERING_WORK): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        109003: {
            'name': '卷材、涂膜屋面防水等级和防水做法应符合表4．5．1的规定',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN, DrawingType.ENGINEERING_WORK,): {
                    'major_drawing': True,
                    'entities': ['engineering_work_table_line'],
                    'operations': ['text_information'],
                }
            },
        },
        109004: {
            'name': '屋面防水工程应根据建筑物的类别、重要程度、使用功能要求确定防水等级，并应按相应等级进行防水设防；',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,DrawingType.ENGINEERING_WORK): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        103040: {
            'name': '公共出入口处应有标识，十层及十层以上住宅的公共出入口应设门厅。',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR_FIRST_FLOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ['window', "door"],
                    'operations': ["combination", "segmentation", "classification"],
                }
            },
        },
        110001: {
            'name': '单层、多层民用建筑内部各部位装修材料的燃烧性能等级，不应低于本规范表5．1．1的规定。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        110002: {
            'name': '高层民用建筑内部各部位装修材料的燃烧性能等级，不应低于本规范表5．2．1的规定。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        110003: {
            'name': '地下民用建筑内部各部位装修材料的燃烧性能等级，不应低于本规范表5．3．1的规定。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        106009: {
            'name': '住宅建筑的疏散楼梯设置应符合三种规定。',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window", "elevator_stair",
                                                                                    "elevator_box"],
                    'operations': ["combination", "segmentation", "classification"],
                }
            },
        },
        101064: {
            'name': '直接对外的单元入户大堂应设置雨篷；挑出宽度≥1.5m；雨棚底高度不应低于3.0m。',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR, ): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window"],
                    'operations': ["combination", "segmentation", "classification"],
                },
                (DrawingType.SECOND_THIRD_FLOOR, ): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["basic"] +
                      LayerConfig.BASIC_LAYERS.value["second_third_segment"] + ['annotation_line', 'door', 'window'],
                    'operations': ["combination", "segmentation"],
                }
            },
        },
        103053: {
            'name': '十层以下的住宅建筑的楼梯间宜通至屋顶，且不应穿越其他房间。通向平屋面的门应向屋面方向开启',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.JIFANG, DrawingType.WUMIAN): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["elevator_stair", "door"],
                    'operations': ['classification', 'combination', 'segmentation'],
                }
            },
        },
        103054: {
            'name': '十层以下的住宅建筑的楼梯间宜通至屋顶，且不应穿越其他房间。通向平屋面的门应向屋面方向开启',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["elevator_stair", "door"],
                    'operations': ['classification', 'combination', 'segmentation'],
                },
                (DrawingType.INDOOR_FIRST_FLOOR, ): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["elevator_stair", "door"],
                    'operations': ['classification', 'combination', 'segmentation'],
                },
                (DrawingType.JIFANG, DrawingType.WUMIAN): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["elevator_stair", "door"],
                    'operations': ['classification', 'combination', 'segmentation'],
                }
            }
        },
        106010: {
            'name': '七层及七层以上住宅建筑入口平台宽度不应小于2．00m，七层以下住宅建筑入口平台宽度不应小于1．50m。',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window",'elevator_stair'],
                    'operations': ["combination", "segmentation", "classification"],
                }
            },
        },
        106011: {
            'name': '住宅建筑安全出口的设置应符合下列规定：',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "elevator_box",
                                                                                    "elevator_door", "elevator_stair"],
                    'operations': ["combination", "segmentation", "classification"],
                }
            },
        },
        106012: {
            'name': '七层及七层以上住宅建筑入口平台宽度不应小于2．00m，七层以下住宅建筑入口平台宽度不应小于1．50m。',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION, DrawingType.SECTION): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "elevator_box",
                                                                                    "elevator_door", "elevator_stair"],
                    'operations': ['combination', 'classification', 'segmentation'],
                }
            },
        },
        106021: {
            'name': '消防电梯应符合下列规定：电梯的载重量不应小于800kg；',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': [],
                },
            },
        },
        106027: {
            'name': '消防电梯应符合下列规定：电梯的载重量不应小于800kg；',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.SECOND_THIRD_FLOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
                (DrawingType.ELEVATION,): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'],
                    'operations': ['combination', 'classification'],
                },
            },
        },
        103064: {
            'name': '每套住宅的自然通风开口面积不应小于地面面积的5％',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window"],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
                (DrawingType.DOOR_WINDOW_DAYANG,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window", "elevation_window", "elevation_window_open_line"],
                    'operations': ['combination', 'classification'],
                },
            },
        },
        103068: {
            'name': '卫生间不应直接布置在下层住户的卧室、起居室（厅）、厨房和餐厅的上层。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
            },

        },
        103076: {
            'name': '位于阳台、外廊及开敞楼梯平台下部的公共出入口，应采取防止物体坠落伤人的安全措施',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR, ): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door"],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
                (DrawingType.SECOND_THIRD_FLOOR,): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['second_third_segment'],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
            },
        },
        104048: {
            'name': '卫生间不应直接布置在下层住户的卧室、起居室（厅）、厨房和餐厅的上层。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
            },
        },
        104049: {
            'name': '每套住宅的自然通风开口面积不应小于地面面积的5％',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window"],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
                (DrawingType.DOOR_WINDOW_DAYANG,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window", "elevation_window", "elevation_window_open_line"],
                    'operations': ['combination', 'classification'],
                },
            },
        },
        115001: {
            'name': '地下工程应进行防水设计',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        104023: {
            'name': '住宅地下室应采取有效防水措施',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            }
        },
        104029: {
            'name': '住宅屋面和外墙的内表面在室内温、湿度设计条件下不应出现结露。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        110004: {
            'name': '住宅屋面和外墙的内表面在室内温、湿度设计条件下不应出现结露。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        110005: {
            'name': '住宅屋面和外墙的内表面在室内温、湿度设计条件下不应出现结露。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        110006: {
            'name': '613消防控制室等重要房间，其顶棚和墙面应采用A级装修材料，地面及其他装修应。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        110007: {
            'name': '建筑物内的厨房，其顶棚、墙面、地面均应采用A级装修材料。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        110008: {
            'name': '涂膜防水层设计应以厚度表示，不得以遍数表示。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN, DrawingType.ENGINEERING_WORK,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ["text_information"],
                }
            },
        },
        108008: {
            'name': '机动车库的服务半径不宜大于500m，非机动车库的服务半径不宜大于100m。',
            'type': MultiBorderPipelineType.TYPE_D,
            'borders': {
                (DrawingType.SITE_PLAN_BUILDING,): {
                    'major_drawing': True,
                    'entities': ['building', 'axis_grid'],
                    'operations': ['segmentation'],
                },
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.UNDERGROUND): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'] + ['door'],
                    'operations': ['segmentation'],
                },
            },
        },
        108009: {
            'name': '机动车库基地出入口应设置减速安全设施。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.PODAO, ): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': [],
                }
            },
        },
        105018: {
            'name': '停车场和车库应符合下列规定：1 居住区停车场和车库的总停车位应设置不少于0.5%的无障碍机动车停车位',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN, ): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ["text_information"],
                },
                (DrawingType.UNDERGROUND,): {
                    'major_drawing': True,
                    'entities': ["parking"],
                    'operations': [],
                }
            },
        },
        106028: {
            'name': '建筑内的电梯井等竖井应符合下列规定： 1 电梯井应独立设置，井内严禁敷设可燃气体和甲、乙、丙类液体管道，不应敷设与电梯无关的电缆、电线等。电梯井的井壁除设置电梯门、安全逃生门和通气孔洞外，不应设置其他开口 3 建筑内的电缆井、管道井应在每层楼板处采用不低于楼板耐火极限的不燃材料或防火封堵材料封堵。建筑内的电缆井、管道井与房间、走道等相连通的孔隙应采用防火封堵材料封堵4 建筑内的垃圾道宜靠外墙设置，垃圾道的排气口应直接开向室外，垃圾斗应采用不燃材料制作，并应能自行关闭。5 电梯层门的耐火极限不应低于1．00h，并应符合现行国家标准《电梯层门耐火试验 完整性、隔热性和热通量测定法》GB／T 27903规定的完整性和隔热性要求。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'window',
                                                                                    'pipe', 'elevator_door', 'annotation_line'],
                    'operations': ["combination", "segmentation", "classification"],
                },
                (DrawingType.STAIR_DAYANG, ): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'window',
                                                                                    'pipe', 'elevator_door', 'annotation_line'],
                    'operations': ["combination", "segmentation", "classification"],
                },
                (DrawingType.BUILDING_DESIGN, ): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ["text_information"],
                 },
            },
        },
        107012: {
            'name': '当室外消防水池设有消防车取水口(井)时，应设置消防车到达取水口(井)的消防车道和消防车回车场地',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.XIAOFANG_SITE_PLAN,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'] + ['door', 'window',  "red_line", "red_line_sub", "road_center_line", "road", "fire_road", 'garage_exit', 'annotation_line'],
                    'operations': ["combination", "segmentation", "classification", "text_information"],
                },
                (DrawingType.SITE_PLAN_ROAD,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'] + ['door', 'window',  "red_line", "red_line_sub", "road_center_line", "road", "fire_road", 'garage_exit', 'annotation_line'],
                    'operations': ["combination", "segmentation", "classification", "text_information"],
                },
            },
        },
        104042: {
            'name': '每个住宅单元至少应有一个出入口可以通达机动车。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.SITE_PLAN_BUILDING,): {
                    'major_drawing': True,
                    'entities': ['building', 'axis_grid'],
                    'operations': ['segmentation'],
                },
                (DrawingType.INDOOR_FIRST_FLOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'] + ['door'],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
            },
        },
        103065: {
            'name': '采用自然通风的房间，其直接或间接自然通风开口面积应符合相应规定。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                    ["door", "window"],
                    'operations': ["combination", "classification", "segmentation"],
                },
                (DrawingType.DOOR_WINDOW_DAYANG,): {
                    'major_drawing': True,
                    'entities': ["door", "window", "elevation_window", "elevation_window_open_line"],
                    'operations': ["combination", "classification"],
                }
            },
        },
        106018: {
            'name': '尽头式消防车道应设置回车道或回车场，回车场的面积不应小于12m×12m；对于高层建筑，不宜小于15m×15m；',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.SITE_PLAN_ROAD,): {      # 提取车道线
                    'major_drawing': True,
                    'entities': ["road",  "road_center_line", "red_line", "building"],
                    'operations': ["segmentation"],
                },
                (DrawingType.SITE_PLAN_BUILDING,): {  # 提取轮廓
                    'major_drawing': True,
                    'entities': ["road", "road_center_line", "red_line", "building"],
                    'operations': ["segmentation"],
                },
                (DrawingType.XIAOFANG_SITE_PLAN,): {  # 消防总平面图
                    'major_drawing': True,
                    'entities': ["road", "road_center_line", "red_line", "building"],
                    'operations': ["segmentation"],
                },
            },
        },
        103073: {
            'name': '当阳台或建筑外墙设置、空调室外机时，其安装位置应符合规定。',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                ["air_conditioner", "air_conditioner_mix", "window", "plan_handrail"],
                    'operations': ['combination', 'classification', 'segmentation'],
                },
                (DrawingType.DOOR_WINDOW_DAYANG,): {
                    'major_drawing': False,
                    'entities': ["window", "elevation_window", "elevation_window_open_line"],
                    'operations': ['combination', 'classification'],
                },
            },
        },
        106022: {
            'name': '消防控制室的设置应符合规定。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR_FIRST_FLOOR, DrawingType.UNDERGROUND): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                ["door", "window", "elevator_stair", "elevator_box"],
                    'operations': ["combination", "classification", "segmentation"],
                }
            },
        },
        106025: {
            'name': '建筑高度大于100m的住宅建筑应设置避难层，避难层的设置应符合本规范第5．5．23条有关避难层的要求。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR, DrawingType.BINANCENG,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window", "elevator_box", "fire_hydrant"],
                    'operations': ["combination", "classification", "segmentation"],
                },
                (DrawingType.ELEVATION,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window", "elevator_box", "fire_hydrant", "elevation_mark", "elevate_biaogao"],
                    'operations': [],
                },
                (DrawingType.DOOR_WINDOW_DAYANG,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window", "elevator_box",
                                                                                    "elevation_window", "elevation_window_open_line"],
                    'operations': ["combination", "classification"],
                }
            },
        },
        106026: {
            'name': '建筑高度大于54m的住宅建筑，每户应有一间房间符合下列规定：1 应靠外墙设置，并应设置可开启外窗；2 内、外墙体的耐火极限不应低于1．00h，该房间的门宜采用乙级防火门，外窗的耐火完整性不宜低于1．00h。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window", "elevator_box"],
                    'operations': ["combination", "classification", "segmentation"],
                },
                (DrawingType.DOOR_WINDOW_DAYANG, ): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window", "elevator_box",
                                                                                    "elevation_window", "elevation_window_open_line"],
                    'operations': ["combination", "classification"],
                }
            },
        },
        111004: {
            'name': '汽车库室内任一点至最近人员安全出口的疏散距离不应大于45m，当设置自动灭火系统时，其距离不应大于60m。 对于单层或设置在建筑首层的汽车库，室内任一点至室外最近出口的疏散距离不应大于 60m。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.UNDERGROUND,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["basic"] +
                                LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                                ["door", "window"],
                    'operations': ["combination", "classification", "segmentation"],
                },
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': [],
                }
            },
        },
        103075: {
            'name': '七层及七层以上住宅电梯应在设有户门和公共走廊的每层设站。住宅电梯宜成组集中布置。',
            'type': MultiBorderPipelineType.TYPE_A,
            'borders': {
                (DrawingType.ELEVATION,): {
                    'major_drawing': False,
                    'entities': LayerConfig.BASIC_LAYERS.value['basic'],
                    'operations': [],
                },
                (DrawingType.INDOOR_FIRST_FLOOR,DrawingType.INDOOR,): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window", "elevator_box"],
                    'operations': ["combination", "segmentation", "classification"],
                }
            },
        },
        104054: {
            'name': '住宅建筑楼梯间顶棚、墙面和地面均应采用不燃性材料。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN, DrawingType.ENGINEERING_WORK,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ['text_information'],
                }
            },
        },
        103079: {
            'name': '在设计说明中查找是否有“住宅污染室内污染物限值表”，若有则结束审查',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.BUILDING_DESIGN,): {
                    'major_drawing': True,
                    'entities': [],
                    'operations': ["text_information"],
                }
            },
        },
        103042: {
            'name': '厨房的使用面积应符合下列规定：1 由卧室、起居室（厅）、厨房和卫生间等组成的住宅套型的厨房使用面积，不应小于4．0m2；2 由兼起居的卧室、厨房和卫生间等组成的住宅最小套型的厨房使用面积，不应小于3．5m2。',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window"],
                    'operations': ["combination", "classification", "segmentation"],
                }
            },
        },
        103048: {
            'name': '套型的使用面积应符合下列规定：1 由卧室、起居室（厅）、厨房和卫生间等组成的套型，其使用面积不应小于30m2； 2 由兼起居的卧室、厨房和卫生间等组成的最小套型，其使用面积不应小于22m2',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window"],
                    'operations': ["combination", "classification", "segmentation"],
                }
            },
        },
        106006: {
            'name': '防烟楼梯间除应符合本规范第6．4．1条的规定, 还需符合其他规定',
            'type': MultiBorderPipelineType.TYPE_C,
            'borders': {
                (DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.UNDERGROUND): {
                    'major_drawing': True,
                    'entities': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ["door", "window", "pillar", "pipe"],
                    'operations': ["combination", "classification", "segmentation"],
                }
            },
        },
    }
