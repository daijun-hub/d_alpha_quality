import re
from ...utils import Iou_temp, extend_margin
from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils.utils_entity import get_form
from ....common.utils import get_centroid, point_euclidean_distance
from ....config_manager.text_config import TextType
from ...utils.utils_entity import *

def _trans_unit(unit_str: str):
    unit, unit_val = unit_str[-1].lower(), unit_str[:-1].strip()
    if unit == 'm':
        unit_val = float(unit_val) * 1000
    elif unit == 'c':
        unit_val = float(unit_val) * 10
    elif unit == 'd':
        unit_val = float(unit_val) * 100
    else:
        unit_val = float(unit_val)
    return str(int(unit_val))


def get_unit_text(border_entity):
    all_text_info = border_entity.border_text_info[TextType.ALL]
    for text in all_text_info:
        if re.search('开关.*((墙边)|(门边)).*距地.*[\d]+\.?[\d]*\s*[cmdCMD]', text.extend_message):
            return re.search('开关.*((墙边)|(门边)).*距地.*[\d]+\.?[\d]*\s*[cmdCMD]', text.extend_message).group()
        elif re.search('[\d]+\.?[\d]*[cmdCMD].*距地.*[\d]+\.?[\d]*\s*[cmdCMD]', text.extend_message):
            return re.search('[\d]+\.?[\d]*[cmdCMD].*距地.*[\d]+\.?[\d]*\s*[cmdCMD]', text.extend_message).group()
    else:
        return ''

# 合并且分类构件
class PingMianTuKaiGuan(ClassifiedEntity):
    
    chinese_name = "平面图开关"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        
        self.chinese_name = "平面图开关"
        self.entity_base_type = EntityBaseType.ELECTRIC_DEVICE
        # 碧桂园产品要求添加属性-形式，本质为要通过此属性区分不同图例。
        self.form = get_form(entity_object.bounding_rectangle.list, border_entity, self.chinese_name)

        # 平面位置
        self.distance_to_wall = self.get_pm_kg_position_entity(entity_object, border_entity, 1200)
        # 安装高度
        # self.install_height = self.get_install_height(border_entity)
        height_target_pattern = r'开关.*?[均]?距地(\s*[\d]+[.]?[\d]*\s*[cmd]?)m'
        self.install_height, self.install_height_bbox = get_install_height("开关", self.bounding_rectangle.list, border_entity, height_target_pattern)

    def get_pm_kg_position_entity(self, entity_object, border_entity, extend_margin):
        """
            获取平面开关的位置

            Args:
                entity_object: 构件对象
                border_entity: 图框全量信息

            Returns:
                平面开关位置
            """
        unit_text = get_unit_text(border_entity)
        if not unit_text:
            default_position = ''
            print('Error: Not found the distance_to_wall plane distance !')
        else:
            default_position = _trans_unit(re.search("[\d]+\.?[\d]*\s*[cmdCMD]", unit_text).group())
        pattern = "^\d{1,}$"
        bbox = entity_object.bounding_rectangle.list
        point_center = get_centroid(bbox)
        ratio = border_entity.ratio
        extend_margin = int(extend_margin * ratio[0])
        bbox_temp = [point_center[0] - extend_margin, point_center[1] - extend_margin, point_center[0] + extend_margin,
                     point_center[1] + extend_margin]
        all_text_info = border_entity.mark_object_dict.get('尺寸标注', [])

        label_text_info = [text for text in all_text_info if re.search(pattern, text.extend_message)]

        if len(label_text_info) == 0:
            return None
        label_text_info.sort(
            key=lambda x: point_euclidean_distance(point_center, get_centroid(x.bounding_rectangle.list)),
            reverse=False)

        first_text = get_centroid(label_text_info[0].bounding_rectangle.list)
        if first_text[0] in range(bbox_temp[0], bbox_temp[2]) and first_text[1] in range(bbox_temp[1], bbox_temp[3]):
            print(f'\033[1;31m 从平面图中获取平面开关平面距离{label_text_info[0].extend_message}mm \033[0m')
            return label_text_info[0].extend_message
        else:
            print(f'\033[1;31m 从备注文本中获取平面开关平面距离{default_position}mm \033[0m')
            return default_position

    # def get_install_height(self, border_entity):
    #     bbox = self.bounding_rectangle.list
    #
    #     # 获取所有虚框
    #     dash_border_list = border_entity.special_info_dict['dash_border_list']
    #     # 判断该构件是否在某个虚框中
    #     outer_border = None
    #     for dash_border in dash_border_list:
    #         iou = Iou_temp(extend_margin(bbox, 10), dash_border)
    #         if iou > 0.9:
    #             outer_border = dash_border
    #             print(f'\033[1;33m 找到构件所在虚框 {dash_border} \033[0m')
    #             break
    #
    #     # 获取引线
    #     anno_line_list = border_entity.special_info_dict['annotation_info_list']
    #
    #     unit_text = get_unit_text(border_entity)
    #     if unit_text:
    #         height_str = re.findall(r'[\d]+\.?[\d]*\s*[cmdCMD]', unit_text)[1]
    #         default_height = _trans_unit(height_str)
    #     else:
    #         default_height = ''
    #         print('Error: Not found the install height of switch!')
    #
    #
    #     min_iou = 0.01
    #     target_text = None
    #     for line_l, text_l, main_end_point in anno_line_list:
    #         # line_l格式为：(支线，主线)，文本在主线两侧
    #         branch_line = line_l[0]
    #         target_text_list = [t for t in text_l if re.search('h=.*[cmdCMD]', t)]
    #         if len(target_text_list) > 0:
    #             if outer_border is not None:
    #                 # 在虚框的构件，用虚框找引线
    #                 iou = Iou_temp(extend_margin(branch_line, 10), extend_margin(outer_border, 10))
    #             else:
    #                 iou = Iou_temp(extend_margin(branch_line, 10), extend_margin(bbox, 10))
    #             if iou > min_iou:
    #                 min_iou = iou
    #                 target_text = target_text_list[0]
    #     if target_text:
    #         height_str = re.findall('h=(.*[cmdCMD])', target_text)[0]
    #         height = _trans_unit(height_str)
    #         print(f'\033[1;31m 从平面图引线中获取平面开关安装高度{height}mm \033[0m')
    #         return height
    #     else:
    #         # 从平面图的备注文本中获取
    #         print(f'\033[1;31m 从备注文本中获取平面开关安装高度{default_height}mm \033[0m')
    #         return default_height

