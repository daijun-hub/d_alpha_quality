import re
from ....common.utils import get_contour_from_bbox, get_contours_iou
from ....config_manager.text_config import TextType
from ..space import Space
from ..base_type import SpaceBaseType
from typing import List
from ...border_entity import BorderEntity


# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加

class ShangRenWuMian(Space):
    chinese_name = "上人屋面"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "上人屋面"

        # 所在楼层
        self.floor = '机房层'
        # 是否种植屋面
        self.is_plant_roof = self._judge_planting_roof(border_entity)

    def _judge_planting_roof(self, border_entity):
        is_planting_roof = False
        text_info = border_entity.border_text_info[TextType.ALL]
        planting_text_bbox_list = [text.bbox.list for text in text_info if re.search("种植", text.extend_message)]
        space_cnt = self.contour.contour
        for text_bbox in planting_text_bbox_list:
            text_cnt = get_contour_from_bbox(text_bbox)
            if get_contours_iou(space_cnt, text_cnt) > 0.3:
                is_planting_roof = True
                break
        return is_planting_roof