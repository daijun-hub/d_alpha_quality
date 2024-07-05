from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils import *
from ....common.utils2 import load_drawing_pkl
from shapely.geometry import LineString, Polygon, MultiLineString, Point
from ....config_manager.structure.drawing_config import DrawingType as drawing_type_structure


class JieGouAnZhu(ClassifiedEntity):
    chinese_name = "结构暗柱"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        self.chinese_name = "结构暗柱"
        self.name_number = get_anzhu_number(entity_object, border_entity)
        self.zongjin_num = []  # 纵筋数量
        self.zongjin_diameter = []  # 纵筋直径
        self.gujin_diameter = []  # 箍筋直径
        self.gujin_distance = []  # 箍筋间距

    def get_cross_border_attribs(self, border_entity, building_object):
        self._get_anzhu_attribs(border_entity, building_object)  # 更新暗柱的 纵筋数量和纵筋直径属性，箍筋直径和箍筋间距属性

    def _get_anzhu_attribs(self, border_entity, building_object):
        ratio = border_entity.ratio
        extend_range = int(1000 * ratio[0])
        if self.name_number is None:
            print('Note: anzhu name number not found !!')
        else:
            all_text_info = border_entity.border_text_info[TextType.ALL]
            need_text_list = [text for text in all_text_info if re.search('柱表', text.extend_message)]
            target_text_list = [text for text in all_text_info if self.name_number == text.extend_message]
            zongjin_text_list = [text for text in all_text_info if re.search('[0-9]%%132[0-9]', text.extend_message)]  # 暗柱纵筋文本中含Φ且不含@
            gujin_text_list = [text for text in all_text_info if re.search('[0-9]@[0-9]', text.extend_message)]  # 暗柱箍筋文本中含Φ且含@
            # 获取该图纸中的表格
            biaoge_list = border_entity.entity_object_dict['表格']
            attribs_ok = False
            if len(biaoge_list) > 0:
                for biaoge in biaoge_list:
                    biaoge_bbox = biaoge.bounding_rectangle.list
                    biaoge_ext_bbox = [biaoge_bbox[0] - extend_range, biaoge_bbox[1] - extend_range,
                                       biaoge_bbox[2] + extend_range, biaoge_bbox[3] + extend_range]
                    text_list = [text for text in need_text_list if Iou_temp(biaoge_ext_bbox, text.bbox.list) > 0]
                    found_target_TABLE = False
                    if len(text_list) > 0:
                        # 判断
                        for target_text in target_text_list:
                            target_text_bbox = target_text.bbox.list
                            if Iou_temp(target_text_bbox, biaoge_ext_bbox) > 0:
                                print('Note: target text found in current drawing ！！')
                                # 找到目标文本的搜索区域
                                target_search_area = [target_text_bbox[0], target_text_bbox[1],
                                                      biaoge_ext_bbox[2], target_text_bbox[3]]
                                # 在该区域内查找目标文本
                                self.zongjin_num, self.zongjin_diameter = get_zongjin_attribs(target_search_area,
                                                                                              zongjin_text_list)
                                self.gujin_diameter, self.gujin_distance = get_gujin_attribs(target_search_area,
                                                                                             gujin_text_list)
                                found_target_TABLE = True
                                attribs_ok = True
                                break
                    if found_target_TABLE:
                        break
            # 需要跨图框获取属性信息
            elif len(biaoge_list) == 0 or attribs_ok is False:
                WALL_COLUMN_DETAILS_list = []
                for special_drawing_dict in building_object.special_drawing_list:
                    for drawing_type, info_dict in special_drawing_dict.items():
                        file_id = info_dict['file_id']
                        if drawing_type == drawing_type_structure.WALL_COLUMN_DETAILS:
                            WALL_COLUMN_DETAILS_list.append(file_id)
                for WALL_COLUMN_DETAILS_id in WALL_COLUMN_DETAILS_list:
                    border_entity_info = load_drawing_pkl(WALL_COLUMN_DETAILS_id)
                    ratio = border_entity_info.ratio
                    extend_range_xt = int(500 * ratio[0])
                    all_text_info = border_entity_info.border_text_info[TextType.ALL]
                    target_text_list_xt = [text for text in all_text_info if re.search(self.name_number, text.extend_message) and
                                           len(self.name_number) == len(text.extend_message)]
                    zongjin_text_list = [text for text in all_text_info if
                                         re.search('[0-9]%%132[0-9]', text.extend_message)]  # 暗柱纵筋文本中含Φ且不含@
                    gujin_text_list = [text for text in all_text_info if
                                       re.search('[0-9]@[0-9]', text.extend_message)]  # 暗柱箍筋文本中含Φ且含@
                    if len(target_text_list_xt) > 0:
                        print('Note: target_text_list_xt:', target_text_list_xt)
                        text_bbox = target_text_list_xt[0].bbox.list
                        target_search_area_xt = [text_bbox[0] - extend_range_xt, text_bbox[1] - extend_range_xt,
                                                 text_bbox[2] + extend_range_xt, text_bbox[3] + extend_range_xt]
                        # 在该区域内查找目标文本
                        self.zongjin_num, self.zongjin_diameter = get_zongjin_attribs(target_search_area_xt,
                                                                                      zongjin_text_list)
                        self.gujin_diameter, self.gujin_distance = get_gujin_attribs(target_search_area_xt,
                                                                                     gujin_text_list)
                        break

