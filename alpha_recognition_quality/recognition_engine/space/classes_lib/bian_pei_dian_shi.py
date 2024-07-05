from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity

from ...utils import get_labeled_height_plumping
from ....config_manager.text_config import TextType
from ....config_manager.architecture.drawing_config import DrawingType as DrawingTypeArchi


class BianPeiDianShi(Space):
    chinese_name = "变配电室"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "变配电室"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE
        # self.labeled_height = get_labeled_height_plumping(self.contour.contour, border_entity)
        self.is_close_space = True
        self.floor = self._get_floor(border_entity)
        self.labeled_height = self._get_biaogao(border_entity)
        # self.contour_area = self._get_contour_are()

    def _get_floor(self, border_entity):
        drawing_type = border_entity.drawing_type
        if drawing_type == DrawingTypeArchi.UNDERGROUND:
            return '地下层'
        elif drawing_type == DrawingTypeArchi.INDOOR_FIRST_FLOOR:
            return '一层'

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


if __name__ == "__main__":
    pass
