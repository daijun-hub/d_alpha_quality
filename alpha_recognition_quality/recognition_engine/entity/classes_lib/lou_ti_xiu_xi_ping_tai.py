from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity
from ...utils import *

# 分类类型
class LouTiXiuXiPingTai(ClassifiedEntity):

    chinese_name = "楼梯休息平台"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "楼梯休息平台"
        self.entity_base_type = EntityBaseType.STAIR
        #位置
        self.position = get_contour_from_bbox(self.bounding_rectangle.list)
        # 构件所在楼层
        self.floor = self.get_floor(border_entity)
        #标高
        self.label_height = self.get_label_height(border_entity)
        #平台宽度
        self.platform_width = self.get_platform_width(border_entity)




    def get_floor(self, border_entity):
        floor = border_entity.floor_num_list
        return floor

    def get_label_height(self, border_entity):
        label_height = None
        biao_gao_label_list = border_entity.mark_object_dict['标高符号']
        if biao_gao_label_list is not None:
            for biao_gao_label in biao_gao_label_list:
                if get_contours_iou(get_contour_from_bbox(self.bounding_rectangle.list), get_contour_from_bbox(biao_gao_label.bounding_rectangle.list)):
                    if biao_gao_label.labeld_type_height_dict:
                        for key, value in biao_gao_label.labeld_type_height_dict.items():
                            if key == "建筑标高":
                                label_height = value
        return label_height

    def get_platform_width(self, border_entity):
        platform_width = None
        ta_bu_list = border_entity.mark_object_dict['平面楼梯踏步']
        if ta_bu_list is not None:
            for ta_bu in ta_bu_list:
                if get_contours_iou(get_contour_from_bbox(ta_bu.bounding_rectangle.list), get_contour_from_bbox(extend_margin(self.bounding_rectangle.list, 10))):
                    ta_bu_length = ta_bu.bounding_rectangle.list[2] - ta_bu.bounding_rectangle.list[0]
                    ta_bu_width = ta_bu.bounding_rectangle.list[3] - ta_bu.bounding_rectangle.list[1]
                    if ta_bu_width > ta_bu_length:
                        platform_width = self.bounding_rectangle.list[2] - self.bounding_rectangle.list[0]
                        break
                    else:
                        platform_width = self.bounding_rectangle.list[3] - self.bounding_rectangle.list[1]
                        break
        return platform_width