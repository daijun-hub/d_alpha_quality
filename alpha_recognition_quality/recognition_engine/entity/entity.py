import numpy as np
from ...common.utils import convert_bbox_to_range, convert_contour_to_CAD_coord, convert_contour_to_dot_set, \
    extend_margin
from ...common.utils import convert_bbox_to_CAD_coord, attributes_handle
from .base_type import EntityBaseType
from ...design_object.cad_base.cad_basic_entity_type import get_basic_entity_type
from ..base.contour import Contour
from ..base.bounding_rectangle import BoundingRectangle
from typing import List, Dict, Union
from ...config_manager.object_storage_config import EntityStorageConfig
from uuid import uuid1
import sys
import json


class GraphicBasicEntity(object):

    def __init__(self,
                 type_str: str,
                 layout_name: str,
                 layer_name: str,
                 coord: List[int],
                 extend_storage: str,
                 style: str,
                 line_weight,
                 color: str,
                 line_description: str,
                 bounds_vertexes: List[int] = None,
                 ):
        self.layout_name = layout_name
        self.layer_name = layer_name
        self.coord = coord  # TODO: 实现Coord类
        self.extend_storage = extend_storage
        self.style = style
        self.line_weight = line_weight
        self.bounds_vertexes = bounds_vertexes
        self.line_description = line_description
        self.color = color
        self.entity_type = get_basic_entity_type(type_str)


class ProcessedGBE(object):

    def __init__(self,
                 layer_name: str,
                 coord: List[int],
                 type_str: str,
                 style: str,
                 line_weight,
                 color: str,
                 line_description: str,
                 ):
        self.layer_name = layer_name
        self.coord = coord
        self.style = style  # Continuous、Dash等信息
        self.line_weight = line_weight
        self.line_description = line_description
        self.color = color
        self.entity_type = get_basic_entity_type(type_str)  # Line、Polyline等信息


class ProcessedGBEStruct(object):

    def __init__(self, layer_name, p_gbe_list: List[ProcessedGBE]) -> None:
        self.layer_name = layer_name
        self.p_gbe_list = p_gbe_list


class Entity(object):
    """标准构件类，定位和识别后的精准构件"""

    def __init__(self,
                 entity_class,
                 bounding_rectangle: BoundingRectangle,
                 CAD_bounding_rectangle: BoundingRectangle = None,
                 origin_class=None,
                 score: float = None,
                 anno_list: List[str] = [],
                 contour=None,
                 ):

        # 基础属性（Required）
        self.chinese_name = "构件基类"  # 构件名称中文名
        self.entity_base_type = EntityBaseType.BASE  # 对象父类

        self.entity_class = entity_class  # 构件类别（最终输出）
        self.bounding_rectangle = bounding_rectangle  # PNG坐标外接矩形
        # 基础属性（Optional）
        self.CAD_bounding_rectangle = CAD_bounding_rectangle  # CAD坐标外接矩形
        self.origin_class = origin_class  # 构件类别（分类模型输出）
        self.score = score  # 分类置信度
        self.contour = contour  # 构件轮廓
        self.lead_mark = anno_list  # 引线标注（含字符串的列表）

        # 自定义属性（Optional）
        self.start_end_point = None  # 起终点

        self.door_wall_width = None  # 门土建宽度
        self.door_height = None  # 门高度
        self.door_fire_resistance_level = None  # 门防火等级
        self.door_usage = None  # 门用途属性
        self.door_towards_direction = None  # 门朝向
        self.door_leaf_number = None  # 门开启扇数量
        self.door_angle = None  # 门开启角度
        self.door_orientation = None  # 门的朝向字符串，用于疏散门判断
        self.door_open_region_contour = None  # 门的开启范围，用contour来保存
        self.door_base_line = None  # 门的土建连线
        self.door_direction_line = None  # 门的朝向线

        self.is_outer_evacuating_door = False  # 是否是疏散外门

        self.wire_parameter = None  # 电缆规格属性

        self.light_amount = None  # 灯具数量属性

        self.outlet_amount = None  # 插座数量属性

        self.contactor_parameter = None  # 接触器参数属性
        self.contactor_type = None  # 接触器属性

        self.electric_meter_parameter = None  # 电表参数属性
        self.electric_meter_type = None  # 电表属性

        self.thermal_relay_parameter = None  # 热继电器参数属性
        self.thermal_relay_type = None  # 热继电器属性

        self.disconnector_type = None  # 断路器属性
        self.disconnector_parameter = None  # 断路器参数属性

        self.circuit_usage = None  # 回路用途属性
        self.circuit_phase_sequence = None  # 回路相序属性
        self.circuit_power = None  # 回路功率属性
        self.circuit_number = None  # 回路编号属性

        self.electric_distribution_box_number = None  # 配电箱编号

        self.window_is_outside = None  # 是否外窗
        self.window_fire_resistance_level = None  # 窗防火等级
        self.window_number = None  # 窗编号
        self.window_width = None  # 窗宽度
        self.window_height = None  # 窗高度
        self.window_open_area = None  # 窗开启面积（用宽、高直接计算）
        self.window_fan_shape_area = None  # 窗开启扇面积

        self.stair_type = None  # 楼梯细分类型

        self.pipe_diameter = None  # 管径

        self.wall_hatch_type = None  # 墙填充类型

        self.stair_long = None  # 楼梯梯段线长度
        self.stair_width = None  # 楼梯梯段线间距离

        self.uuid = uuid1().hex

        self.wall_center_line = None  # 墙中心线
        self.wall_thickness = None  # 墙厚度
        # 记录门窗构件在户型模版上的位置
        self.rectified_contour = None
        self.rectified_contour_flip = None

    def to_dict(self):
        d = {}
        for key, value in vars(self).items():
            if value is not None:
                d[key] = value

        return d

    def to_json(self, drawing_id: int, border_coord, ratio, scale) -> Union[Dict, None]:
        d = self.to_dict()
        entity_type_id = EntityStorageConfig.storage_id_dict.get(d["chinese_name"], "")
        # if not entity_type_id:
        #     print(f"[Objectification] Cannot find {d['chinese_name']} in EntityStorageConfig.")
        #     return {}
        j = {
            "drawingId": drawing_id,
            "elementTypeId": entity_type_id
        }
        private_attr = {}
        for key, value in d.items():
            # 根据object的key处理value（PNG -> CAD, [a, b, c, d] -> [[a, b], [c, d]], etc.)
            if key == "contour":
                final_value = value
                if isinstance(value, Contour):
                    final_value = value.contour
                # final_value = convert_contour_to_CAD_coord(border_coord, value1, ratio, scale)  # 目前contour的值是np_array
                # final_value = convert_contour_to_dot_set(final_value)
                # final_value = str(value)
                # final_value = value1
            elif key == "bounding_rectangle":
                final_value = convert_bbox_to_CAD_coord(border_coord, value.list, ratio, scale)
                final_value = convert_bbox_to_range(final_value)
                final_value = str(final_value)
            elif key == "start_end_point_list":
                final_value = [convert_bbox_to_range(convert_bbox_to_CAD_coord(border_coord, c, ratio, scale)) for c in
                               value]
                final_value = str(final_value)
            elif key == "lead_mark":
                final_value = str(value)
            elif key == "uuid":
                continue
            else:
                final_value = value

            # 根据中台要求出来value,针对枚举类型返回下标
            if d["chinese_name"] in EntityStorageConfig.storage_enum_dict and \
                    key in EntityStorageConfig.storage_enum_dict[d["chinese_name"]] and \
                    final_value in EntityStorageConfig.storage_enum_dict[d["chinese_name"]][key]:
                final_value = EntityStorageConfig.storage_enum_dict[d["chinese_name"]][key].index(final_value)

            # 根据中台的要求处理key
            if key in EntityStorageConfig.attribute_map:
                j[EntityStorageConfig.attribute_map[key]] = final_value
            elif key in EntityStorageConfig.attribute_filter:
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
                    print(f"Entity {self.chinese_name} dumping attribute {key} failed: {str(e)}")
                    continue
                private_attr[key] = final_value

        j["attributes"] = private_attr
        return j


# 合并且分类构件
class ClassifiedEntity(Entity):

    def __init__(self, entity_object: Entity) -> None:
        Entity.__init__(
            self,
            entity_object.entity_class,
            entity_object.bounding_rectangle,
            entity_object.CAD_bounding_rectangle,
            entity_object.origin_class,
            entity_object.score,
            entity_object.lead_mark,
            entity_object.contour
        )
        self.uuid = entity_object.uuid


# 合并类构件
class CombinedEntity(Entity):

    def __init__(self, layer_name: str, bounding_rectangle: BoundingRectangle) -> None:
        Entity.__init__(
            self,
            entity_class=layer_name,
            bounding_rectangle=bounding_rectangle
        )
        self.uuid = uuid1().hex


# 图元类构件
class PrimitiveEntity(Entity):

    def __init__(self, processed_gbe: ProcessedGBE) -> None:

        self.entity_class = processed_gbe.layer_name
        self.bounding_rectangle = self.get_bbox(processed_gbe)
        self.start_end_point_list = [processed_gbe.coord]
        self.uuid = uuid1().hex

    def get_bbox(self, processed_gbe: ProcessedGBE) -> BoundingRectangle:
        bbox = processed_gbe.coord
        extend_margin_factor = 5
        # 圆圈
        if len(bbox) < 4:
            bbox = [bbox[0] - bbox[-1], bbox[1] - bbox[-1],
                    bbox[0] + bbox[-1], bbox[1] + bbox[-1]]
        # 非圆圈
        else:
            bbox = bbox[:4]

        bbox = extend_margin(bbox, extend_margin_factor)
        bbox = BoundingRectangle(bbox)
        return bbox
