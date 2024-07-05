from .architecture.drawing_config import DrawingType as JZType
from .electric.drawing_config import DrawingType as DQType
from .hvac.drawing_config import DrawingType as NTType
from .structure.drawing_config import DrawingType as JGType
from .plumbing.drawing_config import DrawingType as GPSType

from .electric.layer_config import LayerConfig as DQLayerConfig
from .structure.layer_config import LayerConfig as JGLayerConfig

from .major_config import MajorConfig
from .multiple_border_pipeline_config import MultiBorderPipelineType



class CrossMajorRuleConfig:
    CONFIGURATION = {

        # 跨专业配置
        "1302006": {
            'name': '建筑高度小于或等于 54m 且每单元设置一部疏散楼梯的住宅，采用1支消防水枪的1股充实水柱到达室内任何部位，不必采用2股水柱',
            'type': MultiBorderPipelineType.TYPE_C,

            'majors': {
                MajorConfig.ARCHITECTURE:{
                    "main_major":False,
                    "borders":{
                        (JZType.ELEVATION,):{
                            'major_drawing':False,
                        },
                    },
                },
                MajorConfig.PLUMBING:{
                    'main_major': True,
                    'borders':{
                        (GPSType.TOWER_WATER_SUPPLY,):{
                            'major_drawing':True,
                        },
                        (GPSType.TOWER_SECOND_FLOOR_SUPPLY,): {
                            'major_drawing': True,
                        },
                    },
                },
            },
        },
        # 跨专业配置
        "1104039": {
            'name': '生活阳台实际大小不满足洗衣机放置的空间需求',
            'type': MultiBorderPipelineType.TYPE_C,
            'majors': {
                MajorConfig.ARCHITECTURE: {
                    "main_major": True,
                    "borders": {
                        (JZType.INDOOR, JZType.INDOOR_FIRST_FLOOR): {
                            'major_drawing': True,
                            'entities': DQLayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"],
                            'operations': ['combination', 'classification', 'segmentation'],
                        },
                    },
                },
                MajorConfig.ELECTRIC: {
                    'main_major': False,
                    'borders': {
                        (DQType.DIANQI,): {
                            'major_drawing': False,
                            'entities': DQLayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"],
                            'operations': ['combination', 'classification', 'segmentation'],
                        },
                    },
                },
            },
        },
        "1204002": {
            'name': '结构设计中梁偏向位置不合理',
            'type': MultiBorderPipelineType.TYPE_C,
            'majors': {
                MajorConfig.ARCHITECTURE: {
                    "main_major": True,
                    "borders": {
                        (JZType.INDOOR,): {
                            'major_drawing': True,
                            'entities': DQLayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window",
                                                                                              "axis_net", "axis_grid"],
                            'operations': ['combination', 'classification', 'segmentation'],
                        },
                    },
                },
                MajorConfig.STRUCTURE: {
                    'main_major': False,
                    'borders': {
                        (JGType.BEAM_GRAPH,): {
                            'major_drawing': False,
                            'entities': ["beam", "axis_net", "axis_grid"],
                            'operations': ['combination'],
                        },
                    },
                },
            },
        },

        "1204001": {
            'name': '梁设置位置不合适，影响室内使用空间，梁不得穿越卧室室内、客厅及餐厅',
            'type': MultiBorderPipelineType.TYPE_C,
            'majors': {
                MajorConfig.ARCHITECTURE: {
                    "main_major": True,
                    "borders": {
                        (JZType.INDOOR,): {
                            'major_drawing': True,
                            'entities': DQLayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"],
                            'operations': ['combination', 'classification', 'segmentation'],
                        },
                    },
                },
                MajorConfig.STRUCTURE: {
                    'main_major': False,
                    'borders': {
                        (JGType.BEAM_GRAPH,): {
                            'major_drawing': False,
                            'entities': ["axis_net", "axis_grid", "beam"],
                            'operations': ['combination', 'classification', 'segmentation'],
                        },
                    },
                },
            },
        },

        "1204003": {
            'name': '卫生间内侧梁顶标高是低于上层户内标高低20-30MM',
            'type': MultiBorderPipelineType.TYPE_C,
            'majors': {
                MajorConfig.ARCHITECTURE: {
                    "main_major": True,
                    "borders": {
                        (JZType.INDOOR,): {
                            'major_drawing': True,
                            'entities': DQLayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"],
                            'operations': ['combination', 'classification', 'segmentation'],
                        },
                    },
                },
                MajorConfig.STRUCTURE: {
                    'main_major': False,
                    'borders': {
                        (JGType.STRUCTURE_GRAPH,): {
                            'major_drawing': False,
                            'entities': ["axis_net", "axis_grid", "beam"],
                            'operations': ['combination', 'classification', 'segmentation'],
                        },
                    },
                },
            },
        },


    }

