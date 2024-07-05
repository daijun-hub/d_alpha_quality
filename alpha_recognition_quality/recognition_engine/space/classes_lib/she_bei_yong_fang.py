from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity
from ...utils import space_use_attribute


# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加

class SheBeiYongFang(Space):
    chinese_name = "设备用房"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "设备用房"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE
        # 获取设备用房空间内文本，根据文本确定属性值，具体如下：
        # ①若含“送风”文本，则属性值为送风机房
        # ②若含“排风”文本，则属性值为排风机房
        # ③若含“通信”文本，则属性值为通信机房
        # ④若含“垃圾”文本，则属性值为室内垃圾房
        # ⑤若含“消防水池”文本，则属性值为消防水池
        # ⑥若含“进线”文本，则属性值为进线站
        # ⑦若含“换热”文本，则属性值为换热站
        # ⑧若含“加压”文本，则属性为加压机房
        # 若不符合以上情况，则属性值为一般设备用房
        key_words_dict = {
            "送风机房": ["送风"],
            "排风机房": ["排风"],
            "通信机房": ["通信"],
            "室内垃圾房":["垃圾"],
            "消防水池": ["消防水池"],
            "进线站": ["进线"],
            "换热站": ["换热"],
            "加压机房": ["加压"],
        }
        self.device_room_type = space_use_attribute(space_object, border_entity, key_words_dict, "一般设备用房")


if __name__ == "__main__":
    pass
