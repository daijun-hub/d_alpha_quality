from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity

from ...utils import get_labeled_height_plumping


class XiaoFangShuiBengFang(Space):
    chinese_name = "消防水泵房"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "消防水泵房"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE
        # 标高数值属性
        self.labeled_height = get_labeled_height_plumping(self.contour.contour, border_entity)


if __name__ == "__main__":
    pass
