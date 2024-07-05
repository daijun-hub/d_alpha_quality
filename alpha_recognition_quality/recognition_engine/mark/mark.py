from ..base.bounding_rectangle import BoundingRectangle
from ..entity.entity import ProcessedGBEStruct
from ...common.utils import *
from typing import List, Dict, Union
from ...config_manager.object_storage_config import MarkStorageConfig
from uuid import uuid1
import json

class Mark(object):

    _gbe_list = []                          # 类属性：组成图元
    chinese_name = "标记"                   # 标记类别中文名

    # 实例化流程中，流程负责将图元赋值给_gbe_list，本地调用的时候使用self.gbe_list

    def __init__(self, p_gbes: ProcessedGBEStruct) -> None:
        
        # 基础属性（Required）#
        self.bounding_rectangle: BoundingRectangle = None      # 外接矩形
        
        # 特有属性（Optional）#
        self.start_end_point_list = None    # 起终点坐标

        self.arrow_direction = None         # 箭头方向

        self.line_description = None        # 线型名称
        self.line_type = None               # 线型类型
        self.line_weight = None             # 线型宽度

        self.labeled_height = None          # 标高高度
        self.labeled_type = None            # 标高类型
        self.labeled_text = None            # 引注文字
        self.annotation_line_list = None    # 引注引线列表
        self.annotation_start_point = None  # 引注起点坐标

        self.step_width = None              # 踏步宽度
        self.step_length = None             # 踏步长度

        self.wall_type = None               # 墙体细分类型

        self.primitive_color = None         # 图元颜色
        
        self.uuid = uuid1().hex

    def copy(self, p_gbes: ProcessedGBEStruct):
        Mark.__init__(
            self,
            p_gbes
        )

    def to_dict(self):
        d = {
            "chinese_name": self.chinese_name
        }
        for key, value in vars(self).items():
            if value is not None:
                d[key] = value
        
        return d

    def to_json(self, drawing_id: int, border_coord, ratio, scale) -> Union[Dict, None]:
        d = self.to_dict()
        mark_type_id = MarkStorageConfig.storage_id_dict.get(d["chinese_name"], "")
        # if not mark_type_id:
        #     print(f"[Objectification] Cannot find {d['chinese_name']} in MarkStorageConfig.")
        #     return {}
        j = {
            "drawingId": drawing_id,
            "markTypeId": mark_type_id
        }
        private_attr = {}
        for key, value in d.items():
            # 不处理，不返回的配置列表
            if key in MarkStorageConfig.attribute_filter and self.chinese_name not in MarkStorageConfig.attribute_filter_exception.get(key, set()):
                continue
            
            # 根据object的key处理value（PNG -> CAD, etc.)
            if key == "bounding_rectangle":
                final_value = convert_bbox_to_CAD_coord(border_coord, value.list, ratio, scale)
                final_value = convert_bbox_to_range(final_value)
                final_value = str(final_value)
            elif key == "start_end_point_list":
                l = []
                for c in value:
                    if isinstance(c, list):
                        l.append(c)
                    elif isinstance(c, BoundingRectangle):
                        l.append(c.list)
                final_value = [convert_bbox_to_range(convert_bbox_to_CAD_coord(border_coord, c, ratio, scale)) for c in l]
                final_value = str(final_value)
            elif key == "uuid":
                continue
            else:
                final_value = value

            # 根据中台的要求处理key
            if key in MarkStorageConfig.attribute_map:
                j[MarkStorageConfig.attribute_map[key]] = final_value
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
                    print(f"Mark {self.chinese_name} dumping attribute {key} failed: {str(e)}")
                    continue
                private_attr[key] = final_value

        j["attributes"] = private_attr
        return j

    @property
    def gbe_list(self):
        return type(self)._gbe_list
