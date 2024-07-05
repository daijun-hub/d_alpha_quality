from enum import Enum

from .drawing_config import DrawingType


class Entity_Operation_Config(Enum):
    entity_operation_config = {
        DrawingType.IGNORE: {'entities': [], 'operations': []},
        DrawingType.DECORATION_HVAC_VENTILATION_PLAN: {
            'entities': ["air_conditioner",
                         "door",
                         "window",
                         "wall",
                         "pillar",
                         "wall_hatch",
                         "segment",
                         "segment_extra",
                         "axis_net",
                         "annotation_line"],
            'operations': ['combination',
                           'classification',
                           'segmentation',
                           'text_information']
        },
        DrawingType.DECORATION_HEATING_DESCRIPTION: {
            'entities': ['wall',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'building',
                         'engineering_work_table_line'],
            'operations': ['text_information']
        },
        DrawingType.HEATING_PLAN: {
            'entities': [],
            'operations': [],
        },
    }
