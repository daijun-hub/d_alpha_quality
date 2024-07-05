from .electric.drawing_config import DrawingType as electric_drawing_type
from .architecture.drawing_config import DrawingType as architecture_drawing_type
from .plumbing.drawing_config import DrawingType as plumbing_drawing_type

class ComparisonRuleConfig:
    
    RULE = {
        "1503001":{
            "model_drawing": {
                "major_drawing": electric_drawing_type.DIANQI.value,
                "minor_drawing_list": []
            },
            "huo_liang_drawing": {
                "major_drawing": electric_drawing_type.DIANQI.value,
                "minor_drawing_list": []
            }
        },
        "1503002": {
            "model_drawing": {
                "major_drawing": electric_drawing_type.DIANQI.value,
                "minor_drawing_list": []
            },
            "huo_liang_drawing": {
                "major_drawing": electric_drawing_type.DIANQI.value,
                "minor_drawing_list": []
            }
        },
        "1103001": {
            "model_drawing": {
                "major_drawing": architecture_drawing_type.INDOOR.value,
                "minor_drawing_list": []
            },
            "huo_liang_drawing": {
                "major_drawing": architecture_drawing_type.INDOOR.value,
                "minor_drawing_list": []
            }
        },
        "1103002": {
            "model_drawing": {
                "major_drawing": architecture_drawing_type.INDOOR.value,
                "minor_drawing_list": [architecture_drawing_type.DOOR_WINDOW_DAYANG.value]
            },
            "huo_liang_drawing": {
                "major_drawing": architecture_drawing_type.INDOOR.value,
                "minor_drawing_list": [architecture_drawing_type.DOOR_WINDOW_DAYANG.value]
            }
        },
        "1103003": {
            "model_drawing": {
                "major_drawing": architecture_drawing_type.INDOOR.value,
                "minor_drawing_list": [architecture_drawing_type.DOOR_WINDOW_DAYANG.value]
            },
            "huo_liang_drawing": {
                "major_drawing": architecture_drawing_type.INDOOR.value,
                "minor_drawing_list": [architecture_drawing_type.DOOR_WINDOW_DAYANG.value]
            }
        },
        "1103004": {
            "model_drawing": {
                "major_drawing": architecture_drawing_type.INDOOR.value,
                "minor_drawing_list": [architecture_drawing_type.DOOR_WINDOW_DAYANG.value]
            },
            "huo_liang_drawing": {
                "major_drawing": architecture_drawing_type.INDOOR.value,
                "minor_drawing_list": [architecture_drawing_type.DOOR_WINDOW_DAYANG.value]
            }
        },
        "1103005": {
            "model_drawing": {
                "major_drawing": architecture_drawing_type.INDOOR.value,
                "minor_drawing_list": [architecture_drawing_type.DOOR_WINDOW_DAYANG.value]
            },
            "huo_liang_drawing": {
                "major_drawing": architecture_drawing_type.INDOOR.value,
                "minor_drawing_list": [architecture_drawing_type.DOOR_WINDOW_DAYANG.value]
            }
        },
        "1603001": {
            "model_drawing": {
                "major_drawing": architecture_drawing_type.ENGINEERING_WORK.value,
                "minor_drawing_list": []
            },
            "huo_liang_drawing": {
                "major_drawing": architecture_drawing_type.ENGINEERING_WORK.value,
                "minor_drawing_list": []
            }
        }
    }