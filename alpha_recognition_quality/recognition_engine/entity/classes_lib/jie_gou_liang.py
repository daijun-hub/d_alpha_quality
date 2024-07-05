from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity


class JieGouLiang(ClassifiedEntity):
    chinese_name = "结构梁"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)
        self.chinese_name = "结构梁"
        # self.entity_base_type = EntityBaseType.ELECTRIC_DEVICE

        # 粱属性
        self.wall_center_line = entity_object.wall_center_line
        self.beam_width = entity_object.beam_width
        self.beam_height = entity_object.beam_height
        self.beam_class = entity_object.beam_class
        self.beam_number = entity_object.beam_number
        self.kbmbHoop_diameter = entity_object.kbmbHoop_diameter
        self.kbmbHoop_distance = entity_object.kbmbHoop_distance
        self.kbmbHoop_limb = entity_object.kbmbHoop_limb
        self.kbmbJiaLi_number = entity_object.kbmbJiaLi_number
        self.kbmbJiaLi_diameter = entity_object.kbmbJiaLi_diameter
        self.kbmbNYao_number = entity_object.kbmbNYao_number
        self.kbmbNYao_diameter = entity_object.kbmbNYao_diameter
        self.kbmbGYao_number = entity_object.kbmbGYao_number
        self.kbmbGYao_diameter = entity_object.kbmbGYao_diameter
        self.kbmbTong_number = entity_object.kbmbTong_number
        self.kbmbTong_diameter = entity_object.kbmbTong_diameter