
from typing import List, Dict, Union
from collections import defaultdict
from uuid import uuid1
import json

import numpy as np

from .base_type import SpaceBaseType
from ..base.contour import Contour
from ..base.bounding_rectangle import BoundingRectangle
from ..entity.entity import GraphicBasicEntity
from ...common.utils import convert_bbox_to_range, convert_contour_to_CAD_coord, convert_contour_to_dot_set
from ...common.utils import convert_bbox_to_CAD_coord, attributes_handle
from ...config_manager.object_storage_config import SpaceStorageConfig


class Space(object):
    """空间类，分割后的精准空间"""
    def __init__(self,
                 contour: Contour,
                 bbox: BoundingRectangle,
                 name_list: List[str],
                 is_small_room: bool = False,
                 electric_distribution_box_number: str = '',
                 install_power: float = 0.0,
                 required_factor: float = 0.0,
                 power_factor: float = 0.0,
                 calculated_electricity: float = 0.0,
                 usage: str = ''):

        # 基础属性（Required）#
        self.chinese_name = "空间基类"                   # 空间类别中文名
        self.contour = contour                          # 空间轮廓
        self.area = contour.area                        # 面积 - 单位：平方米
        self.bbox = bbox                                # 空间位置（外接矩形）
        self.name_list = list(set(name_list))                      # 名称列表
        self.is_small_room = is_small_room              # 是否是小房间
        self.space_base_type = SpaceBaseType.BASE       # 对象父类
        
        self.inner_space_dict: Dict[str, List[Space]] = defaultdict(list)                   # 内部细分空间列表

        # 特有属性（Optional）

        # "配电箱子图" 空间属性
        self.electric_distribution_box_number = electric_distribution_box_number    # 配电箱编号属性
        self.usage = usage                               # 用途属性
        self.install_power = install_power               # 安装功率属性
        self.required_factor = required_factor           # 需要系数属性
        self.power_factor = power_factor                 # 功率因数属性
        self.calculated_electricity = calculated_electricity                        # 计算电流属性
        self.main_switch_bbox_list = None                # 配电箱子图主开关列表
        self.title_info = None                           # 配电箱子图的标题信息
        self.wire_line_list = None                       # 配电箱子图包含的电线列表
        self.switch_bbox_list = None                     # 配电箱子图包含的开关列表
        self.text_list = None                            # 配电箱子图包含的文本列表

        self.labeled_height = None                      # 标高

        self.turning_radius = None                      # 转弯半径
        self.gradient = None                            # 坡度
        self.shape = None                               # 形状

        self.bedroom_type = None                        # 卧室细分类型
        self.balcony_type = None                        # 阳台细分类型
        self.lobby_type = None                          # 大堂细分类型
        self.kitchen_type = None                        # 厨房细分类型
        self.front_room_type = None                     # 前室细分类型
        self.stair_room_type = None                     # 楼梯间细分类型
        self.elevator_well_type = None                  # 电梯井细分类型
        self.pipe_well_type = None                      # 管道井细分类型
        self.pump_room_type = None                      # 水泵房细分类型
        self.device_room_type = None                    # 设备用房细分类型
        self.turnaround_type = None                     # 回车场细分类型
        self.accessible_ramp_type = None                # 无障碍坡道细分类型
        self.vehicle_passage_way_type = None            # 车型出入口细分类型
        self.wall_type = None                           # 墙体细分类型
        self.attached_public_room_type = None           # 附建公共用房细分类型

        self.road_amount = None                         # 道路条数

        self.building_width = None                      # 屋顶层建筑最大宽度
        self.building_length = None                     # 屋顶层建筑最大长度
        
        self.uuid = uuid1().hex

        # {'普通窗': [chuang_obj1, chuang_obj2], ...}
        self.related_entities_dict = {}                 # 与空间相关联的构件字典
        self.matched_with_model_entities_dict = {}      # 记录已经和板房中同类的构件进行了一一对应的构件，后续只稽查已经匹配了的构件
        self.related_space_dict = {}                    # 用于添加套内水管井

        # 保存空间拓扑关系中RoomNode对象的属性信息
        self.rectified_contour = None
        self.rectified_contour_flip = None

        # TODO: 1004添加
        self.floor = None                               # 空间所在楼层，str类型，如"地下层"、"一层"、"机房层"等
        self.related_wall = None                        # 空间关联墙体
        self.related_door = None                        # 空间关联的门
        self.related_window = None                      # 空间关联的窗户
        self.related_hole = None                        # 空间关联的洞口
        self.is_close_space = None                      # 空间是否为封闭空间
        self.is_refuge_space = None                     # 空间是否为避难间
        self.space_length = None                        # 空间长度
        self.space_width = None                         # 空间宽度
        self.space_perimeter = None                     # 空间周长

    def copy(self, space_object: 'Space') -> None:
        """
        Space的Copy Constructor。仅复制基础属性

        Args:
            space_object (Space): room_info中的Space对象
        """
        # TODO：调整基础属性入参
        Space.__init__(
            self,
            space_object.contour,
            space_object.bbox,
            space_object.name_list,
            space_object.is_small_room,
        )
        self.uuid = space_object.uuid

    def to_dict(self):
        d = {}
        for key, value in vars(self).items():
            if value is not None:
                d[key] = value
        
        return d

    def to_json(self, drawing_id: int, border_coord, ratio, scale) -> Union[Dict, None]:
        d = self.to_dict()
        space_type_id = SpaceStorageConfig.storage_id_dict.get(d["chinese_name"], "")
        # if not space_type_id:
        #     print(f"[Objectification] Cannot find {d['chinese_name']} in SpaceStorageConfig.")
        #     return {}
        j = {
            "drawingId": drawing_id,
            "spaceTypeId": space_type_id
        }
        private_attr = {}
        for key, value in d.items():
            # 根据object的key处理value（PNG -> CAD, etc.)
            if key == "contour":
                final_value = convert_contour_to_CAD_coord(border_coord, value.contour, ratio, scale)
                final_value = convert_contour_to_dot_set(final_value)
                final_value = str(final_value)
            elif key == "bbox":
                final_value = convert_bbox_to_CAD_coord(border_coord, value.list, ratio, scale)
                final_value = convert_bbox_to_range(final_value)
                final_value = str(final_value)
            elif key == "uuid":
                continue
            else:
                final_value = value

            # 根据中台的要求处理key
            if key in SpaceStorageConfig.attribute_map:
                j[SpaceStorageConfig.attribute_map[key]] = final_value
            elif key in SpaceStorageConfig.attribute_filter:
                continue
            else:
                try:
                    if isinstance(final_value, np.ndarray):
                        final_value = final_value.tolist()
                    elif isinstance(final_value, np.int64):
                        final_value = str(final_value)
                    elif isinstance(final_value, list) or isinstance(final_value, BoundingRectangle):
                        final_value = [str(i) for i in final_value]
                    else:
                        try:
                            final_value = json.dumps(final_value)
                        except Exception as e:
                            print(f"Entity dumping attribute {final_value} failed: {str(e)}")
                            final_value = attributes_handle(final_value)
                except Exception as e:
                    print(f"Space {self.chinese_name} dumping attribute {key} failed: {str(e)}")
                    continue
                private_attr[key] = final_value

        j["attributes"] = private_attr
        return j
    
    def is_inner_space(self, other_space):
        contour_iou = self.contour.get_iou(other_space.contour)
        return contour_iou > 0.9 and self.area > other_space.area

# if __name__ == "__main__":
#     a = Space(None, None, None, None)
#     b = Space(a)
