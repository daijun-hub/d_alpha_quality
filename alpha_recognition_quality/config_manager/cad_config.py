from enum import Enum

from .cad_task_config import CADTaskType

from ..config import config_obj

class CADTaskUrl:
    pl_cad_url = config_obj.CAD_SERVICE

    TASK_CREATE_URL = {
        CADTaskType.CREATE_TASK: f"{pl_cad_url}/api/v2/cad_parser",
        CADTaskType.BORDER_TASK: f"{pl_cad_url}/api/v1/border_info/task",
    }
    
    TASK_STATUS_CHECK_URL = {
        CADTaskType.CREATE_TASK: f"{pl_cad_url}/api/v2/cad_parser/{{task_id}}",
    }
    
class CADDrawingUrl:
    CAD_URL = config_obj.CAD_DRAWING_HOST
    CAD_DRAWING_BASE_ROUTE = '/api/v2/cad_draw'
    CAD_DRAWING_STATUS_ROUTE = '/api/v2/cad_draw/{task_id}'
    CAD_DRAWING_URL = f"{CAD_URL}{CAD_DRAWING_BASE_ROUTE}"
    CAD_DRAWING_STATUS_URL = f"{CAD_URL}{CAD_DRAWING_STATUS_ROUTE}"
    
    
