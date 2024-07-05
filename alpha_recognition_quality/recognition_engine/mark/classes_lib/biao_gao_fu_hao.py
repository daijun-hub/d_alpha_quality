from ...entity.base_type import EntityBaseType
from ..mark import Mark
from ...border_entity import BorderEntity
from ...entity.entity import Entity
from ...utils.utils_mark import *
from ....config_manager.architecture.drawing_config import DrawingType

class BiaoGaoFuHao(Mark):

    chinese_name = "标高符号"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:

        self.bounding_rectangle = entity_object.bounding_rectangle
        self.entity_base_type = EntityBaseType.TEXT

        # 标高高度
        self.labeled_height = labeled_height_mark(self.bounding_rectangle.list, border_entity)
        # 标高类型
        self.labeled_type = get_elevation_type_mark(self.bounding_rectangle.list, border_entity)
        # 标高类型-数值对应字典
        self.labeld_type_height_dict = get_elevation_type_value_dict_mark(self.bounding_rectangle.list, border_entity)

        # 建筑外标高
        self.out_attribute = None
        self.judge_biaogao_position(border_entity)

    # 判断是否为建筑外标高
    def judge_biaogao_position(self, border_entity):
        if border_entity.drawing_type in [DrawingType.INDOOR_FIRST_FLOOR]:
            ratio = border_entity.ratio
            room_info = border_entity.room_info
            room_info = [room for room in room_info if "平面图建筑轮廓" in room.name_list]
            # 获取门列表
            entity_bbox_list = [entity for entity in border_entity.entity_bbox_list if
                                entity.entity_class in ['door', 'menlianchuang']]
            for room in room_info:
                contour = room.contour.contour
                if get_contours_iou(contour, get_contour_from_bbox(self.bounding_rectangle.list)) < 0.3:
                    for entity in entity_bbox_list:
                        bbox = extend_margin(entity.bounding_rectangle.list, margin=int(5000 * ratio[0]))
                        if Iou_temp(self.bounding_rectangle.list, bbox) > 0.8:
                            self.out_attribute = "建筑外场地标高"
                            break




