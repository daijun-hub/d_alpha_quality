from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils import *


class PaiShuiGou(ClassifiedEntity):
    chinese_name = "排水沟"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        self.chinese_name = "排水沟"
        self.entity_base_type = EntityBaseType.PIPE

        self.position = self.bounding_rectangle.list

        self.width = None
        self.depth = None

        self.gradient = "0.5%"
        self.have_cover_plate = True

        self.is_indoor = True
        self._get_gutter_width_height(border_entity)

    def _get_gutter_width_height(self, border_entity):
        ratio = border_entity.ratio
        pattern = "([\d]+)[\*xX]([\d]+)"
        text_list = get_entity_nearby_text(self.bounding_rectangle.list, border_entity, map_label=pattern)

        if text_list:
            for text_info in text_list:
                res = re.search(pattern, text_info.extend_message)
                if  200 < int(res.group(1)) < 350 and 200 < int(res.group(2)) < 350:
                    self.width = int(res.group(1))
                    self.depth = int(res.group(2))
                    break

        # 如果宽度没有标注，直接通过轮廓测量
        if not self.width:
            if self.contour is not None:
                contour = np.reshape(self.contour, (-1, 2))
                contour = list(contour)
                contour.append(contour[0])
                contour_1 = contour[1:]
                contour_2 = contour[:-1]
                res = []
                for point1, point2 in zip(contour_1, contour_2):
                    if int(200*ratio[0]) < point_euclidean_distance(point1, point2) < int(360*ratio[0]):
                        res.append(int(point_euclidean_distance(point1, point2) / ratio[0]))

                if res:
                    self.width = res[0]

    def judge_indoor(self, border_entity):
        ratio = border_entity.ratio
        if self.contour is not None:
            center = get_centroid(self.contour)
            image_manager = border_entity.image_manager
            height, width = image_manager.img_height, image_manager.img_width

            bbox = [int(2000*ratio[0]), int(2000*ratio[0]), width-int(2000*ratio[0]), height-int(2000*ratio[0])]

            if  bbox[0]< center[0] < bbox[2] and bbox[1]< center[1] < bbox[3]:
                self.is_indoor = True
            else:
                self.is_indoor = False
