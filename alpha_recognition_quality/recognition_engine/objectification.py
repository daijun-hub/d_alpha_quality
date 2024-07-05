from .border_entity import BorderEntity
from .entity.entity import ProcessedGBE, ProcessedGBEStruct
from ..analysis_engine.utils import convert_CAD_coord_to_coord, rad_to_angle, convert_CAD_point, get_vector_angle_2D, point_in_bbox
from ..config_manager.objectification_config import EntityConfig, SpaceConfig
from ..config_manager.architecture.drawing_config import DrawingType as DrawingTypeArch
# from config_manager.electric.drawing_config import DrawingType as DrawingTypeElec
# from config_manager.plumbing.drawing_config import DrawingType as DrawingTypePlum

from .utils.utils_objectification_common import get_hatch_info_object
from ..common.utils import *
from .space.classes_lib.hu import Hu
import numpy as np
import cv2
import re
import importlib
from time import time
from collections import defaultdict
from ..common.decorator import timer
from .base.bounding_rectangle import BoundingRectangle
from .base.contour import Contour
from .space.space import Space
from .mark.classes_lib.jian_zhu_suo_yin_biao_zhu import JianZhuSuoYinBiaoZhu
from .mark.classes_lib.chuang_bian_hao import ChuangBianHao
from .mark.classes_lib.jian_zhu_pou_mian_biao_zhu import JianZhuPouMianBiaoZhu
from .mark.classes_lib.men_bian_hao import MenBianHao
from .mark.classes_lib.chi_cun_biao_zhu import ChiCunBiaoZhu
from .mark.classes_lib.jian_zhu_mian_ji import JianZhuMianJi
from .mark.classes_lib.ke_ta_mian import KeTaMian
from .mark.classes_lib.biao_gao_fu_hao import BiaoGaoFuHao
from .mark.classes_lib.chang_wai_biao_gao import ChangWaiBiaoGao
from .mark.classes_lib.yin_zhu import YinZhu
from .mark.classes_lib.qiang_tian_chong import QiangTianChong
from .mark.classes_lib.yong_di_hong_xian import YongDiHongXian
from .mark.classes_lib.qiang_xian import QiangXian
from .mark.classes_lib.jian_tou import JianTou
from .mark.classes_lib.ping_mian_lou_ti_ta_bu import PingMianLouTiTaBu
from .mark.classes_lib.chuang_tai_wan_cheng_mian import  ChuangTaiWanChengMian
from .mark.classes_lib.kong_jian_wan_cheng_mian import KongJianWanChengMian
from .mark.classes_lib.lan_gan_wan_cheng_mian import LanGanWanChengMian
from .mark.classes_lib.chu_fang_cao_zuo_tai_bian_xian import ChuFangCaoZuoTaiBianXian
from .mark.classes_lib.chu_fang_xia_gui import ChuFangXiaGui


dict_for_objectficication_debug = {}


def process_gbes(origin_border_entity_info, scale, border_coord, ratio):
    """
    读取原始的图框信息，并对其中的基本图元信息进行坐标转换，封装成ProcessedGBE对象
    Args:
        origin_border_entity_info: 原始的图框信息
        scale: 长宽比例
        border_coord: 图框坐标
        ratio:  比例，图像尺寸/坐标尺寸

    Returns:
        完成转换后的图框信息
    """
    entity_info_all = defaultdict(list)  # 初始化，默认值为列表的字典

    for layer, layer_entity_info in origin_border_entity_info.items():
        p_gbes_list = []
        # 遍历图层内构件信息，构件信息依次为图元坐标，图元类别，图元附加信息
        for entity_info in layer_entity_info:
            entity_coord = entity_info.coord
            entity_class = entity_info.entity_type.value
            ex_info = entity_info.extend_storage
            e_style = entity_info.style
            line_weight = entity_info.line_weight
            line_description = entity_info.line_description
            color = entity_info.color

            hpipe_min_len_pix = 370 * ratio[0]
            layer_name_list = ["cold_life_supply_hpipe", "hot_life_supply_hpipe", "hydrant_hpipe", "sprinkler_hpipe",
                               "inflow_hpipe", "sewage_hpipe", "waste_hpipe", "rain_hpipe", "condensate_hpipe",
                               "ventilate_hpipe"]
            if entity_class == 'Line':  # line坐标直接转model坐标后转png坐标
                ex_info_cov = [_ * scale for _ in eval(ex_info)]  # 处理string形信息并scale换算
                ex_info_cov_pix = convert_CAD_coord_to_coord(border_coord, ex_info_cov, ratio)  # 转为png坐标
                if ex_info_cov_pix is None or len(ex_info_cov_pix) != 4:
                    continue
                ex_info_cov_pix_width = abs(ex_info_cov_pix[3] - ex_info_cov_pix[1])
                ex_info_cov_pix_heigth = abs(ex_info_cov_pix[2] - ex_info_cov_pix[0])
                ex_info_cov_pix_length = max(ex_info_cov_pix_width, ex_info_cov_pix_heigth)
                if ex_info_cov_pix_length < hpipe_min_len_pix and layer in layer_name_list:
                    continue
                p_gbe = ProcessedGBE(layer, ex_info_cov_pix, entity_class, e_style, line_weight, color,
                                     line_description)
                p_gbes_list.append(p_gbe)

            elif entity_class in ['Polyline', 'Polyline2d']:
                ex_info_list = re.split(r'[?::|;|L|A]', ex_info)[2::3]  # 去掉标志符号转png坐标
                # 遍历多段线
                for ex_info_split in ex_info_list:
                    ex_info_split = eval(ex_info_split)  # 处理string信息
                    # 2020年8月之前的万翼解析不含有线宽信息
                    if len(ex_info_split) == 4:
                        ex_info_cov = (np.array(ex_info_split) * scale).tolist()  # 直线型
                    elif len(ex_info_split) == 8:
                        ex_info_cov = [_ * scale for _ in ex_info_split[:-1]] + [
                            rad_to_angle(ex_info_split[-1], ex_info_split[-2])]  # arc型
                    # TODO: 2020年8月之后的万翼解析中含有线宽，但目前不需要，若后期需要，在这里提取
                    elif len(ex_info_split) == 6:
                        ex_info_cov = (np.array(ex_info_split[:4]) * scale).tolist()  # 含有线宽的直线型
                    elif len(ex_info_split) == 10:
                        ex_info_cov = [_ * scale for _ in ex_info_split[:-3]] + [
                            rad_to_angle(ex_info_split[-3], ex_info_split[-4])]  # 含有线宽的arc型
                    else:
                        print('unknown lenth', ex_info_split)
                        continue
                    ex_info_cov_pix = convert_CAD_coord_to_coord(border_coord, ex_info_cov, ratio)  # 转png坐标
                    if ex_info_cov_pix is None or (len(ex_info_cov_pix) != 4 and len(ex_info_cov_pix) != 8):
                        continue
                    ex_info_cov_pix_width = abs(ex_info_cov_pix[3] - ex_info_cov_pix[1])
                    ex_info_cov_pix_heigth = abs(ex_info_cov_pix[2] - ex_info_cov_pix[0])
                    ex_info_cov_pix_length = max(ex_info_cov_pix_width, ex_info_cov_pix_heigth)
                    if ex_info_cov_pix_length < hpipe_min_len_pix and layer in layer_name_list:
                        continue
                    p_gbe = ProcessedGBE(layer, ex_info_cov_pix, entity_class, e_style, line_weight, color,
                                         line_description)
                    p_gbes_list.append(p_gbe)

            elif entity_class == 'Arc' and layer not in layer_name_list:
                ex_info = eval(ex_info)  # string型
                ex_info_cov = [_ * scale for _ in ex_info[:-1]] + [rad_to_angle(ex_info[-1], ex_info[-2])]  # 转模型空间
                ex_info_cov_pix = convert_CAD_coord_to_coord(border_coord, ex_info_cov, ratio)  # 转png坐标
                if ex_info_cov_pix is None or len(ex_info_cov_pix) != 8:
                    continue
                p_gbe = ProcessedGBE(layer, ex_info_cov_pix, entity_class, e_style, line_weight, color,
                                     line_description)
                p_gbes_list.append(p_gbe)

            elif entity_class == 'Hatch' and layer not in layer_name_list:  # Hatch仅返回了bbox
                ex_info_cov_pix = entity_coord
                if len(ex_info_cov_pix) != 4:
                    continue
                p_gbe = ProcessedGBE(layer, ex_info_cov_pix, entity_class, e_style, line_weight, color,
                                     line_description)
                p_gbes_list.append(p_gbe)

            elif entity_class == "Circle" and layer not in layer_name_list:
                ex_info_cov = [_ * scale for _ in eval(ex_info)]  # 处理string形信息并scale换算
                ex_info_cov_pix = convert_CAD_point(border_coord, ex_info_cov[:2], ratio) + \
                                  [int(ex_info_cov[-1] * ratio[0])]  # 转为png坐标
                p_gbe = ProcessedGBE(layer, ex_info_cov_pix, entity_class, e_style, line_weight, color,
                                     line_description)
                p_gbes_list.append(p_gbe)

            elif entity_class == 'Ellipse' and layer not in layer_name_list:
                ex_info = eval(ex_info)  # string型
                if len(ex_info) != 13:
                    continue
                # 转模型空间
                ex_info_cov = [_ * scale for _ in ex_info[:4]] + \
                              [get_vector_angle_2D(ex_info[4:6]), rad_to_angle(ex_info[7], True),
                               rad_to_angle(ex_info[8], True)] + \
                              [_ * scale for _ in ex_info[9:]]
                ex_info_cov_pix = convert_CAD_coord_to_coord(border_coord, ex_info_cov, ratio)  # 转png坐标
                if ex_info_cov_pix is None or len(ex_info_cov_pix) != 11:
                    continue
                p_gbe = ProcessedGBE(layer, ex_info_cov_pix, entity_class, e_style, line_weight, color,
                                     line_description)
                p_gbes_list.append(p_gbe)

            elif entity_class == "Solid" and layer not in layer_name_list:  # Solid仅返回bbox rule506006 通过箭头找引下线
                ex_info_cov_pix = entity_coord
                if len(ex_info_cov_pix) != 4:
                    continue
                p_gbe = ProcessedGBE(layer, ex_info_cov_pix, entity_class, e_style, line_weight, color,
                                     line_description)
                p_gbes_list.append(p_gbe)

            else:
                # print('unresolved entity_class', entity_class)  # 包括hatch poly2d等
                continue
        if len(p_gbes_list) != 0:
            p_gbes = ProcessedGBEStruct(layer, p_gbes_list)
            entity_info_all[layer] = p_gbes

    return entity_info_all


def import_objecification_config(config_dict, module_path, debug_dict):
    """
    导入对象化配置文件
    Args:
        config_dict: 配置文件字典信息
        module_path: 配置文件所在路径
        debug_dict: debug所需配置信息

    Returns:
        读取并封装后的配置信息字典
    """
    result_dict = defaultdict(list)
    for name, file_list in config_dict.items():
        if isinstance(file_list, tuple):
            file_list = [file_list]
        if debug_dict and name not in debug_dict:
            continue
        for file_name, class_name in file_list:
            module_full_path = module_path + file_name
            try:
                module = importlib.import_module(module_full_path)
                entity_class = getattr(module, class_name)
            except (ModuleNotFoundError, AttributeError) as e:
                print(f"[Objectification] {e.__class__.__name__}: {str(e)}")
            else:
                result_dict[name].append(entity_class)

    return result_dict


@timer("objectification")
def run(border_entity: BorderEntity, debug_dict={}):
    """
    对象化主函数，将输入的border_entity中的构件信息对象化后保存到图框对象的属性中
    Args:
        border_entity: 需要对象化的BorderEntity图框对象
        debug_dict: debug配置信息

    Returns:
        经过对象化BorderEntity图框对象
    """
    
    global dict_for_objectficication_debug
    dict_for_objectficication_debug = debug_dict

    entity_dict = defaultdict(list)
    space_dict = defaultdict(list)
    mark_dict = defaultdict(list)

    # Classified entity （ClassifiedEntity）
    time_classified = time()
    entity_bbox_list = border_entity.entity_bbox_list
    for entity in entity_bbox_list:
        entity_obj_list = classification_entity_objectification(entity, border_entity)
        if entity_obj_list:
            for entity_obj in entity_obj_list:
                entity_dict[entity_obj.chinese_name].append(entity_obj)
        
            # print('--> classified entity class saved: {}'.format(new_entity.chinese_name))
    print('[TIME] ClassifiedEntity objectification using time ', time() - time_classified)

    # Combined entity （CombinedEntity）
    time_combined = time()
    entity_combination_result = border_entity.entity_combination_result
    for layer, bounding_rectangle_list in entity_combination_result.items():
        for bounding_rectangle in bounding_rectangle_list:
            for entity_class in entity_combination_dict.get(layer, []):
                print('--> combined entity class objectificating: {}'.format(layer))
                new_entity = entity_class(layer, bounding_rectangle, border_entity)
                entity_dict[new_entity.chinese_name].append(new_entity)  # TODO：优化汇总dict
                # print('--> combined entity class saved: {}'.format(new_entity.chinese_name))
    print('[TIME] CombinedEntity objectification using time ', time() - time_combined)

    # PrimitiveEntity (PrimitiveEntity)
    time_primitive = time()
    origin_border_entity_info = border_entity.origin_border_entity_info
    processed_gbe_dict = process_gbes(origin_border_entity_info, border_entity.space_scale, border_entity.border_coord,
                                      border_entity.ratio)

    for layer, p_gbes in processed_gbe_dict.items():
        for entity_class in entity_primitive_class_dict.get(layer, []):
            print('--> primitive entity class objectificating: {}'.format(layer))
            for p_gbe in p_gbes.p_gbe_list:
                new_entity = entity_class(p_gbe)  # 一类构件
                entity_dict[new_entity.chinese_name].append(new_entity)  # TODO：优化汇总dict
            # print('--> primitive entity class saved: {}'.format(new_entity.chinese_name))
    print('[TIME] PrimitiveEntity objectification using time ', time() - time_primitive)

    # Mark 【挪到预处理】
    # for layer, p_gbes in processed_gbe_dict.items():
    #     for mark_class in mark_config_dict.get(layer, []):
    #         new_mark = mark_class(p_gbes)
    #         mark_dict[new_mark.chinese_name].append(new_mark)  # TODO：优化汇总dict

    # Space
    time_room = time()
    room_info = border_entity.room_info
    for space in room_info:
        space_obj_list = space_objectification(space, border_entity)
        if space_obj_list:
            for space_obj in space_obj_list:
                space_dict[space_obj.chinese_name].append(space_obj)
    print('[TIME] Space objectification using time ', time() - time_room)

    border_entity.update_objectification_result(entity_dict, space_dict)

    # # Apartment 户实例化
    apartment_objectification(border_entity)

    return border_entity


@timer("objectification")
def mark_objectification_run(border_entity: BorderEntity) -> BorderEntity:
    """
    对标记进行对象化处理，将图框对象中的标记符号对象化后保存到图框对象的属性中
    Args:
        border_entity: 需要对象化处理的图框对象

    Returns:
        对象化后的图框对象
    """
    result_dict = defaultdict(list)

    # class_obj = Mark_Class(border_entity)                     # can be other paramater or for loop
    # result_dict[Mark_Class.chinese_name].append(class_obj)

    # "标高符号" 对象化
    time_elevation = time()
    entity_bbox_list = border_entity.entity_bbox_list
    for entity in entity_bbox_list:
        if entity.entity_class == 'elevation_symbol':
            # print('--> entity class objectificating: {}'.format(entity.entity_class))
            new_entity = BiaoGaoFuHao(entity, border_entity)
            result_dict[BiaoGaoFuHao.chinese_name].append(new_entity)
            if new_entity.out_attribute:
                new_entity = ChangWaiBiaoGao(entity, border_entity)
                result_dict[new_entity.chinese_name].append(new_entity)

            # print('--> classified entity class saved: {}'.format(new_entity.chinese_name))
    print('[TIME] 标高符号 objectification using time ', time() - time_elevation)

    # "引注" 对象化
    time_annotation = time()
    annotation_info_list = border_entity.special_info_dict['annotation_info_list']
    for annotation_info in annotation_info_list:
        # print('--> annotation objectificating: {}'.format('yinzhu'))
        new_entity = YinZhu(annotation_info, border_entity)  # 一类构件
        result_dict[YinZhu.chinese_name].append(new_entity)  # TODO：优化汇总dict
        # print('--> annotation class saved: {}'.format(YinZhu.chinese_name))
    print('[TIME] 引注 objectification using time ', time() - time_annotation)

    # "墙填充"、"用地红线" 对象化
    entity_combination_result = border_entity.entity_combination_result
    for layer, bounding_rectangle_list in entity_combination_result.items():
        time_start = time()
        if layer in ['solid_wall_line', 'non_solid_wall_line']:
            # 将填充的边线进行合并，得到每块填充的外接bbox，以及组成每块填充的图元
            hatch_info_list = get_hatch_info_object(bounding_rectangle_list, border_entity)
            for hatch_info in hatch_info_list:
                # print('--> hatch objectificating: {}'.format('qiangtianchong'))
                new_entity = QiangTianChong(layer, hatch_info)
                result_dict[QiangTianChong.chinese_name].append(new_entity)  # TODO：优化汇总dict
                # print('--> hatch class saved: {}'.format(QiangTianChong.chinese_name))
            print('[TIME] 墙填充 objectification using time ', time() - time_start)

        elif layer in ['processed_red_lines']:
            # print('--> processed_red_lines objectificating: {}'.format('yongdihongxian'))
            new_entity = YongDiHongXian(layer, bounding_rectangle_list)
            result_dict[YongDiHongXian.chinese_name].append(new_entity)  # TODO：优化汇总dict
            # print('--> processed_red_lines class saved: {}'.format(YongDiHongXian.chinese_name))
            print('[TIME] 用地红线 objectification using time ', time() - time_start)

        elif layer in ['wall_line', 'pillar_line']:
            for wall in bounding_rectangle_list:
                new_entity = QiangXian(layer, wall)
                result_dict[QiangXian.chinese_name].append(new_entity)  # TODO：优化汇总dict
            print('[TIME] 墙线 objectification using time ', time() - time_start)

        # 箭头
        elif layer in ['arrow_info_list']:
            for arrow_info in bounding_rectangle_list:
                new_entity = JianTou(arrow_info)
                result_dict[JianTou.chinese_name].append(new_entity)  # TODO：优化汇总dict
            print('[TIME] 箭头 objectification using time ', time() - time_start)

        # 平面楼梯踏步
        elif layer in ['tabu_info_list']:
            for tabu_info in bounding_rectangle_list:
                new_entity = PingMianLouTiTaBu(tabu_info)
                result_dict[PingMianLouTiTaBu.chinese_name].append(new_entity)  # TODO：优化汇总dict
            print('[TIME] 平面楼梯踏步 objectification using time ', time() - time_start)

        # 厨房操作台边线、厨房下柜（TODO: 后期优化厨房下柜对象）
        elif layer in ['kit_operate_line']:
            for line in bounding_rectangle_list:
                new_entity = ChuFangCaoZuoTaiBianXian(line)
                new_entity_1 = ChuFangXiaGui(line)
                result_dict[ChuFangCaoZuoTaiBianXian.chinese_name].append(new_entity)  # TODO：优化汇总dict
                result_dict[ChuFangXiaGui.chinese_name].append(new_entity_1)  # TODO：优化汇总dict
            print('[TIME] 厨房操作台边线 objectification using time ', time() - time_start)

        # 栏杆完成面、空间完成面、窗台完成面
        elif layer in ['space_completion_surface_list']:
            for space_completion_surface in bounding_rectangle_list:
                new_entity = KongJianWanChengMian(space_completion_surface)
                result_dict[KongJianWanChengMian.chinese_name].append(new_entity)  # TODO：优化汇总dict
            print('[TIME] 空间完成面 objectification using time ', time() - time_start)
        elif layer in ['sill_completion_surface_list']:
            for sill_completion_surface in bounding_rectangle_list:
                new_entity = ChuangTaiWanChengMian(sill_completion_surface)
                result_dict[ChuangTaiWanChengMian.chinese_name].append(new_entity)  # TODO：优化汇总dict
            print('[TIME] 窗台完成面 objectification using time ', time() - time_start)
        elif layer in ['handrail_completion_surface_list']:
            for handrail_completion_surface in bounding_rectangle_list:
                new_entity = LanGanWanChengMian(handrail_completion_surface)
                result_dict[LanGanWanChengMian.chinese_name].append(new_entity)  # TODO：优化汇总dict
            print('[TIME] 栏杆完成面 objectification using time ', time() - time_start)
        elif layer in ["kt_surface_list"]:
            for ktm in bounding_rectangle_list:
                new_entity = KeTaMian(ktm)
                result_dict[KeTaMian.chinese_name].append(new_entity)  # TODO：优化汇总dict
            print('[TIME] 可踏面 objectification using time ', time() - time_start)
        elif layer in ["arch_area_text_list"]:
            for arch_area_info in bounding_rectangle_list:
                new_entity = JianZhuMianJi(arch_area_info)
                result_dict[JianZhuMianJi.chinese_name].append(new_entity)  # TODO：优化汇总dict
            print('[TIME] 建筑面积文本 objectification using time ', time() - time_start)
        elif layer in ["anno_size_list"]:
            for anno_size_info in bounding_rectangle_list:
                new_entity = ChiCunBiaoZhu(anno_size_info)
                result_dict[ChiCunBiaoZhu.chinese_name].append(new_entity)  # TODO：优化汇总dict
            print('[TIME] 尺寸标注 objectification using time ', time() - time_start)
        elif layer in ["window_number_list"]:
            for win_num_info in bounding_rectangle_list:
                new_entity = ChuangBianHao(win_num_info)
                result_dict[ChuangBianHao.chinese_name].append(new_entity)  # TODO：优化汇总dict
            print('[TIME] 窗编号 objectification using time ', time() - time_start)
        elif layer in ["door_number_list"]:
            for door_num_info in bounding_rectangle_list:
                new_entity = MenBianHao(door_num_info)
                result_dict[MenBianHao.chinese_name].append(new_entity)  # TODO：优化汇总dict
            print('[TIME] 门编号 objectification using time ', time() - time_start)
        elif layer in ["arch_section_anno_list"]:
            for arch_section_anno_info in bounding_rectangle_list:
                new_entity = JianZhuPouMianBiaoZhu(arch_section_anno_info)
                result_dict[JianZhuPouMianBiaoZhu.chinese_name].append(new_entity)  # TODO：优化汇总dict
            print('[TIME] 建筑剖面标注 objectification using time ', time() - time_start)
        elif layer in ["arch_index_list"]:
            for arch_index_info in bounding_rectangle_list:
                new_entity = JianZhuSuoYinBiaoZhu(arch_index_info)
                result_dict[JianZhuSuoYinBiaoZhu.chinese_name].append(new_entity)  # TODO：优化汇总dict
            print('[TIME] 建筑索引标注 objectification using time ', time() - time_start)

    border_entity.update_mark_result(result_dict)

    return border_entity


entity_classification_class_dict = import_objecification_config(EntityConfig.CLASSIFICATION_MAP, EntityConfig.MODULE_PATH, dict_for_objectficication_debug)
entity_combination_dict = import_objecification_config(EntityConfig.COMBINATION_MAP, EntityConfig.MODULE_PATH, dict_for_objectficication_debug)
entity_primitive_class_dict = import_objecification_config(EntityConfig.PRIMITIVE_MAP, EntityConfig.MODULE_PATH, dict_for_objectficication_debug)
space_config_dict = import_objecification_config(SpaceConfig.CLASS_MAP, SpaceConfig.MODULE_PATH, {})


def space_objectification(room, border_entity):
    room_obj_list = []
    # space_obj = Space(Contour(room.contour, border_entity.ratio), BoundingRectangle(room.bbox), room.name_list)
    if len(room.name_list) == 0:
        name_list = ['无名称空间']
    else:
        name_list = room.name_list
    for name in name_list:
        for space_class in space_config_dict.get(name, []):
            room_obj = space_class(room, border_entity)
            room_obj_list.append(room_obj)
    return room_obj_list


def classification_entity_objectification(entity, border_entity):
    entity_obj_list = []
    for entity_class in entity_classification_class_dict.get(entity.entity_class, []):
        new_entity = entity_class(entity, border_entity)
        entity_obj_list.append(new_entity)
    return entity_obj_list


def apartment_objectification(border_entity):
    '''
    户实例化
    '''
    household_list = border_entity.special_info_dict["household_list"]
    apartment_list = []
    # print("household_list", len(household_list), household_list)
    for i, household in enumerate(household_list):
        c = Contour(household.household_contour, border_entity.ratio)
        x1, y1, w, h = cv2.boundingRect(household.household_contour)
        b = BoundingRectangle([x1, y1, x1+w, y1+h])
        apartment = Hu(Space(c, b, ["户"], False), border_entity, i)
        apartment_list.append(apartment)

    border_entity.space_object_dict[Hu.chinese_name] = apartment_list