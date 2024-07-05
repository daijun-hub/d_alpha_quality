from ....analysis_engine.base.basic_entity import CADBasicEntity
from ...entity import EntityBusinessInfo
from typing import List


# TODO: 评估是否需要独立填充构件
class HatchEntity(object):
    """填充构件类"""
    def __init__(self,
                 origin_basic_entity_list: List[CADBasicEntity],
                 entity_business_info: EntityBusinessInfo,
                 *args,
                 **kwargs):
        pass
