# -*- coding: utf-8 -*-

from .border_entity import BorderEntity
from ..config_manager.space_entity_relation_config import SpaceWithRelation
from ..common.decorator import timer


@timer("build_space_entity_relation")
def run(border_entity: BorderEntity):
    """
    对象化主函数，将输入的border_entity中的构件信息对象化后保存到图框对象的属性中
    Args:
        border_entity: 需要对象化的BorderEntity图框对象
    Returns:
        建立了构件与空间关系的图框中设计对象信息
    """
    if border_entity.drawing_type in SpaceWithRelation.keys():
        space_object_dict = border_entity.space_object_dict
        for space_name in SpaceWithRelation[border_entity.drawing_type]:
            space_obj_list = space_object_dict.get(space_name, [])
            for space_obj in space_obj_list:
                space_obj.get_related_entities(border_entity)

    return border_entity
