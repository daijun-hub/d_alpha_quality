from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
import cv2
from ....common.utils_draw_and_rule import get_origin_border_entity_info_rule
from ....analysis_engine.utils.utils_combination import plot_origin_entity
from ....common.utils import *
import numpy as np


class XiLianPen(ClassifiedEntity):
    chinese_name = "洗脸盆"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "洗脸盆"
        self.entity_base_type = EntityBaseType.KITCHEN_RESTROOM_OBJECT
        self.floor = None  # 待定要不要开发的意义
        self.width, self.length, self.basis_point, self.basis_line = self.get_basis_point_line(border_entity)

    def get_basis_point_line(self, border_entity):

        image_manager = border_entity.image_manager
        height, width = image_manager.img_height, image_manager.img_width  # 图框的尺寸
        axis_bbox_list = border_entity.axis_net_bbox_list

        origin_border_entity_info = border_entity.origin_border_entity_info
        space_scale = border_entity.space_scale
        border_coord = border_entity.border_coord
        ratio = border_entity.ratio

        layer_check_drain = ["washbasin"]
        class_check_drain = ["Line", "Polyline", "Polyline2d", 'Ellipse', 'Arc']
        line_drain_dict = get_origin_border_entity_info_rule(origin_border_entity_info, layer_check_drain,
                                                             class_check_drain,
                                                             space_scale, border_coord, ratio)
        line_drain_list = list()
        for _, line_list in line_drain_dict.items():
            line_drain_list.extend(line_list)

        img_drain = np.zeros((height, width, 3), dtype="uint8")
        line_drain_list_ = []
        add = 0.4  # 边框外扩值幅度，跟实际情况调整

        bbox = self.bounding_rectangle.list
        w0, h0 = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x1, y1, x2, y2 = [int(bbox[0] - add * w0), int(bbox[1] - add * h0), int(bbox[2] + add * w0),
                          int(bbox[3] + add * h0)]
        for line_drain in line_drain_list:
            w, h = line_drain[2] - line_drain[0], line_drain[3] - line_drain[1]
            x, y = [int(line_drain[0] + 0.5 * w), int(line_drain[1] + 0.5 * h)]
            dis = ((line_drain[3] - line_drain[1]) ** 2 + (line_drain[2] - line_drain[0]) ** 2) ** 0.5
            if x1 < x < x2 and y1 < y < y2 and dis < (1 + add) * h0:
                line_drain_list_.append(line_drain)
            # cv2.rectangle(img_drain, tuple(bbox[:2]), tuple(bbox[2:]), (255, 0, 0), 1)
        # backgroud_image = np.zeros((height, width, 3), dtype="uint8")
        # img_without_wall = border_entity.image_manager.load_from_manager('border_image_with_wall')
        for line_drain in line_drain_list_:
            if len(line_drain) == 4:
                dis = ((line_drain[3] - line_drain[1]) ** 2 + (line_drain[2] - line_drain[0]) ** 2) ** 0.5
                if dis < 2000:
                    cv2.line(img_drain, tuple(line_drain[:2]), tuple(line_drain[2:]), (255, 255, 255), 1)
            if len(line_drain) == 11:
                plot_origin_entity('ellipse', line_drain, img_drain)
            if len(line_drain) == 8:
                plot_origin_entity('arc', line_drain, img_drain)
        # cv2.imwrite('img_gray.png', img_drain)
        gray = cv2.cvtColor(img_drain, cv2.COLOR_BGR2GRAY)
        if '3.4' in cv2.__version__:
            _, contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_ = []
        for cnt in contours:
            area = contour_area_in_reality(cnt, ratio)
            if area > 0.01:
                contours_.append(cnt)

        # cv2.drawContours(backgroud_image, contours_, -1, (0, 0, 255), 1, lineType=cv2.LINE_AA)
        # cv2.imwrite('img_gray2.png', backgroud_image)

        background = np.zeros((height, width, 3), dtype=np.uint8)
        # backgroud_image2 = np.zeros((height, width, 3), dtype="uint8")
        extend = int(100 * ratio[0])
        if len(contours_) > 0:
            for cnt in contours_:
                cv2.fillPoly(background, [cnt], (255, 255, 255))
                gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
                kernel_size = int(extend)
                if kernel_size < 3:
                    kernel_size = 3
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
                image = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

            # Find contours
            if '3.4' in cv2.__version__:
                _, new_contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            else:
                new_contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # cv2.drawContours(backgroud_image2, new_contours, -1, (0, 0, 255), 1, lineType=cv2.LINE_AA)

            if len(new_contours) > 0:
                cnt = self.get_max_cnt(new_contours)
                x, y, w, h = cv2.boundingRect(cnt)
                jidian = [x, y]
                bbox = [x, y, x + w, y + h]
                for index, e in enumerate(bbox):
                    self.bounding_rectangle.list[index] = e
                # 目前图纸中洗脸盆在空间中会有两种情况：横放和竖放,一般以洗脸盆中心线和短的边平行
                if h < w:
                    jixian = [int(x), int(y - 0.5 * h), int(x), int(y + 0.5 * h)]
                    return int(h / ratio[0]), int(w / ratio[1]), jidian, jixian
                if h >= w:
                    jixian = [int(x - 0.5 * w), int(y), int(x + 0.5 * w), int(y)]
                    return int(w / ratio[0]), int(h / ratio[1]), jidian, jixian
                # cv2.rectangle(backgroud_image2, tuple(bbox[:2]), tuple(bbox[2:]), (0, 255, 255), 1)
                # cv2.imwrite('img_gray3.png', backgroud_image2)

            else:  # 没有得到洗脸盆contours
                w, h = self.bounding_rectangle.list[2] - self.bounding_rectangle.list[0], self.bounding_rectangle.list[3] - \
                       self.bounding_rectangle.list[1]
                x, y = [int(self.bounding_rectangle.list[0] + 0.5 * w), int(self.bounding_rectangle.list[1] + 0.5 * h)]
                return int(w / ratio[0]), int(h / ratio[1]), [x, y], [
                    [int(x), int(y - 0.5 * h), int(x), int(y + 0.5 * h)]]

        if len(contours_) == 0:
            w, h = self.bounding_rectangle.list[2] - self.bounding_rectangle.list[0], self.bounding_rectangle.list[3] - \
                   self.bounding_rectangle.list[1]
            x, y = [int(self.bounding_rectangle.list[0] + 0.5 * w), int(self.bounding_rectangle.list[1] + 0.5 * h)]
            return int(w / ratio[0]), int(h / ratio[1]), [x, y], [
                [int(x), int(y - 0.5 * h), int(x), int(y + 0.5 * h)]]


    def get_max_cnt(self, contours):  # 防止生成新的contour有多个，选最大的
        cnt_dic = {}
        for cnt in contours:
            contour = np.array(cnt)
            contour = contour.reshape(-1, 2)  # [n, 2]
            poly = Polygon(contour)
            poly = poly.buffer(0.0001)  # 加一个较小的buffer
            cnt_dic[poly.area] = cnt
        new_cnt_list = []
        for each in sorted(cnt_dic):
            new_cnt_list.append(cnt_dic[each])  # 按key由小到大
        return new_cnt_list[-1]
