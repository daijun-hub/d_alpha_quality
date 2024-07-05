from ..base_type import EntityBaseType
from ..entity import CombinedEntity, Entity
from ...base.bounding_rectangle import BoundingRectangle
from ...border_entity import BorderEntity
from ....common.utils import *
from ....common.utils2 import load_drawing_pkl
from ....common.utils_draw_and_rule import get_origin_border_entity_info_rule
from ....config_manager.architecture.drawing_config import DrawingType
from ....config_manager.text_config import TextType
from ...utils import *
import re
import cv2
from operator import itemgetter


class PingMianLanGan(CombinedEntity):
    chinese_name = "平面栏杆"

    def __init__(self, layer_name: str, bounding_rectangle: BoundingRectangle, border_entity: BorderEntity) -> None:
        CombinedEntity.__init__(self, layer_name, bounding_rectangle)

        self.chinese_name = "平面栏杆"
        self.entity_base_type = EntityBaseType.HANDRAIL
        self.bbox = self.bounding_rectangle
        self.center = get_centroid(self.bounding_rectangle.list)# [(self.bbox[0] + self.bbox[2]) // 2, (self.bbox[1] + self.bbox[3]) // 2]
        self.space_type = self.get_space_type(border_entity)
        # print("self.space_type", self.space_type)
        self.floor = self.get_floor(border_entity)  # 层属性是为得到栏杆高，辅助设定
        self.height = "" # 栏杆高度
        self.langan_material = None # 栏杆材料
        self.langan_color = None # 栏杆颜色
        self.ganhuchuang_text_list = self.get_gaohuchuang_text(border_entity)
        self.flag = self.get_gaohu_flag(border_entity)
        # self.win_list = self.get_window(border_entity)
        # 位置
        self.position = self.center
        # 楼层
        # self.floor = border_entity.floor_num_list
        # 楼层标高
        self.floor_label_height = get_floor_label_height(self.bounding_rectangle.list, border_entity)

    def get_cross_border_attribs(self, border_entity, building_object):
        self._get_material_and_color(building_object)
        self._get_effective_height(building_object)

    def _get_material_and_color(self, building_object):
        # CrossBorder_list = [DrawingType.EXTERIOR_WALL_MATERIAL]
        # 材料和颜色列表，需要甲方爸爸提供
        # material_list = ["锌钢组合", '锌钢组合玻璃栏杆', '铝合金', '不锈钢', '铁', '木', '钢筋混泥土', '玻璃', '塑料']
        # color_list = ['阿克苏·诺贝尔JN126CH', "阿克苏·诺贝尔富锌底粉ALZ66Z", "正荣粉末富锌底粉HS-9391",
        #               "阿克苏·诺贝尔C02449B2LT", "正荣粉末HS-9083", "正荣粉末BP-62315",
        #               "阿克苏·诺贝尔C28580S3LT", "正荣粉末PD-73135", "正荣粉末PD-63241",
        #               "阿克苏·诺贝尔C27964S3LP", "阿克苏·诺贝尔白色MA812C改D34", "正荣粉末A3-2000"]
        print("Finging langan material and color ...")
        self.langan_color_bbox = None
        self.langan_material_bbox = None
        print("栏杆类型 ", self.space_type)
        # 在外墙材料表图纸中得到栏杆材料和颜色及纹理，在设计说明得到栏杆的高度
        for special_drawing_dict in building_object.special_drawing_list:
            for drawing_type, info_dict in special_drawing_dict.items():
                file_id = info_dict['file_id']
                if drawing_type in [DrawingType.EXTERIOR_WALL_MATERIAL_LIST]:
                    material_border_entity = load_drawing_pkl(file_id)
                    # 外墙材料表有些情况下分为商业部分和住宅部分两个图框，使用图名过滤掉商业部分
                    if is_business_material_border(material_border_entity.drawing_name):
                        continue
                    image_manager = material_border_entity.image_manager
                    img_h, img_w = image_manager.img_height, image_manager.img_width
                    # for debug
                    img_copy = image_manager.load_from_manager(IMG_WITH_WALL_KEY)
                    all_text = material_border_entity.border_text_info[TextType.ALL]
                    # 外墙材料表有些情况下分为商业部分和住宅部分同时在一个图框，找到住宅部分外墙材料表的文本位置
                    text_region_include = [0, 0, img_w, img_h]
                    # TODO 添加函数找到住宅外墙材料表文本区域
                    zhuzhai_pattern = "((住宅|居住|居建|洋房).*外墙材料表)|(外墙材料表.{0,5}(住宅|居住|居建|洋房))"
                    comm_pattern = "((商业|配套|门楼|底商).*外墙材料表)|(外墙材料表.{0,5}(商业|配套|门楼|底商))"
                    text_region_include = self.find_zhuzhai_target_region_bbox(zhuzhai_pattern, comm_pattern, all_text,
                                                                               [],
                                                                               text_region_include)
                    # 部分图纸的图名没有商业，但是在图框里面只有商业外墙材料表
                    # 这种情况直接跳过
                    if text_region_include is None:
                        continue
                    # for debug
                    # cv2.rectangle(img_copy, (text_region_include[0] + 20, text_region_include[1] + 20),
                    #               (text_region_include[2] - 20, text_region_include[3] - 20), (255, 255, 0), 10)
                    all_text = [text for text in all_text if Iou_temp(text.bbox.list, text_region_include) > 0.5]
                    all_text_list = [text.bbox.list + [text.extend_message] for text in all_text if
                                     re.search('栏杆', str(text.extend_message)) and not re.search('^走廊栏杆', str(text.extend_message))]
                    # material_text_list = []
                    # 简单过滤得到 " ***栏杆 "，将字数太少的过滤
                    # for text in all_text_list:
                    #     if len(text[4]) > 12:
                    #         material_text_list.append(text)
                    if len(all_text_list) > 0:
                        for text in all_text_list:
                            x1, y1, x2, y2 = text[:4]
                            w, h = abs(x2 - x1), abs(y2 - y1)
                            target_bbox = [x1, y1, x2 + 2*w, y2 + h]
                            msg_list = []
                            for txt in all_text:
                                if Iou_temp(txt.bbox.list, target_bbox):
                                    msg_list.append(txt.bbox.list + [txt.extend_message])
                            concat_msg = self._concat_text(msg_list)
                            # material_text = text[4]
                            # for material in material_list:
                            material_find_res = re.search('(阳台)?[^(走廊)]栏杆.{1,5}[使用|为|是]([\u4e00-\u9fa5]*)(栏杆)?', concat_msg)
                            if material_find_res:
                                print("concat_msg", concat_msg)
                                if ("阳台栏杆" in concat_msg and self.space_type == "阳台") or \
                                        ("阳台栏杆" not in concat_msg):
                                    print(f'找到材料 。。。 ')
                                    self.langan_material = material_find_res.group(2)
                                    if self.langan_material[-2:] == "栏杆":
                                        self.langan_material = self.langan_material[:-2]
                                    for msg in msg_list:
                                        if "走廊" in msg: continue
                                        if re.search(self.langan_material, msg[4]): # re.search("所有", msg[4]) and
                                            self.langan_material_bbox = msg[:4]
                                    self.langan_material_file_id = material_border_entity.cad_border_id
                                    self.langan_material_pickle_id = file_id
                            material_find_res1 = re.search('[(使用)|为|是]([\u4e00-\u9fa5]*)栏杆',
                                                          concat_msg)
                            if material_find_res is None and material_find_res1 is not None:
                                print("concat_msg", concat_msg)
                                if ("阳台栏杆" in concat_msg and self.space_type == "阳台") or \
                                        ("阳台栏杆" not in concat_msg):
                                    print(f'找到材料 。。。 ')
                                    self.langan_material = material_find_res1.group(1)
                                    if self.langan_material[-2:] == "栏杆":
                                        self.langan_material = self.langan_material[:-2]
                                    for msg in msg_list:
                                        if "走廊" in msg: continue
                                        if re.search(self.langan_material, msg[4]):  # re.search("所有", msg[4]) and
                                            self.langan_material_bbox = msg[:4]
                                    self.langan_material_file_id = material_border_entity.cad_border_id
                                    self.langan_material_pickle_id = file_id
                            self.find_langan_color(concat_msg, msg_list)
                            self.langan_color_file_id = material_border_entity.cad_border_id
                            self.langan_material_pickle_id = file_id
                            if self.langan_material and self.langan_color:
                                # for debug
                                # img_copy = draw_chinese(img_copy, all_text_list)
                                # cv2.rectangle(img_copy, (self.langan_material_bbox[0], self.langan_material_bbox[1]),
                                #                         (self.langan_material_bbox[2], self.langan_material_bbox[3]), (255, 255, 0), 3)
                                # cv2.rectangle(img_copy, (self.langan_color_bbox[0], self.langan_color_bbox[1]),
                                #                         (self.langan_color_bbox[2], self.langan_color_bbox[3]), (0, 255, 255), 3)
                                # cv2.imwrite("langan_material_color.png", img_copy)
                                break
            if self.langan_material and self.langan_color: break
        if self.langan_material:
            print("subproject_name", material_border_entity.subproject_name)
            print("drawing_name", material_border_entity.drawing_name)
        print("self.langan_material --> ", self.langan_material)
        if self.langan_material:
            print("self.langan_material_bbox --> ", self.langan_material_bbox)
        print("self.langan_color --> ", self.langan_color)
        if self.langan_color:
            print("self.langan_color_bbox --> ", self.langan_color_bbox)
        # for debug
        # cv2.imwrite("/Users/xuan.ma/Desktop/ex_mat_debug.png", img_copy)

    def _get_effective_height(self, building_object):
        # CrossBorder_list = [DrawingType.EXTERIOR_WALL_MATERIAL]
        # 在设计说明得到栏杆的高度
        print("Finging langan height ...")
        print("栏杆类型 ", self.space_type)
        ytlg_eff_height_1 = ""
        ytlg_eff_height_2 = ""
        hclg_eff_height = ""
        for special_drawing_dict in building_object.special_drawing_list:
            for drawing_type, info_dict in special_drawing_dict.items():
                # 在设计说明得到栏杆的高度
                if drawing_type in [DrawingType.BUILDING_DESIGN]:
                    file_id = info_dict['file_id']
                    design_border_entity = load_drawing_pkl(file_id)
                    image_manager = design_border_entity.image_manager
                    img_width, img_height = image_manager.img_width, image_manager.img_height
                    # for debug
                    img_copy = image_manager.load_from_manager(IMG_WITH_WALL_KEY)
                    ytlg_height_bbox = [img_width, img_height, 0, 0]
                    hclg_height_bbox = [img_width, img_height, 0, 0]
                    all_text = design_border_entity.border_text_info[TextType.ALL]
                    for text in all_text:
                        if self.space_type == "阳台" and ytlg_eff_height_1  and ytlg_eff_height_2: break
                        if self.space_type == "窗户" and hclg_eff_height: break
                        if re.search("栏杆工程", text.extend_message): # 有效高度|六层及六层以下|七层及七层以上|阳台、平台的?栏杆
                            x1, y1, x2, y2 = text.bbox.list
                            w, h = abs(x2 - x1), abs(y2 - y1)
                            target_bbox = [x1, y1, x1 + img_width//5, y2 + 13*h]
                            msg_txt_list = []
                            msg_digit_list = []
                            ignore_pat_list = ["\d{0,3}\.\d{0,3}", '√']
                            for text in all_text:
                                if Iou_temp(text.bbox.list, target_bbox):
                                    for ignore_pat in ignore_pat_list:
                                        if re.search(ignore_pat, text.extend_message):
                                            break
                                    else:
                                        if text.extend_message.isdigit():
                                            msg_digit_list.append(text.bbox.list + [text.extend_message])
                                        else:
                                            msg_txt_list.append(text.bbox.list + [text.extend_message])
                            # print("msg_digit_list", msg_digit_list)
                            # print("msg_txt_list", msg_txt_list)
                            concat_text_msg = self._concat_text(msg_txt_list)
                            concat_text_msg_list = concat_text_msg.split()
                            split_sign = ","
                            concat_digit_msg = self._concat_text(msg_digit_list, split_sign=split_sign)
                            concat_digit_msg_list = concat_digit_msg.split(split_sign)
                            concat_msg = ""
                            for i in range(len(concat_text_msg_list)):
                                concat_msg += concat_text_msg_list[i]
                                if i < len(concat_digit_msg_list):
                                    concat_msg += concat_digit_msg_list[i]
                            h_find_result_1 = re.search("六层及六层以下.*阳台.*平台的?栏杆的?有效?高度(\d{1,5})。.*七层及七层", concat_msg)
                            if h_find_result_1:
                                ytlg_eff_height_1 = h_find_result_1.group(1)
                                # self.height += eff_height_1
                                for msg in msg_txt_list + msg_digit_list:
                                    if re.search(ytlg_eff_height_1, msg[4]):
                                        ytlg_height_bbox = [min(msg[0], ytlg_height_bbox[0]),
                                                            min(msg[1], ytlg_height_bbox[1]),
                                                            max(msg[2], ytlg_height_bbox[2]),
                                                            max(msg[3], ytlg_height_bbox[3])
                                                          ]
                            h_find_result_2 = re.search("七层及七层以上.*阳台.*平台的?栏杆的?有效?高度(\d{1,5})。", concat_msg)
                            if h_find_result_2:
                                ytlg_eff_height_2 = h_find_result_2.group(1)
                                # self.height += eff_height_2
                                for msg in msg_txt_list + msg_digit_list:
                                    if re.search(ytlg_eff_height_2, msg[4]):
                                        ytlg_height_bbox = [min(msg[0], ytlg_height_bbox[0]),
                                                            min(msg[1], ytlg_height_bbox[1]),
                                                            max(msg[2], ytlg_height_bbox[2]),
                                                            max(msg[3], ytlg_height_bbox[3])
                                                           ]
                            h_find_result_3 = re.search("护窗的?栏杆的?有效?高度(\d{1,5})", concat_msg)
                            if h_find_result_3:
                                hclg_eff_height = h_find_result_3.group(1)
                                # self.height += eff_height_2
                                for msg in msg_digit_list + msg_txt_list:
                                    if re.search(hclg_eff_height, msg[4]):
                                        hclg_height_bbox = msg[:4]
                            if self.space_type == "阳台":
                                self.height = ytlg_eff_height_1 + "," + ytlg_eff_height_2
                                self.height_bbox = ytlg_height_bbox
                                self.height_file_id = design_border_entity.cad_border_id
                                self.height_pickle_id = file_id
                                break
                            elif self.space_type == "窗户":
                                self.height = hclg_eff_height
                                self.height_bbox = hclg_height_bbox
                                self.height_file_id = design_border_entity.cad_border_id
                                self.height_pickle_id = file_id
                                break

                    # langan_list = [text.bbox.list + [text.extend_message] for text in all_text if
                    #                re.search('栏杆工程', str(text.extend_message))]
                    # if len(langan_list) > 0:
                    #     langan_gaodu_list = [text.bbox.list + [text.extend_message] for text in all_text if
                    #                          re.search('(\d+)', str(text.extend_message))]
                    #     num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
                    #     new_gaodu_list = []
                    #     for l in langan_gaodu_list:
                    #         flag = True
                    #         for i in l[4]:
                    #             if i not in num:
                    #                 flag = False
                    #                 break
                    #         if flag and int(l[4]) > 400:
                    #             l = [l[0], l[1], l[2], l[3], int(l[4])]
                    #             new_gaodu_list.append(l)
                    #
                    #     langan = langan_list[0]
                    #     x1, y1, x2, y2 = langan[0], langan[1], langan[2], langan[3]
                    #     w, h = 15 * abs(x2 - x1), 10 * abs(y2 - y1)
                    #     x3, y3, x4, y4 = x1, y1, x2 + w, y2 + h
                    #     new_langan_list = []
                    #     for gaodu in new_gaodu_list:
                    #         y, x = gaodu[1] + int(abs(gaodu[3] - gaodu[1]) / 2), gaodu[0] + int(
                    #             abs(gaodu[2] - gaodu[0]) / 2)
                    #         if x3 < x < x4 and y3 < y < y4:
                    #             new_langan_list.append(gaodu)
                    #     new_langan_list = sorted(new_langan_list, key=itemgetter(1, 2))
                    #     # 根据楼层判断栏杆高度
                    #     if not self.flag:
                    #         self.height = [int(new_langan_list[1][-1]), int(new_langan_list[0][-1])]
                    #         self.height_bbox = ytlg_height_bbox
                    #         self.height_file_id = design_border_entity.cad_border_id
                    #         self.height_pickle_id = file_id
                    #     elif self.flag:
                    #         self.height = int(new_langan_list[-1][-1])
                    #         self.height_bbox = hclg_height_bbox
                    #         self.height_file_id = design_border_entity.cad_border_id
                    #         self.height_pickle_id = file_id
            if self.height != '': break
        if self.height:
            print("subproject_name", design_border_entity.subproject_name)
            print("drawing_name", design_border_entity.drawing_name)
        print("self.height --> ", self.height)
        # for debug
        # try:
        #     print("self.height_bbox --> ", self.height_bbox)
        #     cv2.rectangle(img_copy, tuple(self.height_bbox[:2]), tuple(self.height_bbox[2:]), (0, 255, 255), 3)
        #     cv2.imwrite(f"/Users/xuan.ma/Desktop/{design_border_entity.drawing_name}_{self.space_type}_ping_mian_lan_gan_height_bbox.png", img_copy)
        # except Exception as e:
        #     print(e)

    def find_zhuzhai_target_region_bbox(self, zhuzhai_pattern, comm_pattern, text_all, text_concat_list, text_region_include):
        # 先确定是否有商业外墙材料表和住宅外墙材料表
        zhuzhai_text_bbox = None
        comm_text_bbox = None
        for text in text_concat_list:
            text_bbox = text[:4]
            text_msg = text[-1]
            if re.search(zhuzhai_pattern, text_msg):
                zhuzhai_text_bbox = text_bbox
            if re.search(comm_pattern, text_msg):
                comm_text_bbox = text_bbox
        # 表格合并问题导致没获取到商业外墙材料表
        # 通过单个文本外扩获取
        if zhuzhai_text_bbox is None:
            zhuzhai_text_bbox = self.find_target_text_bbox(text_all, zhuzhai_pattern, "住|居|居|洋|外")
        if comm_text_bbox is None:
            comm_text_bbox = self.find_target_text_bbox(text_all, comm_pattern, "商|配|门|底|外")
        if comm_text_bbox is None:
            print("没找到商业外墙材料表 。。。 ")
            return text_region_include
        if zhuzhai_text_bbox is None:
            print("没找到住宅外墙材料表 。。。 ")
            return None
        # 1. 住宅外墙材料表和商业外墙材料表上下放置
        # bbox在宽度方向的投影出合度大于0.5
        if self.find_line_intersection_len(zhuzhai_text_bbox, comm_text_bbox, proj_dir = "width")/abs(zhuzhai_text_bbox[2]-zhuzhai_text_bbox[0]) > 0.5:
            # 住宅外墙材料表在上，商业外墙材料表在下
            if zhuzhai_text_bbox[1] < comm_text_bbox[1]:
                text_region_include = [0, 0, text_region_include[2], comm_text_bbox[1]]
                print("住宅外墙材料表在上，商业外墙材料表在下")
                return text_region_include
            # 商业外墙材料表在上，住宅外墙材料表在下
            else:
                text_region_include = [0, zhuzhai_text_bbox[2], text_region_include[2], text_region_include[3]]
                print("商业外墙材料表在上，住宅外墙材料表在下")
                return text_region_include
        # 2. 住宅外墙材料表和商业外墙材料表左右放置
        # bbox在高度方向的投影出合度大于0.5
        if self.find_line_intersection_len(zhuzhai_text_bbox, comm_text_bbox, proj_dir = "height")/abs(zhuzhai_text_bbox[3]-zhuzhai_text_bbox[1]) > 0.5:
            # 住宅外墙材料表在左，商业外墙材料表在右
            if zhuzhai_text_bbox[0] < comm_text_bbox[2]:
                text_region_include = [0, 0, comm_text_bbox[0], text_region_include[3]]
                print("住宅外墙材料表在左，商业外墙材料表在右")
                return text_region_include
            # 商业外墙材料表在左，住宅外墙材料表在右
            else:
                text_region_include = [zhuzhai_text_bbox[0], zhuzhai_text_bbox[3], text_region_include[2], text_region_include[3]]
                print("商业外墙材料表在左，住宅外墙材料表在右")
                return text_region_include


    # 通过图名获得楼层数
    def get_floor(self, border_entity):
        # namelist = border_entity.drawing_name.split("层")
        # floor = namelist[1][-3:-1]
        # floor_dic = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
        # num = 0
        # if len(floor) == 1:
        #     num = floor_dic[floor]
        # if len(floor) >= 1:
        #     num = 10
        floor_num_list = border_entity.floor_num_list
        if floor_num_list:
            return floor_num_list[0]
        return None

    # 通过表格获得楼层数
    # def get_floor_form(self, border_entity):
    #     all_text = border_entity.border_text_info[TextType.ALL]
    #
    #     all_text_list = [text.bbox.list + [text.extend_message] for text in all_text if
    #                      re.search('层数', str(text.extend_message))]
    #     all_num_list = [text.bbox.list + [text.extend_message] for text in all_text if
    #                     re.search('(\d+)', str(text.extend_message))]
    #     num_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    #     # 默认取第一个
    #     if len(all_text_list) > 0:
    #         ceng_text_bbox = all_text_list[0]
    #         w = abs(ceng_text_bbox[2] - ceng_text_bbox[0])
    #         h = abs(ceng_text_bbox[3] - ceng_text_bbox[1])
    #         tmp_bbox = [ceng_text_bbox[0] - w, ceng_text_bbox[1], ceng_text_bbox[2] + w, ceng_text_bbox[3] + 5 * h]
    #         num = 0
    #         floor_num_list = []
    #         for num_bbox in all_num_list:
    #             flag = True
    #             floor_num_str = num_bbox[4]  # type: str
    #             floor_num_str = floor_num_str.replace('层', '')
    #             for i in floor_num_str:
    #                 if i not in num_list:
    #                     flag = False
    #             if flag:
    #                 iou1 = Iou_temp(tmp_bbox, num_bbox[0:4])
    #                 if iou1 != 0 and iou1 > 0:
    #                     floor_num_list.append(int(floor_num_str))
    #         if len(floor_num_list) > 0:
    #             num = max(floor_num_list)
    #         if num == 0:
    #             print("NOT find building floor num!")
    #             return 0
    #         return num
    #     else:
    #         return 0

    def get_space_type(self, border_entity):
        '''
        获取栏杆所属空间, 目前只支持阳台和窗户
        Args:
            border_entity:

        Returns:

        '''
        ratio = border_entity.ratio
        room_info = border_entity.room_info
        # balcony_list = border_entity.space_object_dict.get("阳台", [])
        balcony_list = [room for room in room_info if "阳台" in room.name_list]
        for balcony in balcony_list:
            ext_bal_contour = expand_contour(balcony.contour.contour, 165*ratio[0])
            if get_contours_iou(ext_bal_contour, get_contour_from_bbox(self.bounding_rectangle.list)) > 0:
                return "阳台"
        # window_list = border_entity.space_object_dict.get("其他窗", [])
        entity_bbox_list = border_entity.entity_bbox_list
        window_list = [entity for entity in entity_bbox_list if entity.entity_class in ["other_window"]]
        for window in window_list:
            if Iou_temp(self.bounding_rectangle.list, window.bounding_rectangle.list) > 0.5:
                return "窗户"
        return None

        # room_info = border_entity.room_info
        # # 排除小空间，只留下大空间
        # name_list = ["大堂", "大厅", "门厅", "阳台", "卧室", "卫生间", "餐厅", "客厅", "厨房", "走廊"]
        # langan_room_list = []
        # distance_dic = {}
        # # 默认阳台栏杆
        # text = "阳台栏杆"
        # for info in room_info:
        #     room_name_str = ''.join(info.name_list)
        #     for room_name in name_list:
        #         if room_name in room_name_str:
        #             bbox = info.bbox.list
        #             lifo_ = [bbox[0], bbox[1], bbox[2], bbox[3], room_name]
        #             langan_room_list.append(lifo_)
        #
        # bbox = self.bounding_rectangle
        # ly, lx = bbox[1] + int(abs(bbox[3] - bbox[1]) / 2), bbox[0] + int(abs(bbox[2] - bbox[0]) / 2)
        # for info in langan_room_list:
        #     bbox1 = info[0:4]
        #     ry, rx = bbox1[1] + int(abs(bbox1[3] - bbox1[1]) / 2), bbox1[0] + int(abs(bbox1[2] - bbox1[0]) / 2)
        #     distance = ((ry - ly) ** 2 + (rx - lx) ** 2) ** 0.5
        #     distance_dic[distance] = info[4]
        # if len(distance_dic) > 0:
        #     keys = distance_dic.keys()
        #     keys = list(keys)
        #     minkey = min(keys)
        #     text = distance_dic[minkey]
        #     text = text + "栏杆"
        # return text

    def get_gaohuchuang_text(self, border_entity):
        all_text = border_entity.border_text_info[TextType.ALL]
        gaohuchuang_text_list = [text.bbox.list for text in all_text if
                                 re.search('.*窗.*(栏杆|护栏)', str(text.extend_message))]

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
            w1 = abs(text[2] - text[0])
            h1 = abs(text[3] - text[1])
            x1, y1 = text[0] + int(w1 / 2), text[1] + int(h1 / 2)
            text_are = w1 * h1
            distance = ((y - y1) ** 2 + (x - x1) ** 2) ** 0.5
            distance_dic[distance] = [w, h, win_are / text_are, distance / h1]
        if len(distance_dic) > 0:
            keys = distance_dic.keys()
            keys = list(keys)
            minkey = min(keys)
            bbox = distance_dic[minkey]
            if bbox[0] > 1 and bbox[1] > 1 and bbox[2] < 3 and bbox[3] < 10:
                gaochuang_flag = True

        return gaochuang_flag

    def _concat_text(self, split_msg_list, split_sign = ""):
        '''
        将文本合并在一起
        split_msg_list: [[x1, y1, x2, y2, text], ... ]
        '''
        # 直接排序有问题，特别是尺寸数据和文本不为同一个文本，坐标有偏差，导致文本合并问题
        # split_msg_list.sort(key=lambda x: (x[1], x[0]))
        # split_msg = "".join([msg[-1] for msg in split_msg_list])
        if not split_msg_list: return ""
        line_height = abs(split_msg_list[0][3] - split_msg_list[0][1])
        # 先根据文本中心确认有几行文本
        split_msg_center_y_list = [get_centroid(split_msg[:4])[1] for split_msg in split_msg_list]
        # row_y_list = []
        vis = [False] * len(split_msg_center_y_list)
        y_arr = np.array(split_msg_center_y_list)
        total_text_list = []
        for yi, y in enumerate(split_msg_center_y_list):
            if vis[yi]: continue
            row_text_list = []
            minor_diff_idxs = np.where(np.abs(y_arr[yi:] - y) < line_height / 2)[0] + yi
            # print("minor_diff_idxs", minor_diff_idxs)
            for idx in minor_diff_idxs:
                vis[idx] = True
                row_text_list.append(split_msg_list[idx])
            row_text_list.sort(key=lambda x: x[0])
            total_text_list.append([y, row_text_list.copy()])
            # row_y_list.append(y)
        # # 从上到下户获取每一行的文本
        total_text_list.sort(key=lambda x: x[0])
        split_msg = ""
        for center_y, row_text_list in total_text_list:
            split_msg += split_sign.join([text[-1] for text in row_text_list]) + split_sign
        return split_msg

    def find_line_intersection_len(self, bbox1, bbox2, proj_dir = "width"):
        if proj_dir == "width":
            return abs(max(bbox1[0], bbox2[0]) - min(bbox1[2], bbox2[2]))
        elif proj_dir == "height":
            return abs(max(bbox1[1], bbox2[1]) - min(bbox1[3], bbox2[3]))

    def find_target_text_bbox(self, text_all, full_pattern, pattern):
        target_bbox = None
        kw_msg_list = []
        for text in text_all:
            text_bbox = text.bbox.list
            text_msg = text.extend_message
            if re.search(pattern, text_msg):
                kw_msg_list.append(text_bbox + [text_msg])
        for kw_msg in kw_msg_list:
            kw_msg_bbox = kw_msg[:4]
            # 向右延长bbox
            ext_len = 50 * abs(kw_msg_bbox[2]-kw_msg_bbox[0])
            kw_msg_bbox_ext = [kw_msg_bbox[0], kw_msg_bbox[1], kw_msg_bbox[2]+ext_len, kw_msg_bbox[3]]
            msg_list = []
            for text in text_all:
                text_bbox = text.bbox.list
                text_msg = text.extend_message
                if Iou_temp(text_bbox, kw_msg_bbox_ext):
                    msg_list.append(text_bbox + [text_msg])
            text_concat = self._concat_text(msg_list)
            if re.search(full_pattern, text_concat):
                target_bbox = kw_msg_bbox_ext
                break
        return target_bbox

    def find_langan_color(self, concat_msg, msg_list):
        '''
        正则匹配栏杆颜色
        '''
        print("concat_msg", concat_msg)
        color_find_res3 = re.search('(阳台)?[^(走廊)]栏杆.{0,20}颜色及?纹理((灰|黑)色半光)。?',concat_msg)
        if color_find_res3:
            if ("阳台栏杆" in concat_msg and self.space_type == "阳台") or \
               ("阳台栏杆" not in concat_msg):
                print(f'找到颜色 。。。 ')
                self.langan_color = color_find_res3.group(2)
                self.langan_color_bbox = [float("inf"), float("inf"), -float("inf"), -float("inf")]
                for msg in msg_list:
                    # print("msg", msg)
                    if msg[4] in self.langan_color or self.langan_color in msg[4]:
                        # self.langan_color_bbox = msg[:4]
                        self.langan_color_bbox = [min(msg[0], self.langan_color_bbox[0]),
                                                  min(msg[1], self.langan_color_bbox[1]),
                                                  max(msg[2], self.langan_color_bbox[2]),
                                                  max(msg[3], self.langan_color_bbox[3]),
                                                  ]
        color_find_res = re.search('(阳台)?[^(走廊)]栏杆.{0,20}颜色及?纹理.{0,2}((阿克苏.?诺贝尔|正荣粉末)?[A-Z0-9\-（）()]*[\u4e00-\u9fa5]{0,5}[A-Z0-9\-（）()]*)。?', concat_msg)
        group_find_res = re.search('(集团.{0,10}标准)', concat_msg)
        # for color in color_list:
        if self.langan_color is None and color_find_res:
            if ("阳台栏杆" in concat_msg and self.space_type == "阳台") or \
               ("阳台栏杆" not in concat_msg):
                print(f'找到颜色 。。。 ')
                self.langan_color = color_find_res.group(2)
                self.langan_color_bbox = [float("inf"), float("inf"), -float("inf"), -float("inf")]
                for msg in msg_list:
                    # print("msg", msg)
                    if msg[4] in self.langan_color or self.langan_color in msg[4]:
                        # self.langan_color_bbox = msg[:4]
                        self.langan_color_bbox = [min(msg[0], self.langan_color_bbox[0]),
                                                  min(msg[1], self.langan_color_bbox[1]),
                                                  max(msg[2], self.langan_color_bbox[2]),
                                                  max(msg[3], self.langan_color_bbox[3]),
                                                  ]

        color_find_res1 = re.search('[^(走廊)]栏杆.{0,20}颜色[为参]?([\u4e00-\u9fa5]{0,5}色[\u4e00-\u9fa5]{0,5})。?纹理.{0,2}((阿克苏.?诺贝尔|正荣粉末)?[A-Z0-9\-（）()]*[\u4e00-\u9fa5]{0,5}[A-Z0-9\-（）()]*)。?', concat_msg)
        if self.langan_color is None and color_find_res1:
            print(f'找到颜色 。。。 ')
            self.langan_color = color_find_res1.group(1) + "," + color_find_res1.group(2)
            self.langan_color_bbox = [float("inf"), float("inf"), -float("inf"), -float("inf")]
            for color_text in self.langan_color.split(","):
                for msg in msg_list:
                    if re.search(msg[4], color_text):
                        self.langan_color_bbox = [min(msg[0], self.langan_color_bbox[0]),
                                                  min(msg[1], self.langan_color_bbox[1]),
                                                  max(msg[2], self.langan_color_bbox[2]),
                                                  max(msg[3], self.langan_color_bbox[3]),
                                                  ]
        color_find_res2 = re.search('[^(走廊)]栏杆.{0,20}颜色[为参]?[：:]?([\u4e00-\u9fa5]{0,5}色[\u4e00-\u9fa5]{0,5})。?',
                                    concat_msg)
        if self.langan_color is None and color_find_res2:
            print(f'找到颜色 。。。 ')
            self.langan_color = color_find_res2.group(1)
            self.langan_color_bbox = [float("inf"), float("inf"), -float("inf"), -float("inf")]
            for msg in msg_list:
                if re.search(self.langan_color, msg[4]):
                    self.langan_color_bbox = msg[:4]

        if group_find_res:
            # self.langan_color += "," + group_find_res.group(1) if self.langan_color is not None else group_find_res.group(1)
            if self.langan_color is None:
                self.langan_color = group_find_res.group(1)
            else:
                self.langan_color += "," + group_find_res.group(1)

            for msg in msg_list:
                if re.search(self.langan_color, msg[4]):
                    if self.langan_color_bbox is not None:
                        self.langan_color_bbox = [min(msg[0], self.langan_color_bbox[0]),
                                                  min(msg[1], self.langan_color_bbox[1]),
                                                  max(msg[2], self.langan_color_bbox[2]),
                                                  max(msg[3], self.langan_color_bbox[3]),
                                                  ]
                    else:
                        self.langan_color_bbox = msg[:4]

