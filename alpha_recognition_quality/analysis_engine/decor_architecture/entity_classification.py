import os
from time import time

from PIL import Image
import numpy as np
import cv2

from ...config import env as export_env
from ...config_manager.decor_architecture.classify_config import ClassifyConfig, ClassifyType
from ...config_manager.decor_architecture.drawing_config import DrawingType, DrawingConfig
from ...config_manager.decor_architecture.layer_config import LayerConfig
from ...config_manager.text_config import TextType

from ...common.utils import *
from ...common.CONSTANTS import IMAGE_PRINT_EXTENSION
from ...common.decorator import timer

from ..utils.utils_classification import *
from ..utils.utils_analysis_common import *
from ..CONSTANTS import *
from ..model_service.tfserving_client import tf_restful

from ...common.debug_image_drawer import DebugImageDrawer
from ...common.image_manager import ImageManager
from ...config import SAVE_RECOG_GEN_IMG_ONLINE


@timer('entity_classification')
def run(border_name, border_entity_info, result_path, drawing_type, rule_index=None, crop_image_path=None):
    """
    构件分类

    :param border_name: 图框序号，例如 Model_0
    :param border_entity_info: 图框构件信息
    :param result_path: 中间结果保存路径
    :param drawing_type: 图框类型
    :param rule_index: 规则序号，为None 表示按照图纸类型粒度来运行，如果不为None，表示按照规则粒度来运行
    :return: 补充信息的 border_entity_info
    """

    image_manager: ImageManager = border_entity_info['image_manager']
    debug_drawer = DebugImageDrawer(image_manager)

    border_img_with_wall_copy = debug_drawer.create_copy(IMG_WITH_WALL_KEY)
    border_size = image_manager.img_height, image_manager.img_width
    img_debug = image_manager.load_from_manager(IMG_WITH_WALL_KEY)
    entity_bbox_dict = border_entity_info.get('entity_bbox_dict', {})
    border_text_info = border_entity_info['border_text_info']
    origin_border_entity_info = border_entity_info['origin_border_entity_info']
    border_coord = border_entity_info['border_coord']
    space_scale = border_entity_info['space_scale']
    ratio = border_entity_info['ratio']
    ext_margin = border_entity_info['ext_margin']
    door_base_coords = border_entity_info.get("door_base_coords",[])

    border_entity_info['entity_class_dict'] = {}
    border_entity_info['entity_score_dict'] = {}
    all_origin_entity_class = []
    # 引线系统
    main_branch_text_list = border_entity_info.get('main_branch_text_list', [])

    # 创建该图框图元保存路径
    if crop_image_path is not None:
        entity_save_path = os.path.join(crop_image_path, '{}_{}'.format(border_name, drawing_type.value))
        if not os.path.exists(entity_save_path):
            os.mkdir(entity_save_path)

    # 获取墙信息，用于空调识别结果矫正
    wall_bbox_line = entity_bbox_dict.get('wall_line', [])
    # 坐标网格化分割参数
    w_height, w_width = image_manager.img_height, image_manager.img_width
    n_num = 20
    h_range = np.ceil(w_height / n_num)  # grid size
    w_range = np.ceil(w_width / n_num)  # grid size

    # 获取房间信息，用于空调识别结果矫正
    room_infos = border_entity_info['room_info'] if 'room_info' in border_entity_info else []
    small_room_infos = border_entity_info['small_room_info'] if 'small_room_info' in border_entity_info else []
    all_room_infos = room_infos + small_room_infos
    kitchen_room = ['厨房', '厨']
    bathroom = ['卫生间', '卫']
    elevator_room = ['电梯井']
    anteroom = ['电梯前室', '合用前室', '前室']
    bedroom = ['卧室']
    living_room = ['客厅']
    storage_room = ['储藏室']
    closet_room = ['衣帽间']
    balcony_room = ['阳台']
    housekeeping_room = ['家政间']
    study_room = ['书房']
    dianjing_room = ['电井']
    air_room_area = SpaceConfig.AC_INDOOR_ROOM_LIST.value

    kitchen_infos = [room_info for room_info in room_infos if len(set(room_info[2]) & set(kitchen_room)) > 0]
    living_room_infos = [room_info for room_info in room_infos if len(set(room_info[2]) & set(living_room)) > 0]
    bathroom_infos = [room_info for room_info in room_infos if len(set(room_info[2]) & set(bathroom)) > 0]
    # 有些卫生间因为卫生间文本在干区，导致其判为无名称空间
    # 因此对于无名称空间，满足以下条件即为卫生间
    #   1. 如果空间边界和含有主卫、客卫、卫生间的相隔的最小距离在500mm以内
    #   2. 空间的长宽和面积满足要求
    null_bathroom_infos = get_null_bathroom_infos(room_infos + small_room_infos, ratio, border_text_info)
    bathroom_infos += null_bathroom_infos
    elevator_room_infos = [room_info for room_info in room_infos if len(set(room_info[2]) & set(elevator_room)) > 0]
    anteroom_infos = [room_info for room_info in room_infos if len(set(room_info[2]) & set(anteroom)) > 0]
    bedroom_infos = [room_info for room_info in room_infos if len(set(room_info[2]) & set(bedroom)) > 0]
    storage_room_infos = [room_info for room_info in room_infos if len(set(room_info[2]) & set(storage_room)) > 0]
    closet_room_infos = [room_info for room_info in room_infos if len(set(room_info[2]) & set(closet_room)) > 0]
    balcony_room_infos = [room_info for room_info in room_infos if len(set(room_info[2]) & set(balcony_room)) > 0]
    housekeeping_room_infos = [room_info for room_info in room_infos if
                               len(set(room_info[2]) & set(housekeeping_room)) > 0]
    study_room_infos = [room_info for room_info in room_infos if len(set(room_info[2]) & set(study_room)) > 0]
    air_room_infos = [room_info for room_info in room_infos if len(set(room_info[2]) & set(air_room_area)) > 0]
    dianjing_room_infos = [room_info for room_info in all_room_infos if len(set(room_info[2]) & set(dianjing_room)) > 0]
    print(dianjing_room_infos)
    ### 获取无名空间主要是为了判断凸窗 ###
    non_name_infos = [room_info for room_info in room_infos + small_room_infos if len(room_info[2]) == 0 and not is_wall_contour(room_info[0], wall_thickness_CAD*ratio[0])]
    for room in non_name_infos:
        if re.search("公寓", "".join(room[2])):
            air_room_infos.append(room)
    # 获取套内空间
    indoor_infos = kitchen_infos + bathroom_infos + bedroom_infos + living_room_infos + closet_room_infos + housekeeping_room_infos
    entity_annotation_list = []  # 保存所有构件的引注文本，可能一个构件有0个、1个或多个文本，构件顺序和entity_bbox_list一致

    for layer, entity_bbox in entity_bbox_dict.items():
        border_entity_info['entity_class_dict'][layer] = []
        border_entity_info['entity_score_dict'][layer] = []

    for layer, entity_bbox_list in entity_bbox_dict.items():
        if len(entity_bbox_list) == 0:
            continue
        # for debug
        # if layer not in ["door"]: continue
        # for ei, entity_bbox in enumerate(entity_bbox_list):
        #     cv2.rectangle(img_debug, (entity_bbox[0], entity_bbox[1]), (entity_bbox[2], entity_bbox[3]), (255, 255, 0), 5)
        #     cv2.putText(img_debug, f"{ei}", (entity_bbox[0], entity_bbox[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # cv2.imwrite(f"/Users/xuan.ma/Desktop/{layer}_cls_bbox_debug.png", img_debug)
        if layer in LayerConfig.CLASSIFICATION_EXCLUDE_LAYERS.value + LayerConfig.LAYERS_WITH_SLOPE_LINE_REVISED.value + \
                LayerConfig.DASH_LINE_REVISED.value + ['door_intersect_bboxes', 'door_combine_bbox']:
            print('[Note] this layer do not need classification:{}'.format(layer))
            continue

        print('[Note] classify for layer:{}\t entity num:{}'.format(layer, len(entity_bbox_list)))
        entity_bbox_list = [get_normal_bbox(entity_bbox) for entity_bbox in entity_bbox_list]
        entity_image_list = get_entity_image_list(drawing_type, layer, entity_bbox_list, border_entity_info, ext_margin,
                                                  major='decor_architecture')
        # 获取引线文本，用于构件后处理
        annotation_list, _ = match_entity_annotation(main_branch_text_list, entity_list=entity_bbox_list,
                                                     img_anno=None, entity_type='vpipe')
        entity_annotation_list.extend(annotation_list)

        # 地上模型分类
        if drawing_type in DrawingConfig.DRAWING_OPERATION_CONFIG.value['classify_indoor']:
            start_time = time()
            predict_prob = tf_restful(entity_image_list, ClassifyConfig.MODEL_URL[export_env][ClassifyType.INDOOR],
                                      ClassifyType.INDOOR.value, expand='padding')

            print("[Note]模型前向时间:{:.2f} seconds".format(time() - start_time))

            predict_result = np.max(predict_prob, axis=1)
            predict_result_indx = np.argmax(predict_prob, axis=1)

            predict_class = [ClassifyConfig.MODEL_CLASS[ClassifyType.INDOOR][i] for i in predict_result_indx]
            predict_result = np.array(predict_result)
            predict_class = np.array(predict_class)
            # predict_class[predict_result<0.8] = 'others'
            predict_class = list(predict_class)

            # 根据图层，尺寸信息等先验知识对分类结果进行矫正
            all_origin_entity_class.extend(predict_class)
            for i in range(len(predict_class)):
                bb = entity_bbox_list[i]
                entity_cnt = get_contour_from_bbox(bb)
                margin = ext_margin - 2 if ext_margin >= 2 else ext_margin
                long_side, short_side, long_ratio, short_ratio = get_side_ratio(bb, ratio, margin)
                if short_side == 0:
                    short_side = 1
                # 构件的引线文本
                annotation_text = str(annotation_list[i]) if annotation_list[i] else ''

                # 对误分类的车位进行矫正
                if layer == 'parking' and predict_class[i] == "others":
                    if short_side > int(PARKING_SHORT_SIDE_RANGE[0] * short_ratio):
                        predict_class[i] = "normal_parking"

                # 剖面图中的误分类普通窗进行矫正
                # if predict_class[i] == "window" and drawing_type in [DrawingType.SECTION]:
                #     predict_class[i] = "elevation_window"
                livingroom_single_stove = False
                # 客厅内的洗衣机尺寸比较大的置为洗衣机，尺寸比较小的置为炉灶（开放式厨房），其他的置为others
                if predict_class[i] in ['washer'] and \
                        any((get_contours_iou(room[0], entity_cnt) > 0.8) for room in living_room_infos) and \
                        len(room_infos) > 0:
                    # 尺寸小于单孔炉灶的置为炉灶
                    if long_side < SINGLE_STOVE_SIDE_MAX * long_ratio:
                        predict_class[i] = 'stove'
                        livingroom_single_stove = True
                    elif long_side > WASHER_SIDE_MIN * long_ratio:
                        predict_class[i] = 'washer'
                    else:
                        predict_class[i] = 'others'
                # 客厅内的diamond_bath重置为others
                if predict_class[i] in ['diamond_bath'] and \
                        any((get_contours_iou(room[0], entity_cnt) > 0.8) for room in living_room_infos) and \
                        len(room_infos) > 0:
                    predict_class[i] = 'others'
                # 置信度比较低的洗面器矫正为others
                if predict_class[i] in ['washbasin'] and predict_result[i] < 0.9:
                    predict_class[i] = 'others'
                # 客厅分类结果中长宽比很小的洗面器重置为others
                if predict_class[i] in ['washbasin'] and long_side / short_side < 1.1 and \
                        any((get_contours_iou(room[0], entity_cnt) > 0.8) for room in living_room_infos) and \
                        len(room_infos) > 0:
                    predict_class[i] = 'others'
                # 厨房内的洗面器矫正为others，以检测结果为准
                if predict_class[i] in ['washbasin'] and \
                        any((get_contours_iou(room[0], entity_cnt) > 0.8) for room in kitchen_infos) and \
                        len(room_infos) > 0:
                    predict_class[i] = 'others'
                # 分类结果中阳台内的洗面器都矫正为others，以检测结果为准
                if predict_class[i] in ['washbasin'] and predict_result[i] < 0.9 and \
                        any((get_contours_iou(room[0], entity_cnt) > 0.8) for room in balcony_room_infos) and \
                        len(room_infos) > 0:
                    predict_class[i] = 'others'
                # 分类结果中短边较长的洗面器重置为others
                if predict_class[i] in ['washbasin'] and \
                        (short_side > WASHBASIN_SHORT_SIDE_RANGE[1] * short_ratio or
                         short_side < WASHBASIN_SHORT_SIDE_RANGE[0] * short_ratio or
                         long_side > WASHBASIN_LONG_SIDE_RANGE[1] * long_ratio or
                         long_side < WASHBASIN_LONG_SIDE_RANGE[0] * long_ratio) and \
                        predict_result[i] != 1:
                    predict_class[i] = 'others'
                # 分类结果中卧室内的洗面器都矫正为others
                if predict_class[i] in ['washbasin'] and \
                        any((get_contours_iou(room[0], entity_cnt) > 0.8) for room in bedroom_infos) and \
                        len(room_infos) > 0:
                    predict_class[i] = 'others'
                # 厨房内过大的炉灶矫正为others，以检测结果为准
                if predict_class[i] in ['stove'] and \
                        any((get_contours_iou(entity_cnt, room[0]) > 0.5) for room in kitchen_infos) and \
                        len(room_infos) > 0:
                    predict_class[i] = 'others'
                # 厨房之外空间内的炉灶矫正为others
                if predict_class[i] in ['stove'] and \
                        all((get_contours_iou(room[0], entity_cnt) < 0.5) for room in kitchen_infos) and \
                        len(room_infos) > 0 and not livingroom_single_stove:
                    predict_class[i] = 'others'
                # 厨房内分类置信度低于0.9的冰箱矫正为others，以检测结果为准
                if predict_class[i] in ['fridge'] and predict_result[i] < 0.9 and \
                        any((get_contours_iou(room[0], entity_cnt) > 0.6) for room in kitchen_infos) and \
                        len(room_infos) > 0:
                    predict_class[i] = 'others'
                # 客厅内分类置信度低于0.9的冰箱矫正为others
                if predict_class[i] in ['fridge'] and predict_result[i] < 0.9 and \
                        any((get_contours_iou(room[0], entity_cnt) > 0.8) for room in living_room_infos) and \
                        len(room_infos) > 0:
                    predict_class[i] = 'others'
                # 厨房内分类置信度低于0.9的炉灶矫正为others，以检测结果为准
                if predict_class[i] in ['stove'] and predict_result[i] < 0.9 and \
                        any((get_contours_iou(room[0], entity_cnt) > 0.8) for room in kitchen_infos) and \
                        len(room_infos) > 0:
                    predict_class[i] = 'others'
                # 置信度比较低的便器矫正为others
                if predict_class[i] in ['closestool', 'toilet'] and predict_result[i] < 0.6:
                    predict_class[i] = 'others'
                # 楼梯大样图中的便器矫正为others
                # if predict_class[i] in ['closestool', 'toilet'] and \
                #         drawing_type in [DrawingType.STAIR_DAYANG, DrawingType.WALL_DAYANG]:
                #     predict_class[i] = 'others'
                # 尺寸过大的便器矫正为others
                if predict_class[i] in ['closestool', 'toilet'] and long_side > CLOSESTOOL_LONG_SIDE_MAX * long_ratio:
                    predict_class[i] = 'others'
                # 卫生间之外空间内的便器矫正为others
                if predict_class[i] in ['closestool', 'toilet'] and \
                        all((get_contours_iou(room[0], entity_cnt) < 0.5) for room in bathroom_infos) and \
                        len(room_infos) > 0:
                    predict_class[i] = 'others'
                # 卧室、卫生间、阳台内的洗涤槽矫正为others
                if predict_class[i] in ['sink'] and \
                        any((get_contours_iou(room[0], entity_cnt) > 0.8)
                            for room in bedroom_infos + bathroom_infos + balcony_room_infos) and \
                        len(room_infos) > 0:
                    predict_class[i] = 'others'
                # 不完全在厨房内的洗涤槽矫正为others，以检测结果为准
                if predict_class[i] in ['sink'] and \
                        all((get_contours_iou(room[0], entity_cnt) < 0.9) for room in kitchen_infos) and \
                        len(room_infos) > 0:
                    predict_class[i] = 'others'
                # 厨房内分类置信度低于0.9的洗涤槽矫正为others，以检测结果为准
                if predict_class[i] in ['sink'] and predict_result[i] < 0.9 and \
                        any((get_contours_iou(room[0], entity_cnt) > 0.8) for room in kitchen_infos) and \
                        len(room_infos) > 0:
                    predict_class[i] = 'others'
                # 客厅内的便器矫正为others，以检测结果为准
                if predict_class[i] in ['closestool', 'toilet'] and \
                        any((get_contours_iou(room[0], entity_cnt) > 0.8) for room in living_room_infos) and \
                        len(room_infos) > 0:
                    predict_class[i] = 'others'
                # 卫生间之外空间内的洗浴器矫正为others
                if predict_class[i] in ['shower'] and \
                        all((get_contours_iou(room[0], entity_cnt) < 0.5) for room in bathroom_infos) and \
                        len(room_infos) > 0:
                    predict_class[i] = 'others'
                # # 厨房、客厅、书房、卧室内的洗浴器矫正为others，以检测结果为准
                # if predict_class[i] in ['shower'] and \
                #         any((get_contours_iou(room[0], entity_cnt) > 0.5)
                #             for room in kitchen_infos + living_room_infos + study_room_infos + bedroom_infos + elevator_room_infos) and \
                #         len(room_infos) > 0:
                #     predict_class[i] = 'others'
                # 置信度比较低的洗浴器矫正为others

                # 门窗大样图中误分类的立面窗置为立面窗
                # if drawing_type in [DrawingType.DOOR_WINDOW_DAYANG] and layer in ["door", "window"]:
                #     if predict_class[i] in ["window", "others", "zhexianchuang"]:
                #         predict_class[i] = "limianchuang"
                        
                if predict_class[i] in ['shower'] and predict_result[i] < 0.6:
                    predict_class[i] = 'others'
                # 卫生间内过大的洗浴器矫正为others，以检测结果为准
                if predict_class[i] in ['shower'] and \
                        any((get_contours_iou(room[0], entity_cnt) > 0.5) for room in bathroom_infos) and \
                        long_side > SHOWER_LONG_SIDE_MAX * long_ratio and len(room_infos) > 0:
                    predict_class[i] = 'others'
                # 楼梯大样图中的洗浴器置为others
                # if predict_class[i] in ['shower'] and \
                #         drawing_type in [DrawingType.STAIR_DAYANG, DrawingType.WALL_DAYANG]:
                #     predict_class[i] = 'others'
                # 非立面图纸中立面窗过滤
                # if (predict_class[i] == 'limianchuang'
                #         and drawing_type not in [DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION,
                #                                  DrawingType.DOOR_WINDOW_DAYANG]):
                #     predict_class[i] = 'others_lmc'
                #     # 过滤分体空调
                #     for text in border_text_info[TextType.ALL]:
                #         if re.search("K|KT", text[-1]) and Iou_temp(text[:4], bb):
                #             predict_class[i] = "air_conditioner"
                #             break
                # elif (predict_class[i] not in ['limianchuang', 'elevation_symbol']
                #       and drawing_type in [DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION,
                #                            DrawingType.DOOR_WINDOW_DAYANG]):
                #     predict_class[i] = 'others'
                # 排烟道
                if layer == 'kitchen_exhaust_pipe':
                    if predict_class[i] == 'others':
                        for text_info in border_text_info[TextType.ALL]:
                            if re.search('YD', text_info[4]):
                                text_YD_bbox = text_info[:4]
                                if Iou_temp(text_YD_bbox, bb) > 0:
                                    predict_class[i] = 'kitchen_exhaust_pipe'

                # # 厨房内的洗衣机矫正为others，以检测模型为准
                # if predict_class[i] in ['washer'] and \
                #         any((get_contours_iou(room[0], entity_cnt) > 0.8) for room in kitchen_infos) and \
                #         len(room_infos) > 0:
                #     predict_class[i] = 'others'
                # 含地漏的混合图层，'paishuikou', 'paiqikou', 'baiye', 'others'中符合尺寸要求的为地漏
                if layer == 'floor_drain_mix':
                    # others中满足尺寸要求的判定为地漏，长边大小和长短边比例
                    if (
                            predict_class[i] in ['others']
                            and DILOU_SIDE_RANGE[0] * long_ratio <= long_side <= DILOU_SIDE_RANGE[1] * long_ratio
                            and DILOU_SIDE_RATIO[0] <= long_side / short_side <= DILOU_SIDE_RATIO[1]
                    ):
                        # 获取弧线(通过弧线判断是否是地漏)
                        class_to_check = ['Arc', 'Polyline', 'Polyline2d']
                        _arc_dict = get_origin_border_entity_info(origin_border_entity_info, [layer], class_to_check,
                                                                  space_scale, border_coord, ratio)
                        arc_list = []
                        for _, entity_list in _arc_dict.items():
                            arc_list.extend(entity_list)
                        arc_list = list(filter(lambda x: len(x) == 8, arc_list))  # Polyline中有line，需要过滤
                        # arc_list = [arc[2:6] for arc in arc_list]
                        arc_in_entity_list = entity_in_bbox(arc_list, bb)
                        if len(arc_in_entity_list) > 0:
                            print("------->>>after filter arc, others fix to dilou")
                            predict_class[i] = 'dilou'
                    # 云效ID 279722 如果构件在厨卫图层、满足尺寸要求，则该构件为淋浴器（淋浴器为一个弧形和直线构成）
                    elif (
                            predict_class[i] in ['others']
                            and SMALL_SHOWER_LONG_SIDE_RANGE[0] * long_ratio <= long_side
                            <= SMALL_SHOWER_LONG_SIDE_RANGE[1] * long_ratio
                            and SMALL_SHOWER_SHORT_SIDE_RANGE[0] * long_ratio <= short_side
                            <= SMALL_SHOWER_SHORT_SIDE_RANGE[1] * short_ratio
                    ):
                        # 获取直线
                        class_to_check = ['Line', 'Polyline', 'Polyline2d']
                        _line_dict = get_origin_border_entity_info(origin_border_entity_info, [layer], class_to_check,
                                                                   space_scale, border_coord, ratio)
                        line_list = []
                        for _, entity_list in _line_dict.items():
                            line_list.extend(entity_list)
                        line_list = list(filter(lambda x: len(x) == 4, line_list))
                        line_in_entity_list = get_line_in_bbox(line_list, bb)
                        # 获取弧线
                        class_to_check = ['Arc', 'Polyline', 'Polyline2d']
                        _arc_dict = get_origin_border_entity_info(origin_border_entity_info, [layer], class_to_check,
                                                                  space_scale, border_coord, ratio)
                        arc_list = []
                        for _, entity_list in _arc_dict.items():
                            arc_list.extend(entity_list)
                        arc_list = list(filter(lambda x: len(x) == 8, arc_list))  # Polyline中有line，需要过滤
                        # arc_list = [arc[2:6] for arc in arc_list]
                        arc_in_entity_list = entity_in_bbox(arc_list, bb)
                        # 可以获取到一个弧形和一个直线，则为淋浴器
                        if len(line_in_entity_list) == 1 and len(arc_in_entity_list) == 1:
                            predict_class[i] = 'shower'

                    # 排水口、排气口、百叶中满足尺寸要求的为地漏，通过长边最大值，这三类疑似地漏构件，存在中长短边比例可能不是1或尺寸较大的地漏构件
                    elif predict_class[i] in ['paishuikou', 'paiqikou', 'baiye'] \
                            and long_side <= DILOU_SIDE_RANGE[1] * long_ratio:
                        predict_class[i] = 'dilou'
                    elif predict_class[i] in ['pipe']:
                        predict_class[i] = 'others'
                    # 含地漏的混合图层中可能有空调，分类为空调且尺寸符合要求的为空调
                    elif predict_class[i] == 'air_conditioner':
                        # for issue1561,误识别为空调的橱柜长边1057mm。
                        if not (short_side < AIR_CONDITIONER_SHORT_SIDE_RANGE[0] * short_ratio
                                or long_side < AIR_CONDITIONER_LONG_SIDE_RANGE[0] * long_ratio
                                or long_side > AIR_CONDITIONER_LONG_SIDE_RANGE[1] * long_ratio):
                            rect = get_min_rect(entity_image_list[i])
                            if len(rect) != 0:
                                short_side_new = min(rect[1][0], rect[1][1])
                                if short_side_new > AIR_CONDITIONER_SHORT_SIDE_RANGE[1] * short_ratio:
                                    predict_class[i] = 'others'
                        else:
                            predict_class[i] = 'others'
                    # 含地漏的混合图层识别为楼梯、电梯厢的构件置为others
                    elif predict_class[i] in ['stair', 'elevator_box']:
                        predict_class[i] = 'others'

                # 'washbasin', 'diamond_bath'层中非'washbasin', 'diamond_bath', 'closestool'构件为others
                elif layer in ['washbasin', 'diamond_bath']:
                    if predict_class[i] not in ['washbasin', 'diamond_bath', 'closestool', 'washer', 'shower']:
                        predict_class[i] = 'others_wsh'

                # 空调层矫正逻辑： 1. 获取可能为空调的类别['xiaohuoshuan', 'elevator_box', 'others', 'window', 'others_lmc']
                # 1.1符合空调尺寸的为空调， 1.2非xiaohuoshuan，elevator_box为others
                # 2.其余类别不符合空调尺寸的为others，对误分类进行过滤
                elif layer == 'air_conditioner':
                    if predict_class[i] in ['xiaohuoshuan', 'elevator_box']:
                        if not (
                                short_side < AIR_CONDITIONER_SHORT_SIDE_RANGE[0] * short_ratio
                                or long_side < AIR_CONDITIONER_LONG_SIDE_RANGE[0] * long_ratio
                                or long_side > AIR_CONDITIONER_LONG_SIDE_RANGE[1] * long_ratio
                        ):
                            predict_class[i] = 'air_conditioner'
                        else:
                            predict_class[i] = 'others'
                    elif (
                            short_side < AIR_CONDITIONER_SHORT_SIDE_RANGE[0] * short_ratio
                            or long_side < AIR_CONDITIONER_LONG_SIDE_RANGE[0] * long_ratio
                            or long_side > AIR_CONDITIONER_LONG_SIDE_RANGE[1] * long_ratio
                    ):
                        predict_class[i] = 'others'

                # 含空调的混合图层，可能含大量家具构件，仅需识别空调，可能被误识别为电梯厢,也可能有真实的电梯厢（在家具层）
                # 整体逻辑与air_conditioner层相近
                elif layer == 'air_conditioner_mix':
                    if predict_class[i] in ['air_conditioner', 'elevator_box']:
                        if not (
                                short_side < AIR_CONDITIONER_SHORT_SIDE_RANGE[0] * short_ratio
                                or long_side < AIR_CONDITIONER_LONG_SIDE_RANGE[0] * long_ratio
                                or long_side > AIR_CONDITIONER_LONG_SIDE_RANGE[1] * long_ratio
                        ):
                            # 符合空调尺寸的电梯厢为空调
                            if predict_class[i] in ['elevator_box']:
                                predict_class[i] = "air_conditioner"
                            # 获取构件最小外接矩形框，不满足空调尺寸置为others
                            if predict_class[i] in ['air_conditioner']:
                                rect = get_min_rect(entity_image_list[i])
                                if len(rect) != 0:
                                    short_side_new = min(rect[1][0], rect[1][1])
                                    if short_side_new > AIR_CONDITIONER_SHORT_SIDE_RANGE[1] * short_ratio:
                                        predict_class[i] = 'others'
                        else:
                            predict_class[i] = 'others'

                # 电梯厢层类别过滤
                elif layer == 'elevator_box':
                    if predict_class[i] in ["window", "zhexianchuang", "diamond_bath"]:
                        predict_class[i] = 'others'

                    # 电梯厢层不符合电梯厢尺寸的构件置为others
                    elif predict_class[i] in ['elevator_box']:
                        if not (long_side / short_side < ELEVATOR_GAP_RATIO[1]
                                and ELEVATOR_GAP_RANGE[0] * long_ratio < long_side < ELEVATOR_GAP_RANGE[1] * long_ratio
                                and ELEVATOR_GAP_RANGE[0] * short_ratio < short_side < ELEVATOR_GAP_RANGE[
                                    1] * short_ratio
                        ):
                            predict_class[i] = 'others'

                    # 电梯厢有空调，尺寸变大
                    elif predict_class[i] in ['air_conditioner']:
                        if not (
                                short_side < AIR_CONDITIONER_SHORT_SIDE_RANGE[0] * short_ratio
                                or long_side < AIR_CONDITIONER_LONG_SIDE_RANGE[0] * long_ratio
                                or long_side > AIR_CONDITIONER_LONG_SIDE_RANGE[1] * long_ratio
                        ):
                            # 过滤掉可能误识别的冰箱，如短边大于550mm置为others。
                            rect = get_min_rect(entity_image_list[i])
                            if len(rect) != 0:
                                short_side_new = min(rect[1][0], rect[1][1])
                                if short_side_new > AIR_CONDITIONER_SHORT_SIDE_RANGE[1] * short_ratio:
                                    predict_class[i] = 'others'
                        else:
                            predict_class[i] = 'others'
                    
                    # 消火栓误识别尺寸矫正
                    elif predict_class[i] in ["xiaohuoshuan"]:
                        if long_side < FIRE_HYDRANT_LONG_SIDE_RANGE[0] * long_ratio:
                            predict_class[i] = "others"
                            
                    # # 电梯厢层符合电梯厢尺寸的构件置为电梯厢，for #1370
                    # if (long_side / short_side < ELEVATOR_GAP_RATIO[1]
                    #     and ELEVATOR_GAP_RANGE[0] * long_ratio < long_side < ELEVATOR_GAP_RANGE[1] * long_ratio
                    #     and ELEVATOR_GAP_RANGE[0] * short_ratio < short_side < ELEVATOR_GAP_RANGE[1] * short_ratio
                    # ):
                    #     class_to_check = ['Line', 'Polyline', 'Polyline2d']
                    #     _line_dict = get_origin_border_entity_info(origin_border_entity_info, [layer], class_to_check,
                    #                                                space_scale, border_coord, ratio)
                    #     line_list = []
                    #     for _, entity_list in _line_dict.items():
                    #         line_list.extend(entity_list)
                    #     # Polyline中有arc，需要过滤
                    #     line_list = list(filter(lambda x: len(x) == 4, line_list))
                    #     print('Note: stair line num: {}'.format(len(line_list)))
                    #     # 匹配bbox内的楼梯直线图元
                    #     bb_cnt = get_contour_from_bbox(bb)
                    #     stair_line_list = get_drawing_stair_line_list(bb_cnt, line_list, ratio, drawing_type='plan',
                    #                                                   len_min_plan=500, len_max_plan=1900)
                    #     # 合并楼梯构件
                    #     stair_entity_info = get_stair_entity_info(stair_line_list, ratio, drawing_type='plan',
                    #                                               margin_max_plan=400, margin_min_plan=100,
                    #                                               min_line_num=3)
                    #     if len(stair_entity_info) > 0:
                    #         predict_class[i] = 'stair'
                    #     else:
                    #         predict_class[i] = 'elevator_box'
                # 立管尺寸限制
                elif predict_class[i] == 'pipe':
                    if long_side > PIPE_SIDE_RANGE[1] * long_ratio:
                        predict_class[i] = 'others_p'

                # 分类为'air_conditioner', 'xiaohuoshuan'尺寸超限
                # 或在'pipe', 'elevator_box', 'floor_drain'， 'window', 'door', 'elevator_door'层中为others
                elif predict_class[i] in ['air_conditioner', 'xiaohuoshuan']:
                    if (
                            short_side < AIR_CONDITIONER_SHORT_SIDE_RANGE[0] * short_ratio
                            or long_side > AIR_CONDITIONER_LONG_SIDE_RANGE[1] * long_ratio
                            or long_side < AIR_CONDITIONER_LONG_SIDE_RANGE[0] * long_ratio
                            or layer in ['pipe', 'floor_drain', 'window', 'door', 'elevator_door']
                    ):
                        if predict_class[i] in ['air_conditioner']:
                            # 根据issue2107，一种很长的、由四块门板组成的推拉门（一般的推拉门由两块门板组成）被误分类为空调，然后被调整为others
                            if (long_side / short_side) > 5:
                                predict_class[i] = 'tuila_door'
                            else:
                                predict_class[i] = 'others'
                    # 如果分类结果是消火栓但图层不在消火栓图层或尺寸不匹配，则置为others
                    if predict_class[i] in ['xiaohuoshuan']:
                        if layer not in ['fire_hydrant']:
                            if layer in ['yu_liu_kong_dong']:
                                predict_class[i] = 'reserved_hole'
                            else:
                                predict_class[i] = 'others'
                    if predict_class[i] in ['air_conditioner'] and layer in ["fire_hydrant"]:
                        predict_class[i] = 'xiaohuoshuan'
                # 分类为'paiqikou', 'paishuikou'为others
                elif predict_class[i] in ['paiqikou', 'paishuikou']:
                    # 在门窗图层的置为百叶
                    if layer in ['window', 'door']:
                        predict_class[i] = 'baiye'
                    else:
                        predict_class[i] = 'others_d'

                # 厨房排烟管道一定在厨房
                elif predict_class[i] in ['kitchen_exhaust_pipe']:
                    temp_list = [room_info for room_info in kitchen_infos if
                                 get_contours_iou(room_info[0], entity_cnt) > 0.5]
                    if not temp_list:
                        predict_class[i] = 'others'
                    # 纠正卫生间排风井
                    temp_list = [room_info for room_info in bathroom_infos if
                                 get_contours_iou(room_info[0], entity_cnt) > 0.5]
                    if temp_list:
                        predict_class[i] = 'washroom_paifengjing'

                # 将误识别为楼梯的小构件置为other
                elif predict_class[i] == 'stair':
                    if (long_side < STAIR_LONG_SIDE_RANGE[0] * long_ratio
                            or short_side < STAIR_SHORT_SIDE_RANGE[0] * short_ratio
                    ):
                        # 纠正门联窗漏识别
                        if (
                                DOOR_SHORT_SIDE_RANGE[0] * short_ratio < short_side
                                < 1200 * short_ratio
                                and long_side >= 3000 * long_ratio
                        ) and layer in ['window', 'door']:
                            predict_class[i] = 'menlianchuang'
                        else:
                            predict_class[i] = 'others'

                elif predict_class[i] == 'others' and layer in ['window', 'door', 'elevator_door']:
                    # issue 2132,一种很长的推拉门被误分类为other.长宽比为2305/55=41.9
                    if (25 < (long_side / short_side) < 45
                            and TUILA_DOOR_SHORT_SIDE_RANGE[0] * short_ratio < short_side
                            < TUILA_DOOR_SHORT_SIDE_RANGE[1] * short_ratio
                    ):
                        predict_class[i] = 'tuila_door'
                    elif (10 < (long_side / short_side) < 100
                          and WINDOW_SHORT_SIDE_RANGE[0] * short_ratio < short_side
                          < WINDOW_SHORT_SIDE_RANGE[1] * short_ratio
                    ):
                        predict_class[i] = 'window'
                    elif ((long_side / short_side) < 1.5
                          and DOOR_LONG_SIDE_RANGE[0] * long_ratio < long_side < DOOR_LONG_SIDE_RANGE[1] * long_ratio
                          and DOOR_SHORT_SIDE_RANGE[0] * short_ratio < short_side < DOOR_SHORT_SIDE_RANGE[
                              1] * short_ratio
                    ):
                        predict_class[i] = 'door'

                # 统一进行尺寸、图层限制
                # 地漏
                if predict_class[i] == 'dilou':
                    # 尺寸
                    if short_side > DILOU_SIDE_RANGE[1] * short_ratio or long_side < DILOU_SIDE_RANGE[0] * long_ratio:
                        print("---------->>> fix dilou with size")
                        print(short_side, long_side)
                        print(short_ratio, long_ratio)
                        predict_class[i] = 'others_d'
                    # 图层
                    elif layer not in ['floor_drain', 'floor_drain_mix']:
                        print("---------->>> fix dilou with layer")
                        print(layer)
                        predict_class[i] = 'others_d'
                    # 根据图元进行过滤
                    # 获取直线
                    class_to_check = ['Line', 'Polyline', 'Polyline2d']
                    _line_dict = get_origin_border_entity_info(origin_border_entity_info, [layer], class_to_check,
                                                               space_scale, border_coord, ratio)
                    line_list = []
                    for _, entity_list in _line_dict.items():
                        line_list.extend(entity_list)
                    line_list = list(filter(lambda x: len(x) == 4, line_list))
                    line_in_entity_list = get_line_in_bbox(line_list, bb)
                    class_to_check = ['Arc', 'Polyline', 'Polyline2d']
                    _arc_dict = get_origin_border_entity_info(origin_border_entity_info, [layer], class_to_check,
                                                              space_scale, border_coord, ratio)
                    arc_list = []
                    for _, entity_list in _arc_dict.items():
                        arc_list.extend(entity_list)
                    arc_list = list(filter(lambda x: len(x) == 8, arc_list))  # Polyline中有line，需要过滤
                    # arc_list = [arc[2:6] for arc in arc_list]
                    arc_in_entity_list = entity_in_bbox(arc_list, bb)
                    if len(arc_in_entity_list) > 2 or len(line_in_entity_list) == 0:
                        predict_class[i] = "others_d"
                    # pipe图层内带十字线的立管被误分为地漏，进行矫正
                    elif layer in ["pipe"] and len(line_in_entity_list) == 2:
                        line_1 = line_in_entity_list[0]
                        line_2 = line_in_entity_list[1]
                        angle = angle_between_segment2(np.array([line_1[:2], line_1[2:]]), np.array([line_2[:2], line_2[2:]]))
                        if 87 < angle < 93:
                            predict_class[i] = 'pipe'
                # 电梯厢误分类，根据尺寸和关键字进行矫正
                if predict_class[i] == "others" and ELEVATOR_GAP_RANGE[0] * long_ratio < long_side < ELEVATOR_GAP_RANGE[
                    1] * long_ratio and ELEVATOR_GAP_RANGE[0] * short_ratio < short_side < ELEVATOR_GAP_RANGE[
                    1] * short_ratio:
                    text_info_all = border_text_info[TextType.ALL]
                    for text_info in text_info_all:
                        if re.search("客梯", text_info[4]):
                            text_cnt = get_contour_from_bbox(text_info[:4])
                            if get_contours_iou(entity_cnt, text_cnt) > 0.8:
                                predict_class[i] = 'elevator_box'
                                break
                # 为避免下面的将推拉门分为窗户，判断在电梯井附近的推拉门符合条件，置为电梯门
                if predict_class[i] == 'tuila_door':
                    # tuila_ext_bbox = extend_margin(bb, 50)
                    tuila_ext_bbox = extend_margin_by_side(bb, int(500 * ratio[0]))
                    tuila_ext_cnt = get_contour_from_bbox(tuila_ext_bbox)
                    for room_info in elevator_room_infos:
                        room_contour, room_box, room_name = room_info
                        if get_contours_iou(room_contour, tuila_ext_cnt) > 0:
                            predict_class[i] = 'elevator_door'
                            break
                if predict_class[i] in ['guanjingmen', 'door', 'menlianchuang', 'zhexianchuang', 'window',
                                        'tuila_door']:
                    # 云效254164，其他图层构件误识别为门，管井门
                    if layer in ['air_conditioner']:
                        predict_class[i] = 'air_conditioner'
                    elif layer not in ['window', 'door', 'elevator_door', 'elevator_box', 'emergency_door', "chu_wei"]: # 有些卫生间的推拉门在厨卫图层
                        predict_class[i] = 'others_d'

                    # 门板和门的弧线没有合并在一起，导致门板会被误识别为窗
                    # 通过判断创附近有没有90的弧线进行过滤
                    # 有些窗的开启弧线也是90度，导致会把窗致为others_d
                    # 因此看bbox周围是否有窗文本，没有再去判定
                    has_window_text = False
                    all_text = border_text_info[TextType.ALL]
                    for text in border_text_info[TextType.ALL]:
                        # 匹配窗文本 C0612，LC12+10a1, LC06a1, LC10-5; C8，LC3a，LC3，LC3-1
                        if re.search("C.*(\d{2}[a-z\-+]?\d{1,2}|\d{1}[a-z\-]?\d*)", text[-1]) and not re.search("M", text[-1]) and Iou_temp(text[:4], extend_margin_by_side(bb, 5*ext_margin)):
                            has_window_text = True
                            print("has_window_text", text[-1])
                            break
                    # 如果没有窗文本，正常情况下可以判断窗线两侧会和墙线相交
                    if predict_class[i] in ["window"] and not has_window_text:
                        layer_to_check = ['door', 'window', "wall"]
                        class_to_check = ['Line', 'Polyline', 'Polyline2d']
                        line_dict = get_origin_border_entity_info(origin_border_entity_info, layer_to_check,
                                                                  class_to_check, space_scale, border_coord,
                                                                  ratio)
                        wind_line_list = []
                        wall_line_list = []
                        for layer_name, entity_list in line_dict.items():
                            if layer_name == "wall":
                                wall_line_list.extend(entity_list)
                            else:
                                wind_line_list.extend(entity_list)
                        # Polyline中有Arc，需要过滤
                        wind_line_list = list(filter(lambda x: len(x) == 4, wind_line_list))
                        wall_line_list = list(filter(lambda x: len(x) == 4, wall_line_list))
                        bb_ext = extend_margin(bb, 3*ext_margin)
                        wind_line_list = entity_in_bbox(wind_line_list, bb_ext)
                        wall_line_list = entity_in_bbox(wall_line_list, bb_ext) + \
                                         [wall_line for wall_line in wall_line_list if line_overlap_poly(get_contour_from_bbox(bb_ext), wall_line)]
                        bbox = remove_margin(bb, ext_margin)

                        # {相同斜率：{相同长度：line_list}}
                        wind_parallel_line_dict = get_parallel_line_list_with_same_len(wind_line_list, ratio)
                        # 查找窗线，和bbox一边基本等长
                        # 对于倾斜的窗， bbox尺寸不能正确反映构件的尺寸， 用bbox的对角线长度近似代替实际长度
                        long_side = point_euclidean_distance(bbox[:2], bbox[2:])
                        intersect_wall_line = False
                        is_window = True
                        for k, item_dict in wind_parallel_line_dict.items():
                            for l, line_list in item_dict.items():
                                inter_wall_side_1 = False
                                inter_wall_side_2 = False
                                if len(line_list) >= 2:
                                    if abs(l/long_side - 1) < 0.35:
                                        for line in line_list:
                                            line_bbox_1 = [line[0] - 2, line[1] - 2, line[0] + 2, line[1] + 2]
                                            line_bbox_2 = [line[2] - 2, line[3] - 2, line[2] + 2, line[3] + 2]
                                            for wall_line in wall_line_list:
                                                if abs(Calculate_angle(line, wall_line) - 90) < 5:
                                                    if line_overlap_poly(get_contour_from_bbox(line_bbox_1),
                                                                          wall_line):
                                                        inter_wall_side_1 = True
                                                    if line_overlap_poly(get_contour_from_bbox(line_bbox_2),
                                                                          wall_line):
                                                        inter_wall_side_2 = True
                                            print("inter_wall_side_1, inter_wall_side_2", inter_wall_side_1, inter_wall_side_2)
                                            if inter_wall_side_2 and inter_wall_side_1:
                                                intersect_wall_line = True
                                                break
                                    elif abs(l/long_side - 0.5) < 0.1:
                                        # 对于图元长度只有构件长边长度一半左右的的构件，置为推拉门
                                        predict_class[i] = "tuila_door"
                                        is_window = False

                        print("intersect_wall_line", intersect_wall_line)
                        if is_window and not intersect_wall_line:
                            predict_class[i] = "others_d"

                    if predict_class[i] in ["window"] and not has_window_text:
                        layer_to_check = [layer, 'door', 'window']
                        class_to_check = ['Arc', 'Polyline', 'Polyline2d', "Ellipse"]
                        arc_line_dict = get_origin_border_entity_info(origin_border_entity_info, layer_to_check,
                                                                      class_to_check, space_scale, border_coord,
                                                                      ratio)
                        arc_entity_list = []
                        for _, e_list in arc_line_dict.items():
                            arc_entity_list.extend(e_list)
                        # Polyline中有line，需要过滤
                        arc_line_list = list(filter(lambda x: len(x) == 8, arc_entity_list))
                        ellipse_line_list = list(filter(lambda x: len(x) == 11, arc_entity_list))
                        arc_list = [arc for arc in arc_line_list if Iou_temp(arc[:4], bb)]
                        ellipse_list = [ellipse for ellipse in ellipse_line_list if Iou_temp(ellipse[:4], bb)]
                        # 有圆弧且圆心角为90
                        if (arc_list and abs(arc_list[0][-1] - 90) < 5) or (
                                ellipse_list and abs(ellipse_list[0][-1] - ellipse_list[0][-2] - 90) < 5):
                            predict_class[i] = "others_d"
                    # 根据文本纠正管井门
                    if predict_class[i] in ["window"]:
                        for text in border_text_info[TextType.ALL]:
                            if re.search("M\d{4}", text[-1]) and Iou_temp(text[:4], bb):
                                predict_class[i] = "guanjingmen"
                                break
                    # 2020年2月3号更新需求窗构件和套内空间相连并且中间有小于4平米的无名空间
                    if predict_class[i] in ['zhexianchuang', 'window']:
                        ## 判断窗构件外扩1000mm是否和套内空间相连
                        indoor_room_iou = None
                        non_name_room_iou = None
                        dianjing_room_iou = None
                        bb_ext = extend_margin_by_side(bb, int(1000 * ratio[0]))
                        for room in indoor_infos:
                            if get_contours_iou(room[0], get_contour_from_bbox(bb_ext)) > 0:
                                print('识别到和套内空间相交')
                                indoor_room_iou = get_contours_iou(room[0], get_contour_from_bbox(bb_ext))
                                break
                        for room in non_name_infos:
                            if get_contours_iou(room[0],
                                                get_contour_from_bbox(bb_ext)) > 0 and contour_area_in_reality(
                                room[0], ratio) < 4:
                                print('shibie dao 和无名空间相交！！！')
                                # 有的凸窗附近有一些干扰的无名空间影响，添加筛选iou最高的无名空间
                                if non_name_room_iou:
                                    non_name_room_iou = max(non_name_room_iou,
                                                            get_contours_iou(room[0], get_contour_from_bbox(bb_ext)))
                                else:
                                    non_name_room_iou = get_contours_iou(room[0], get_contour_from_bbox(bb_ext))
                                # break
                        for room in dianjing_room_infos:
                            if get_contours_iou(room[0], get_contour_from_bbox(bb_ext)) > 0:
                                dianjing_room_iou = get_contours_iou(room[0], get_contour_from_bbox(bb_ext))
                        print('non_name_room_iou', non_name_room_iou)
                        print('indoor_room_iou', indoor_room_iou)
                        if indoor_room_iou is not None and non_name_room_iou is not None and non_name_room_iou > indoor_room_iou:
                            predict_class[i] = 'tuchuang'
                            print('shibie 到凸窗！！！！')
                        if dianjing_room_iou:
                            predict_class[i] = 'guanjingmen'
                        elif predict_class[i] == 'zhexianchuang':
                            # 纠正门联窗
                            layer_to_check = [layer, 'door', 'window']
                            class_to_check = ['Arc', 'Polyline', 'Polyline2d', "Ellipse"]
                            arc_line_dict = get_origin_border_entity_info(origin_border_entity_info, layer_to_check,
                                                                              class_to_check, space_scale, border_coord,
                                                                              ratio)
                            arc_entity_list = []
                            for _, e_list in arc_line_dict.items():
                                arc_entity_list.extend(e_list)
                            # Polyline中有line，需要过滤
                            arc_line_list = list(filter(lambda x: len(x) == 8, arc_entity_list))
                            ellipse_line_list = list(filter(lambda x: len(x) == 11, arc_entity_list))
                            arc_list = entity_in_bbox(arc_line_list, bb)
                            ellipse_list = entity_in_bbox(ellipse_line_list, bb)
                            line_class_to_check = ['Line', 'Polyline', 'Polyline2d']
                            line_line_dict = get_origin_border_entity_info(origin_border_entity_info, layer_to_check,
                                                                          line_class_to_check, space_scale, border_coord,
                                                                          ratio)
                            line_entity_list = []
                            for _, e_list in line_line_dict.items():
                                line_entity_list.extend(e_list)
                            # Polyline中有line，需要过滤
                            line_line_list = list(filter(lambda x: len(x) == 4, line_entity_list))
                            bb_nrl = remove_margin(bb, ext_margin//2)
                            line_line_list_in_bbox = entity_in_bbox(line_line_list, bb_nrl)
                            # 有圆弧且圆心角为90
                            if (arc_list and abs(arc_list[0][-1]-90) < 5) or (ellipse_list and abs(ellipse_list[0][-1]-ellipse_list[0][-2]-90) < 5):
                                predict_class[i] = "menlianchuang"
                            # bbox只有一条门窗图元线
                            elif len(line_line_list_in_bbox) == 1:
                                predict_class[i] = "others_w"
                            else:
                                predict_class[i] = 'corner_window'

                    # 门连窗尺寸矫正
                    elif predict_class[i] in ['menlianchuang']:
                        # 添加Ellipse图元，因为圆弧有可能用Ellipse画
                        class_to_check = ['Line', 'Polyline', 'Polyline2d', 'Arc', "Ellipse"]
                        _Line_dict = get_origin_border_entity_info(origin_border_entity_info, [layer],
                                                                   class_to_check,
                                                                   space_scale, border_coord, ratio)
                        line_list_all = []
                        for _, entity_list in _Line_dict.items():
                            line_list_all.extend(entity_list)
                        line_list = list(filter(lambda x: len(x) == 4, line_list_all))  # Polyline中有line，需要过滤
                        ellipse_entity_list = list(filter(lambda x: len(x) == 11, line_list_all))
                        arc_list = list(filter(lambda x: len(x) == 8, line_list_all))
                        # arc_list = [arc[2:] for arc in arc_list]
                        line_in_entity_list = entity_in_bbox(line_list, bb)
                        ellipse_entity_list = entity_in_bbox(ellipse_entity_list, bb)
                        arc_in_entity_list = entity_in_bbox(arc_list, bb)
                        # 计算Ellipse的夹角
                        ellipse_entity_list = [ellipse[:] + [abs(ellipse[-1]-ellipse[-2])] for ellipse in ellipse_entity_list]
                        # 窗误分类为门联窗进行矫正
                        if len(arc_in_entity_list + ellipse_entity_list) == 0 or not any(abs(arc[-1]) > 50 for arc in arc_in_entity_list+ellipse_entity_list):
                            predict_class[i] = 'window'
                        # 短边异常的门联窗进行过滤
                        elif short_side > DOOR_SHORT_SIDE_RANGE[1] * short_ratio:
                            if len(arc_in_entity_list) != 4 and layer not in ["window", "door"]:
                                for line in line_in_entity_list:
                                    if line[0] == line[2] or line[1] == line[3]:
                                        predict_class[i] = 'others_m'
                                        break
                        # 若满足门的尺寸，继续判定
                        elif long_side < DOOR_LONG_SIDE_RANGE[1] * long_ratio:
                            # 可以获取到一个大于100度的弧形，则为门
                            if any(abs(arc[-1]) > 100 for arc in arc_in_entity_list):
                                predict_class[i] = 'door'

                        # 纠正普通窗：有些窗的开启圆弧也是90度，导致被分为门联窗
                        # 通过窗附近的文本Cxxxx来过滤
                        if predict_class[i] in ["menlianchuang"]:
                            all_text = border_text_info[TextType.ALL]
                            for text in all_text:
                                if Iou_temp(text[:4], extend_margin(bb, ext_margin)) and re.search("C\d{4}", text[-1]) and not re.search("M", text[-1]):
                                    predict_class[i] = "window"
                                    break

                    # 窗图层不满足推拉门尺寸的置为窗户，云效268455、268457、窗长5m，宽25cm。
                    elif predict_class[i] in ['tuila_door']:
                        if (layer in ['window']
                                and short_side > TUILA_DOOR_SHORT_SIDE_RANGE[1] * short_ratio
                                and long_side > ELEVATOR_GAP_RANGE[1] * long_ratio
                        ):
                            predict_class[i] = 'window'
                    elif predict_class[i] in ['door']:
                        # 将误识别为门的小构件置为管井门，for issue 1264
                        if (long_side < DOOR_LONG_SIDE_RANGE[0] * long_ratio
                                and short_side < DOOR_SHORT_SIDE_RANGE[0] * short_ratio
                        ):
                            # 与室内空间有交集的不是管井门
                            entity_coord = get_contour_from_bbox(bb)
                            if any(get_contours_iou(room_info[0], entity_coord)
                                   for room_info in (bathroom_infos + kitchen_infos + bedroom_infos + study_room_infos)):
                                pass
                            else:
                                predict_class[i] = 'guanjingmen'

                        elif long_side > DOOR_LONG_SIDE_RANGE[1] * long_ratio:
                            if long_side > 2 * DOOR_LONG_SIDE_RANGE[1] * long_ratio:
                                if layer in ["window", "door"]:
                                    predict_class[i] = 'menlianchuang'
                            else:
                                predict_class[i] = 'others_d'
                    elif predict_class[i] in ['guanjingmen']:
                        # 获取圆弧
                        arc_entity_list = []
                        arc_entity_dict = get_origin_border_entity_info(origin_border_entity_info, layer,
                                                                        ['Arc'], space_scale, border_coord, ratio)
                        for _, entity_list in arc_entity_dict.items():
                            arc_entity_list.extend(entity_list)
                        arc_entity_list = entity_in_bbox(arc_entity_list, bb)
                        # 根绝圆心角过滤， arc 结构为（起点，终点，圆心点，半径，圆心角）
                        arc_entity_list = [arc for arc in arc_entity_list if abs(arc[-1] - 90) < 1]
                        if len(arc_entity_list) == 1:
                            # print("arc_entity_list", len(arc_entity_list))
                            predict_class[i] = 'door'
                        # print("predict class after filter", predict_class[i])
                # 厨房的拐角线误识别为转角窗
                if predict_class[i] == "corner_window":
                    for room in kitchen_infos:
                        if get_contours_iou(room[0], entity_cnt) > 0.7:
                            predict_class[i] = "others_l"

                # 窗误识别为推拉门
                if predict_class[i] == 'tuila_door':
                    # 有些卫生间的推拉门在厨卫图层
                    layer_to_check = ['door', 'window', "floor_drain_mix"]
                    class_to_check = ['Line', 'Polyline', 'Polyline2d']
                    cabinet_line_dict = get_origin_border_entity_info(origin_border_entity_info,
                                                                      layer_to_check,
                                                                      class_to_check, space_scale,
                                                                      border_coord, ratio)
                    cabinet_line_list = []
                    for _, e_list in cabinet_line_dict.items():
                        cabinet_line_list.extend(e_list)
                    # Polyline中有arc，需要过滤
                    cabinet_line_list = list(filter(lambda x: len(x) == 4, cabinet_line_list))

                    cabinet_line_list = get_line_in_bbox(cabinet_line_list, bb)
                    if len(cabinet_line_list) == 1:
                        predict_class[i] = "others_l"
                    else:
                        window_bbox = bb
                        long = max(window_bbox[2] - window_bbox[0], window_bbox[3] - window_bbox[1])
                        short = min(window_bbox[2] - window_bbox[0], window_bbox[3] - window_bbox[1])
                        if short / long < 0.2:
                            window_line = []
                            long_line = []
                            for cabinet_line in cabinet_line_list:
                                if cabinet_line[0] >= window_bbox[0] and cabinet_line[1] >= window_bbox[
                                    1] and cabinet_line[2] <= window_bbox[2] and cabinet_line[3] <= \
                                        window_bbox[3]:
                                    line_long = ((cabinet_line[2] - cabinet_line[0]) ** 2 + (
                                            cabinet_line[3] - cabinet_line[1]) ** 2) ** 0.5
                                    if line_long < 10:
                                        diff = cabinet_line[0] - window_bbox[0]
                                        not_add = True
                                        for win in window_line:
                                            if abs(win - diff) < 50:
                                                not_add = False
                                        if not_add:
                                            window_line.append(diff)
                                    else:
                                        if abs(cabinet_line[0] - cabinet_line[2]) < 2:
                                            long_line.append(min(cabinet_line[1], cabinet_line[3]))
                                        elif abs(cabinet_line[1] - cabinet_line[3]) < 2:
                                            long_line.append(min(cabinet_line[0], cabinet_line[2]))
                            long_line.sort()
                            if len(long_line) > 1:
                                if (len(window_line) == 2 or len(window_line) == 3 or len(
                                        window_line) == 0) and long_line[-1] - long_line[0] < 5:
                                    predict_class[i] = 'window'
                # 一种长形推拉门大概6500mm和4200mm，错分为baiye,others，下面进行矫正，根据尺寸和所在空间为客厅过滤
                if predict_class[i] in ['baiye', 'others'] and layer in ['door']:
                    if long_side > 4200 * long_ratio:
                        ext_by_bbox = extend_margin(bb, 10)
                        ext_by_cnt = get_contour_from_bbox(ext_by_bbox)
                        for room in living_room_infos:
                            room_contour, room_box, room_name = room
                            if get_contours_iou(room_contour, ext_by_cnt) > 0:
                                predict_class[i] = 'tuila_door'
                                break

                # 根据空间分割信息对空调进行矫正，卫生间、厨房的空调置为others
                if predict_class[i] in ['air_conditioner']:
                    ac_coord = get_air_conditione_coord(entity_image_list[i], bb)
                    for room_info in (kitchen_infos + bathroom_infos + anteroom_infos):
                        room_contour, room_box, room_name = room_info
                        if '客厅' not in room_name and get_contours_iou(room_contour, ac_coord) > 0.5:
                            predict_class[i] = 'others'
                            break

                # 结合墙信息矫正空调，若空调中有两条平行于空调长边且距离超过阈值的墙线穿过其中，则置为other。
                # for issue 873,2139
                if predict_class[i] in ['air_conditioner']:
                    ac_rect = get_min_rect(entity_image_list[i])
                    ac_coord = get_air_conditione_coord(entity_image_list[i], bb)
                    ac_contour = np.array([[ac_coord[0]], [ac_coord[1]], [ac_coord[2]], [ac_coord[3]]])
                    # 网格化分割墙的bbox，并获取空调范围附近墙线搜索范围
                    wall_bbox_line_dict = get_mesh_grid_dict(wall_bbox_line, w_range, h_range)
                    wall_line_range = get_grid_range(bb, wall_bbox_line_dict, w_range, h_range)
                    line_inside = []
                    for wall_line in wall_line_range:
                        inter_line = line_intercept_by_poly(wall_line, ac_contour)
                        if inter_line != None:
                            k = get_point_skew((wall_line[0], wall_line[1]), (wall_line[2], wall_line[3]))
                            if long_side == bb[2] - bb[0]:  # 空调平行于x轴放置
                                if abs(k) < 1:  # 取斜率绝对值小于1的墙线
                                    line_inside = get_ac_inside_wall(line_inside, wall_line, short_side / 2)
                            else:  # 空调平行于y轴放置
                                if not (abs(k) < 1):  # 取斜率绝对值不小于1的墙线
                                    line_inside = get_ac_inside_wall(line_inside, wall_line, short_side / 2)
                        if len(line_inside) >= 2:
                            predict_class[i] = 'others'
                            break

                # 结合空调文本信息矫正符合空调尺寸的空调（针对构件小图中只有一个矩形框的空调）,for issue 1235,1735.
                if predict_class[i] in ['others'] and layer in ["air_conditioner", "air_conditioner_mix"]:
                    if not (
                            short_side < AIR_CONDITIONER_SHORT_SIDE_RANGE[0] * short_ratio
                            or long_side < AIR_CONDITIONER_LONG_SIDE_RANGE[0] * long_ratio
                            or long_side > AIR_CONDITIONER_LONG_SIDE_RANGE[1] * long_ratio
                    ):
                        aircon_text = border_text_info[TextType.AIRCON]
                        for text_info in aircon_text:
                            text_cnt = get_contour_from_bbox(text_info[:4])
                            if get_contours_iou(entity_cnt, text_cnt) > 0.8:
                                predict_class[i] = 'air_conditioner'
                                break
                    # 超长门连窗漏识别，for issue 1321
                    if (
                            DOOR_SHORT_SIDE_RANGE[0] * short_ratio < short_side
                            < 1000 * short_ratio
                            and long_side >= 3000 * long_ratio
                    ) and layer in ['window', 'door']:
                        predict_class[i] = 'menlianchuang'

                # 结合空间信息，所有电梯井里的符合电梯厢的构件置为电梯厢
                if (long_side / short_side < ELEVATOR_GAP_RATIO[1]
                        and ELEVATOR_GAP_RANGE[0] * long_ratio < long_side < ELEVATOR_GAP_RANGE[1] * long_ratio
                        and ELEVATOR_GAP_RANGE[0] * short_ratio < short_side < ELEVATOR_GAP_RANGE[1] * short_ratio
                ):
                    for room_info in elevator_room_infos:
                        room_contour, room_box, room_name = room_info
                        # 如果电梯井大于50平，则空间分割有误、不作为后处理依据
                        if contour_area_in_reality(room_contour, ratio) > 50:
                            continue
                        if get_contours_iou(room_contour, entity_cnt) > 0.8:
                            predict_class[i] = 'elevator_box'
                            break

                # 结合空间信息（所有在卧室、客厅、厨房、卫生间等空间）将电梯厢的构件置为others
                if predict_class[i] in ['elevator_box']:
                    if (ELEVATOR_GAP_RANGE[0] * long_ratio > long_side
                            or ELEVATOR_GAP_RANGE[0] * short_ratio > short_side
                    ):
                        predict_class[i] = 'others'
                    else:
                        entity_coord = get_contour_from_bbox(bb)
                        for room_info in (bedroom_infos + living_room_infos + kitchen_infos
                                          + bathroom_infos + storage_room_infos + closet_room_infos
                                          + balcony_room_infos + housekeeping_room_infos):
                            room_contour, room_box, room_name = room_info
                            if get_contours_iou(room_contour, entity_coord) > 0.8:
                                predict_class[i] = 'others'
                                break
                # 误分类的信报箱根据图层和尺寸置为空调
                if predict_class[i] == "mailbox" and layer in ["air_conditioner", "air_conditioner_mix"]:
                    if not (
                            short_side < AIR_CONDITIONER_SHORT_SIDE_RANGE[0] * short_ratio
                            or long_side < AIR_CONDITIONER_LONG_SIDE_RANGE[0] * long_ratio
                            or long_side > AIR_CONDITIONER_LONG_SIDE_RANGE[1] * long_ratio
                    ):
                        predict_class[i] = "air_conditioner"
                if predict_class[i] == "mailbox" and layer in ["fire_hydrant"]:
                    predict_class[i] = "xiaohuoshuan"

                # 根据构件所在空间区分空调室内机、室外机
                if predict_class[i] in ['air_conditioner'] and layer in ["air_conditioner", "air_conditioner_mix"]:
                    entity_coord = get_contour_from_bbox(bb)
                    if any((get_contours_iou(air_room_info[0], entity_coord) > 0.35) for air_room_info in
                           air_room_infos):
                        predict_class[i] = 'air_conditioner_ins'
                    else:
                        predict_class[i] = 'air_conditioner_out'
                    for text in border_text_info[TextType.ALL]:
                        if re.search("A/C|AC", text[4]):
                            if get_contours_iou(entity_cnt, get_contour_from_bbox(text[:4])) > 0.5:
                                predict_class[i] = 'air_conditioner_out'

                                break
                # ============================1230：构件细分类 ============================
                # 楼梯细分类逻辑：两个上和两个下为剪刀楼梯，一个上和一个下为双跑楼梯，一个上或一个下为直跑楼梯
                if predict_class[i] in ['stair']:
                    stair_text_1 = [text_info for text_info in border_text_info[TextType.ALL] if
                                    re.search('^上$', text_info[4].strip())]
                    stair_text_2 = [text_info for text_info in border_text_info[TextType.ALL] if
                                    re.search('^下$', text_info[4].strip())]
                    entity_bbox = extend_margin(bb, 100)
                    entity_cnt_ext = get_contour_from_bbox(entity_bbox)
                    temp_stair_text_1 = [text_info for text_info in stair_text_1 if
                                         get_contours_iou(entity_cnt_ext, get_contour_from_bbox(text_info[:4])) > 0.5]
                    temp_stair_text_2 = [text_info for text_info in stair_text_2 if
                                         get_contours_iou(entity_cnt_ext, get_contour_from_bbox(text_info[:4])) > 0.5]
                    if len(temp_stair_text_1) > 1 and len(temp_stair_text_2) > 1:
                        predict_class[i] = 'scissors_stair'
                    elif len(temp_stair_text_1) >= 1 or len(temp_stair_text_2) >= 1:
                        predict_class[i] = 'double_stair'
                    else:
                        predict_class[i] = 'single_stair'
                if predict_class[i] in ["single_stair"] and layer not in ['elevator_stair', 'elevator_box',
                                                                          'stair_dayang_plan_stair', 'stair_dayang_profile_stair']:
                    # 纠正门联窗漏识别
                    if (
                            DOOR_SHORT_SIDE_RANGE[0] * short_ratio < short_side
                            < 1200 * short_ratio
                            and long_side >= 3000 * long_ratio
                    ) and layer in ['window', 'door']:
                        predict_class[i] = 'menlianchuang'
                    else:
                        predict_class[i] = 'others'

                # 分类误分为others的跟据图层和尺寸限制，以及电梯井空间来判断为电梯门
                if predict_class[i] == 'others' and layer in ["door", "window", "elevator_door"]:
                    length_d = point_euclidean_distance(bb[:2], bb[2:])
                    if 900 * short_ratio < length_d < 1500 * short_ratio:
                        # tuila_ext_bbox = extend_margin(bb, 50)
                        tuila_ext_bbox = extend_margin_by_side(bb, int(500 * ratio[0]))
                        tuila_ext_cnt = get_contour_from_bbox(tuila_ext_bbox)
                        for room_info in elevator_room_infos:
                            room_contour, room_box, room_name = room_info
                            if get_contours_iou(room_contour, tuila_ext_cnt) > 0:
                                predict_class[i] = 'elevator_door'
                                break

                # 信报箱: 引线标注，标注文本：“信报箱”
                if re.search('信报箱', annotation_text) is not None:
                    predict_class[i] = 'mailbox'
                    
                # 根据引线矫正预留孔洞
                if re.search("'[BQ]'|'K[123]'", annotation_text, re.I) is not None:
                    print(f"******* long_side:{long_side} short_side:{short_side} annotation_text: {annotation_text} bbox:{bb} layer:{layer}")
                    if layer in ['yu_liu_kong_dong']:
                        predict_class[i] = 'reserved_hole'
                    elif long_side < 800*short_ratio and short_side < 600*short_ratio and predict_class[i] in ['others']:
                        predict_class[i] = 'reserved_hole'
                
                # 信报箱: 和墙相交的others外扩300mm找“信报箱”文本
                if predict_class[i] in ['others', 'air_conditioner'] and layer not in ["elevation_handrail", "gutter",
                                                                                       "second_third_space",
                                                                                       "elevator_stair", "elevator_box",
                                                                                       "indoor_access"]:
                    Flag_mailbox_text = False
                    entity_ext_cnt = get_contour_from_bbox(extend_margin(bb, 300 * long_ratio))
                    mailbox_text = border_text_info[TextType.MAILBOX]
                    for text_info in mailbox_text:
                        text_cnt = get_contour_from_bbox(text_info[:4])
                        # print(get_contours_iou(entity_ext_cnt, text_cnt))
                        if get_contours_iou(entity_ext_cnt, text_cnt) > 0.1:
                            Flag_mailbox_text = True
                            break
                    if Flag_mailbox_text:
                        wall_bbox_line_dict = get_mesh_grid_dict(wall_bbox_line, w_range, h_range)
                        wall_line_range = get_grid_range(bb, wall_bbox_line_dict, w_range, h_range)
                        for wall_line in wall_line_range:
                            inter_line = line_intercept_by_poly(wall_line, entity_cnt)
                            if inter_line != None:
                                predict_class[i] = 'mailbox'
                                break

                ################一种长宽形的露台被误分类成百叶窗，根据尺寸将其去除####################
                if predict_class[i] == "baiye" and layer in ["door", "window"]:
                    if 7800 * long_ratio < long_side < 8200 * long_ratio and 900 * short_ratio < short_side < 1100 * short_ratio:
                        predict_class[i] = 'others_w'

                ################墙身大样图中的保温层被误识别成百叶窗，根据图层进行过滤####################
                if predict_class[i] == "baiye" and layer not in ['door', 'window', 'elevator_door']:
                    predict_class[i] = "others"

                # 普通窗误分类为百叶窗
                # 根绝文本进行区分，百叶窗文本有B
                # 如果没有文本，则根据平行短线数量进行区分
                if predict_class[i] == "baiye":
                    for text in border_text_info[TextType.ALL]:
                        if Iou_temp(text[:4], extend_margin_by_side(bb, ext_margin)) and re.search("C\d{4}",text[-1]) and \
                                not re.search("B|b", text[-1]):
                            predict_class[i] = "window"
                            break

                ################根据百叶窗内部的小线，将错识别成普通窗的百叶置为百叶窗####################
                if predict_class[i] == "window" and layer in ['door', 'window']:
                    layer_to_check = ['door', 'window']
                    class_to_check = ['Line', 'Polyline', 'Polyline2d']
                    cabinet_line_dict = get_origin_border_entity_info(origin_border_entity_info, layer_to_check,
                                                                      class_to_check, space_scale, border_coord, ratio)
                    cabinet_line_list = []
                    for _, e_list in cabinet_line_dict.items():
                        cabinet_line_list.extend(e_list)
                    # Polyline中有arc，需要过滤
                    cabinet_line_list = list(filter(lambda x: len(x) == 4, cabinet_line_list))
                    cabinet_line_list = get_line_in_bbox(cabinet_line_list, bb)
                    # 只有一根线的窗户置为其他
                    if len(cabinet_line_list) == 1:
                        predict_class[i] = "others"
                    short_line = []
                    long_line = []
                    for line in cabinet_line_list:
                        if point_euclidean_distance(line[:2], line[2:]) < 250 * short_ratio:
                            short_line.append(line)
                        else:
                            if abs(line[0] - line[2]) < 2:
                                long_line.append(min(line[1], line[3]))
                            elif abs(line[1] - line[3]) < 2:
                                long_line.append(min(line[0], line[2]))
                    long_line.sort()
                    # 纠正普通窗, 误分为百叶窗
                    # 找到相互平行且等长的短线
                    # {相同斜率：{相同长度：line_list}}
                    # if short_line:
                    parallel_lines_dict = get_parallel_line_list_with_same_len(short_line, ratio, len_threshold = 10)
                    # 对于平行的直线要找到其中间距相同的平行线
                    max_count_total = 0
                    for k,item_dict in parallel_lines_dict.items():
                        for l, parallel_line_list in item_dict.items():
                            dist_list = []
                            for i_1 in range(len(parallel_line_list) - 1):
                                dist_list.append(get_parallel_line_distance(parallel_line_list[i_1], parallel_line_list[i_1+1]))
                            # {dist: num}
                            dist_dict = {}
                            for di in range(len(dist_list)):
                                dist_dict[dist_list[di]] = 1
                                for dj in range(di+1, len(dist_list)):
                                    if abs(dist_list[di] - dist_list[dj]) < 20 * ratio[0]:
                                        dist_dict[dist_list[di]] += 1
                            max_count = max(list(dist_dict.values()))
                            max_count_total = max(max_count_total, max_count)
                    # print("max_count_total", max_count_total)

                    # 百叶窗平行短线的数量最小阈值暂定为 10
                    if len(short_line) > 10 and max_count_total > 10:
                        predict_class[i] = "baiye"
                    elif 3 < len(long_line) < 6 and long_line[-1] - long_line[0] > 600 * long_ratio and len(
                            short_line) > 3:
                        predict_class[i] = "tuila_door"

                # 纠正推拉门漏识别
                if predict_class[i] in ["others"] and layer in ["door"]:
                    # 推拉门一般和两个空间相交
                    bb_ext = extend_margin_by_side(bb, ext_margin)
                    intersect_room_num = 0
                    for room in kitchen_infos + living_room_infos + bathroom_infos + bedroom_infos + storage_room_infos + closet_room_infos + \
                                balcony_room_infos + housekeeping_room_infos + study_room_infos:
                        if get_contours_iou(room[0], get_contour_from_bbox(bb_ext)):
                            intersect_room_num += 1
                    if intersect_room_num == 2 and \
                       TUILA_DOOR_SHORT_SIDE_RANGE[0] <= short_side <= 300 * ratio[0] and \
                       TUILA_DOOR_LONG_SIDE_RANGE[0] <= long_side <= TUILA_DOOR_LONG_SIDE_RANGE[1]:
                        predict_class[i] = "tuila_door"

                # 保存图元图像，用于训练构件分类模型
                if crop_image_path is not None:
                    entity_save_path_by_class = os.path.join(entity_save_path, predict_class[i])
                    if not os.path.exists(entity_save_path_by_class):
                        os.makedirs(entity_save_path_by_class)
                    entity_img_name = 'layer_{}_{}.png'.format(layer, i)
                    entity_img_saved_path = os.path.join(entity_save_path_by_class, entity_img_name)
                    entity_img_pil = Image.fromarray(entity_image_list[i][:, :, ::-1])
                    entity_img_pil.save(entity_img_saved_path)

                if layer in ['chu_wei'] and drawing_type in [DrawingType.DECORATION_PLAN_LAYOUT]:
                    e_cnt = get_contour_from_bbox(bb)
                    heater_text = [txt for txt in border_text_info[TextType.ALL] if re.search('^热水器$', txt[-1])]
                    for txt in heater_text:
                        iou = get_contours_iou(e_cnt, get_contour_from_bbox(txt[:4]))
                        if iou > 0.7:
                            for room in kitchen_infos + balcony_room_infos:
                                if get_contours_iou(room[0], e_cnt) > 0.6 and get_contours_iou(e_cnt, room[0]) > 0:
                                    predict_class[i] = 'heater'
                                    break
        # 地下模型分类
        elif drawing_type in DrawingConfig.DRAWING_OPERATION_CONFIG.value['classify_underground']:  # 地下室模型，暂时分开训练
            start_time = time()
            predict_prob = tf_restful(entity_image_list,
                                      ClassifyConfig.MODEL_URL[export_env][ClassifyType.UNDERGROUND],
                                      ClassifyType.UNDERGROUND.value, expand='padding')

            print("[Note]模型前向时间:{:.2f} seconds".format(time() - start_time))

            predict_result = np.max(predict_prob, axis=1)
            predict_result_indx = np.argmax(predict_prob, axis=1)

            predict_class = [ClassifyConfig.MODEL_CLASS[ClassifyType.UNDERGROUND][i] for i in predict_result_indx]
            predict_result = np.array(predict_result)
            predict_class = np.array(predict_class)
            #             predict_class[predict_result<0.8] = 'others'
            predict_class = list(predict_class)

            truck_parking_text = border_text_info[TextType.TRUCK_PAKRING]
            print('truck parking text:{}'.format(truck_parking_text))
            for text_info in truck_parking_text:
                bbox = text_info[:4]
                debug_drawer.draw(cv2.rectangle, border_img_with_wall_copy, (bbox[0], bbox[1]), (bbox[2], bbox[3]),
                                  (0, 0, 255), 1)
                debug_drawer.draw(cv2.putText, border_img_with_wall_copy, 'truck', (bbox[0], bbox[1]),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # 根据先验知识校正识别结果
            all_origin_entity_class.extend(predict_class)
            for i in range(len(predict_class)):
                bb = entity_bbox_list[i]
                margin = ext_margin - 2 if ext_margin >= 2 else ext_margin
                long_side, short_side, long_ratio, short_ratio = get_side_ratio(bb, ratio, margin)
                if short_side == 0:
                    short_side = 1
                # 构件的引线文本
                annotation_text = str(annotation_list[i]) if annotation_list[i] else ''

                # 利用引线文本纠正集水坑
                if re.search("集水(坑|井)", annotation_text):
                    print("annotation_text", annotation_text)
                    predict_class[i] = "water_pit"
                    continue
                # 对误分类的车位进行矫正
                if layer == 'parking' and predict_class[i] == "others":
                    if short_side > int(PARKING_SHORT_SIDE_RANGE[0] * short_ratio):
                        predict_class[i] = "normal_parking"
                # 对于分类结果是others或水井 且图层在集水坑图层且在地下室平面图，结果置为集水坑
                elif predict_class[i] in ['others', 'shuijing'] and layer in ['water_pit'] and drawing_type.value in ["地下车库平面图"]:
                    predict_class[i] = 'water_pit'
                    # 如果集水坑尺寸不满足其尺寸范围 则置为others
                    if short_side < WATER_PIT_SIDE_RANGE[0] * long_ratio or long_side > WATER_PIT_SIDE_RANGE[1] * long_ratio:
                        predict_class[i] = 'others'
                # 对误分类为窗的管井门进行矫正
                if predict_class[i] == "window" and layer in ["door", "window"]:
                    layer_to_check = ['door', 'window']
                    class_to_check = ['Arc', 'Polyline', 'Polyline2d']
                    cabinet_line_dict = get_origin_border_entity_info(origin_border_entity_info, layer_to_check,
                                                                      class_to_check, space_scale, border_coord, ratio)
                    cabinet_line_list = []
                    for _, e_list in cabinet_line_dict.items():
                        cabinet_line_list.extend(e_list)
                    # Polyline中有arc，需要过滤
                    cabinet_line_list = list(filter(lambda x: len(x) == 8, cabinet_line_list))
                    arc_list = entity_in_bbox(cabinet_line_list, bb)
                    # 有两个圆弧且相交、角度小于50度
                    if len(arc_list) == 2:
                        if is_arc_connect(arc_list) and arc_list[0][-1] < 50 and arc_list[1][-1] < 50:
                            predict_class[i] = "guanjingmen"
                if predict_class[i] == 'fire_hydrants':
                    if layer not in ['fire_hydrant']:
                        predict_class[i] = 'others'
                # modify parking via size, othersp is intermediate class for entity changed from parking to others
                elif predict_class[i] in ['normal_parking', 'cd_parking', 'wza_cd_parking', 'wza_parking']:
                    if (
                            long_side < PARKING_CLS_LONG_SIDE_RANGE[0] * long_ratio
                            or short_side < PARKING_CLS_SHORT_SIDE_RANGE[0] * short_ratio
                            or long_side > PARKING_CLS_LONG_SIDE_RANGE[1] * long_ratio
                            or short_side > PARKING_CLS_SHORT_SIDE_RANGE[1] * short_ratio
                            or long_side / short_side > 4.5
                            or long_side > np.sqrt(np.power(PARKING_CLS_LONG_SIDE_RANGE[1], 2) +
                                                   np.power(PARKING_CLS_SHORT_SIDE_RANGE[1], 2)) * long_ratio
                    ):
                        # 门窗图层的误识别构件，满足电梯厢尺寸置为other，其他的置为door。
                        if layer in ['door', 'window', 'elevator_door']:
                            if (
                                    long_side > DOOR_SHORT_SIDE_RANGE[1] * long_ratio
                                    and short_side > DOOR_SHORT_SIDE_RANGE[1] * short_ratio
                                    and long_side / short_side < 1.2
                            ):
                                predict_class[i] = 'others_p'
                            else:
                                predict_class[i] = 'door'
                        else:
                            predict_class[i] = 'others_p'

                    # 将误识别为停车位的楼梯/电梯构件置为others
                    if layer in ['elevator_box']:
                        predict_class[i] = 'others_pp'

                # 将误识别为楼梯的小构件置为other
                elif predict_class[i] == 'louti':
                    if long_side < STAIR_SHORT_SIDE_RANGE[0] * long_ratio:
                        predict_class[i] = 'others'

                # 与地下规则判断无关的构件分类为others
                elif predict_class[i] in ['famen', 'juanlianmen', 'shuijing']:
                    predict_class[i] = 'others'

                # 被分类为门窗的非门层构件分类为others
                elif predict_class[i] in ['door', 'window', 'renfang_door', 'guanjingmen', 'menlianchuang']:
                    if layer not in ['door', 'window', 'elevator_door', 'emergency_door']:
                        # 停车位图层误识别为door的满足停车位尺寸的构件，矫正为停车位
                        if predict_class[i] in ['door'] and layer in ['parking']:
                            if (
                                    long_side < PARKING_CLS_LONG_SIDE_RANGE[0] * long_ratio
                                    or short_side < PARKING_CLS_SHORT_SIDE_RANGE[0] * short_ratio
                                    or long_side > PARKING_CLS_LONG_SIDE_RANGE[1] * long_ratio
                                    or short_side > PARKING_CLS_SHORT_SIDE_RANGE[1] * short_ratio
                                    or long_side / short_side > 4.5
                                    or long_side > np.sqrt(np.power(PARKING_CLS_LONG_SIDE_RANGE[1], 2) +
                                                           np.power(PARKING_CLS_SHORT_SIDE_RANGE[1], 2)) * long_ratio
                            ):
                                predict_class[i] = 'others_d'
                            else:
                                predict_class[i] = 'normal_parking'
                        else:
                            predict_class[i] = 'others_d'
                    # ['menlianchuang']在地下规则判断是与门同类
                    if predict_class[i] in ['menlianchuang']:
                        predict_class[i] = 'door'
                    # 将误识别为门的小构件置为管井门
                    elif predict_class[i] in ['door']:
                        if (long_side < DOOR_LONG_SIDE_RANGE[0] * long_ratio
                                and short_side < DOOR_SHORT_SIDE_RANGE[0] * short_ratio
                        ):
                            predict_class[i] = 'guanjingmen'
                        elif (short_side < GUANJINGMEN_SHORT_SIDE_RANGE[0] * short_ratio
                              or long_side > DOOR_LONG_SIDE_RANGE[1] * short_ratio
                              or short_side > DOOR_SHORT_SIDE_RANGE[1] * short_ratio
                        ):
                            predict_class[i] = 'others'

                    # 将误识别为管井门的构件置为others
                    elif predict_class[i] in ['guanjingmen']:
                        if short_side < GUANJINGMEN_SHORT_SIDE_RANGE[0] * short_ratio:
                            predict_class[i] = 'others'
                        elif DOOR_SHORT_SIDE_RANGE[0] * short_ratio < short_side < DOOR_SHORT_SIDE_RANGE[
                            1] * short_ratio:
                            predict_class[i] = 'door'

                elif predict_class[i] == 'gutter':
                    if long_side / short_side < 2 or layer != 'gutter':
                        predict_class[i] = 'others'
                # 分类模型误分类的电梯门通过是否在电梯井附近去除
                if predict_class[i] in ['elevator_door']:
                    # tuila_ext_bbox = extend_margin(bb, 50)
                    tuila_ext_bbox = extend_margin_by_side(bb, int(500 * ratio[0]))
                    tuila_ext_cnt = get_contour_from_bbox(tuila_ext_bbox)
                    is_door = False
                    for room_info in elevator_room_infos:
                        room_contour, room_box, room_name = room_info
                        if get_contours_iou(room_contour, tuila_ext_cnt) > 0:
                            is_door = True
                            break
                    if not is_door:
                        predict_class[i] = "others_d"
                # 分类误分为others的跟据图层和尺寸限制，以及电梯井空间来判断为电梯门
                if predict_class[i] == 'others' and layer in ["door", "window", "elevator_door"]:
                    length_d = point_euclidean_distance(bb[:2], bb[2:])
                    if 900 * short_ratio < length_d < 1500 * short_ratio:
                        # tuila_ext_bbox = extend_margin(bb, 50)
                        tuila_ext_bbox = extend_margin_by_side(bb, int(500 * ratio[0]))
                        tuila_ext_cnt = get_contour_from_bbox(tuila_ext_bbox)
                        for room_info in elevator_room_infos:
                            room_contour, room_box, room_name = room_info
                            if get_contours_iou(room_contour, tuila_ext_cnt) > 0:
                                predict_class[i] = 'elevator_door'
                                break

                # 人防门误识别
                if predict_class[i] == 'others' and layer in ["emergency_door"]:
                    text_info = border_text_info[TextType.ALL]
                    renfangmen_text_list = [text for text in text_info if re.search("人防门", text[-1])]
                    for renfangmen_text in renfangmen_text_list:
                        text_bbox = renfangmen_text[:4]
                        if Iou_temp(text_bbox, extend_margin(bb, 250)):
                            predict_class[i] = "renfang_door"
                            break

                # 卷帘门误分类为窗，进行矫正
                if predict_class[i] == 'window':
                    layer_to_check = ['door', 'window']
                    class_to_check = ['Line', 'Polyline', 'Polyline2d']
                    cabinet_line_dict = get_origin_border_entity_info(origin_border_entity_info, layer_to_check,
                                                                      class_to_check, space_scale, border_coord, ratio)
                    cabinet_line_list = []
                    for _, e_list in cabinet_line_dict.items():
                        cabinet_line_list.extend(e_list)
                    # Polyline中有arc，需要过滤
                    cabinet_line_list = list(filter(lambda x: len(x) == 4, cabinet_line_list))
                    cabinet_line_list = get_line_in_bbox(cabinet_line_list, bb)
                    # 只有一根线的窗户置为其他
                    if len(cabinet_line_list) == 1:
                        predict_class[i] = "others"
                    long_line = []
                    for line in cabinet_line_list:
                        if point_euclidean_distance(line[:2], line[2:]) > 500 * long_ratio:
                            long_line.append(line)
                    if len(long_line) == 4:
                        end_point = []
                        for line in long_line:
                            if line[0] == line[2]:
                                if line[1] > line[3]:
                                    end_point.append([line[0], line[1]])
                                else:
                                    end_point.append([line[0], line[3]])
                                end_point.sort(key=lambda x: x[0])
                            else:
                                if line[0] > line[2]:
                                    end_point.append([line[2], line[3]])
                                else:
                                    end_point.append([line[0], line[1]])
                                end_point.sort(key=lambda x: x[1])

                        dis1 = point_euclidean_distance(end_point[0], end_point[1])
                        dis2 = point_euclidean_distance(end_point[1], end_point[2])
                        dis3 = point_euclidean_distance(end_point[2], end_point[3])
                        print(dis1, dis2, dis3)
                        if abs(dis1 - dis3) < 2 and dis2 > dis1 * 5:
                            predict_class[i] = "juanlianmen"

                # 误分类成窗的卷帘门通过附近文本进行矫正
                if predict_class[i] == 'window':
                    ext_bbox = extend_margin(bb, 100)
                    ext_w_cnt = get_contour_from_bbox(ext_bbox)
                    JLM_text = [text_info for text_info in border_text_info[TextType.ALL] if
                                re.search('JL', text_info[4])]
                    for text in JLM_text:
                        if get_contours_iou(ext_w_cnt, get_contour_from_bbox(text[:4])) > 0:
                            predict_class[i] = 'juanlianmen'
                            break
                    RFM_text = [text_info for text_info in border_text_info[TextType.ALL] if
                                re.search('HM', text_info[4])]
                    for text in RFM_text:
                        if get_contours_iou(ext_w_cnt, get_contour_from_bbox(text[:4])) > 0:
                            predict_class[i] = 'renfang_door'
                            break

                # 人防门中只有两根平行等长的直线的置为密闭门
                if predict_class[i] == 'renfang_door':
                    layer_to_check = ['door', 'window']
                    class_to_check = ['Line', 'Polyline', 'Polyline2d']
                    cabinet_line_dict = get_origin_border_entity_info(origin_border_entity_info, layer_to_check,
                                                                      class_to_check, space_scale, border_coord, ratio)
                    cabinet_line_list = []
                    for _, e_list in cabinet_line_dict.items():
                        cabinet_line_list.extend(e_list)
                    # Polyline中有arc，需要过滤
                    cabinet_line_list = list(filter(lambda x: len(x) == 4, cabinet_line_list))
                    line_list = get_line_in_bbox(cabinet_line_list, bb)
                    if len(line_list) == 2:
                        if abs(point_euclidean_distance(line_list[0][:2], line_list[0][2:]) - point_euclidean_distance(line_list[1][:2], line_list[1][2:])) < 2:
                            if get_point_skew(line_list[0][:2], line_list[0][2:]) == get_point_skew(line_list[1][:2], line_list[1][2:]):
                                predict_class[i] = 'sealed_door'

                # ============================1230：构件细分类 ============================
                # 楼梯细分类逻辑：两个上和两个下为剪刀楼梯，一个上和一个下为双跑楼梯，一个上或一个下为直跑楼梯
                if predict_class[i] in ['louti']:
                    stair_text_1 = [text_info for text_info in border_text_info[TextType.ALL] if
                                    re.search('^上$', text_info[4].strip())]
                    stair_text_2 = [text_info for text_info in border_text_info[TextType.ALL] if
                                    re.search('^下$', text_info[4].strip())]
                    entity_bbox = extend_margin(bb, 100)
                    entity_cnt_ext = get_contour_from_bbox(entity_bbox)
                    temp_stair_text_1 = [text_info for text_info in stair_text_1 if
                                         get_contours_iou(entity_cnt_ext, get_contour_from_bbox(text_info[:4])) > 0.5]
                    temp_stair_text_2 = [text_info for text_info in stair_text_2 if
                                         get_contours_iou(entity_cnt_ext, get_contour_from_bbox(text_info[:4])) > 0.5]
                    if len(temp_stair_text_1) > 1 and len(temp_stair_text_2) > 1:
                        predict_class[i] = 'scissors_stair'
                    elif len(temp_stair_text_1) >= 1 or len(temp_stair_text_2) >= 1:
                        predict_class[i] = 'double_stair'
                    elif layer in ['stair', 'stair_dayang_plan_stair', 'stair_dayang_profile_stair']:
                        predict_class[i] = 'single_stair'
                    # 一种弯曲的疏散楼梯需要过滤掉
                    layer_to_check = ['elevator_stair', 'stair_dayang_plan_stair', 'stair_dayang_profile_stair']
                    class_to_check = ['Arc', 'Polyline', 'Polyline2d']
                    cabinet_line_dict = get_origin_border_entity_info(origin_border_entity_info,
                                                                      layer_to_check,
                                                                      class_to_check, space_scale,
                                                                      border_coord, ratio)
                    cabinet_line_list = []
                    for _, e_list in cabinet_line_dict.items():
                        cabinet_line_list.extend(e_list)
                    cabinet_line_list = list(filter(lambda x: len(x) == 8, cabinet_line_list))
                    cabinet_line_list = get_line_in_bbox(cabinet_line_list, bb)
                    if len(cabinet_line_list) == 2:
                        print(abs(cabinet_line_list[0][-1] - cabinet_line_list[1][-1]))
                        if abs(cabinet_line_list[0][-1] - cabinet_line_list[1][-1]) > 10:
                            predict_class[i] = 'others_l'

                # 保存图元图像，用于训练构件分类模型
                if crop_image_path is not None:
                    entity_save_path_by_class = os.path.join(entity_save_path, predict_class[i])
                    if not os.path.exists(entity_save_path_by_class):
                        os.makedirs(entity_save_path_by_class)
                    entity_img_name = 'layer_{}_{}.png'.format(layer, i)
                    entity_img_saved_path = os.path.join(entity_save_path_by_class, entity_img_name)
                    entity_img_pil = Image.fromarray(entity_image_list[i][:, :, ::-1])
                    entity_img_pil.save(entity_img_saved_path)

            if layer == 'parking':
                parking_start_time = time()
                parking_bbox_coord = {
                    'regular_parking_coord': [],
                    'lean_parking_coord': []
                }
                num_bbox = len(predict_class)
                parking_bboxes = [entity_bbox_list[i] for i in range(num_bbox)
                                  if predict_class[i] in ['cd_parking', 'normal_parking',
                                                          'wza_cd_parking', 'wza_parking']]

                if len(parking_bboxes) > 0:
                    raw_parking_lines = get_line_entity_info(border_entity_info, ['parking'])
                    # 找出普通车位或倾斜车位的四个顶点坐标(按照顺时针排序)
                    parking_coords, parking_types = get_leanParking_coord(
                        parking_bboxes, raw_parking_lines, border_size, ratio)
                    for parking_bbox, parking_coord, parking_type in zip(
                            parking_bboxes, parking_coords, parking_types):
                        true_parking_bbox = remove_margin(parking_bbox, ext_margin)
                        # 矫正失败的车位，加入regular parking
                        if parking_coord is None:
                            parking_bbox_coord['regular_parking_coord'].append(
                                [get_bbox_coord_by_order(true_parking_bbox),
                                 true_parking_bbox])
                            continue
                        # 判断是否为货车位，根据车位rect中是否包括"货"字样
                        parking_cnt = np.expand_dims(np.array(parking_coord), axis=1)
                        for text_info in truck_parking_text:
                            text_cnt = get_contour_from_bbox(text_info[:4])
                            if get_contours_iou(parking_cnt, text_cnt) > 0.8:
                                predict_class[i] = 'truck_parking'
                                break
                        # 放进parking_bbox_coord字典
                        if parking_type == 'regular':
                            parking_bbox_coord['regular_parking_coord'].append(
                                [parking_coord, true_parking_bbox])
                        elif parking_type == 'lean':
                            parking_bbox_coord['lean_parking_coord'].append(
                                [parking_coord, true_parking_bbox])
                        else:
                            print("车位bbox: {}矫正失败".format(parking_bbox))

                print('[Note] Time for get parking coord:{:.2f} 秒'.format(
                    time() - parking_start_time))
                print('[Note] 普通车位数量: {}\t 倾斜车位数量: {}'.format(
                    len(parking_bbox_coord['regular_parking_coord']),
                    len(parking_bbox_coord['lean_parking_coord'])))

                border_entity_info['parking_bbox_coord'] = parking_bbox_coord

            elif layer == 'gutter':
                # 用排水沟图元合并出的bbox中，若被分类成gutter以外的类别，全部换成others
                for i in range(len(predict_class)):
                    if predict_class[i] != 'gutter':
                        predict_class[i] = 'others'
            # TODO 如果有需要的话，完善其他类型图纸的分类模型
        else:
            raise Exception('unsupported drawing type for classification:{}'.format(drawing_type))

        border_entity_info['entity_class_dict'][layer] = predict_class
        border_entity_info['entity_score_dict'][layer] = predict_result

    all_entity_bbox = []
    all_entity_class = []
    all_entity_score = []
    for layer, value in entity_bbox_dict.items():
        if layer in LayerConfig.CLASSIFICATION_EXCLUDE_LAYERS.value + LayerConfig.LAYERS_WITH_SLOPE_LINE_REVISED.value + \
                LayerConfig.DASH_LINE_REVISED.value + ['door_intersect_bboxes', 'door_combine_bbox']:
            continue
        all_entity_bbox.extend(value)
        all_entity_class.extend(border_entity_info['entity_class_dict'][layer])
        all_entity_score.extend(border_entity_info['entity_score_dict'][layer])

    if drawing_type in [DrawingType.DECORATION_PLAN_LAYOUT,]:
        # 通过电梯厢、电梯空间判断电梯门
        elevator_bbox_list = [all_entity_bbox[i] for i in range(len(all_entity_class))
                              if all_entity_class[i] == 'elevator_box']
        for i in range(len(all_entity_class)):
            if all_entity_class[i] in ['tuila_door']:
                bb = all_entity_bbox[i]
                elv_door_center = [(bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2]
                # 对异常推拉门进行过滤
                long_side, short_side, long_ratio, short_ratio = get_side_ratio(bb, ratio, ext_margin)
                if short_side <= TUILA_DOOR_SHORT_SIDE_RANGE[0] * short_ratio or long_side <= TUILA_DOOR_LONG_SIDE_RANGE[0] * long_ratio:
                    all_entity_class[i] = 'others_tl'
                # 通过电梯厢，判定电梯门
                for elevator_bbox in elevator_bbox_list:
                    elv_box_center = [(elevator_bbox[0] + elevator_bbox[2]) / 2,
                                      (elevator_bbox[1] + elevator_bbox[3]) / 2]
                    if point_euclidean_distance(elv_door_center, elv_box_center) < ELEVATOR_GAP_RANGE[0] * long_ratio:
                        all_entity_class[i] = 'elevator_door'
                        break
                # 通过电梯空间，判定电梯门
                entity_coord = get_contour_from_bbox(bb)
                for room_info in elevator_room_infos:
                    room_contour, room_box, room_name = room_info
                    if get_contours_iou(room_contour, entity_coord):
                        all_entity_class[i] = 'elevator_door'
                        break

        # visualize the result image with classification result
        # L折线形阳台边沿包住空调，可能会被分累为空调，通过遍历和空调构件计算Iou进筛选过滤
        air_conditioner_bbox_list = [all_entity_bbox[i] for i in range(len(all_entity_class)) if
                                     all_entity_class[i] in ['air_conditioner_ins', 'air_conditioner_out']]
        if len(air_conditioner_bbox_list) != 0:
            for i in range(len(all_entity_class)):
                bbox = all_entity_bbox[i]
                check_list = air_conditioner_bbox_list
                if all_entity_class[i] in ['air_conditioner_ins', 'air_conditioner_out']:
                    check_list = [i for i in air_conditioner_bbox_list if i != bbox]
                iou1, iou2 = calculate_iou(np.array(check_list), np.array([bbox]))
                if iou2 is None:
                    continue
                if np.max(iou2, axis=0)[0] >= 0.8 and \
                        all_entity_class[i] not in ['scissors_stair', 'elevator_box', 'door', "window"]:
                    all_entity_class[i] = 'others_w'

        # 洗衣机地漏: 地漏外扩1m找洗衣机，若有，则为洗衣机地漏
        washer_bbox_list = [all_entity_bbox[i] for i in range(len(all_entity_class)) if all_entity_class[i] == 'washer']
        if len(washer_bbox_list) != 0:
            for i in range(len(all_entity_class)):
                if all_entity_class[i] == 'dilou':
                    ext_bbox = extend_margin(all_entity_bbox[i], margin=1000 * ratio[0])
                    if any(Iou_temp(washer_bb, ext_bbox) > 0.5 for washer_bb in washer_bbox_list):
                        all_entity_class[i] = 'dilou_washmachine'

    # 空调外机边上分类为窗的，窗的一侧为空调外机，一侧为室外空间的置为栏杆
    win_index = []
    air_index = []
    cor_win_index = []
    for i, tmp in enumerate(all_entity_class):
        if tmp == "window":
            win_index.append(i)
        elif tmp == "air_conditioner_out":
            air_index.append(i)
        elif tmp == "corner_window":
            cor_win_index.append(i)
    for i in win_index:
        w_bbox = all_entity_bbox[i]
        if point_euclidean_distance([w_bbox[0], w_bbox[1]], [w_bbox[2], w_bbox[1]]) > point_euclidean_distance([w_bbox[0], w_bbox[1]], [w_bbox[0], w_bbox[3]]):
            u_ext_bbox = [w_bbox[0], w_bbox[1] - 60, w_bbox[2], w_bbox[1]]
            d_ext_bbox = [w_bbox[0], w_bbox[3], w_bbox[2], w_bbox[3] + 60]
        else:
            u_ext_bbox = [w_bbox[0] - 60, w_bbox[1], w_bbox[0], w_bbox[3]]
            d_ext_bbox = [w_bbox[2], w_bbox[1], w_bbox[2] + 60, w_bbox[3]]
        u_ext_cnt = get_contour_from_bbox(u_ext_bbox)
        d_ext_cnt = get_contour_from_bbox(d_ext_bbox)
        inter_room = False
        for j in air_index:
            a_bbox = all_entity_bbox[j]
            a_cnt = get_contour_from_bbox(a_bbox)
            if get_contours_iou(u_ext_cnt, a_cnt) > 0.5:
                for room_info in room_infos:
                    room_contour, room_box, room_name = room_info
                    if get_contours_iou(room_contour, d_ext_cnt) > 0:
                        inter_room = True
                        break
                if not inter_room:
                    # 碧桂园图纸有空调外机之外是窗户的情况，暂时将该矫正注释掉
                    # all_entity_class[i] = "other_langan"
                    pass
                else:
                    break
            elif get_contours_iou(d_ext_cnt, a_cnt) > 0.5:
                for room_info in room_infos:
                    room_contour, room_box, room_name = room_info
                    if get_contours_iou(room_contour, u_ext_cnt) > 0:
                        inter_room = True
                        break
                if not inter_room:
                    # 碧桂园图纸有空调外机之外是窗户的情况，暂时将该矫正注释掉
                    # all_entity_class[i] = "other_langan"
                    pass
                else:
                    break
    # 包含空调外机的转角窗置为其他
    for i in cor_win_index:
        c_w_bbox = all_entity_bbox[i]
        c_w_cnt = get_contour_from_bbox(c_w_bbox)
        for j in air_index:
            a_bbox = all_entity_bbox[j]
            a_cnt = get_contour_from_bbox(a_bbox)
            if get_contours_iou(c_w_cnt, a_cnt) > 0.7:
                all_entity_class[i] = "other_l"
                break

    # 由于空间分割导致同一空间内有多个空调内机，根据尺寸，将尺寸较大的分为空调外机
    air_ins_ind = [i for i in range(len(all_entity_class)) if all_entity_class[i] == "air_conditioner_ins"]
    for room in air_room_infos:
        room_cnt, room_bbox, room_name = room
        air_ind = []
        for i in air_ins_ind:
            if get_contours_iou(room_cnt, get_contour_from_bbox(all_entity_bbox[i])) > 0.3:
                air_ind.append(i)
        if len(air_ind) > 1:
            air_ind_length = []
            for j in air_ind:
                bbox = all_entity_bbox[j]
                long_length = max(bbox[2] - bbox[0], bbox[3] - bbox[1])
                air_ind_length.append([j, long_length])
            air_ind_length.sort(key=lambda x: x[1])
            mid_length = (air_ind_length[-1][1] - air_ind_length[0][1]) / 2
            for air in air_ind_length:
                ind, length = air
                if length > mid_length:
                    all_entity_class[ind] = "air_conditioner_out"

    ###################对于将双跑和剪刀楼梯合并分成单跑的，需要进行重新合并，根据在同一空间进行合并#################
    index_stair = []
    for i, cls in enumerate(all_entity_class):
        if cls in ["single_stair", "double_stair", "scissors_stair"]:
            index_stair.append(i)
    print("index_stair: ", index_stair)
    for room_info in room_infos:
        room_contour, room_box, room_name = room_info
        c_stair = []
        c_bbox = []
        for j in index_stair:
            if get_contours_iou(room_contour, get_contour_from_bbox(all_entity_bbox[j])) > 0.5 and \
                    get_contours_iou(get_contour_from_bbox(all_entity_bbox[j]), room_contour) > 0.3:  # 画图issue开放式的空间不应合并楼梯，添加楼梯占空间比例阈值

                c_stair.append(j)
                c_bbox.append(all_entity_bbox[j])
        if len(c_stair) > 1:
            x = []
            y = []
            for bbox in c_bbox:
                x.append(bbox[0])
                x.append(bbox[2])
                y.append(bbox[1])
                y.append(bbox[3])
            xmin = min(x)
            xmax = max(x)
            ymin = min(y)
            ymax = max(y)
            new_bbox = [xmin, ymin, xmax, ymax]
            stair_text_1 = [text_info for text_info in border_text_info[TextType.ALL] if
                            re.search('^上$', text_info[4].strip())]
            stair_text_2 = [text_info for text_info in border_text_info[TextType.ALL] if
                            re.search('^下$', text_info[4].strip())]
            entity_bbox = extend_margin(new_bbox, 100)
            entity_cnt_ext = get_contour_from_bbox(entity_bbox)
            temp_stair_text_1 = [text_info for text_info in stair_text_1 if
                                 get_contours_iou(entity_cnt_ext, get_contour_from_bbox(text_info[:4])) > 0.5]
            temp_stair_text_2 = [text_info for text_info in stair_text_2 if
                                 get_contours_iou(entity_cnt_ext, get_contour_from_bbox(text_info[:4])) > 0.5]
            if len(temp_stair_text_1) > 1 and len(temp_stair_text_2) > 1:
                all_entity_class[c_stair[0]] = 'scissors_stair'
            elif len(temp_stair_text_1) >= 1 or len(temp_stair_text_2) >= 1:
                all_entity_class[c_stair[0]] = 'double_stair'
            all_entity_bbox[c_stair[0]] = new_bbox
            for k in c_stair[1:]:
                all_entity_class[k] = "others"
    # 获取其他门、其他窗
    for i in range(len(all_entity_class)):
        if all_entity_class[i] in ['door', 'elevator_door', 'tuila_door', 'sealed_door', 'juanlianmen']:
            all_entity_class.append('other_door')
            all_entity_bbox.append(all_entity_bbox[i])
            all_origin_entity_class.append(all_origin_entity_class[i])
            all_entity_score.append(all_entity_score[i])
            entity_annotation_list.append(entity_annotation_list[i])
        elif all_entity_class[i] in ['window', 'corner_window', 'tuchuang', 'baiye', 'elevation_window',
                                     'limianchuang']:
            all_entity_class.append('other_window')
            all_entity_bbox.append(all_entity_bbox[i])
            all_origin_entity_class.append(all_origin_entity_class[i])
            all_entity_score.append(all_entity_score[i])
            entity_annotation_list.append(entity_annotation_list[i])

    # 分类成洗衣机的热水器、热水箱进行矫正
    boiler_text_info_list = [txt for txt in border_text_info[TextType.ALL] if re.search('^热水器$|^热水箱$', txt[4])]
    for i in range(len(all_entity_class)):
        if all_entity_class[i] in ['washer']:
            bbox_washer = all_entity_bbox[i]
            for txt in boiler_text_info_list:
                if Iou_temp(txt[:4], bbox_washer) > 0.5:
                    all_entity_class[i] = 'others_washer'
                    break

    # 折线窗误分类成推拉门，通过短边长度进行矫正
    tuila_door_max_len_pix = int(300 * ratio[0])
    for i in range(len(all_entity_class)):
        if all_entity_class[i] in ['tuila_door']:
            bbox_door = all_entity_bbox[i]
            # 对于倾斜的推拉门，通过bbox获取的长宽不是实际的长宽
            # 不能用尺寸去过滤
            # 根据门的土建连线判断门是否倾斜
            is_oblique = False
            bbox_door_base_coord_list = entity_in_bbox(door_base_coords, extend_margin(bbox_door,  2 * ext_margin))
            if len(bbox_door_base_coord_list) == 1:
                door_base_coord = bbox_door_base_coord_list[0]
                if not abs(door_base_coord[0]-door_base_coord[2]) < 3 and not abs(door_base_coord[1]-door_base_coord[3]) < 3:
                    is_oblique = True
            if is_oblique: continue
            bbox_door = remove_margin(bbox_door, ext_margin)
            short_len = min((bbox_door[2] - bbox_door[0]), (bbox_door[3] - bbox_door[1]))
            if short_len > tuila_door_max_len_pix:
                all_entity_class[i] = 'others_tuila'

    # 平开门短边如果小于650，置为管井门，因为单扇平开门最小的是卫生间门，宽度750。阈值取的稍微小一点
    pingkaimen_min_len_pix = int(650 * ratio[0])
    for i in range(len(all_entity_class)):
        if all_entity_class[i] in ['door']:
            bbox_door = all_entity_bbox[i]
            short_len = min((bbox_door[2] - bbox_door[0]), (bbox_door[3] - bbox_door[1]))
            if short_len < pingkaimen_min_len_pix:
                all_entity_class[i] = 'guanjingmen'

    # 误识别的便器，通过最大长度进行矫正，便器的最小宽度一般大于300
    bianqi_max_len_pix = int(400 * ratio[0])
    for i in range(len(all_entity_class)):
        if all_entity_class[i] in ['closestool', 'toilet']:
            bbox_toilet = all_entity_bbox[i]
            long_len = max((bbox_toilet[2] - bbox_toilet[0]), (bbox_toilet[3] - bbox_toilet[1]))
            if long_len < bianqi_max_len_pix:
                all_entity_class[i] = 'others_toilet'

    # 误识别的洗衣机，通过长边和短边的长度差值是否大于150mm，矫正成others
    len_diff_max_pix = int(150 * ratio[0])
    for i in range(len(all_entity_class)):
        if all_entity_class[i] in ['washer']:
            bbox_washer = all_entity_bbox[i]
            height_washer = bbox_washer[3] - bbox_washer[1]
            width_washer = bbox_washer[2] - bbox_washer[0]
            if abs(height_washer - width_washer) > len_diff_max_pix:
                all_entity_class[i] = 'others_washer'
    
    # 根据引线生成孔洞
    hole_shape = [int(300*ratio[0]), int(300*ratio[0])]
    for branch_text_obj in main_branch_text_list:
        generate_result = generate_entity_by_annotation(branch_text_obj, ['P','p'], 'reserved_hole', hole_shape)
        entity_box, entity_class, origin_entity_class, entity_score, entity_annotation_list_ = generate_result
        all_entity_bbox.extend(entity_box)
        all_entity_class.extend(entity_class)
        all_origin_entity_class.extend(origin_entity_class)
        all_entity_score.extend(entity_score)
        entity_annotation_list.extend(entity_annotation_list_)

    all_detect_class = border_entity_info.get('entity_class_list_detection', [])
    # 根据引线添加热水器构件
    if "heater" not in all_detect_class:
        heater_shape = [int(200*ratio[0]), int(400*ratio[0])]
        for branch_text_obj in main_branch_text_list:
            generate_result = generate_entity_by_annotation(branch_text_obj, ['热水器'], 'heater', heater_shape)
            entity_box, entity_class, origin_entity_class, entity_score, entity_annotation_list_ = generate_result
            if len(entity_box) == 1:
                entity_contour = get_contour_from_bbox(entity_box[0])
                for room in kitchen_infos + balcony_room_infos:
                    if get_contours_iou(room[0], entity_contour) > 0.6 and get_contours_iou(entity_contour, room[0]) > 0:
                        all_entity_bbox.extend(entity_box)
                        all_entity_class.extend(entity_class)
                        all_origin_entity_class.extend(origin_entity_class)
                        all_entity_score.extend(entity_score)
                        entity_annotation_list.extend(entity_annotation_list_)
            else:
                all_entity_bbox.extend(entity_box)
                all_entity_class.extend(entity_class)
                all_origin_entity_class.extend(origin_entity_class)
                all_entity_score.extend(entity_score)
                entity_annotation_list.extend(entity_annotation_list_)

    # 根据引线添加燃气表构件
    if "gas_meter" not in all_detect_class:
        heater_shape = [int(200*ratio[0]), int(350*ratio[0])]
        for branch_text_obj in main_branch_text_list:
            generate_result = generate_entity_by_annotation(branch_text_obj, ['燃气表', "煤气表"], 'gas_meter', heater_shape)
            entity_box, entity_class, origin_entity_class, entity_score, entity_annotation_list_ = generate_result
            all_entity_bbox.extend(entity_box)
            all_entity_class.extend(entity_class)
            all_origin_entity_class.extend(origin_entity_class)
            all_entity_score.extend(entity_score)
            entity_annotation_list.extend(entity_annotation_list_)

    # 因为从检测模块得到的置信度不满足要求的bbox, 放在entity_detection_bboxes里面继续进行再次分类;
    # 而正常走合并模型之后也会生成可能包含构件的bbox，这两部分的产生的bbox会重叠导致识别结果重复;
    # 因此需要根据分类模型的置信度将重合的置信度较低的bbox剔除
    all_entity_class, all_origin_entity_class, all_entity_bbox, all_entity_score = remove_duplicate_bbox(all_entity_class,
                                                                                                         all_origin_entity_class,
                                                                                                         all_entity_bbox,
                                                                                                         all_entity_score)

    # visualize the result image with classification result
    for cls, ori_cls, bbox, score in zip(all_entity_class, all_origin_entity_class, all_entity_bbox, all_entity_score):
        # ori_box = remove_margin(bbox, ext_margin)
        # debug_drawer.draw(cv2.rectangle, border_img_with_wall_copy, (ori_box[0], ori_box[1]), (ori_box[2], ori_box[3]), (0, 180, 255), 1)
        if cls in ["other_door", "other_window"]: continue
        debug_drawer.draw(cv2.rectangle, border_img_with_wall_copy, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 0, 255),
                          1)
        debug_drawer.draw(cv2.putText, border_img_with_wall_copy, '{} {:.2f}'.format(cls, score),
                          (bbox[0], bbox[1] - 5),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
        debug_drawer.draw(cv2.putText, border_img_with_wall_copy, '{} '.format(ori_cls), (bbox[2], bbox[3] - 5),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 9), 1)
    entity_CAD_coord_list = list(
        map(lambda bboxes: convert_bbox_to_CAD_coord(border_coord, bboxes, ratio), all_entity_bbox))

    # 在保存构件的bbox之前先去除margin
    all_entity_bbox = [remove_margin(bbox, ext_margin) for bbox in all_entity_bbox]

    border_entity_info['entity_bbox_list'] = all_entity_bbox
    border_entity_info['entity_class_list'] = all_entity_class
    border_entity_info['entity_ori_class_list'] = all_origin_entity_class
    border_entity_info['entity_score_list'] = all_entity_score
    border_entity_info['entity_coord_list'] = entity_CAD_coord_list
    border_entity_info['entity_annotation_list'] = entity_annotation_list

    add_detection_result(border_entity_info)

    # 去掉分图层打印的图像，减少内存占用及变量传输成本
    image_manager.remove(IMG_ENTITY_CLEAR_1_KEY)
    image_manager.remove(IMG_ENTITY_CLEAR_2_KEY)

    # 保存中间结果
    img_path_temp = os.path.join(result_path, border_name)

    if rule_index is None:
        save_name = '{}_{}_{}'.format(img_path_temp, drawing_type.value, IMAGE_PRINT_EXTENSION[4])
    else:
        save_name = '{}_{}_rule_{}_{}'.format(img_path_temp, drawing_type.value, rule_index, IMAGE_PRINT_EXTENSION[4])

    debug_drawer.save_to(border_img_with_wall_copy, save_name)
    # 将目标结果保存到image manager
    if SAVE_RECOG_GEN_IMG_ONLINE:
        image_manager.load_to_manager(IMG_CLS_RESULT, debug_drawer.get_copy(border_img_with_wall_copy))
        # for debug
        # cls = image_manager.load_from_manager(IMG_CLS_RESULT)
        # cv2.imwrite("/Users/xuan.ma/Desktop/cls.png", cls)

    return border_entity_info


def generate_entity_by_annotation(branch_text_obj, label_text_list, entity_name, entity_shape):
    """[summary]

    Args:
        branch_text_obj ([list]): [引注文本对象]
        label_text ([list]): [寻找的标注]
        entity_name ([string]): [对象类别]
    
    return:
    
    """
    entity_box = []
    entity_class = []
    origin_entity_class = []
    entity_score = []
    entity_annotation_list = []
    
    w,h = entity_shape
    
    main_branch, main_end, branch, anno_text_list = branch_text_obj
    # 引线点集
    branch_points = [main_end]
    for i in branch:
        if len(i) != 4:
            continue
        branch_points.append(i[:2])
        branch_points.append(i[2:])
    for anno_text in anno_text_list:
        if not any([re.search(label_text, anno_text[3]) for label_text in label_text_list]):
            continue
        print(f'find entity {entity_name} by annotation text {anno_text[3]}')
        anno_point = np.array(anno_text[2])
        # 从引线点集中寻找距离文本最远的点作为构件生成的中心点
        max_distance = -1
        center_p = None
        for branch_point in branch_points:
            branch_dist = np.linalg.norm(anno_point- np.array(branch_point))
            if branch_dist > max_distance:
                max_distance = branch_dist
                center_p = branch_point
        x1,y1 = center_p - np.array([w//2, h//2])
        x2,y2 = center_p + np.array([w//2, h//2])
        entity_box.append([x1,y1,x2,y2])
        entity_class.append(entity_name)
        origin_entity_class.append('bygenerate')
        entity_score.append(1)
        entity_annotation_list.append(anno_text[3])
        
    return entity_box, entity_class, origin_entity_class, entity_score, entity_annotation_list


@timer('entity_classification')
def add_detection_result(border_entity_info):
    # 检测、分类结果合并
    all_classify_bbox = border_entity_info.get('entity_bbox_list', [])
    print("all_classify_bbox", len(all_classify_bbox))
    all_classify_class = border_entity_info.get('entity_class_list', [])
    print("all_classify_class", len(all_classify_class))
    all_classify_origin_class = border_entity_info.get('entity_ori_class_list', [])
    all_classify_score = border_entity_info.get('entity_score_list', [])
    all_classify_cad_coord = border_entity_info.get('entity_coord_list', [])
    all_classify_annotation = border_entity_info.get('entity_annotation_list', [])

    all_detect_bbox = border_entity_info.get('entity_bbox_list_detection', [])
    all_detect_class = border_entity_info.get('entity_class_list_detection', [])
    all_detect_origin_class = border_entity_info.get('entity_ori_class_list_detection', [])
    all_detect_score = border_entity_info.get('entity_score_list_detection', [])
    all_detect_cad_coord = border_entity_info.get('entity_coord_list_detection', [])
    all_detect_annotation = border_entity_info.get('entity_annotation_list_detection', [])
    detect_num = len(all_detect_bbox)
    classify_num = len(all_classify_bbox)
    for i in range(detect_num):
        never_exist = True
        for j in range(classify_num):
            # 如果分类结果是others，不需要再去尝试刷新检测的结果
            if all_classify_class[j].startswith("others"): continue
            if Iou_temp(all_detect_bbox[i], all_classify_bbox[j]) >= 0.6:     # 暂定阈值0.6
                if all_detect_class[i] == all_classify_class[j]:
                    never_exist = False
                    if all_detect_score[i] > all_classify_score[j]:
                        # 通过置信度判定，以置信度高的为当前框内的分类结果
                        all_classify_bbox[j] = all_detect_bbox[i]
                        all_classify_class[j] = all_detect_class[i]
                        all_classify_origin_class[j] = all_detect_origin_class[i]
                        all_classify_score[j] = all_detect_score[i]
                        all_classify_cad_coord[j] = all_detect_cad_coord[i]
                        all_classify_annotation[j] = all_detect_annotation[i]
                    break

        if never_exist:
            all_classify_bbox.append(all_detect_bbox[i])
            all_classify_class.append(all_detect_class[i])
            all_classify_origin_class.append(all_detect_origin_class[i])
            all_classify_score.append(all_detect_score[i])
            all_classify_cad_coord.append(all_detect_cad_coord[i])
            all_classify_annotation.append(all_detect_annotation[i])
    if 'entity_bbox_list_detection' in border_entity_info:
        border_entity_info.pop('entity_bbox_list_detection')
    if 'entity_class_list_detection' in border_entity_info:
        border_entity_info.pop('entity_class_list_detection')
    if 'entity_ori_class_list_detection' in border_entity_info:
        border_entity_info.pop('entity_ori_class_list_detection')
    if 'entity_score_list_detection' in border_entity_info:
        border_entity_info.pop('entity_score_list_detection')
    if 'entity_coord_list_detection' in border_entity_info:
        border_entity_info.pop('entity_coord_list_detection')
    if 'entity_annotation_list_detection' in border_entity_info:
        border_entity_info.pop('entity_annotation_list_detection')

def remove_duplicate_bbox(all_entity_class, all_origin_entity_class, all_entity_bbox, all_entity_score, iou_thre = 0.6):
    """
    根据IOU和置信度将同一构件重复bbox去重，保留置信度较大的bbox作为构件最终的bbox
    """
    print("bbox数量：", len(all_entity_bbox))
    # print("kitchen_exhaust_pipe数量：", len([entity_class for entity_class in all_entity_class if entity_class in ["kitchen_exhaust_pipe"]]))
    remove_idxs_set = set()
    for i in range(len(all_entity_bbox)):
        if i in remove_idxs_set: continue
        cls_i = all_entity_class[i]
        # if cls_i not in ["kitchen_exhaust_pipe"]: continue
        bbox_i = all_entity_bbox[i]
        score_i = all_entity_score[i]
        for j in range(i+1, len(all_entity_bbox)):
            if j in remove_idxs_set: continue
            cls_j = all_entity_class[j]
            # if cls_i not in ["kitchen_exhaust_pipe"]: continue
            bbox_j = all_entity_bbox[j]
            score_j = all_entity_score[j]
            if cls_i == cls_j and Iou_temp(bbox_j, bbox_i) > 0.6:
                if score_j > score_i:
                    score_i = score_j
                    bbox_i = bbox_j
                    remove_idxs_set.add(j)
                    all_entity_bbox[i], all_entity_bbox[j] = all_entity_bbox[j], all_entity_bbox[i]
                    all_entity_class[i], all_entity_class[j] = all_entity_class[j], all_entity_class[i]
                    all_origin_entity_class[i], all_origin_entity_class[j] = all_origin_entity_class[j], all_origin_entity_class[i]
                    all_entity_score[i], all_entity_score[j] = all_entity_score[j], all_entity_score[i]
                else:
                    remove_idxs_set.add(j)
    print("remove_idxs_set ", remove_idxs_set)
    all_entity_bbox = [all_entity_bbox[idx] for idx in range(len(all_entity_bbox)) if idx not in remove_idxs_set]
    all_entity_class = [all_entity_class[idx] for idx in range(len(all_entity_class)) if idx not in remove_idxs_set]
    all_origin_entity_class = [all_origin_entity_class[idx] for idx in range(len(all_origin_entity_class)) if idx not in remove_idxs_set]
    all_entity_score = [all_entity_score[idx] for idx in range(len(all_entity_score)) if idx not in remove_idxs_set]
    # print("kitchen_exhaust_pipe数量：",
    #       len([entity_class for entity_class in all_entity_class if entity_class in ["kitchen_exhaust_pipe"]]))
    print("去重之后bbox数量：", len(all_entity_bbox))
    return all_entity_class, all_origin_entity_class, all_entity_bbox, all_entity_score