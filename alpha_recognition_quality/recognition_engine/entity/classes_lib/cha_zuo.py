from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils.utils_entity import *
from ....config_manager.decor_electric.drawing_config import DrawingType
from ....common.utils2 import load_drawing_pkl


# 合并且分类类型
class ChaZuo(ClassifiedEntity):
    
    chinese_name = "插座"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "插座"
        self.entity_base_type = EntityBaseType.ELECTRIC_DEVICE
        # 碧桂园产品要求添加属性-形式，本质为要通过此属性区分不同图例。
        self.form = get_form(entity_object.bounding_rectangle.list, border_entity, self.chinese_name)
        self.distance_to_wall = get_distance_to_wall(self.chinese_name, self.bounding_rectangle.list, border_entity)
        # 获取安装高度
        height_target_pattern = r'插座[均]?距地(\s*[\d]+[.]?[\d]*\s*[cmd]?)m'
        self.install_height, self.install_height_bbox = get_install_height(self.chinese_name, self.bounding_rectangle.list, border_entity, height_target_pattern)
        self.plug_height_map = {}


    def get_cross_border_attribs(self, border_entity, building_object):
        try:
            self.get_new_install_height(border_entity, building_object)
        except Exception:
            print('Error: 插座跨图框属性获取失败')


    def get_new_install_height(self, border_entity, building_object):
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
            self.get_table_install_height(file_id, border_entity_info)


    def get_table_install_height(self,file_id, border_entity_info):
        self.plug_height_map = {}
        all_text_info = border_entity_info.border_text_info[TextType.ALL]
        # 安装方式
        the_way = {}
        install_way_list = []
        for text in all_text_info:
            if re.search('安装方式', text.extend_message):
                if not the_way.get(text.bbox[0], None):
                    the_way[text.bbox[0]] = 1
                    install_way_list.append(text)

        if not install_way_list:
            return False
        # 唯一强电箱文本,并纵向外扩
        plug_list = [text for text in all_text_info if re.search('.*插座.*', text.extend_message)]
        if not plug_list:
            return False
        keyword_bbox = plug_list[0].bbox.list
        # 距离配电箱较近的安装方式列，并横向外扩
        install_way_list.sort(
            key=lambda x: point_euclidean_distance(get_centroid(keyword_bbox), get_centroid(x.bbox.list)),
            reverse=False)
        left_install_way = install_way_list[0]
        right_install_way = install_way_list[1]

        for plug in plug_list:
            plug_key = re.sub(r"[()（）]", "", plug.extend_message)
            for text in all_text_info:
                re_match = re.search('h=?(.*)m', text.extend_message)
                if re_match:
                    if plug.bbox.list[0] < left_install_way.bbox.list[0]:
                        entity_box_left = [
                            abs(left_install_way.bbox.list[0] - 400),
                            abs(plug.bbox[1] - 100),
                            abs(left_install_way.bbox.list[2] + 400),
                            abs(plug.bbox[3] + 100)
                        ]
                        if text.bbox[0] >= entity_box_left[0] and text.bbox[1] >= entity_box_left[1] and text.bbox[2] <= entity_box_left[2] and text.bbox[3] <= entity_box_left[3]:
                            if not self.plug_height_map.get(plug_key, None):
                                plug_value = text.bbox.list + ["%.2f" % float(re_match.group(1))]
                                self.plug_height_map[plug_key] = plug_value
                                # print("获取 %s 安装高度为：%s m" % (plug.extend_message, re_match.group(1)))
                                break

                    else:
                        entity_box_right = [
                            abs(right_install_way.bbox.list[0] - 400),
                            abs(plug.bbox[1] - 100),
                            abs(right_install_way.bbox.list[2] + 400),
                            abs(plug.bbox[3] + 100)
                        ]
                        if text.bbox[0] >= entity_box_right[0] and text.bbox[1] >= entity_box_right[1] and text.bbox[2] <= entity_box_right[2] and text.bbox[3] <= entity_box_right[3]:
                            if not self.plug_height_map.get(plug_key, None):
                                plug_value = text.bbox.list + ["%.2f" % float(re_match.group(1))]
                                self.plug_height_map[plug_key] = plug_value
                                # print("获取 %s 安装高度为：%s m" % (plug.extend_message, re_match.group(1)))
                                break

                else:
                    if not self.plug_height_map.get(plug_key, None):
                        self.plug_height_map[plug_key] = None

