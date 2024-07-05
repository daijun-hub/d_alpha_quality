from ..space import Space
from typing import List
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity
from ...utils.utils_space import space_use_attribute


# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加

class FuJianGongGongYongFang(Space):
    chinese_name = "附建公共用房"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "附建公共用房"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE
        # 获取附建公共用房空间内文本，根据文本获取细分类型属性值，具体如下：
        # ①若含“社区”文本，属性值为社区服务用房
        # ②若含“物业”文本，属性值为物业管理用房
        # ③若含“商业”、“商铺”、“商店”、“餐饮”文本，属性值为商业服务用房
        key_words_dict = {
            "社区服务用房": ["社区"],
            "物业管理用房": ["物业"],
            "商业服务用房":["商业","商铺","商店","餐饮"]
        }
        self.attached_public_room_type = space_use_attribute(space_object, border_entity, key_words_dict, None)


if __name__ == "__main__":
    pass
