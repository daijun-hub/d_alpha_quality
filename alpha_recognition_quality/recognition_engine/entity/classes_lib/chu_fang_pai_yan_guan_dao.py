from ..base_type import EntityBaseType
from ...border_entity import BorderEntity
from ..entity import ClassifiedEntity, Entity
from ....common.utils import get_centroid
from ....config_manager.text_config import TextType
import re
from ...utils import *
from ....recognition_engine.base.contour import Contour

# 分类构件
class ChuFangPaiYanGuanDao(ClassifiedEntity):
    chinese_name = "厨房排烟管道"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "厨房排烟管道"
        self.entity_base_type = EntityBaseType.PIPE
        self.space_type = "厨房"
        self.bbox = self.bounding_rectangle
        self.center = [(self.bbox[0] + self.bbox[2]) // 2, (self.bbox[1] + self.bbox[3]) // 2]

        self.size = None
        # 根据构件bbox内的图元，获取厨房油烟井的长和宽
        self.size, contour = get_cfyyj_w_h(entity_object, border_entity)
        if self.size is None:
            # 通过尺寸标注获取构件的长宽
            self.size = self.get_size(border_entity)
        if contour is not None:
            print("len(contour)", len(contour))
            if len(contour) == 4:
                print("Adding 厨房排烟管道 conotur info ... ")
                self.contour = Contour(contour, border_entity.ratio)
        print("厨房排烟管道 size", self.size)

    def get_size(self, border_entity):
        mark_list = border_entity.mark_object_dict["尺寸标注"]
        size = None
        all_mark_list = [mark.bounding_rectangle.list + [mark.extend_message] for mark in mark_list if
                         re.search('(\d+)', str(mark.extend_message))]
        x1, y1, x2, y2 = self.bounding_rectangle[0], self.bounding_rectangle[1], \
                         self.bounding_rectangle[2], self.bounding_rectangle[3]
        w, h = 1.5 * abs(x2 - x1), 1.5 * abs(y2 - y1)
        x3, y3, x4, y4 = x1 - w, y1 - h, x2 + w, y2 + h

        x_size, y_size = 0, 0
        for mark_list in all_mark_list:
            bbox = mark_list[0:4]
            y, x = bbox[1] + int(abs(bbox[3] - bbox[1]) / 2), bbox[0] + int(abs(bbox[2] - bbox[0]) / 2)
            if (y > y2 or y < y1) and x3 < x < x4 and y3 < y < y4:
                x_size = int(float(mark_list[4]))

            if y1 < y < y2 and x3 < x < x4 and y3 < y < y4:
                y_size = int(float(mark_list[4]))

        if x_size != 0 and y_size != 0:
            size = (min(x_size, y_size), max(x_size, y_size))
        return size if size else None