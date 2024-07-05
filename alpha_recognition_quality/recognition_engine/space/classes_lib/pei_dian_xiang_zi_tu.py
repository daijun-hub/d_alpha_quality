from ..space import Space
from ..base_type import SpaceBaseType
from typing import List
from ...border_entity import BorderEntity


# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加

class PeiDianXiangZiTu(Space):
    chinese_name = "配电箱子图"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "配电箱子图"
        self.space_base_type = SpaceBaseType.SYSTEM_LOCATION
        self.electric_distribution_box_number = space_object.electric_distribution_box_number  # 配电箱编号属性
        self.install_power = space_object.install_power  # 安装功率属性
        self.required_factor = space_object.required_factor  # 需要系数属性
        self.power_factor = space_object.power_factor  # 功率因数属性
        self.calculated_electricity = space_object.calculated_electricity  # 计算电流属性
        self.usage = space_object.usage  # 用途属性
        self.main_switch_bbox_list = space_object.main_switch_bbox_list  # 主开关列表
        self.title_info = space_object.title_info  # 标题信息
        self.wire_line_list = space_object.wire_line_list  # 配电箱子图包含的电线列表
        self.switch_bbox_list = space_object.switch_bbox_list  # 配电箱子图包含的开关列表
        self.text_list = space_object.text_list  # 配电箱子图包含的文本列表
        self.switch_num = len(self.switch_bbox_list)       # 配电箱系统图的开关数目
