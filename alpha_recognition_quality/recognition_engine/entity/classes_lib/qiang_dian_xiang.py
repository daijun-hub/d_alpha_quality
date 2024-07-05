"""
强电箱
又名：配电箱
"""
from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils.utils_entity import *
from ....config_manager.decor_electric.drawing_config import DrawingType
from ....common.utils2 import load_drawing_pkl


class QiangDianXiang(ClassifiedEntity):
    chinese_name = "强电箱"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "强电箱"
        self.entity_base_type = EntityBaseType.ELECTRIC_DEVICE
        # 平面位置
        self.position = get_dx_position_entity(self, border_entity, extend_margin=1200)
        # 安装高度
        self.install_heights = []

    def get_cross_border_attribs(self, border_entity, building_object):
        try:
            self.update_install_height(border_entity, building_object)
        except Exception:
            print('Error: 强电箱跨图框属性获取失败')

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
        keyword = [text for text in all_text_info if re.search('家居配电箱', text.extend_message)]
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
        # 配电箱行、安装方式列的安装高度
        install_heights_list = []
        for install_height in install_height_list:
            install_height_bbox = install_height.bbox.list
            point_center = get_centroid(install_height_bbox)
            if point_center[0] in range(install_way_bbox_extend[0], install_way_bbox_extend[2]) and point_center[1] in range(keyword_bbox_extend[1], keyword_bbox_extend[3]):
                install_height_text = install_height.extend_message
                print(f'找到家居配电箱的安装高度{install_height_text}')
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
