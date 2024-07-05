from ..base_type import EntityBaseType
from ..entity import Entity, ClassifiedEntity
from ...border_entity import BorderEntity
from ...utils.utils_entity import get_form, get_distance_to_wall, get_install_height


# 合并且分类类型
class XinXiChaZuo(ClassifiedEntity):
    
    chinese_name = "信息插座"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "信息插座"
        self.entity_base_type = EntityBaseType.DATA_DEVICE
        self.distance_to_wall = get_distance_to_wall(self.chinese_name, self.bounding_rectangle.list, border_entity)
        # 获取安装高度
        height_target_pattern = r'插座[均]?距地(\s*[\d]+[.]?[\d]*\s*[cmd]?)m'
        self.install_height, self.install_height_bbox = get_install_height("插座", self.bounding_rectangle.list, border_entity, height_target_pattern)
