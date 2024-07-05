import re
import numpy.ma
from ..base_type import EntityBaseType
from ..entity import Entity, ClassifiedEntity
from ...border_entity import BorderEntity
from ...utils.utils_entity import *
from ....common.utils2 import load_drawing_pkl
from ....config_manager.decor_electric.drawing_config import DrawingType

from ....common.log_manager import LOG as logger


# 合并且分类类型
class KeShiDuiJiang(ClassifiedEntity):
    chinese_name = "可视对讲"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "可视对讲"
        self.entity_base_type = EntityBaseType.ELECTRIC_EQUIPMENT
        # 安装高度
        self.install_heights = []

        ## 平面位置
        self.position = self.get_keshi_position_entity(border_entity)

    def get_cross_border_attribs(self, border_entity, building_object):
        try:
            self.update_install_height(border_entity, building_object)
            if not self.position:
                self.position = self.get_keshi_cross_border_position(border_entity, building_object)
            # self.position = self.get_position(border_entity)
        except Exception as e:
            print(f'Error: {e}, 可视对讲跨图框属性获取失败')

    def update_install_height(self, border_entity, building_object):
        # 图例及主要设备材料表获取安装高度
        for special_drawing_dict in building_object.special_drawing_list:
            info_dict = special_drawing_dict.get(DrawingType.DECORATION_ELECTRIC_EQUIPMENT_SCHEDULE)
            if not info_dict:
                continue
            file_id = info_dict['file_id']
            border_entity_info = load_drawing_pkl(file_id)
            # 板房与货量的subproject_name不一样，只拿一种
            if border_entity.subproject_name != border_entity_info.subproject_name:
                continue
            self.get_height(file_id, border_entity_info)

    def get_height(self, file_id, border_entity_info):
        self.install_heights = []
        self.install_heights_bbox = []
        self.install_heights_file_id = border_entity_info.cad_border_id
        self.install_heights_pickle_id = file_id
        all_text_info = border_entity_info.border_text_info[TextType.ALL]
        # 安装方式
        install_way_list = [text for text in all_text_info if re.search('安装方式', text.extend_message)]
        if not install_way_list:
            return False
        # 唯一强电箱文本,并纵向外扩
        keyword = [text for text in all_text_info if re.search('可视对讲.*?室内分机', text.extend_message)]
        if not keyword:
            return False
        keyword_bbox = keyword[0].bbox.list
        extend_y_distance = keyword_bbox[3] - keyword_bbox[1]
        keyword_bbox_extend = [keyword_bbox[0], (keyword_bbox[1] - extend_y_distance),
                               keyword_bbox[2], (keyword_bbox[3] + extend_y_distance)]
        # 距离配电箱较近的安装方式列，并横向外扩
        install_way_list.sort(
            key=lambda x: point_euclidean_distance(get_centroid(keyword_bbox), get_centroid(x.bbox.list)),
            reverse=False)
        install_way_bbox = install_way_list[0].bbox.list
        extend_x_distance = install_way_bbox[2] - install_way_bbox[0]
        install_way_bbox_extend = [(install_way_bbox[0] - extend_x_distance), install_way_bbox[1],
                                   (install_way_bbox[2] + extend_x_distance), install_way_bbox[3]]
        # 安装高度
        install_height_list = [text for text in all_text_info if re.search('h=?.*m', text.extend_message)]
        if not install_height_list:
            return False
        # 可视对讲行、安装方式列的安装高度
        install_heights_list = []
        for install_height in install_height_list:
            install_height_bbox = install_height.bbox.list
            point_center = get_centroid(install_height_bbox)
            if point_center[0] in range(install_way_bbox_extend[0], install_way_bbox_extend[2]) and point_center[
                1] in range(keyword_bbox_extend[1], keyword_bbox_extend[3]):
                install_height_text = install_height.extend_message
                print(f'找到可视对讲室内分机的安装高度{install_height_text}')
                h = re.search("\d+(\.\d+)?[cCmMdD]{0,2}$", install_height_text)
                h = h.group() if h else install_height_text
                self.install_heights.append(h)
                install_heights_list.append(install_height)
        bbox = install_heights_list[0].bbox.list
        for install_heights in install_heights_list:
            bbox[0] = min(bbox[0], install_heights.bbox.list[0])
            bbox[1] = min(bbox[1], install_heights.bbox.list[1])
            bbox[2] = max(bbox[2], install_heights.bbox.list[2])
            bbox[3] = max(bbox[3], install_heights.bbox.list[3])
        self.install_heights_bbox = bbox

    def two_bbox_distance(self, target, text_info, flag=True):
        if flag:
            mid_text_x = (text_info[0] + text_info[2]) // 2
            return numpy.ma.sqrt(np.power(target[0] - mid_text_x, 2) + np.power(target[1] - text_info[3], 2))
        else:
            return numpy.ma.sqrt(np.power(target[2] - text_info[2], 2) + np.power(target[3] - text_info[3], 2))

    def get_position(self, border_entity_info):
        all_text_info_obj = border_entity_info.border_text_info[TextType.ALL]
        all_text_info = [text.bbox.list + [text.extend_message] for text in all_text_info_obj]
        mark_text_info = []
        if border_entity_info.mark_object_dict.get("尺寸标注"):
            mark_text_info = [obj.bounding_rectangle.list + [obj.extend_message] for obj in
                              border_entity_info.mark_object_dict.get("尺寸标注") if
                              re.search("[\d]+\.?[\d]*$", obj.extend_message)]
        mark_text_info.extend([item for item in all_text_info if re.search("[\d]+\.?[\d]*$", item[-1])])
        text_info_list = []
        other_text_info_list = []
        for text in all_text_info:
            if re.search("对讲分机", text[-1]) and not re.search("((备注)|(注)).*对讲分机", text[-1]) \
                    and not re.search("对讲分机.*((示意)|(尺寸))", text[-1]) and not re.search("对讲分机.*面板", text[-1]):
                text_info_list.append(text)
            if re.search("86底盒", text[-1]):
                other_text_info_list.append(text)
        print(f"======找到可视对讲分机：{text_info_list}=======")
        print(f'===============other可视对讲分机: {other_text_info_list}===========')
        if text_info_list and other_text_info_list:
            o_y = min(other_text_info_list, key=lambda v: v[1])
            y = min(text_info_list, key=lambda v: v[1])
            if y[1] - o_y[1] > 40:
                text_info_list = []

        if len(text_info_list) == 0 and len(other_text_info_list) > 0:
            min_y = min(other_text_info_list, key=lambda v: v[1])
            temp_l = [item for item in other_text_info_list if item[1] in range(min_y[1] - 3, min_y[1] + 25)]
            print(f'temp_l: {temp_l}')
            temp_l = sorted(temp_l, key=lambda x: x[0])
            if len(temp_l) == 2:
                text_info_list.append(temp_l[1])
            elif len(temp_l) == 1 or len(temp_l) > 2:
                text_info_list.append(temp_l[(len(temp_l) - 1) // 2])
        if len(text_info_list) == 1:
            print(text_info_list, text_info_list[0])
            text_info = text_info_list[0]
            width = abs(text_info[2] - text_info[0])
            left_x = text_info[0] - width * 3
            right_x = text_info[2] + width * 3
            mid_xy = ((text_info[0] + text_info[2]) // 2, text_info[1])
            text_result = []
            for text in mark_text_info:
                if text[0] >= left_x and text[2] <= right_x and text[3] < text_info[1]:
                    text_result.append(text)
        elif len(text_info_list) > 1:
            mid_xy, max_list = None, []
            for text_info in text_info_list:
                width = abs(text_info[2] - text_info[0])
                left_x = text_info[0] - width * 3
                right_x = text_info[2] + width * 3
                temp = []
                for text in mark_text_info:
                    if text[0] >= left_x and text[2] <= right_x and text[3] < text_info[1]:
                        temp.append(text)
                if len(temp) > 0 and len(temp) > len(max_list):
                    max_list = temp
                    mid_xy = ((text_info[0] + text_info[2]) // 2, text_info[1])
            text_result = max_list
        else:
            text_result = []
        print(f"可视对讲上附近的数字文本：{text_result}")
        if text_result:
            text_result.sort(key=lambda x: self.two_bbox_distance(mid_xy, x))
            lately_text = text_result[0]
            print(f"可视频对讲最近数字文本：{lately_text}")
            height = abs(lately_text[3] - lately_text[1]) // 4
            up_y = lately_text[1] - height
            down_y = lately_text[3] + height
            mid_x = (lately_text[0] + lately_text[2]) // 2
            l_text_result, r_text_result = [], []
            for text in mark_text_info:
                if text[:4] == lately_text[:4]:
                    continue
                if text[1] >= up_y and text[3] <= down_y:
                    if text[2] < mid_x:
                        l_text_result.append(text)
                    elif text[0] > mid_x:
                        r_text_result.append(text)
            print(f"======= 找到可视对讲分机距离左右两侧数字文本：{l_text_result}, {r_text_result}======= ")
            if l_text_result or r_text_result:
                ret = []
                if l_text_result:
                    l_text_result = list(set([tuple(item) for item in l_text_result]))
                    l_text_result.sort(key=lambda x: self.two_bbox_distance(lately_text, x, flag=False))
                    ret.append(l_text_result[0][-1])
                ret.append(lately_text[-1])
                if r_text_result:
                    r_text_result = list(set([tuple(item) for item in r_text_result]))
                    r_text_result.sort(key=lambda x: self.two_bbox_distance(lately_text, x, flag=False))
                    ret.append(r_text_result[0][-1])
                # try:
                #     ret = int(sum([float(v[-1]) for v in text_result[:3]]))
                # except Exception as e:
                #     ret = None
                #     logger.error(f"可视对讲报错，错误:{str(e)}, text_result:{text_result}")
                return ret
            else:
                print("===== 可视对象位置没找到 =====")
                return []
        else:
            print("===== 可视对象位置没找到 =====")
            return []

    def get_keshi_position_entity(self, border_entity):
        return self.get_position(border_entity)

    def get_keshi_cross_border_position(self, border_entity, building_object):
        for special_drawing_dict in building_object.special_drawing_list:
            info_dict = special_drawing_dict.get(DrawingType.DECORATION_ELECTRIC_EQUIPMENT_SCHEDULE)
            if not info_dict:
                continue
            file_id = info_dict['file_id']
            border_entity_info = load_drawing_pkl(file_id)
            # 板房与货量的subproject_name不一样，只拿一种
            if border_entity.subproject_name != border_entity_info.subproject_name:
                continue
            return self.get_position(border_entity_info)
