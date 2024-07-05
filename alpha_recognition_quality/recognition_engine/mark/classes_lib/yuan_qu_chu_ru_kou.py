from ..mark import Mark
from ...entity.entity import ProcessedGBEStruct


class YuanQuChuRuKou(Mark):
    """
    对于标记类，需要实现__init__和create_object_list方法。
    """
    chinese_name = "园区出入口"

    def __init__(self, p_gbes: ProcessedGBEStruct) -> None:
        Mark.copy(self, p_gbes)

        self.chinese_name = "园区出入口"