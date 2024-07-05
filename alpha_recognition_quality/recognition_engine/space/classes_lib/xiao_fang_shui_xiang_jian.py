from ..space import Space
from ..base_type import SpaceBaseType
from typing import List
from ...border_entity import BorderEntity
from ....config_manager.architecture.drawing_config import DrawingType as DrawingTypeArchi
from ....config_manager.text_config import TextType


# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加

class XiaoFangShuiXiangJian(Space):
    chinese_name = "消防水箱间"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "消防水箱间"
        self.is_close_space = True
        self.floor = "机房层"
        self.labeled_height = self._get_biaogao(border_entity)

    def _get_biaogao(self, border_entity):
        # 获取标高信息
        elevation_text_info = border_entity.border_text_info[TextType.ELEVATION]
        biaogao_list = [text.bbox.list + [text.extend_message] for text in elevation_text_info]

        bg = []
        for biaogao in biaogao_list:
            bg_bbox = biaogao[0:4]
            w, h = (bg_bbox[2] - bg_bbox[0]), (bg_bbox[3] - bg_bbox[1])
            x1, y1, x2, y2 = (self.bbox[0] + w), (self.bbox[1] + h), (self.bbox[2] - w), (self.bbox[3] - h)
            if bg_bbox[0] > x1 and bg_bbox[1] > y1 and bg_bbox[2] < x2 and bg_bbox[3] < y2:
                h = float(biaogao[4])
                h = int(h * 1000) / 1000
                bg.append(h)
        if len(bg) > 0:
            return max(bg)
        else:
            return