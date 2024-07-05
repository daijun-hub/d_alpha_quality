#!/usr/bin/env python
# coding: utf-8

# 配置
import numpy as np

rule_path = r'/Users/daijun/workspace/alpha_quality/develop/notebook_demo/build/保利1'
rule_index = "1103044"
# label_list = [
#             {
#                 'major': 'architecture',
#                 'subproject': '湘潭碧桂园大学印象二期5#楼',
#                 'floor': '四~三十一层平面图',
#                 'coord': [132381, 76050, 147753, 88945],
#                 'house_type': 'A',
#             },
#             {
#                 'major': 'architecture',
#                 'subproject': '湘潭碧桂园大学印象二期5#楼',
#                 'floor': '四~三十一层平面图',
#                 'coord': [139347, 56654, 149347, 70254],
#                 'house_type': 'B',
#             },
#         ]
# label_list = [
#             {
#                 'major': 'architecture',
#                 'subproject': '湘潭碧桂园大学印象二期5#楼',
#                 'floor': '二层平面图',
#                 'coord': [132607, 196585, 147204, 205079],
#                 'house_type': 'Z2_104',
#             },
#             {
#                 'major': 'architecture',
#                 'subproject': '湘潭碧桂园大学印象二期5#楼',
#                 'floor': '二层平面图',
#                 'coord': [154776, 194268, 164232, 207105],
#                 'house_type': 'Z2_105',
#             },
#         ]
# label_list = [{'subproject': '湘潭碧桂园大学印象二期5#楼',
#                'major': 'architecture',
#                'house_type': 'aaa',
#                'coord': [133051.36692126596, 132467.77330248873, 150403.9694627227, 149514.15344615508],
#                'floor': '三层平面图'}]
# label_list = [{'house_type': 'ddd', 'subproject': '桃江凤凰城A#楼', 'floor': '二层平面图', 'major': 'architecture',
#                'coord': [9858585.194185492, 324386.62695108016, 9879364.98531647, 341757.2335996318]},
#               {'house_type': 'bbb', 'subproject': '桃江凤凰城A#楼', 'floor': '二层平面图', 'major': 'architecture',
#                'coord': [9903187.72116974, 318058.79093061376, 9918738.570078421, 329349.13328897045]},
#               {'house_type': 'aaa', 'subproject': '桃江凤凰城A#楼', 'floor': '二层平面图', 'major': 'architecture',
#                'coord': [9922362.9593313, 318401.9984027231, 9936919.690044904, 330710.1284369904]},
#               {'house_type': 'ccc', 'subproject': '桃江凤凰城A#楼', 'floor': '二层平面图', 'major': 'architecture',
#                'coord': [9880500.52378927, 318697.86691316223, 9898927.214619419, 332651.025865471]}]
# label_list = [
#     {'coord': [2756767.2384653045, 300514.36771350383, 2773521.534019538, 310615.0435021805], 'major': 'architecture',
#      'floor': '二层平面图', 'house_type': 'aaa', 'subproject': '星耀碧桂园1号楼'},
#     {'coord': [2758697.4446851597, 335108.9678590183, 2775192.1141421404, 351405.7012825152], 'major': 'architecture',
#      'floor': '二层平面图', 'house_type': 'ccc', 'subproject': '星耀碧桂园1号楼'},
#     {'coord': [2761402.5704761045, 311950.4519414176, 2772223.0736398837, 326366.79304681864], 'major': 'architecture',
#      'floor': '二层平面图', 'house_type': 'bbb', 'subproject': '星耀碧桂园1号楼'}]
# label_list = None
# label_list = [
#             {'major': 'architecture',
#              'subproject': '星耀碧桂园1号楼',
#              'floor': '二层平面图',
#              'coord': [2761456, 335172, 2772106, 349546],
#              'house_type': 'A_100'
#              },
#             {'major': 'architecture',
#              'subproject': '星耀碧桂园1号楼',
#              'floor': '二层平面图',
#              'coord': [2761456, 312472, 2772106, 326272],
#              'house_type': 'B_101'},
#             {'major': 'architecture',
#              'subproject': '星耀碧桂园1号楼',
#              'floor': '二层平面图',
#              'coord': [2761655, 300672, 2772106, 310472],
#              'house_type': 'C_102'},
#         ]
# label_list = [
#             {
#                 'major': 'architecture',
#                 'subproject': '凤鸣广场8栋',
#                 'floor': '二层平面图',
#                 'coord': [2582396, 1216100, 2592195, 1227150],
#                 'house_type': 'D_107',
#             },
#             {
#                 'major': 'architecture',
#                 'subproject': '凤鸣广场8栋',
#                 'floor': '二层平面图',
#                 'coord': [2586246, 1204600, 2598346, 1214700],
#                 'house_type': 'E_108',
#             },
#             {
#                 'major': 'architecture',
#                 'subproject': '凤鸣广场8栋',
#                 'floor': '二层平面图',
#                 'coord': [2582396, 1191800, 2590996, 1204250],
#                 'house_type': 'F_109',
#             },
#         ]
# label_list = [
#         {
#             'major': 'architecture',
#             'subproject': '高明荷城碧桂园一期五号楼',
#             'floor': '二层平面图',
#             'coord': [711368, -228926, 726757, -214792],
#             'house_type': '户型20',
#         },
#         {
#             'major': 'architecture',
#             'subproject': '高明荷城碧桂园一期五号楼',
#             'floor': '二层平面图',
#             'coord': [718546, -244576, 727146, -232046],
#             'house_type': '户型21',
#         },
#     ]
# label_list = [{'subproject': '碧桂园城市之光花园2#',
#                'coord': [1223585.0516816298, 11590.862199010442, 1226551.7821648335, 14492.389814451386],
#                'major': 'architecture',
#                'floor': '首层平面图',
#                'house_type': 'aa'}]

label_list = []

use_pickle = True
use_pickle_all = False  # all process
use_pickle_convert = False  # convert_border_image
use_pickle_combination = False  # 1
use_pickle_segmentation = False  # space_segmentation
use_pickle_detection = True  # entity_detection
use_pickle_classification = True  # entity_classification
use_pickle_integration = True  # entity_integration
use_pickle_mark_objectification = True  # mark objectification
use_pickle_entity_space_objectification = True  # entity and space objectification
use_pickle_project = True

use_pickle_cross = True

# 过滤相关配置
skip_drawing_name = []
skip_layout_name = []
skip_subproject_name_list = []
skip_drawing_type = []
# 正则表达式
drawing_name_pattern = None

# try:
#     from build.config import *
# except:
#     print('没有加载自定义脚本')
#     pass

import time
import os
import sys
import pickle
import glob
import shutil
import cv2
import re
import importlib

cv2.setNumThreads(0)
os.environ['env'] = "test"
os.environ['no_proxy'] = "*"
# 添加自己的alpha_recognition_quality路径
sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                 'recog'))

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                 'alpha-draw'))
from alpha_recognition_quality.common.log_manager import LOG
from collections import defaultdict
from alpha_recognition_quality.config_manager.decor_hvac.rule_config import RuleConfig as RuleConfigHEATING
from alpha_recognition_quality.common.major_config_router import MajorConfigRouter
from alpha_recognition_quality.common.utils2 import upload_drawing_pkl, _load_pkl, load_drawing_pkl
from alpha_recognition_quality.analysis_engine import convert_border_image
from alpha_recognition_quality.config_manager.major_config import MajorConfig
from alpha_recognition_quality.recognition_engine.border_entity import BorderEntity
from alpha_recognition_quality.design_object.cad_base.result_base import CADResult
from alpha_recognition_quality.analysis_engine.realdwg_parser import get_border_entity_info
from alpha_recognition_quality.analysis_engine.axis_net import get_axis_info
from alpha_recognition_quality.common import FileServiceClient
from alpha_recognition_quality.design_object.cad_base import CADResult, CADTaskCreator
from alpha_recognition_quality.recognition_engine.objectification import mark_objectification_run
from alpha_recognition_quality.recognition_engine import objectification
from alpha_recognition_quality.recognition_engine import space_entity_relation
# from alpha_recognition_quality.config_manager.architecture.drawing_entity_operation_config import Entity_Operation_Config
from alpha_recognition_quality.analysis_engine.pre_process import pre_process_cad_entity
from alpha_recognition_quality.project_engine.project import Project
from alpha_recognition_quality.project_engine import get_cross_border_attributes
from alpha_recognition_quality.project_engine import extract_model_house
from alpha_recognition_quality.project_engine import apartments_entities_mapping
from alpha_recognition_quality.config_manager.rule_engine import CargoCheckRuleEngine

# import configs for five majors
# architecture
from alpha_recognition_quality.config_manager.architecture.drawing_config import DrawingType as DrawingTypeArchi
from alpha_recognition_quality.config_manager.architecture.rule_config import RuleConfig as RuleConfigArchi
from alpha_recognition_quality.config_manager.architecture.multi_border_rule_config import \
    MultiBorderRuleConfig as MultiBorderRuleConfigArchi
# from alpha_recognition_quality.config_manager.architecture.layer_config import *

from alpha_recognition_quality.config_manager.electric.drawing_config import DrawingType as DrawingTypeElec
from alpha_recognition_quality.config_manager.electric.rule_config import RuleConfig as RuleConfigElec
from alpha_recognition_quality.config_manager.electric.multi_border_rule_config import \
    MultiBorderRuleConfig as MultiBorderRuleConfigElec
# from alpha_recognition_quality.config_manager.electric.layer_config import *

from alpha_recognition_quality.config_manager.plumbing.drawing_config import DrawingType as DrawingTypePlum
from alpha_recognition_quality.config_manager.plumbing.rule_config import RuleConfig as RuleConfigPlum
from alpha_recognition_quality.config_manager.plumbing.multi_border_rule_config import \
    MultiBorderRuleConfig as MultiBorderRuleConfigPlum
# from alpha_recognition_quality.config_manager.plumbing.layer_config import *

from alpha_recognition_quality.config_manager.hvac.drawing_config import DrawingType as DrawingTypeHvac
from alpha_recognition_quality.config_manager.hvac.rule_config import RuleConfig as RuleConfigHvac
from alpha_recognition_quality.config_manager.hvac.multi_border_rule_config import \
    MultiBorderRuleConfig as MultiBorderRuleConfigHvac
# from alpha_recognition_quality.config_manager.hvac.layer_config import *

from alpha_recognition_quality.config_manager.structure.drawing_config import DrawingType as DrawingTypeStruc
from alpha_recognition_quality.config_manager.structure.rule_config import RuleConfig as RuleConfigStruc
from alpha_recognition_quality.config_manager.structure.multi_border_rule_config import \
    MultiBorderRuleConfig as MultiBorderRuleConfigStruc
# from alpha_recognition_quality.config_manager.structure.layer_config import *
from alpha_recognition_quality.config_manager.structure.structure_drawing_type_configs import DrawingTypeConfig

from alpha_recognition_quality.config_manager.decor_architecture.drawing_config import \
    DrawingType as DrawingTypeDecorArchi
from alpha_recognition_quality.config_manager.decor_architecture.rule_config import RuleConfig as RuleConfigDecorArchi
from alpha_recognition_quality.config_manager.decor_architecture.multi_border_rule_config import \
    MultiBorderRuleConfig as MultiBorderRuleConfigDecorArchi

from alpha_recognition_quality.config_manager.decor_electric.rule_config import RuleConfig as RuleConfigDecorElec


major = None


def get_dwg_path_list(rule_path,dwg_path_list):
    dwg_list = os.listdir(rule_path)
    for dwg_name in dwg_list:
        if dwg_name.endswith(".dwg"):
            dwg_path = os.path.join(rule_path, dwg_name)
            dwg_path_list.append(dwg_path)
        else:
            if os.path.isdir(os.path.join(rule_path,dwg_name)):
                get_dwg_path_list(os.path.join(rule_path,dwg_name),dwg_path_list)
    return dwg_path_list

dwg_path_list = []
dwg_path_list = get_dwg_path_list(rule_path,dwg_path_list)


project_pkl_info_list = []
for dwg_path in dwg_path_list:
    print(f"{dwg_path} start!!!")
    result_saved_root = dwg_path[:-4] + '_result_drawing_service/'
    os.makedirs(result_saved_root, exist_ok=True)

    realdwg_parse_info = dwg_path[:-4] + '_realdwg_parse_info.pkl'
    parse_info = dict()
    if use_pickle and os.path.exists(realdwg_parse_info):
        with open(realdwg_parse_info, 'rb') as f:
            parse_info = pickle.load(f)
            task_id = parse_info["task_id"]
            file_struct = parse_info["file_struct"]
            cad_result_manager = CADResult(task_id)
            task_result = cad_result_manager.fetch_results()
            layers_list = cad_result_manager.get_layers()
            border_list = cad_result_manager.process_border_info()
    else:
        file_service = FileServiceClient()
        file_struct = file_service.upload_file(dwg_path)

        task_creator = CADTaskCreator(file_struct)
        cad_result_manager = CADResult(task_creator.task_id)
        task_result = cad_result_manager.fetch_results()
        layers_list = cad_result_manager.get_layers()
        border_list = cad_result_manager.process_border_info()

        parse_info["task_id"] = task_creator.task_id
        parse_info["file_struct"] = file_struct
        with open(realdwg_parse_info, 'wb') as pf:
            pickle.dump(parse_info, pf)
    print("CAD task finished")

    dwg_parse_task_id = cad_result_manager.task_id

    border_entity = None

    rules_pickle_path_list = dwg_path.split('/')[:-1]
    print(rules_pickle_path_list)
    rules_pickle_saved_root = '/'.join(rules_pickle_path_list) + '/标准层和货量pickle/'
    os.makedirs(rules_pickle_saved_root, exist_ok=True)
    print(rules_pickle_saved_root)
    # 临时保存标准层和货量pickel去测试规则
    info_pickle_file_standard = None
    info_pickle_file_product = None

    for border_index, cad_border in enumerate(border_list):
        pkl_info = {}
        drawing_type_list = cad_border.drawing_type_list
        border_name = cad_border.drawing_identifier

        border_info = cad_border.to_tuple()
        drawing_name, border_coord, scale, subproject, major, layout_name, label_range, border_object, *others = border_info
        pkl_info["major"] = major

        if layout_name in skip_layout_name:
            print(f'######过滤布局 {layout_name}')
            continue
        print(drawing_name)
        # if drawing_name in skip_drawing_name:

        # if drawing_name not in ["二层平面图", "门窗大样、门窗表", "门窗表门窗大样图一", "门窗大样图二", "三~二十六层平面图"]:
        # if drawing_name not in ["酒店五--十六层平面图"]:
        if drawing_name not in ["首层平面（一）","首层平面(一)"]:
            print(f'#####过滤drawing_name {drawing_name}')
            continue
        if drawing_name_pattern is not None and not re.search(drawing_name_pattern, drawing_name):
            continue

        print(
            'border_name:{} subproject_name:{} drawing_name:{} drawing type list:{}'.format(border_name, subproject,
                                                                                            drawing_name,
                                                                                            drawing_type_list))

        if cad_border.is_ignore_border:
            LOG.debug(f"[Recognization] Border {border_name} ignored")
            continue

        if major not in ['structure']:
            major_config_router = MajorConfigRouter(major)
            all_drawing_type_configs = major_config_router.gather_all_configs()
        else:
            major_config_router = MajorConfigRouter(major)
            all_drawing_type_configs = DrawingTypeConfig.STR.value

        origin_border_entity_info = cad_result_manager.fetch_basic_entity_result(border_object)

        for drawing_type in drawing_type_list:
            # 需要过滤的图纸类型
            if drawing_type in skip_drawing_type:
                continue

            pkl_info["drawing_type"] = drawing_type
            print('-----> drawing type:{}'.format(drawing_type))
            LOG.debug('[Recognization] drawing type:{}'.format(drawing_type))
            if major in ['architecture']:
                need_entity, operation_list = pre_process_cad_entity.get_entity_operation(drawing_type)
                layer_recommendation = pre_process_cad_entity.get_layers(major_config_router.get_recommended_layers,
                                                                         need_entity, layers_list)
            else:
                need_entity = all_drawing_type_configs[drawing_type]['entities']
                operation_list = all_drawing_type_configs[drawing_type]['operations']
                layer_recommendation = major_config_router.get_recommended_layers.run(need_entity, layers_list)
            img_print_layers = major_config_router.get_printing_layers(layer_recommendation, drawing_type,
                                                                       layers_list)

            print('[Note] need entities:{}'.format(need_entity))
            print('[Note] need operations:{}'.format(operation_list))

            pickle_file_dict = {}
            pickle_type_list = ['all', 'convert', 'combination', 'segmentation', 'detection', 'classification',
                                'integration', 'mark_objectification', 'objectification']
            for p in pickle_type_list:
                pickle_name = f"{border_name}_{drawing_type.value}_info_{p}.pkl"
                pickle_file_dict[f'info_pickle_file_{p}'] = os.path.join(result_saved_root, pickle_name)

            if not use_pickle_all or not os.path.exists(pickle_file_dict['info_pickle_file_all']):
                if not use_pickle_convert or not os.path.exists(pickle_file_dict['info_pickle_file_convert']):
                    # 读取图框图像并转换构件坐标
                    if major in ['architecture']:
                        border_entity_info = pre_process_cad_entity.pre_processing(major_config_router,
                                                                                   layer_recommendation,
                                                                                   origin_border_entity_info,
                                                                                   layers_list,
                                                                                   cad_result_manager, cad_border,
                                                                                   border_name, border_info,
                                                                                   drawing_type,
                                                                                   result_saved_root)
                        # img_height, img_width = border_entity_info.get("image_manager").img_height, border_entity_info.get("image_manager").img_width
                        # img_zero = np.zeros((img_height, img_width, 3), dtype=np.uint8)
                        # for line in border_entity_info.get("origin_border_entity_info").get("plane_decorative_line"):
                        #     x1, y1, x2, y2 = line[0][0],line[0][1],line[0][2],line[0][3]
                        #     img_zero = cv2.rectangle(img_zero, (x1, y1), (x2, y2), (0, 0, 255), 10)
                        # cv2.imwrite('vpipe2.png', img_zero)
                    else:
                        cad_result_manager.print_image_batch(cad_border, drawing_type, img_print_layers,
                                                             result_saved_root,
                                                             text_clean=True, hatch_clean=True)

                        border_entity_info_CAD = get_border_entity_info(origin_border_entity_info, border_info,
                                                                        layer_recommendation, drawing_type)

                        # 读取图框图像并转换构件坐标
                        border_entity_info = convert_border_image.run(border_name, border_entity_info_CAD, border_info,
                                                                      result_saved_root, drawing_type)

                    # 添加轴网
                    border_entity_info = get_axis_info(border_entity_info)
                    with open(pickle_file_dict['info_pickle_file_convert'], 'wb') as pf:
                        pickle.dump(border_entity_info, pf)
                else:
                    with open(pickle_file_dict['info_pickle_file_convert'], 'rb') as f:
                        border_entity_info = pickle.load(f)

                if not use_pickle_combination or not os.path.exists(pickle_file_dict['info_pickle_file_combination']):
                    # 构件合并
                    if 'combination' in operation_list:
                        border_entity_info = major_config_router.entity_combination.run(border_name, border_entity_info,
                                                                                        result_saved_root,
                                                                                        drawing_type)  # 调参True
                        with open(pickle_file_dict['info_pickle_file_combination'], 'wb') as pf:
                            pickle.dump(border_entity_info, pf)
                else:
                    with open(pickle_file_dict['info_pickle_file_combination'], 'rb') as f:
                        border_entity_info = pickle.load(f)

                if not use_pickle_segmentation or not os.path.exists(pickle_file_dict['info_pickle_file_segmentation']):
                    # 空间分割
                    if 'segmentation' in operation_list:
                        border_entity_info = major_config_router.space_segmentation.run(border_name, border_entity_info,
                                                                                        result_saved_root, drawing_type)
                    with open(pickle_file_dict['info_pickle_file_segmentation'], 'wb') as pf:
                        pickle.dump(border_entity_info, pf)
                else:
                    with open(pickle_file_dict['info_pickle_file_segmentation'], 'rb') as f:
                        border_entity_info = pickle.load(f)

                if not use_pickle_detection or not os.path.exists(pickle_file_dict['info_pickle_file_detection']):
                    # 目标检测
                    if drawing_type in major_config_router.drawing_config.DRAWING_WITH_DETECTION.value:
                        border_entity_info = major_config_router.entity_detection.run(border_name, border_entity_info,
                                                                                      result_saved_root, drawing_type)
                        with open(pickle_file_dict['info_pickle_file_detection'], 'wb') as pf:
                            pickle.dump(border_entity_info, pf)
                else:
                    with open(pickle_file_dict['info_pickle_file_detection'], 'rb') as f:
                        border_entity_info = pickle.load(f)

                if not use_pickle_classification or not os.path.exists(
                        pickle_file_dict['info_pickle_file_classification']):
                    # 构件分类
                    if 'classification' in operation_list:
                        border_entity_info = major_config_router.entity_classification.run(border_name,
                                                                                           border_entity_info,
                                                                                           result_saved_root,
                                                                                           drawing_type)
                        with open(pickle_file_dict['info_pickle_file_classification'], 'wb') as pf:
                            pickle.dump(border_entity_info, pf)

                else:
                    with open(pickle_file_dict['info_pickle_file_classification'], 'rb') as f:
                        border_entity_info = pickle.load(f)

                ## 空间分类
                if not use_pickle_integration or not os.path.exists(pickle_file_dict['info_pickle_file_integration']):
                    # 后处理
                    if 'segmentation' in operation_list or 'classification' in operation_list:
                        border_entity_info = major_config_router.entity_info_integration.run(border_entity_info,
                                                                                             result_saved_root,
                                                                                             drawing_type)
                        with open(pickle_file_dict['info_pickle_file_integration'], 'wb') as pf:
                            pickle.dump(border_entity_info, pf)
                else:
                    with open(pickle_file_dict['info_pickle_file_integration'], 'rb') as f:
                        border_entity_info = pickle.load(f)

                # TODO
                border_entity_info['cad_border_id'] = border_name
                border_entity = BorderEntity.read_from_dict(border_entity_info)

                # 标记对象化
                if not use_pickle_mark_objectification or not os.path.exists(
                        pickle_file_dict['info_pickle_file_mark_objectification']):
                    border_entity = objectification.mark_objectification_run(border_entity)
                    with open(pickle_file_dict['info_pickle_file_mark_objectification'], 'wb') as pf:
                        pickle.dump(border_entity, pf)
                else:
                    with open(pickle_file_dict['info_pickle_file_mark_objectification'], 'rb') as f:
                        border_entity = pickle.load(f)

                # 构件和空间对象化
                if not use_pickle_entity_space_objectification or not os.path.exists(
                        pickle_file_dict['info_pickle_file_objectification']):
                    border_entity = objectification.run(border_entity)
                    with open(pickle_file_dict['info_pickle_file_objectification'], 'wb') as pf:
                        pickle.dump(border_entity, pf)
                else:
                    with open(pickle_file_dict['info_pickle_file_objectification'], 'rb') as f:
                        border_entity = pickle.load(f)

                # 获取部分空间相关的构件（如空间内的构件）
                border_entity = space_entity_relation.run(border_entity)
                # 暂时使用 TODO
                border_entity.cad_border_id = border_name

                fileid = upload_drawing_pkl(border_entity)
                border_entity.fileid = fileid
                with open(pickle_file_dict['info_pickle_file_all'], 'wb') as pf:
                    pickle.dump(border_entity, pf)
                print('---> fileid of pickle: ', fileid)
                pkl_info["file_id"] = border_entity.fileid
                pkl_info["recognition_id"] = border_entity.fileid  # fake value
                pkl_info["subproject_list"] = border_entity.subproject_num_list
                pkl_info["floor_list"] = list(map(str, border_entity.floor_num_list))
                pkl_info['cad_parsed_file_id'] = border_name
                # 增加subproject_name 用于装修板房、货量抽取
                pkl_info['subproject_name'] = border_entity.subproject_name
            else:
                with open(pickle_file_dict['info_pickle_file_all'], 'rb') as f:
                    border_entity = pickle.load(f)
                print('---> fileid of pickle: ', border_entity.fileid)
                pkl_info["file_id"] = border_entity.fileid
                pkl_info["recognition_id"] = border_entity.fileid  # fake value
                pkl_info["subproject_list"] = border_entity.subproject_num_list
                pkl_info["floor_list"] = border_entity.floor_num_list
                pkl_info['cad_parsed_file_id'] = border_name
                # 增加subproject_name 用于装修板房、货量抽取
                pkl_info['subproject_name'] = border_entity.subproject_name

            project_pkl_info_list.append(pkl_info)

rules_pickle_saved_root = os.path.join(rule_path, '标准层和货量pickle')
os.makedirs(rules_pickle_saved_root, exist_ok=True)
# 临时保存标准层和货量pickel去测试规则
product_info_pickle_file = os.path.join(rules_pickle_saved_root, "rule_pickle_info_to_check.pkl")
standard_info_pickle_file = os.path.join(rules_pickle_saved_root, "rule_pickle_info_standard.pkl")
cross_info_pickle_file = os.path.join(rules_pickle_saved_root, "cross_pickle_info.pkl")

if not use_pickle_project or not os.path.exists(product_info_pickle_file) or not os.path.exists(
        standard_info_pickle_file):
    proj_obj = Project(project_pkl_info_list)

    if not use_pickle_cross or not os.path.exists(cross_info_pickle_file):
        proj_obj = get_cross_border_attributes.run(proj_obj)
        with open(cross_info_pickle_file, 'wb') as pf:
            pickle.dump(proj_obj, pf)
    else:
        with open(cross_info_pickle_file, 'rb') as f:
            proj_obj = pickle.load(f)

    proj_obj = extract_model_house.run(proj_obj, label_list)
    recognition_result, standard_dict = apartments_entities_mapping.run(proj_obj)
    product_border_info_list = []
    for result in recognition_result:
        product_border_info_list.append(load_drawing_pkl(result['file_id']))
    with open(product_info_pickle_file, 'wb') as pf:
        pickle.dump(product_border_info_list, pf)
    # standard = load_drawing_pkl(model_house_id)
    # standard_dict = load_drawing_pkl(model_house_id)[major]
    # standard_dict['proj_obj'] = proj_obj
    with open(standard_info_pickle_file, 'wb') as pf:
        pickle.dump(standard_dict, pf)
else:
    with open(product_info_pickle_file, 'rb') as f:
        product_border_info_list = pickle.load(f)
    with open(standard_info_pickle_file, 'rb') as f:
        standard_dict = pickle.load(f)

print("识图结果列表", product_border_info_list, "元素个数", len(product_border_info_list))
rule_file_name = CargoCheckRuleEngine.RULE[rule_index]["module"]
print("-------------------", rule_file_name)
rule_name = CargoCheckRuleEngine.SPECIAL_BORDER_RULE_PATH.format(module=rule_file_name)
print(rule_name)
rule_module = importlib.import_module(rule_name)

# 规则
for border_entity_info in product_border_info_list:
    major = border_entity_info.major
    standard_dict_major = standard_dict.get(major, None)
    if standard_dict_major is None: continue
    print(border_entity_info.subproject_name)
    if border_entity_info.subproject_name in skip_subproject_name_list:
        print(f"过滤子项 {border_entity_info.subproject_name}")
        continue
    # if border_entity_info.drawing_name != "三层平面图":
    #     continue
    # if border_entity_info.layout_name != "Model":
    #     continue

    rule_config_dict = None
    if border_entity_info.drawing_type in RuleConfigArchi.VANKE_RULES.value.keys():
        rule_config_dict = RuleConfigArchi.VANKE_RULES
    if border_entity_info.drawing_type in RuleConfigPlum.VANKE_RULES.value.keys():
        rule_config_dict = RuleConfigPlum.VANKE_RULES
    if border_entity_info.drawing_type in RuleConfigStruc.VANKE_RULES.value.keys():
        rule_config_dict = RuleConfigStruc.VANKE_RULES
    if border_entity_info.drawing_type in RuleConfigHvac.VANKE_RULES.value.keys():
        rule_config_dict = RuleConfigHvac.VANKE_RULES
    if border_entity_info.drawing_type in RuleConfigDecorArchi.VANKE_RULES.value.keys():
        rule_config_dict = RuleConfigDecorArchi.VANKE_RULES
    if border_entity_info.drawing_type in RuleConfigDecorElec.VANKE_RULES.value.keys():
        rule_config_dict = RuleConfigDecorElec.VANKE_RULES
    if border_entity_info.drawing_type in RuleConfigHEATING.VANKE_RULES.value.keys():
        rule_config_dict = RuleConfigHEATING.VANKE_RULES

    if rule_config_dict is not None and rule_index in rule_config_dict.value[border_entity_info.drawing_type]:
        rule = getattr(rule_module, CargoCheckRuleEngine.RULE_CLASS_NAME)(border_entity_info,
                                                                          standard_dict_major,
                                                                          rule_index,
                                                                          result_path=rule_path)

        result = rule.run()
