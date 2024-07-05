from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity


class LuZao(ClassifiedEntity):
    chinese_name = "炉灶"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        self.chinese_name = "炉灶"
        self.entity_base_type = EntityBaseType.KITCHEN_RESTROOM_OBJECT
        self.floor = None  # 待定要不要开发的意义
        self.location = "厨房"
        self.width, self.length = self.get_w_h(border_entity)

    def get_w_h(self, border_entity):
        ratio = border_entity.ratio
        w, h = self.bounding_rectangle[2] - self.bounding_rectangle[0], \
               self.bounding_rectangle[3] - self.bounding_rectangle[1]
        if w < h:
            return int(w / ratio[0]), int(h / ratio[1])
        if w >= h:
            return int(h / ratio[0]), int(w / ratio[1])