from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils import *
from ....common.utils2 import load_drawing_pkl
from shapely.geometry import LineString, Polygon, MultiLineString, Point
from ....config_manager.structure.drawing_config import DrawingType as drawing_type_structure


class JieGouZhu(ClassifiedEntity):
    chinese_name = "结构柱"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        self.chinese_name = "结构柱"

        # 相关属性
        self.pillar_number = entity_object.pillar_number
        self.pillar_type = entity_object.pillar_type
        self.angle_bar_dia = entity_object.angle_bar_dia
        self.angle_bar_num = entity_object.angle_bar_num
        self.Hside_middle_bar_dia = entity_object.Hside_middle_bar_dia
        self.Hside_middle_bar_num = entity_object.Hside_middle_bar_num
        self.Bside_middle_bar_dia = entity_object.Bside_middle_bar_dia
        self.Bside_middle_bar_num = entity_object.Bside_middle_bar_num
        self.Hside_stirrup_bodynum = entity_object.Hside_stirrup_bodynum
        self.Bside_stirrup_bodynum = entity_object.Bside_stirrup_bodynum
        self.dense_stirrup_dia = entity_object.dense_stirrup_dia
        self.dense_stirrup_dis = entity_object.dense_stirrup_dis
        self.Ndense_stirrup_dia = entity_object.Ndense_stirrup_dia
        self.Ndense_stirrup_dis = entity_object.Ndense_stirrup_dis
        self.node_core_stirrup_dia = entity_object.node_core_stirrup_dia
        self.node_core_stirrup_dis = entity_object.node_core_stirrup_dis
        self.longitud_bar_dia = entity_object.longitud_bar_dia
        self.longitud_bar_num = entity_object.longitud_bar_num
        self.cross_border_flag = entity_object.cross_border_flag  # 判断是否需要跨图框拿到属性
        self.pillar_number_flag = entity_object.pillar_number_flag
        self.pillar_number_bbox = entity_object.pillar_number_bbox

    # # 跨图框属性获取
    # def get_cross_border_attribs(self, border_entity, building_object):
    #     self._get_attribs(building_object, border_entity)

    def _get_attribs(self, building_object, border_entity):
        # 住宅墙柱平法施工图、地下室墙柱平法施工图,  只对在【住宅墙柱平法施工图】和【地下室墙柱平法施工图】中识别到的柱子，需获取属性
        special_drawingType_list = [drawing_type_structure.WALL_COLUMN_GRAPH, drawing_type_structure.BASEMENT_WALL_COLUMN_GRAPH]
        drawing_name = border_entity.drawing_name
        drawing_name_list = []
        if "层" in drawing_name:
            drawing_name_list = drawing_name.split("层")
            drawing_name_list.pop()
        if "m" in drawing_name:
            drawing_name_list = drawing_name.split("m")
            drawing_name_list.pop()
        subproject_name = border_entity.subproject_name

        # 对象属性获取需跨图:住宅墙柱详图、 地下室墙柱详图,必须同子项 楼层重合，这个方法是取省的方法
        if self.cross_border_flag:
            cross_drawingType_list = [drawing_type_structure.WALL_COLUMN_DETAILS,
                                      drawing_type_structure.BASEMENT_WALL_COLUMN_DETAILS]
            for special_drawing_dict in building_object.special_drawing_list:
                for drawing_type, file_id in special_drawing_dict.items():
                    if drawing_type in special_drawingType_list:
                        border_entity = load_drawing_pkl(file_id)
                        drawing_name_detail = border_entity.drawing_name
                        flag = False
                        if len(drawing_name_list) > 0:
                            for l in drawing_name_list:
                                if l in drawing_name_detail:
                                    flag = True
                        subproject_name_detail = border_entity.subproject_name
                        if subproject_name == subproject_name_detail and flag:
                            all_text = border_entity["border_text_info"][TextType.ALL]

                            # 跨图获取配筋属性的获取
                            # 原位标注获取
                            insitu_label_flag = self.get_attribs_insitu_label(all_text)
                            legend_table_flag = False
                            # 图例表获取
                            if insitu_label_flag == False:
                                legend_table_flag = self.get_attribs_legend_table(all_text, border_entity)
                            # 柱表格获取
                            if legend_table_flag == False:
                                parameter_table_flag = self.get_attribs_parameter_table(all_text, border_entity)


    def get_attribs_insitu_label(self, all_text):  # 在柱的原位标注中获取属性
        # 原位标注含有4种类型格式
        if self.pillar_number_flag == 0:
            number_text_list = []
            number_bbox = self.pillar_number_bbox
            w, h = self.get_wh(number_bbox)

            number_6_bbox = [number_bbox[0] - w, number_bbox[1] - h, number_bbox[2] + 2 * w, number_bbox[3] + 7 * h]

            # 在柱的左下角6*w, h范围进行文本获取
            for text in all_text:
                iou = Iou_temp(number_6_bbox, text[0:4])
                if iou != 0 and iou > 0:
                    number_text_list.append(text)
            insitu_label_flag = False
            if len(number_text_list) > 4:  # 针对最少文本情况
                # 对获取文本生成离编号距离
                number_text_dic = {}
                for text in number_text_list:
                    dis = int(self.get_distance(number_bbox, text[0:4]))
                    number_text_dic[dis] = text

                # 对文本生成离编号距离进行排序
                new_number_text_list = []
                for each in sorted(number_text_dic):
                    new_number_text_list.append(number_text_dic[each])

                BH_flag = False
                for text in new_number_text_list:
                    if "B" in text[4] or "H" in text[4]:
                        BH_flag = True

                # 第一种情况，多个柱角筋文本，无柱中部筋文本，文本行数在7行
                if BH_flag == False and len(new_number_text_list) == 7:
                    insitu_label_flag = True
                    angle_bar_text = new_number_text_list[2]
                    Hside_middle_bar_text = new_number_text_list[3]
                    Bside_middle_bar_text = new_number_text_list[4]
                    stirrup_dia_text = new_number_text_list[5]
                    stirrup_bodynum_text = new_number_text_list[6]

                    # 得到柱角筋属性
                    angle_bar_list = angle_bar_text[4].split("x")  # 4x(2ø200)
                    if len(angle_bar_list) == 1:
                        result = re.search('(\d+).*?(\d+).*', angle_bar_text[4])
                        groups = list(result.groups())
                        self.angle_bar_dia = int(groups[1][-2:])
                        self.angle_bar_num = int(groups[0])
                    else:  # 4ø200
                        text = angle_bar_list[1]
                        result = re.search('(\d+).*?(\d+).*', text)
                        groups = list(result.groups())
                        self.angle_bar_dia = int(groups[1][-2:])
                        self.angle_bar_num = int(angle_bar_list[0]) * int(groups[0])

                    Hside_middle_bar_list = Hside_middle_bar_text[4].split("%%132")  # 4ø200
                    if len(Hside_middle_bar_list) > 1:
                        self.Hside_middle_bar_dia = int(Hside_middle_bar_list[1])
                        self.Hside_middle_bar_num = int(Hside_middle_bar_list[0])

                    Bside_middle_bar_list = Bside_middle_bar_text[4].split("%%132")  # 4ø200
                    if len(Bside_middle_bar_list) > 1:
                        self.Bside_middle_bar_dia = int(Bside_middle_bar_list[1])
                        self.Bside_middle_bar_num = int(Bside_middle_bar_list[0])

                    stirrup_bar_list = stirrup_dia_text[4].split("%%132")
                    if len(stirrup_bar_list) > 1:

                        num = 0
                        for f in stirrup_bar_list[1]:
                            if f == "@":
                                num += 1
                        if "/" in stirrup_bar_list[1] and num == 1:  # 针对 （%%132）ø8@100/200
                            result = re.search('(\d+).*?(\d+).*?(\d+).*', stirrup_bar_list[1])
                            groups = list(result.groups())
                            self.dense_stirrup_dia = int(groups[0])
                            self.dense_stirrup_dis = int(groups[1])
                            self.Ndense_stirrup_dia = int(groups[0])
                            self.Ndense_stirrup_dis = int(groups[2])
                        if "/" in stirrup_bar_list[1] and num == 2:  # 针对 （%%132）ø8@100/ø6@200
                            result = re.search('(\d+).*?(\d+).*?(\d+).*?(\d+).*', stirrup_bar_list[1])
                            groups = list(result.groups())
                            self.dense_stirrup_dia = int(groups[0])
                            self.dense_stirrup_dis = int(groups[1])
                            self.Ndense_stirrup_dia = int(groups[2])
                            self.Ndense_stirrup_dis = int(groups[3])
                        if num == 1 and "/" not in stirrup_bar_list[1]:
                            result = re.search('(\d+).*?(\d+).*', stirrup_bar_list[1])  # ø8@200
                            groups = list(result.groups())
                            self.dense_stirrup_dia = int(groups[0])
                            self.dense_stirrup_dis = int(groups[1])
                            self.Ndense_stirrup_dia = int(groups[0])
                            self.Ndense_stirrup_dis = int(groups[1])

                    stirrup_bodynum_list = stirrup_bodynum_text[4].split("x")
                    if len(stirrup_bodynum_list) > 1:
                        self.Hside_stirrup_bodynum = stirrup_bodynum_list[0][-1:]
                        self.Bside_stirrup_bodynum = stirrup_bodynum_list[1][0]

                # 第二种情况，一个柱角筋文本，一个柱中部筋文本，文本行数在6行
                if BH_flag and len(new_number_text_list) == 6:
                    insitu_label_flag = True
                    angle_bar_text = new_number_text_list[2]
                    HBside_middle_bar_text = new_number_text_list[3]
                    stirrup_dia_text = new_number_text_list[4]
                    stirrup_bodynum_text = new_number_text_list[5]

                    # 得到柱角筋属性
                    angle_bar_list = angle_bar_text[4].split("x")  # 4x(2ø200)
                    if len(angle_bar_list) == 1:
                        result = re.search('(\d+).*?(\d+).*', angle_bar_text[4])
                        groups = list(result.groups())
                        self.angle_bar_dia = int(groups[1][-2:])
                        self.angle_bar_num = int(groups[0])
                    else:  # 4ø200
                        text = angle_bar_list[1]
                        result = re.search('(\d+).*?(\d+).*', text)
                        groups = list(result.groups())
                        self.angle_bar_dia = int(groups[1][-2:])
                        self.angle_bar_num = int(angle_bar_list[0]) * int(groups[0])

                    result = re.search('(\d+).*?(\d+).*?(\d+).*?(\d+).*', HBside_middle_bar_text[4])
                    groups = list(result.groups())  # B:4ø25;4ø25
                    if len(groups) > 3:
                        self.Hside_middle_bar_dia = int(groups[1][-2:])
                        self.Hside_middle_bar_num = int(groups[0])
                        self.Bside_middle_bar_dia = int(groups[3][-2:])
                        self.Bside_middle_bar_num = int(groups[2])

                    stirrup_bar_list = stirrup_dia_text[4].split("%%132")
                    if len(stirrup_bar_list) > 1:
                        num = 0
                        for f in stirrup_bar_list[1]:
                            if f == "@":
                                num += 1
                        if "/" in stirrup_bar_list[1] and num == 1:  # 针对 （%%132）ø8@100/200
                            result = re.search('(\d+).*?(\d+).*?(\d+).*', stirrup_bar_list[1])
                            groups = list(result.groups())
                            self.dense_stirrup_dia = int(groups[0])
                            self.dense_stirrup_dis = int(groups[1])
                            self.Ndense_stirrup_dia = int(groups[0])
                            self.Ndense_stirrup_dis = int(groups[2])
                        if "/" in stirrup_bar_list[1] and num == 2:  # 针对 （%%132）ø8@100/ø6@200
                            result = re.search('(\d+).*?(\d+).*?(\d+).*?(\d+).*', stirrup_bar_list[1])
                            groups = list(result.groups())
                            self.dense_stirrup_dia = int(groups[0])
                            self.dense_stirrup_dis = int(groups[1])
                            self.Ndense_stirrup_dia = int(groups[2])
                            self.Ndense_stirrup_dis = int(groups[3])
                        if num == 1 and "/" not in stirrup_bar_list[1]:
                            result = re.search('(\d+).*?(\d+).*', stirrup_bar_list[1])  # ø8@200
                            groups = list(result.groups())
                            self.dense_stirrup_dia = int(groups[0])
                            self.dense_stirrup_dis = int(groups[1])
                            self.Ndense_stirrup_dia = int(groups[0])
                            self.Ndense_stirrup_dis = int(groups[1])

                    stirrup_bodynum_list = stirrup_bodynum_text[4].split("x")
                    if len(stirrup_bodynum_list) > 1:
                        self.Hside_stirrup_bodynum = stirrup_bodynum_list[0][-1:]
                        self.Bside_stirrup_bodynum = stirrup_bodynum_list[1][0]

                # 第三种情况，一个柱角筋文本，二个柱中部筋文本，文本行数在7行
                if BH_flag and len(new_number_text_list) == 7:
                    insitu_label_flag = True
                    angle_bar_text = new_number_text_list[2]
                    Hside_middle_bar_text = new_number_text_list[3]
                    Bside_middle_bar_text = new_number_text_list[4]
                    stirrup_dia_text = new_number_text_list[5]
                    stirrup_bodynum_text = new_number_text_list[6]

                    # 得到柱角筋属性
                    angle_bar_list = angle_bar_text[4].split("x")  # 4x(2ø200)
                    if len(angle_bar_list) == 1:
                        result = re.search('(\d+).*?(\d+).*', angle_bar_text[4])
                        groups = list(result.groups())
                        self.angle_bar_dia = int(groups[1][-2:])
                        self.angle_bar_num = int(groups[0])
                    else:  # 4ø200
                        text = angle_bar_list[1]
                        result = re.search('(\d+).*?(\d+).*', text)
                        groups = list(result.groups())
                        self.angle_bar_dia = int(groups[1][-2:])
                        self.angle_bar_num = int(angle_bar_list[0]) * int(groups[0])

                    Hresult = re.search('(\d+).*?(\d+).*', Hside_middle_bar_text[4])
                    Hgroups = list(Hresult.groups())  # B:4ø200
                    if len(Hgroups) > 1:
                        self.Hside_middle_bar_dia = int(Hgroups[1][-2:])
                        self.Hside_middle_bar_num = int(Hgroups[0])

                    Bresult = re.search('(\d+).*?(\d+).*', Bside_middle_bar_text[4])  # H:4ø200
                    Bgroups = list(Bresult.groups())
                    if len(Bgroups) > 1:
                        self.Bside_middle_bar_dia = int(Bgroups[1][-2:])
                        self.Bside_middle_bar_num = int(Bgroups[0])

                    stirrup_bar_list = stirrup_dia_text[4].split("%%132")
                    if len(stirrup_bar_list) > 1:

                        num = 0
                        for f in stirrup_bar_list[1]:
                            if f == "@":
                                num += 1
                        if "/" in stirrup_bar_list[1] and num == 1:  # 针对 （%%132）ø8@100/200
                            result = re.search('(\d+).*?(\d+).*?(\d+).*', stirrup_bar_list[1])
                            groups = list(result.groups())
                            self.dense_stirrup_dia = int(groups[0])
                            self.dense_stirrup_dis = int(groups[1])
                            self.Ndense_stirrup_dia = int(groups[0])
                            self.Ndense_stirrup_dis = int(groups[2])
                        if "/" in stirrup_bar_list[1] and num == 2:  # 针对 （%%132）ø8@100/ø6@200
                            result = re.search('(\d+).*?(\d+).*?(\d+).*?(\d+).*', stirrup_bar_list[1])
                            groups = list(result.groups())
                            self.dense_stirrup_dia = int(groups[0])
                            self.dense_stirrup_dis = int(groups[1])
                            self.Ndense_stirrup_dia = int(groups[2])
                            self.Ndense_stirrup_dis = int(groups[3])
                        if num == 1 and "/" not in stirrup_bar_list[1]:
                            result = re.search('(\d+).*?(\d+).*', stirrup_bar_list[1])  # ø8@200
                            groups = list(result.groups())
                            self.dense_stirrup_dia = int(groups[0])
                            self.dense_stirrup_dis = int(groups[1])
                            self.Ndense_stirrup_dia = int(groups[0])
                            self.Ndense_stirrup_dis = int(groups[1])

                    stirrup_bodynum_list = stirrup_bodynum_text[4].split("x")
                    if len(stirrup_bodynum_list) > 1:
                        self.Hside_stirrup_bodynum = stirrup_bodynum_list[0][-1:]
                        self.Bside_stirrup_bodynum = stirrup_bodynum_list[1][0]

                # 第四种情况，一个柱角筋文本，无柱中部筋文本，文本行数在5行
                if BH_flag == False and len(new_number_text_list) == 5:
                    insitu_label_flag = True
                    angle_bar_text = new_number_text_list[2]
                    stirrup_dia_text = new_number_text_list[5]
                    stirrup_bodynum_text = new_number_text_list[6]

                    # 得到柱角筋属性
                    result = re.search('(\d+).*?(\d+).*', angle_bar_text[4])
                    groups = list(result.groups())  # 16ø200
                    if len(groups) > 1:
                        self.angle_bar_dia = int(groups[1][-2:])
                        self.angle_bar_num = 4
                        self.Hside_middle_bar_dia = int(groups[1][-2:])
                        self.Hside_middle_bar_num = int((int(groups[0]) - 4) / 4)
                        self.Bside_middle_bar_dia = int(groups[1][-2:])
                        self.Bside_middle_bar_num = int((int(groups[0]) - 4) / 4)

                    stirrup_bar_list = stirrup_dia_text[4].split("%%132")
                    if len(stirrup_bar_list) > 1:

                        num = 0
                        for f in stirrup_bar_list[1]:
                            if f == "@":
                                num += 1
                        if "/" in stirrup_bar_list[1] and num == 1:  # 针对 （%%132）ø8@100/200
                            result = re.search('(\d+).*?(\d+).*?(\d+).*', stirrup_bar_list[1])
                            groups = list(result.groups())
                            self.dense_stirrup_dia = int(groups[0])
                            self.dense_stirrup_dis = int(groups[1])
                            self.Ndense_stirrup_dia = int(groups[0])
                            self.Ndense_stirrup_dis = int(groups[2])
                        if "/" in stirrup_bar_list[1] and num == 2:  # 针对 （%%132）ø8@100/ø6@200
                            result = re.search('(\d+).*?(\d+).*?(\d+).*?(\d+).*', stirrup_bar_list[1])
                            groups = list(result.groups())
                            self.dense_stirrup_dia = int(groups[0])
                            self.dense_stirrup_dis = int(groups[1])
                            self.Ndense_stirrup_dia = int(groups[2])
                            self.Ndense_stirrup_dis = int(groups[3])
                        if num == 1 and "/" not in stirrup_bar_list[1]:
                            result = re.search('(\d+).*?(\d+).*', stirrup_bar_list[1])  # ø8@200
                            groups = list(result.groups())
                            self.dense_stirrup_dia = int(groups[0])
                            self.dense_stirrup_dis = int(groups[1])
                            self.Ndense_stirrup_dia = int(groups[0])
                            self.Ndense_stirrup_dis = int(groups[1])

                    stirrup_bodynum_list = stirrup_bodynum_text[4].split("x")
                    if len(stirrup_bodynum_list) > 1:
                        self.Hside_stirrup_bodynum = stirrup_bodynum_list[0][-1:]
                        self.Bside_stirrup_bodynum = stirrup_bodynum_list[1][0]
            return insitu_label_flag

    def get_attribs_legend_table(self, all_text, border_entity_info):  # 在柱的图例表中获取属性
        biaoge_list = border_entity_info.entity_object_dict['表格']
        # biaoge_list = [[9000, 1600, 11000, 5000]]
        legend_tablehead_name = ["截面", "编号", "标高", "纵筋", "箍筋/拉筋"]
        tablehead_text_list = [text for text in all_text if text[-1] in legend_tablehead_name]

        number_text_list = [text for text in all_text if
                            re.search('Z', text[-1])]
        attribs_text_list = [text for text in all_text if
                        re.search('(\d+)', text[-1])]

        # 确定含有图样例表头名的表
        legend_table_flag = False
        tablehead_num = 0
        table = []
        for biao in biaoge_list:
            biao_bbox = biao.bounding_rectangle.list
            # biao_bbox = biao
            for text in tablehead_text_list:
                iou = Iou_temp(biao_bbox, text[0:4])
                if iou != 0 and iou > 0:
                    tablehead_num += 1

            if tablehead_num > 5:
                table = biao_bbox
                break
        # 在确定的图样例表中获取柱的编号集和属性集合
        kz_list = []
        attribs_list = []
        if len(table) > 0:
            for text in number_text_list:
                flag = True
                # 过滤含"GB" 和 "YB" 的柱及带()的
                if "GB" in text[-1] or "YB" in text[-1]:
                    flag = False
                if "("  in text[-1]:
                    text[-1] = text[-1].split("(")[1].split(")")[0]

                iou = Iou_temp(table, text[0:4])
                if iou != 0 and iou > 0 and flag:
                    kz_list.append(text)

            for text in attribs_text_list:
                iou = Iou_temp(table, text[0:4])
                if iou != 0 and iou > 0:
                    attribs_list.append(text)
        # 获取以编号为key的属性值字典
        kz_attribs_dic = {}
        if len(kz_list) > 0 and len(attribs_list) > 0:
            for kz in kz_list:
                w, h = self.get_wh(kz[0:4])
                add_kz = [kz[0] - 2 * w, kz[1] + h, kz[2] + 2 * w,  kz[3] + 6 * h] # 这需要微调
                attribs = {}
                for attrib in attribs_list:
                    iou = Iou_temp(add_kz, attrib[0:4])
                    if iou != 0 and iou > 0:
                        dis = self.get_distance(kz[0:4], attrib[0:4])
                        attribs[dis] = attrib[-1]

                attribs_text = []
                if len(attribs) > 0:
                    # 对文本生成离编号距离进行排序
                    for each in sorted(attribs):
                        attribs_text.append(attribs[each])
                kz_attribs_dic[kz[-1]] = attribs_text
        for key, value in kz_attribs_dic.items():
            if self.pillar_number == key:
                legend_table_flag = True
                angle_bar_text = value[-2]
                num = 0
                # 纵筋分为3种情况
                for f in angle_bar_text:
                    if f == "+":
                        num += 1
                if num == 0:  # 12ø22
                    result = re.search('(\d+).*?(\d+).*', angle_bar_text)
                    groups = list(result.groups())
                    self.angle_bar_dia = int(groups[1][-2:])
                    self.angle_bar_num = 4
                    self.Hside_middle_bar_dia = int(groups[1][-2:])
                    self.Hside_middle_bar_num = int((int(groups[0]) - 4) / 4)
                    self.Bside_middle_bar_dia = int(groups[1][-2:])
                    self.Bside_middle_bar_num = int((int(groups[0]) - 4) / 4)

                if num == 1:  # 4ø22 + 8ø22
                    result = re.search('(\d+).*?(\d+).*?(\d+).*?(\d+).*', angle_bar_text)
                    groups = list(result.groups())
                    self.angle_bar_dia = int(groups[1][-2:])
                    self.angle_bar_num = int(groups[0])
                    self.Hside_middle_bar_dia = int(groups[3][-2:])
                    self.Hside_middle_bar_num = int((int(groups[2])) / 4)
                    self.Bside_middle_bar_dia = int(groups[3][-2:])
                    self.Bside_middle_bar_num = int((int(groups[2])) / 4)

                if num == 2:  # 4ø22 + 4ø22 + 6ø22
                    result = re.search('(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*', angle_bar_text)
                    groups = list(result.groups())
                    self.angle_bar_dia = int(groups[1][-2:])
                    self.angle_bar_num = int(groups[0])
                    self.Hside_middle_bar_dia = int(groups[3][-2:])
                    self.Hside_middle_bar_num = int(groups[2])
                    self.Bside_middle_bar_dia = int(groups[5][-2:])
                    self.Bside_middle_bar_num = int(groups[4])

                # 箍筋分为3种情况
                stirrup_bar_list = value[-1].split("%%132")
                if len(stirrup_bar_list) > 1:
                    num = 0
                    for f in stirrup_bar_list[1]:
                        if f == "@":
                            num += 1
                    if "/" in stirrup_bar_list[1] and num == 1:  # 针对 （%%132）ø8@100/200
                        result = re.search('(\d+).*?(\d+).*?(\d+).*', stirrup_bar_list[1])
                        groups = list(result.groups())
                        self.dense_stirrup_dia = int(groups[0])
                        self.dense_stirrup_dis = int(groups[1])
                        self.Ndense_stirrup_dia = int(groups[0])
                        self.Ndense_stirrup_dis = int(groups[2])
                    if "/" in stirrup_bar_list[1] and num == 2:  # 针对 （%%132）ø8@100/ø6@200
                        result = re.search('(\d+).*?(\d+).*?(\d+).*?(\d+).*', stirrup_bar_list[1])
                        groups = list(result.groups())
                        self.dense_stirrup_dia = int(groups[0])
                        self.dense_stirrup_dis = int(groups[1])
                        self.Ndense_stirrup_dia = int(groups[2])
                        self.Ndense_stirrup_dis = int(groups[3])
                    if num == 1 and "/" not in stirrup_bar_list[1]:
                        result = re.search('(\d+).*?(\d+).*', stirrup_bar_list[1])  # (%%132）ø8@200
                        groups = list(result.groups())
                        self.dense_stirrup_dia = int(groups[0])
                        self.dense_stirrup_dis = int(groups[1])
                        self.Ndense_stirrup_dia = int(groups[0])
                        self.Ndense_stirrup_dis = int(groups[1])

        return legend_table_flag

    def get_attribs_parameter_table(self, all_text, border_entity_info):  # 在柱的参数表中获取属性
        biaoge_list = border_entity_info.entity_object_dict['表格']
        # biaoge_list = [[9000, 1600, 11000, 4000]]
        parameter_table_name = ["柱号", "标高", "bxh", "全部纵筋", "角筋", "b边一侧中部筋", "h边一侧中部筋",
                                 "箍筋类型号", "箍筋", '节点核心区箍筋', '节点核心区']
        tablehead_text_list = [text for text in all_text if text[-1] in parameter_table_name]
        simple_parameter_table_name = set([text[-1] for text in tablehead_text_list])

        number_text_list = [text for text in all_text if
                            re.search('Z', text[-1])]
        attribs_text_list = [text for text in all_text if
                             re.search('(\d+)', text[-1])]

        # 确定含有柱参数表头名的表
        parameter_table_flag = False
        tablehead_num = 0
        table = []
        for biao in biaoge_list:
            biao_bbox = biao.bounding_rectangle.list
            # biao_bbox = biao
            for text in tablehead_text_list:
                iou = Iou_temp(biao_bbox, text[0:4])
                if iou != 0 and iou > 0:
                    tablehead_num += 1

            # 柱参数表头名至少在5个以上
            if tablehead_num > 5:
                table = biao_bbox
                break

        # 在确定的柱参数表中获取柱的编号集和属性集合
        kz_list = []
        attribs_list = []
        if len(table) > 0:
            for text in number_text_list:
                flag = True
                # 过滤含"GB" 和 "YB" 的柱
                if "GB" in text[-1] or "YB" in text[-1]:
                    flag = False

                iou = Iou_temp(table, text[0:4])
                if iou != 0 and iou > 0 and flag:
                    kz_list.append(text)

            for text in attribs_text_list:
                iou = Iou_temp(table, text[0:4])
                if iou != 0 and iou > 0:
                    attribs_list.append(text)

        # 获取以编号为key的属性值字典
        kz_attribs_dic = {}
        if len(kz_list) > 0 and len(attribs_list) > 0:
            for kz in kz_list:
                y1, y2 = kz[1], kz[3]
                attribs = []
                for text in tablehead_text_list:
                    x1, x2 = text[0:4]
                    head_list = [text[-1], ""]
                    temp_bbox = [x1, y1, x2, y2]

                    for attrib in attribs_list:
                        iou = Iou_temp(temp_bbox, attrib[0:4])
                        if iou != 0 and iou > 0:
                            attribs.pop()
                            attribs.append(attrib[-1])
                            break
                    attribs.append(head_list)
                kz_attribs_dic[kz[-1]] = attribs

        # 获取柱的配筋属性
        for key, value in kz_attribs_dic.items():
            if self.pillar_number == key:
                parameter_table_flag = True
                for l in value:
                    if "全部纵筋" in l and len(l[1]) > 0:
                        attrib = l[1]
                        result = re.search('(\d+).*?(\d+).*', attrib)
                        groups = list(result.groups())
                        self.angle_bar_dia = int(groups[1][-2:])
                        self.angle_bar_num = 4
                        self.Hside_middle_bar_dia = int(groups[1][-2:])
                        self.Hside_middle_bar_num = int((int(groups[0]) - 4) / 4)
                        self.Bside_middle_bar_dia = int(groups[1][-2:])
                        self.Bside_middle_bar_num = int((int(groups[0]) - 4) / 4)

                    if "角筋" in l and len(l[1]) > 0:
                        attrib = l[1]
                        result = re.search('(\d+).*?(\d+).*', attrib)
                        groups = list(result.groups())
                        self.angle_bar_dia = int(groups[1][-2:])
                        self.angle_bar_num = int(groups[0])

                    if "b边一侧中部筋" in l and len(l[1]) > 0:
                        attrib = l[1]
                        result = re.search('(\d+).*?(\d+).*', attrib)
                        groups = list(result.groups())
                        self.Bside_middle_bar_dia = int(groups[1][-2:])
                        self.Bside_middle_bar_num = int(groups[0])

                    if "h边一侧中部筋" in l and len(l[1]) > 0:
                        attrib = l[1]
                        result = re.search('(\d+).*?(\d+).*', attrib)
                        groups = list(result.groups())
                        self.Hside_middle_bar_dia = int(groups[1][-2:])
                        self.Hside_middle_bar_num = int(groups[0])

                    if "箍筋" in l and len(l[1]) > 0:
                        attrib = l[1]
                        stirrup_bar_list = attrib.split("%%132")
                        if len(stirrup_bar_list) > 1:
                            num = 0
                            for f in stirrup_bar_list[1]:
                                if f == "@":
                                    num += 1
                            if "/" in stirrup_bar_list[1] and num == 1:  # 针对 （%%132）ø8@100/200
                                result = re.search('(\d+).*?(\d+).*?(\d+).*', stirrup_bar_list[1])
                                groups = list(result.groups())
                                self.dense_stirrup_dia = int(groups[0])
                                self.dense_stirrup_dis = int(groups[1])
                                self.Ndense_stirrup_dia = int(groups[0])
                                self.Ndense_stirrup_dis = int(groups[2])
                            if "/" in stirrup_bar_list[1] and num == 2:  # 针对 （%%132）ø8@100/ø6@200
                                result = re.search('(\d+).*?(\d+).*?(\d+).*?(\d+).*', stirrup_bar_list[1])
                                groups = list(result.groups())
                                self.dense_stirrup_dia = int(groups[0])
                                self.dense_stirrup_dis = int(groups[1])
                                self.Ndense_stirrup_dia = int(groups[2])
                                self.Ndense_stirrup_dis = int(groups[3])
                            if num == 1 and "/" not in stirrup_bar_list[1]:
                                result = re.search('(\d+).*?(\d+).*', stirrup_bar_list[1])  # (%%132）ø8@200
                                groups = list(result.groups())
                                self.dense_stirrup_dia = int(groups[0])
                                self.dense_stirrup_dis = int(groups[1])
                                self.Ndense_stirrup_dia = int(groups[0])
                                self.Ndense_stirrup_dis = int(groups[1])

                    if "箍筋类型号" in l and len(l[1]) > 0:
                        attrib = l[1]
                        stirrup_bodynum_list = attrib.split("x")
                        if len(stirrup_bodynum_list) > 1:
                            self.Hside_stirrup_bodynum = stirrup_bodynum_list[0][-1:]
                            self.Bside_stirrup_bodynum = stirrup_bodynum_list[1][0]

                    if "节点核心区箍筋" or "节点核心区" in l and len(l[1]) > 0:
                        attrib = l[1]
                        result = re.search('(\d+).*?(\d+).*', attrib)
                        groups = list(result.groups())
                        self.node_core_stirrup_dis = int(groups[1])
                        self.node_core_stirrup_dia = int(groups[0])
        return parameter_table_flag

    def get_k(self, point1, point2):  # 得到柱line的斜率K，用于判断4*line的柱是否为矩形
        x = point2[0] - point1[0]
        y = point2[1] - point1[1]

        if x == 0:
            return float("inf")
        if y == 0:
            return 0
        if x != 0 and y != 0:
            return y / x

    def get_wh(self, pillar_list):  # 得到矩形w,h
        w, h = abs(pillar_list[2] - pillar_list[0]), abs(pillar_list[3] - pillar_list[1])
        return w, h

    def get_center(self, pillar_list):  # 得到矩形中心点
        w, h = self.get_wh(pillar_list)
        x, y = int(pillar_list[0] + w / 2), int(pillar_list[1] + h / 2)
        return x, y

    def get_distance(self, list1, list2):  # 得到两矩形框中心点距离
        x1, y1 = self.get_center(list1)
        x2, y2 = self.get_center(list2)
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return distance


