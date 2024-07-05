from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils import *
from ....config_manager.architecture.drawing_config import DrawingType as drawing_type_architecture
from ....common.utils2 import load_drawing_pkl


class YuLiuKongDongP(ClassifiedEntity):

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        self.chinese_name = "预留孔洞P"
        self.entity_base_type = EntityBaseType.HOLE
        # 定义构件在户空间相对于户中心和入户门的土建连线中点为极轴逆时针的夹脚
        self.angle_against_apartment = None
        # 到户中心的距离
        self.dist_to_apartment_centroid = None
        # 定义构件在所属空间相对于所在空间中心和门的土建连线中点为极轴逆时针的夹脚
        self.angle_against_room = None
        # 到所属空间中心的距离
        self.dist_to_room_centroid = None
        # 跨图框属性
        self.floor_distance = None
        self.wall_distance = None

    def get_cross_border_attribs(self, border_entity, building_object):
        # 通过设计说明图来找到预留孔洞距所依墙边距离数值
        # self._get_wall_distance(building_object)
        # 预留孔洞中心”距本层楼板距离”数值
        self._get_floor_distance(building_object)

    def _get_floor_distance(self, building_object):
        text_mark_list = []
        text_louban_list = []
        text_wall_list = []
        text_num_list = []
        for special_drawing_dict in building_object.special_drawing_list:
            for drawing_type, info_dict in special_drawing_dict.items():
                file_id = info_dict['file_id']
                if drawing_type == drawing_type_architecture.BUILDING_DESIGN:
                    bd_border_entity = load_drawing_pkl(file_id)
                    ratio = bd_border_entity.ratio
                    text_all = bd_border_entity.border_text_info[TextType.ALL]
                    for text in text_all:
                        if re.search(''.join(self.lead_mark), text.extend_message):
                            text_mark_list.append(text)
                        if re.search(".*本层楼板", text.extend_message):
                            text_louban_list.append(text)
                        elif re.search("距.*楼面", text.extend_message):
                            text_louban_list.append(text)
                        elif re.search("孔顶贴.*底", text.extend_message):
                            text_louban_list.append(text)
                        if re.search(".*墙边", text.extend_message):
                            text_wall_list.append(text)
                        if re.search("^[0-9]\d*$", text.extend_message):
                            text_num_list.append(text)
                        if re.search("梁|板", text.extend_message):
                            text_num_list.append(text)
                    for text_mark in text_mark_list:
                        for text_louban in text_louban_list:
                            if Iou_temp([text_mark.bbox.list[0], text_mark.bbox.list[1],
                                         text_mark.bbox.list[2] + 8000 * ratio[0],
                                         text_mark.bbox.list[3] + 1000 * ratio[0]],
                                        text_louban.bbox.list):
                                for text_num in text_num_list:
                                    if Iou_temp([text_louban.bbox.list[0], text_louban.bbox.list[1],
                                                 text_louban.bbox.list[2] + 2300 * ratio[0], text_louban.bbox.list[3]],
                                                text_num.bbox.list):
                                        self.floor_distance = text_num
                                        self.floor_distance_bbox = text_num.bbox.list
                                        self.floor_distance_file_id = bd_border_entity.cad_border_id
                                        self.floor_distance_pickle_id = file_id
                                        break
                            if self.floor_distance != None:
                                break
                        for text_wall in text_wall_list:
                            if Iou_temp([text_mark.bbox.list[0], text_mark.bbox.list[1],
                                         text_mark.bbox.list[2] + 8000 * ratio[0], text_mark.bbox.list[3]],
                                        text_wall.bbox.list):
                                for text_num in text_num_list:
                                    if Iou_temp([text_wall.bbox.list[0], text_wall.bbox.list[1],
                                                 text_wall.bbox.list[2] + 2300 * ratio[0], text_wall.bbox.list[3]],
                                                text_num.bbox.list):
                                        self.wall_distance = text_num
                                        self.wall_distance_bbox = text_num.bbox.list
                                        self.wall_distance_file_id = bd_border_entity.cad_border_id
                                        self.wall_distance_pickle_id = file_id
                                        break
                                if self.wall_distance != None:
                                    break

