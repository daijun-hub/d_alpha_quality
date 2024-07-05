from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity


# 分类构件
class BaiYeChuang(ClassifiedEntity):
    
    chinese_name = "百叶窗"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "百叶窗"
        self.entity_base_type = EntityBaseType.WINDOW

        self.width = self._get_baiye_width()
        # 有效系数，
        # 0.5（即实际通风口有效面积/实际百叶口面积
        self.effective_ventilation_area = 0.5

    def _get_baiye_width(self):
        width = max(abs(self.bounding_rectangle[2]-self.bounding_rectangle[0]),
            abs(self.bounding_rectangle[3]-self.bounding_rectangle[1]))
        height = min(abs(self.bounding_rectangle[2] - self.bounding_rectangle[0]),
            abs(self.bounding_rectangle[3] - self.bounding_rectangle[1]))

        # 如果构件水平或竖直
        if width // height > 3:
            return width

        # 如果构件倾斜
        return None


