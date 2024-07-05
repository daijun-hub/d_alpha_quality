from enum import Enum

from .drawing_config import DrawingType


class Entity_Operation_Config(Enum):
    entity_operation_config = {
        DrawingType.IGNORE: {'entities': [], 'operations': []},
        DrawingType.DECORATION_KITCHEN_ELEVATION:{
            'entities':['wall'],
            'operations':['combination']
        },
        DrawingType.DECORATION_BATHROOM_ELEVATION:{
            'entities': ['wall'],
            'operations': ['combination']
        }
    }
