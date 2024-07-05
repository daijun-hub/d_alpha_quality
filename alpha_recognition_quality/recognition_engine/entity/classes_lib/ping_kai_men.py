from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ....common.utils_draw_and_rule import door_nearby_text
from ...utils import *


class PingKaiMen(ClassifiedEntity):
    chinese_name = "平开门"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        text_cls = door_nearby_text(entity_object.bounding_rectangle.list, border_entity)

        self.chinese_name = "平开门"
        self.entity_base_type = EntityBaseType.DOOR
        self.door_wall_width = door_width_entity(entity_object.bounding_rectangle.list, border_entity, text_cls)
        self.door_height = door_height_entity(entity_object.bounding_rectangle.list, border_entity, text_cls)
        self.door_usage, self.door_orientation = door_usage_entity(entity_object.bounding_rectangle.list, border_entity)
        self.door_towards_direction = self.get_door_direction(border_entity)
        self.door_leaf_number = door_leaf_number_entity(entity_object.bounding_rectangle.list, border_entity)
        self.door_angle = door_angle_entity(entity_object.bounding_rectangle.list, border_entity)
        self.door_fire_linked_control = door_xiaofang_control(entity_object.bounding_rectangle.list, border_entity)
        self.door_open_region_contour = get_door_open_region_contour(entity_object.bounding_rectangle.list, border_entity)
        if self.door_leaf_number == '单扇':
            # 门扇侧、非门扇侧属性。形式为[point1,point2]，point1代表门扇侧，point2代表非门扇侧
            self.start_end_point = door_leaf_orientation(entity_object.bounding_rectangle.list, border_entity)
        self.is_outer_evacuating_door = judge_evacuating_door(entity_object.bounding_rectangle.list, border_entity)
        self.door_open_area = self.door_height * self.door_wall_width if self.door_height and self.door_wall_width else None
        self.door_base_line = get_door_base_line_entity(entity_object.bounding_rectangle.list, border_entity)
        self.door_direction_line = get_door_direction_line_entity(entity_object.bounding_rectangle.list, border_entity)

        # 编号
        map_label = "(LM|M|FM|MC|TLM|MD)[]?[甲乙丙]?(\d{1,2})?"
        self.door_number = get_door_label_number(entity_object.bounding_rectangle.list, border_entity, extend_margin=1800, map_label=map_label)
        # map_label = "(LM|M)[ ]?[甲乙丙]?\d{1,2}"
        # self.door_number = get_entity_label_number(entity_object.bounding_rectangle.list, border_entity, extend_margin=1800, map_label=map_label)
        self.door_fire_resistance_level = self.get_fire_proof_level(border_entity)
        self.is_ping_kai_men = True
        self.open_mode = '平开门'

    def get_fire_proof_level(self, border_entity):
        door_number = self.door_number
        if door_number is None:
            return None
        cls_dic = {"甲级": "JFM|甲", "乙级": "YFM|乙", "丙级": "BFM|丙"}
        # all_text_info = border_entity.border_text_info[TextType.ALL]
        level_pattern = '|'.join(cls_dic.values())
        level_texts = re.search(level_pattern, door_number)
        door_fm_info = None
        if level_texts:
            level_text = level_texts[0]
            for key, value in cls_dic.items():
                if re.search(value, level_text):
                    door_fm_info = key
                    break
        return door_fm_info

        #
        # level_texts = [t for t in all_text_info if re.search(level_pattern, t.extend_message)]
        # if len(level_texts) <= 0:
        #     return None
        # print(f'找到目标文本：{[_.extend_message for _ in level_texts]}')
        # door_bbox = self.bounding_rectangle.list
        # door_h = door_bbox[3] - door_bbox[1]
        # door_w = door_bbox[2] - door_bbox[0]
        # # 扁平的门框，按垂直方向外扩
        # if door_w > 2*door_h:
        #     ext_door_bbox = [door_bbox[0], door_bbox[1] - door_w/3,
        #                      door_bbox[2], door_bbox[3] + door_w/3]
        # elif door_h > 2*door_w:
        #     ext_door_bbox = [door_bbox[0] - door_h/3, door_bbox[1],
        #                      door_bbox[2] + door_h/3, door_bbox[3]]
        # else:
        #     ext_door_bbox = [door_bbox[0] - door_w/3, door_bbox[1] - door_h/3,
        #                      door_bbox[2] + door_w/3, door_bbox[3] + door_h/3]
        #
        # match_texts = list()
        # for level_text in level_texts:
        #     text_bbox = level_text.bbox.list
        #     if Iou_temp(text_bbox, ext_door_bbox) > 0.271828:
        #         match_texts.append(level_text)
        # # sort and join
        # match_texts.sort(key=lambda k: (k.bbox.list[0], k.bbox.list[1]))
        # match_text = ''.join([_.extend_message for _ in match_texts])
        # print(f"\033[1;31m 找到门附近文本: {match_text} \033[0m")
        #
        # door_fm_info = None
        # if match_text:
        #     for key, value in cls_dic.items():
        #         if re.search(value, match_text):
        #             door_fm_info = key
        #             break
        # print(f"\033[1;31m 门编号：{self.door_number}, 防火等级: {door_fm_info} \033[0m")
        # return door_fm_info

    def get_door_direction(self, border_entity):
        """
        获取平开门的开启方向（朝向的空间）
        其它方向定义问题：
            1. 与分割空间平面垂直，朝向所在空间的向量：户型旋转之后难以比较，且比较时需要旋转信息
            2. 以所在空间的空间名称：相同户型的相同空间也可做不同用途，而且名称也不确定（比如卫生间和卫）
            3. 以门的bbox为朝向：因门相对空间较小，平移（旋转）户型，会导致相同的门，bbox也不相交
        :return:
        """
        room_info = border_entity.room_info
        door_contour = get_contour_from_bbox(self.bounding_rectangle.list)
        location_room = None
        min_area = float('inf')
        for room in room_info:
            room_contour = room.contour.contour
            # 找到门所在的空间
            if get_contours_iou_v2(room_contour, door_contour) > 0.8:
                # 所有包含该门的空间中，取面积最小的
                print(f'\033[1;31m 找到该门的空间:{room.name_list} \033[0m')
                _area = bbox_area(room.bbox)
                if _area < min_area:
                    if location_room:
                        print(f'用: {room.name_list}，替换掉门的较大空间:{location_room.name_list}')
                    min_area = _area
                    location_room = room
        return location_room
