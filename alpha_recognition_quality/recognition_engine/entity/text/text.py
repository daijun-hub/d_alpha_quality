
from ....config_manager.text_config import TextType
from ...base.bounding_rectangle import BoundingRectangle
from ...base.bounding_vertex import BoundingVertex


class TextEntity(object):
    """文本构件类"""
    def __init__(self,
                 bbox: BoundingRectangle,
                 text_type: TextType,
                 extend_message: str,
                 layer: str,
                 ):
        self.bbox = bbox
        self.text_type = text_type
        self.layer = layer
        self.extend_message = extend_message

    def to_dict(self):
        d = {
            "bbox": self.bbox.list,
            "type": self.text_type.value,
            "layer": self.layer,
            "extend_message": self.extend_message
        }
        return d


class TextEntityWithBoundVertex(object):
    def __init__(self,
                 bbox: BoundingVertex,
                 text_type: TextType,
                 extend_message: str,
                 ):
        self.bbox = bbox
        self.type = text_type
        self.extend_message = extend_message
