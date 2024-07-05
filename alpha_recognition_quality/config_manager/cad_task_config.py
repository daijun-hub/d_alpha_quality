from enum import Enum


class CADTaskStatus(Enum):
    PENDING = 'pending'
    FINISHED = 'finished'


class CADTaskType(Enum):
    CREATE_TASK = 'create_task'
    LAYER_TASK = 'layer_task'
    BORDER_TASK = 'border_task'
    VIEWPORT_TASK = 'viewport_task'
    PRIMITIVE_TASK = 'primitive_task'
    PRINTING_TASK = 'printing_task'
    INFORMATION_TASK = "information_task"
    AXIS_TASK = "axis_task"


class CADTaskConfig(Enum):

    TASK_CALLBACK_ID = {
        0: CADTaskType.CREATE_TASK,
        1: CADTaskType.LAYER_TASK,
        2: CADTaskType.BORDER_TASK,
        4: CADTaskType.PRINTING_TASK,
        5: CADTaskType.PRIMITIVE_TASK,
        6: CADTaskType.VIEWPORT_TASK,
        7: CADTaskType.INFORMATION_TASK,
        8: CADTaskType.AXIS_TASK
    }
