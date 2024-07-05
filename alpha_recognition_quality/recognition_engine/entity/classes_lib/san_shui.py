from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity
from ...utils import *


# 分类类型
class SanShui(ClassifiedEntity):

    chinese_name = "散水"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "散水"
        self.entity_base_type = EntityBaseType.BASE
        #位置
        self.position = self.get_position(border_entity)
        #坡度
        self.gradient = self.get_gradient(border_entity)
        #宽度
        self.width = self.get_width(border_entity)
        #明/暗散水
        self.is_ming_san_shui = self.get_is_ming_san_shui(border_entity)

    def get_position(self, border_entity):
        position = None
        position = get_contour_from_bbox(remove_margin(self.bounding_rectangle.list))

        return position

    def get_gradient(self, border_entity):
        gradient = None
        annotation_list = border_entity.mark_object_dict['引注']
        for anno in annotation_list:
            anno_contour_extend = get_contour_from_bbox(extend_margin(anno.bounding_rectangle.list))
            san_shui_contour = get_contour_from_bbox(extend_margin(self.bounding_rectangle.list))
            if get_contours_iou(anno_contour_extend, san_shui_contour):
                anno_text = ''.join(anno.labeled_text)
                if anno_text:
                    if re.search('散水', anno_text):
                        gradient = int(''.join(re.findall(r"散水.*\((\d*)%\)", anno_text)))
                        break

        return gradient

    def get_width(self, border_entity):
        width = None
        # # 文本
        # all_text_info = border_entity[TextType.ALL]
        # # 尺寸标注文本
        # size_text_info_list = list()
        # size_pat = "\d+\.\d{2}$"
        # for text_info in all_text_info:
        #     text_str = text_info.extend_message
        #     if re.search(size_pat, text_str):
        #         size_text_info_list.append(text_info)

        # #尺寸标注bbox
        # chi_cun_bbox_list = list()
        # for chi_cun in border_entity.mark_object_dict["尺寸标注"]:
        #     chi_cun_bbox_list.append(chi_cun.bounding_rectangle.list)
        #
        # chi_cun_bbox_text_dict = {}
        # for bbox in chi_cun_bbox_list:
        #     for text in size_text_info_list:
        #         if text.extend_message not in chi_cun_bbox_text_dict.values():
        #             if get_contours_iou(get_contour_from_bbox(bbox), get_contour_from_bbox(text.bbox.list)):
        #                 chi_cun_bbox_text_dict[text.extend_message] = bbox

        #获得尺寸标注对象list
        chi_cun_mark_list = border_entity.mark_object_dict["尺寸标注"]
        for chi_cun_mark in chi_cun_mark_list:
            if re.match("\d+$", chi_cun_mark.extend_message):
                chi_cun_mark_contour = get_contour_from_bbox(chi_cun_mark.bounding_rectangle.list)
                san_shui_contour = get_contour_from_bbox(extend_margin(self.bounding_rectangle.list))
                if get_contours_iou(chi_cun_mark_contour, san_shui_contour):
                    width = int(chi_cun_mark.extend_message)
                    break

        return width

    def get_is_ming_san_shui(self, border_entity):
        is_ming_san_shui = None
        # 图框基本信息
        ratio = border_entity.ratio
        space_scale = border_entity.space_scale
        border_coord = border_entity.border_coord

        class_to_check = ["Line", "Polyline", "Polyline2d"]

        origin_border_entity_info = border_entity.origin_border_entity_info



        # 查找带线型类型的开闭线图元
        apron_layer_to_check = ["apron"]
        apron_list = get_origin_border_entity_info_with_style_rule(origin_border_entity_info, apron_layer_to_check,
                                                                       class_to_check, space_scale, border_coord,
                                                                       ratio)[
            "apron"]

        san_shui_contour = get_contour_from_bbox(extend_margin(self.bounding_rectangle.list))
        for line in apron_list:
            if line_overlap_poly(line[0], san_shui_contour):
                if re.search("DASH", line[1]):
                    is_ming_san_shui = False
                else:
                    is_ming_san_shui = True

        return is_ming_san_shui


