from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity
from ...utils.utils_entity import *
from ....config_manager.architecture.drawing_config import DrawingType as drawing_type_architecture
from ....common.utils2 import load_drawing_pkl


class FengJingBaiYe(ClassifiedEntity):
    
    chinese_name = "风井百叶"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "风井百叶"
        self.entity_base_type = EntityBaseType.WINDOW

        # 编号
        map_label= "(BY|BYC)\d{1,2}"
        self.baiye_label = get_entity_label_number(entity_object.bounding_rectangle.list, border_entity, extend_margin=1800, map_label=map_label)
        self.lm_width = None
        self.lm_height = None

    def get_cross_border_attribs(self, border_entity, building_object):
        self._get_baiye_width_height(building_object)

    def _get_baiye_width_height(self, building_object):
        baiye_number = self.baiye_label
        if baiye_number:
            for special_drawing_dict in building_object.special_drawing_list:
                for drawing_type, info_dict in special_drawing_dict.items():
                    file_id = info_dict['file_id']
                    if drawing_type == drawing_type_architecture.DOOR_WINDOW_DAYANG:
                        # 返回结果字典
                        bbox = None
                        border_entity_info = load_drawing_pkl(file_id)
                        ratio = border_entity_info.ratio
                        # 找到大样图的立面窗
                        lm_window_obj_list = border_entity_info.entity_object_dict['立面窗']
                        for lm_window_obj in lm_window_obj_list:
                            if baiye_number in lm_window_obj.window_number:
                                bbox = lm_window_obj.bounding_rectangle.list
                                break
                        if bbox is not None:
                            ext_range = int(1000 * ratio[0])
                            all_text_info = border_entity_info.border_text_info[TextType.ALL]
                            # 矩形框的高和宽
                            bbox_height = bbox[3] - bbox[1]
                            bbox_width = bbox[2] - bbox[0]
                            window_bbox_height = bbox_height // ratio[0]
                            window_bbox_width = bbox_width // ratio[0]
                            ext_bbox1 = [bbox[0], bbox[1], bbox[2], bbox[3] + ext_range]  # 向下外扩
                            ext_bbox2 = [bbox[0], bbox[1], bbox[2] + ext_range, bbox[3]]  # 向右外扩
                            d_value1 = float('inf')
                            d_value2 = float('inf')
                            all_text_info = [text for text in all_text_info if re.search('^[0-9]*$', text.extend_message)]
                            for text in all_text_info:
                                text_bbox, text_message = text.bbox.list, text.extend_message
                                if Iou_temp(ext_bbox1, text_bbox) > 0:
                                    d_value = abs(window_bbox_width - eval(text_message))
                                    if d_value < d_value1:
                                        self.lm_width = eval(text_message)
                                        d_value1 = d_value
                                if Iou_temp(ext_bbox2, text_bbox) > 0:
                                    d_value = abs(window_bbox_height - eval(text_message))
                                    if d_value < d_value2:
                                        self.lm_height = eval(text_message)
                                        d_value2 = d_value
                            print('Note: lm_width: ', self.lm_width)
                            print('Note: lm_height: ', self.lm_height)
                            self.win_size_bbox = bbox
                            self.win_size_file_id = border_entity_info.cad_border_id
                            self.win_size_pickle_id = file_id
