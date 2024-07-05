import re

from ..space import Space
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity
from ...utils.utils_space import get_space_related_entity, get_space_related_space
from ....common.utils import expand_contour, get_contours_iou, get_contour_from_bbox
import cv2
import time
# TODO: 空间先不实现特殊属性，仅仅实现基础属性，待后续新规则用到的时候再添加

class WeiShengJian(Space):
    chinese_name = "卫生间"

    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "卫生间"
        self.space_base_type = SpaceBaseType.INDOOR_FUNCTIONAL_SPACE
        self.vpipe_num = None

        # self.get_related_entities(border_entity)
        # self.get_vpipe_num(border_entity)
        
    def get_related_entities(self, border_entity):
        """
        获取相关的构件
        Args:
            border_entity: 

        Returns:

        """
        # 立管
        # img_copy = border_entity.image_manager.load_from_manager('border_image_with_wall')
        vpipe_num = 0
        print(self.bbox)
        for k in border_entity.entity_object_dict.keys():
            if re.match('.*立管$', k):
                entity_list = border_entity.entity_object_dict.get(k,[])
                
                # for entity_obj in entity_list:
                #     bbox = entity_obj.bounding_rectangle
                #     print(f"{k}, {bbox}")
                    
                #     img_copy = cv2.rectangle(img_copy, (bbox[:2]),(bbox[2:]), (255, 255, 255), 10)

                entity_list = get_space_related_entity(self, border_entity, k, use_bbox=True)

                self.related_entities_dict[k] = entity_list
                vpipe_num += len(entity_list)
        self.get_related_shui_guanjing(border_entity)
        # 更新跨对象属性
        # cv2.imwrite( f"{int(time.time())}.png",img_copy)
        self.vpipe_num = vpipe_num
        self.deng_ju_list = self.get_related_entity(border_entity, "灯具")
        self.pu_tong_deng_list = self.get_related_entity(border_entity, "普通灯")

    def get_related_shui_guanjing(self, border_entity):
        """
        获取卫生间附近的水管井
        :param border_entity:
        :return:
        """
        space_name = '套内水管井'
        related_obj_list = get_space_related_space(self, border_entity, space_name, margin=100)

        self.related_space_dict[space_name] = related_obj_list

    def get_related_entity(self, border_entity, entity_name, min_iou=0.5):
        """
        根据构件名字获取构件列表
        Args:
            border_entity:
            entity_name:
            min_iou:

        Returns:

        """
        related_entity_list = []
        entity_list = border_entity.entity_object_dict.get(entity_name, [])
        for entity_obj in entity_list:
            bbox = entity_obj.bounding_rectangle.list
            cnt = get_contour_from_bbox(bbox)
            if get_contours_iou(expand_contour(self.contour.contour, 400 * border_entity.ratio[0]), cnt) > min_iou:
                related_entity_list.append(entity_obj)
        return related_entity_list