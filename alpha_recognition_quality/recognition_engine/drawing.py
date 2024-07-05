from typing import Dict, List, Tuple, Union

from .entity.entity import GraphicBasicEntity, Entity
from .space.space import Space
from .mark.mark import Mark
from .entity.text.text import TextEntity, TextEntityWithBoundVertex
from ..common.image_manager import ImageManager

class Drawing:
    """
    保存原始图元数据及对象的图框类，作为画图逻辑代码的入参
    """
    def __init__(self,
                drawing_name: str,
                originial_primitive: Dict[str, List[GraphicBasicEntity]],
                entity_list: List[Entity],
                space_list: List[Space],
                mark_list: List[Mark],
                border_text_info: Dict[str, List[TextEntity]],
                border_text_info_with_bound_vertex: Dict[str, List[TextEntityWithBoundVertex]],
                image_manager: ImageManager):
        pass

    def __deepcopy__(self, other_border):
        # 复制一个新的图框实例
        pass
