from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils.utils_entity import get_form


class ShuangQieKaiGuan(ClassifiedEntity):
    
    chinese_name = "双切开关"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "双切开关"
        self.entity_base_type = EntityBaseType.ELECTRIC_DEVICE
        # 碧桂园产品要求添加属性-形式，本质为要通过此属性区分不同图例。
        self.form = get_form(entity_object.bounding_rectangle.list, border_entity, self.chinese_name)