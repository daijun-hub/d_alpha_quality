from ..base_type import EntityBaseType
from ..entity import CombinedEntity, Entity
from ...base.bounding_rectangle import BoundingRectangle
from ...border_entity import BorderEntity
from ....common.utils import *
from ....common.utils2 import load_drawing_pkl
from ....common.utils_draw_and_rule import get_origin_border_entity_info_rule
from ....config_manager.architecture.drawing_config import DrawingType
from alpha_recognition_quality.config_manager.text_config import TextType
from ...utils import *
import re
import cv2


class LanGan(CombinedEntity):
    chinese_name = "栏杆"

    def __init__(self, layer_name: str, bounding_rectangle: BoundingRectangle, border_entity: BorderEntity) -> None:
        CombinedEntity.__init__(self, layer_name, bounding_rectangle)

        self.chinese_name = "栏杆"
        self.entity_base_type = EntityBaseType.HANDRAIL
        self.bbox = self.bounding_rectangle
        self.center = [(self.bbox[0] + self.bbox[2]) // 2, (self.bbox[1] + self.bbox[3]) // 2]
        self.space_type = self.get_space_type(border_entity)
        self.floor = self.get_floor_form(border_entity)  # 层属性是为得到栏杆高，辅助设定
        self.height, self.langan_material, self.langan_color = None, None, None
        self.ganhuchuang_text_list = self.get_gaohuchuang_text(border_entity)
        self.flag = self.get_gaohu_flag(border_entity)
        # self.win_list = self.get_window(border_entity)
        # 位置
        self.position = self.center
        # 楼层
        # self.floor = border_entity.floor_num_list
        # 楼层标高
        self.floor_label_height = get_floor_label_height(self.bounding_rectangle.list, border_entity)
        self.langan_color = None
        self.langan_material = None

    def get_cross_border_attribs(self, border_entity, building_object):
        self._get_material(building_object)

    def _get_material(self, building_object):
        # CrossBorder_list = [DrawingType.BUILDING_DESIGN, DrawingType.EXTERIOR_WALL_MATERIAL]
        # 材料和颜色列表，需要甲方爸爸提供
        material_list = ["锌钢", '锌钢组合玻璃栏杆', '铝合金', '不锈钢', '铁', '木', '钢筋混泥土', '玻璃', '塑料']
        color_list = ['阿克苏·诺贝尔JN126CH', "阿克苏·诺贝尔富锌底粉ALZ66Z", "正荣粉末富锌底粉HS-9391",
                      "阿克苏·诺贝尔C02449B2LT", "正荣粉末HS-9083", "正荣粉末BP-62315",
                      "阿克苏·诺贝尔C28580S3LT", "正荣粉末PD-73135", "正荣粉末PD-63241",
                      "阿克苏·诺贝尔C27964S3LP", "阿克苏·诺贝尔白色MA812C改D34", "正荣粉末A3-2000"]

        # 在外墙材料表图纸中得到栏杆材料和颜色及纹理，在设计说明得到栏杆的高度
        for special_drawing_dict in building_object.special_drawing_list:
            for drawing_type, info_dict in special_drawing_dict.items():
                file_id = info_dict['file_id']
                # 在设计说明得到栏杆的高度
                if drawing_type == DrawingType.BUILDING_DESIGN:
                    design_border_entity = load_drawing_pkl(file_id)
                    all_text = design_border_entity.border_text_info[TextType.ALL]
                    langan_list = [text.bbox.list + [text.extend_message] for text in all_text if
                                re.search('栏杆工程', str(text.extend_message))]
                    if len(langan_list) > 0:
                        langan_gaodu_list = [text.bbox.list + [text.extend_message] for text in all_text if
                                            re.search('(\d+)', str(text.extend_message))]
                        num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                        new_gaodu_list = []
                        for l in langan_gaodu_list:
                            flag = True
                            for i in l[4]:
                                if i not in num:
                                    flag = False
                                    break
                            if flag and int(l[4]) > 600:
                                l = [l[0], l[1], l[2], l[3], int(l[4])]
                                new_gaodu_list.append(l)

                        langan = langan_list[0]
                        x1, y1, x2, y2 = langan[0], langan[1], langan[2], langan[3]
                        w, h = 15 * abs(x2 - x1), 10 * abs(y2 - y1)
                        x3, y3, x4, y4 = x1, y1, x2 + w, y2 + h
                        new_langan_list = []
                        gao_num = []
                        for gaodu in new_gaodu_list:
                            y, x = gaodu[1] + int(abs(gaodu[3] - gaodu[1]) / 2), gaodu[0] + int(
                                abs(gaodu[2] - gaodu[0]) / 2)
                            if x3 < x < x4 and y3 < y < y4:
                                new_langan_list.append(gaodu)
                                gao_num.append(int(gaodu[4]))
                        gao_num = list(set(gao_num))  # 去重
                        gao_num.sort(reverse=True)
                        # 根据楼层判断栏杆高度
                        if int(self.floor) >= 7 and not self.flag:
                            self.height = max(gao_num)
                        if 0 < int(self.floor) < 7 and not self.flag:
                            self.height = gao_num[-2]
                        if self.flag:
                            self.height = gao_num[-1]

                if drawing_type == DrawingType.EXTERIOR_WALL_MATERIAL_LIST:
                    material_border_entity = load_drawing_pkl(file_id)
                    all_text = material_border_entity.border_text_info[TextType.ALL]
                    all_text_list = [text.bbox.list + [text.extend_message] for text in all_text if
                                    re.search('栏杆', str(text.extend_message))]
                    material_text_list = []
                    # 简单过滤得到 " ***栏杆 "，将字数太少的过滤
                    for text in all_text_list:
                        if len(text[4]) > 12:
                            material_text_list.append(text)
                    if len(material_text_list) > 0:
                        for text in material_text_list:
                            material_text = text[4]
                            for material in material_list:
                                if re.search('栏杆.*[使用|为|是]%s.*' % material, material_text):
                                    self.langan_material = material
                            for color in color_list:
                                if color in material_text:
                                    print(f'找到颜色 {color}')
                                    self.langan_color = color

    # 通过图名获得楼层数
    def get_floor(self, border_entity):
        namelist = border_entity.drawing_name.split("层")
        floor = namelist[1][-3:-1]
        floor_dic = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
        num = 0
        if len(floor) == 1:
            num = floor_dic[floor]
        if len(floor) >= 1:
            num = 10
        return num

    # 通过表格获得楼层数
    def get_floor_form(self, border_entity):
        all_text = border_entity.border_text_info[TextType.ALL]

        all_text_list = [text.bbox.list + [text.extend_message] for text in all_text if
                         re.search('层数', str(text.extend_message))]
        all_num_list = [text.bbox.list + [text.extend_message] for text in all_text if
                        re.search('(\d+)', str(text.extend_message))]
        num_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        # 默认取第一个
        if len(all_text_list) > 0:
            ceng_text_bbox = all_text_list[0]
            w = abs(ceng_text_bbox[2] - ceng_text_bbox[0])
            h = abs(ceng_text_bbox[3] - ceng_text_bbox[1])
            tmp_bbox = [ceng_text_bbox[0] - w, ceng_text_bbox[1], ceng_text_bbox[2] + w, ceng_text_bbox[3] + 5 * h]
            num = 0
            floor_num_list = []
            for num_bbox in all_num_list:
                flag = True
                floor_num_str = num_bbox[4]  # type: str
                floor_num_str = floor_num_str.replace('层', '')
                for i in floor_num_str:
                    if i not in num_list:
                        flag = False
                if flag:
                    iou1 = Iou_temp(tmp_bbox, num_bbox[0:4])
                    if iou1 != 0 and iou1 > 0:
                        floor_num_list.append(int(floor_num_str))
            if len(floor_num_list) > 0:
                num = max(floor_num_list)
            if num == 0:
                print("NOT find building floor num!")
                return 0
            return num
        else:
            return 0

    def get_space_type(self, border_entity):
        # if border_entity.drawing_type == DrawingType.INDOOR:
        # lan_list = border_entity.entity_object_dict.get('平面栏杆', [])
        # height = border_entity.image_manager.img_height
        # width = border_entity.image_manager.img_width
        # img = np.zeros((height, width, 3), dtype="uint8")
        # for lan in lan_list:
        #     bbox = lan.bounding_rectangle
        #
        #     x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
        #     cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 10)

        room_info = border_entity.room_info
        # 排除小空间，只留下大空间
        name_list = ["大堂", "大厅", "门厅", "阳台", "卧室", "卫生间", "餐厅", "客厅", "厨房", "走廊", "主卧", "次卧"]
        langan_room_list = []
        distance_dic = {}
        # 默认阳台栏杆
        text = "阳台栏杆"
        for info in room_info:
            room_name_str = ''.join(info.name_list)
            for room_name in name_list:
                if room_name in room_name_str:
                    bbox = info.bbox.list
                    lifo_ = [bbox[0], bbox[1], bbox[2], bbox[3], room_name]
                    langan_room_list.append(lifo_)

        bbox = self.bounding_rectangle
        ly, lx = bbox[1] + int(abs(bbox[3] - bbox[1]) / 2), bbox[0] + int(abs(bbox[2] - bbox[0]) / 2)
        for info in langan_room_list:
            bbox1 = info[0:4]
            ry, rx = bbox1[1] + int(abs(bbox1[3] - bbox1[1]) / 2), bbox1[0] + int(abs(bbox1[2] - bbox1[0]) / 2)
            distance = ((ry - ly) ** 2 + (rx - lx) ** 2) ** 0.5
            distance_dic[distance] = info[4]
        if len(distance_dic) > 0:
            keys = distance_dic.keys()
            keys = list(keys)
            minkey = min(keys)
            text = distance_dic[minkey]
            text = text + "栏杆"
        return text

    def get_gaohuchuang_text(self, border_entity):
        all_text = border_entity.border_text_info[TextType.ALL]
        gaohuchuang_text_list = [text.bbox.list for text in all_text if
                                 re.search('高护窗栏杆', str(text.extend_message))]

        return gaohuchuang_text_list

    # def get_window(self, border_entity):
    #     entity_bbox_dict = border_entity['entity_bbox_dict']
    #     windows_list = entity_bbox_dict['window']

    # return windows_list

    def get_gaohu_flag(self, border_entity):
        # 通过找到最近文本获取栏杆是否为高护窗栏杆
        gaochuang_flag = False
        w = abs(self.bounding_rectangle[2] - self.bounding_rectangle[0])
        h = abs(self.bounding_rectangle[3] - self.bounding_rectangle[1])
        x, y = self.bounding_rectangle[0] + int(w / 2), self.bounding_rectangle[1] + int(h / 2)
        win_are = w * h
        distance_dic = {}
        for text in self.ganhuchuang_text_list:
            w1 = abs(text[2] - text[0]) if abs(text[2] - text[0]) else 0.0001
            h1 = abs(text[3] - text[1]) if abs(text[3] - text[1]) else 0.0001
            x1, y1 = text[0] + int(w1 / 2), text[1] + int(h1 / 2)
            text_are = w1 * h1
            distance = ((y - y1) ** 2 + (x - x1) ** 2) ** 0.5
            distance_dic[distance] = [w, h, win_are / text_are , distance / h1]
        if len(distance_dic) > 0:
            keys = distance_dic.keys()
            keys = list(keys)
            minkey = min(keys)
            bbox = distance_dic[minkey]
            if bbox[0] > 1 and bbox[1] > 1 and bbox[2] < 3 and bbox[3] < 10:
                gaochuang_flag = True

        return gaochuang_flag




