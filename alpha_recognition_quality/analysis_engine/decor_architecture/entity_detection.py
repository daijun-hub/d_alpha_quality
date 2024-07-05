import gc
import os
from time import time

from PIL import Image
import numpy as np
import cv2

from ...config import env as export_env
from ...config_manager.decor_architecture.detect_config import DetectType, DetectConfig
from ...config_manager.text_config import TextType
from ...config import DEBUG_MODEL, SAVE_RECOG_GEN_IMG_ONLINE

from ...common.utils import *
from ...common.utils_draw_and_rule import *
from ...common.CONSTANTS import IMAGE_PRINT_EXTENSION
from ...common.decorator import timer

from ..utils.utils_classification import *
from ..utils.utils_analysis_common import *
from ..utils.utils_detection import *
from ..CONSTANTS import *
from ..model_service.detection_client import tf_restful_detection

from ...common.debug_image_drawer import DebugImageDrawer
from ...common.image_manager import ImageManager
from ...config_manager.decor_architecture.drawing_config import DrawingType as decor_architecture_drawing_type


@timer('entity_detection')
def run(border_name, border_entity_info, result_path, drawing_type, rule_index=None):
    """
    构件分类

    :param border_name: 图框序号，例如 Model_0
    :param border_entity_info: 图框构件信息
    :param result_path: 中间结果保存路径
    :param drawing_type: 图框类型
    :param rule_index: 规则序号，为None 表示按照图纸类型粒度来运行，如果不为None，表示按照规则粒度来运行
    :return: 补充信息的 border_entity_info
    """
    entity_bbox_dict = border_entity_info.get('entity_bbox_dict', {})
    entity_bbox_dict['entity_detection_bboxes'] = []

    kitchen_images_list = []
    kitchen_bbox_list = []
    washroom_images_list = []
    washroom_bbox_list = []
    balcony_images_list = []
    balcony_bbox_list = []
    livingroom_images_list = []
    livingroom_bbox_list = []
    bedroom_images_list = []
    bedroom_bbox_list = []
    shufang_images_list = []
    shufang_bbox_list = []

    limian_kitchen_images_list = []
    limian_kitchen_bbox_list = []
    limian_washroom_images_list = []
    limian_washroom_bbox_list = []

    image_manager = border_entity_info['image_manager']
    img_copy = image_manager.load_from_manager(IMG_WITH_WALL_KEY)
    debug_drawer = DebugImageDrawer(image_manager)
    border_img_with_wall_copy = debug_drawer.create_copy(IMG_WITH_WALL_KEY)
    border_image_entity_clear_3 = image_manager.load_from_manager(IMG_ENTITY_CLEAR_3_KEY)
    border_image_entity_clear_4 = image_manager.load_from_manager(IMG_ENTITY_CLEAR_4_KEY)
    border_coord = border_entity_info['border_coord']
    ratio = border_entity_info['ratio']
    ext_margin = border_entity_info['ext_margin']
    border_text_info = border_entity_info['border_text_info']
    boiler_text_info_list = [txt for txt in border_text_info[TextType.ALL] if re.search('^热水器$|^热水箱$', txt[4])]
    scale = border_entity_info["space_scale"]
    origin_border_entity_info = border_entity_info["origin_border_entity_info"]
    main_branch_text_list = border_entity_info.get("main_branch_text_list", [])

    if border_image_entity_clear_3 is None:
        print('border_image_entity_clear_3 not exists !!!')
        return border_entity_info

    img_entity_clear_3 = border_image_entity_clear_3.copy()
    del border_image_entity_clear_3
    gc.collect()

    if border_image_entity_clear_4 is None:
        print('border_image_entity_clear_5 not exists !!!')
        return border_entity_info
    img_entity_clear_4 = border_image_entity_clear_4.copy()
    del border_image_entity_clear_4
    gc.collect()

    # 创建该图框小图保存路径
    if DEBUG_MODEL:
        room_images_path = os.path.join(result_path, '{}_{}_room_images'.format(border_name, drawing_type.value))
        if not os.path.exists(room_images_path):
            os.mkdir(room_images_path)

    room_info = border_entity_info.get('room_info', []) + border_entity_info.get('small_room_info', [])

    num_room = 0
    # 分别截取卫生间、厨房、阳台、客厅、卧室、书房的空间小图
    for room in room_info:
        if '卫生间' not in "".join(room[-1]) and '厨房' not in "".join(room[-1]) and '阳台' not in "".join(room[-1]) and \
                '客厅' not in "".join(room[-1]) and "卧室" not in "".join(room[-1]) and "书房" not in "".join(room[-1]):
            continue
        margin = 10
        masked = crop_room_small_images_v2(img_entity_clear_3, room, margin=margin)
        bg_img = np.zeros((masked.shape[0], masked.shape[1], 3), np.uint8)
        # 小图若是全黑，跳过
        if np.all(masked == bg_img):
            del masked, bg_img
            gc.collect()
            continue
        del bg_img
        gc.collect()
        if '卫生间' in "".join(room[-1]):
            if DEBUG_MODEL:
                image_save_path_by_room = os.path.join(room_images_path, '卫生间')
                image_name = '{}_{}.png'.format('卫生间', num_room)
            washroom_images_list.append(masked)
            washroom_bbox = [room[1][0] - margin, room[1][1] - margin, room[1][2] + margin, room[1][3] + margin]
            washroom_bbox_list.append(washroom_bbox)
        elif '卧室' in "".join(room[-1]):
            if DEBUG_MODEL:
                image_save_path_by_room = os.path.join(room_images_path, '卧室')
                image_name = '{}_{}.png'.format('卧室', num_room)
            bedroom_images_list.append(masked)
            bedroom_bbox = [room[1][0] - margin, room[1][1] - margin, room[1][2] + margin, room[1][3] + margin]
            bedroom_bbox_list.append(bedroom_bbox)
            # 客厅和卧室有些情况下为同一个空间
            if '客厅' in "".join(room[-1]):
                if DEBUG_MODEL:
                    image_save_path_by_room = os.path.join(room_images_path, '客厅')
                    image_name = '{}_{}.png'.format('客厅', num_room)
                livingroom_images_list.append(masked)
                livingroom_bbox = [room[1][0] - 10, room[1][1] - 10, room[1][2] + 10, room[1][3] + 10]
                livingroom_bbox_list.append(livingroom_bbox)
        elif '书房' in "".join(room[-1]):
            if DEBUG_MODEL:
                image_save_path_by_room = os.path.join(room_images_path, '书房')
                image_name = '{}_{}.png'.format('书房', num_room)
            shufang_images_list.append(masked)
            shufang_bbox = [room[1][0] - margin, room[1][1] - margin, room[1][2] + margin, room[1][3] + margin]
            shufang_bbox_list.append(shufang_bbox)
        elif '厨房' in "".join(room[-1]):
            if DEBUG_MODEL:
                image_save_path_by_room = os.path.join(room_images_path, '厨房')
                image_name = '{}_{}.png'.format('厨房', num_room)
            kitchen_images_list.append(masked)
            kitchen_bbox = [room[1][0] - margin, room[1][1] - margin, room[1][2] + margin, room[1][3] + margin]
            kitchen_bbox_list.append(kitchen_bbox)
        elif '阳台' in "".join(room[-1]):
            if DEBUG_MODEL:
                image_save_path_by_room = os.path.join(room_images_path, '阳台')
                image_name = '{}_{}.png'.format('阳台', num_room)
            balcony_images_list.append(masked)
            balcony_bbox = [room[1][0] - margin, room[1][1] - margin, room[1][2] + margin, room[1][3] + margin]
            balcony_bbox_list.append(balcony_bbox)
        else:
            if DEBUG_MODEL:
                image_save_path_by_room = os.path.join(room_images_path, '客厅')
                image_name = '{}_{}.png'.format('客厅', num_room)
            livingroom_images_list.append(masked)
            livingroom_bbox = [room[1][0] - margin, room[1][1] - margin, room[1][2] + margin, room[1][3] + margin]
            livingroom_bbox_list.append(livingroom_bbox)

        if DEBUG_MODEL:
            if not os.path.exists(image_save_path_by_room):
                os.makedirs(image_save_path_by_room)
            img_saved_path = os.path.join(image_save_path_by_room, image_name)
            cv2.imencode('.png', masked)[1].tofile(img_saved_path)
            num_room += 1
        del masked
        gc.collect()

    if drawing_type == decor_architecture_drawing_type.DECORATION_KITCHEN_ELEVATION and DEBUG_MODEL:
        img_save_path_by_elevation = os.path.join(room_images_path, '厨房立面图')
        if not os.path.exists(img_save_path_by_elevation):
            os.makedirs(img_save_path_by_elevation)
        limian_kitchen_images_list, limian_kitchen_bbox_list = crop_evevation_image(img_entity_clear_4,
                                                                                    img_save_path_by_elevation, '厨房')

    if drawing_type == decor_architecture_drawing_type.DECORATION_BATHROOM_ELEVATION and DEBUG_MODEL:
        img_save_path_by_elevation = os.path.join(room_images_path, '卫生间立面图')
        if not os.path.exists(img_save_path_by_elevation):
            os.makedirs(img_save_path_by_elevation)
        limian_washroom_images_list, limian_washroom_bbox_list = crop_evevation_image(img_entity_clear_4,
                                                                                      img_save_path_by_elevation, '卫生间')
    predict_detection_bedroom = []
    # 获取家具图层的直线，对检测结果进行处理

    start_time = time()
    predict_detection_washroom = washroom_detection(washroom_images_list, washroom_bbox_list, ext_margin,
                                                    entity_bbox_dict)
    predict_detection_shufang = shufang_detection(shufang_images_list, shufang_bbox_list, origin_border_entity_info,
                                                  scale, border_coord, ratio,
                                                  border_entity_info, img_copy)
    predict_detection_kitchen = kitchen_detection(kitchen_images_list, kitchen_bbox_list, ext_margin,
                                                  main_branch_text_list, entity_bbox_dict)
    predict_detection_balcony = balcony_detection(balcony_images_list, balcony_bbox_list, ext_margin,
                                                  main_branch_text_list, entity_bbox_dict)
    predict_detection_livingroom = livingroom_detection(livingroom_images_list, livingroom_bbox_list, ext_margin,
                                                        entity_bbox_dict)

    # predict_detection_limian_washroom = limian_washroom_detection(limian_washroom_images_list, limian_washroom_bbox_list)
    # predict_detection_limian_kitchen = limian_kitchen_detection(limian_kitchen_images_list, limian_kitchen_bbox_list)
    predict_detection_limian_washroom = []
    predict_detection_limian_kitchen = []
    del washroom_images_list
    del bedroom_images_list
    del shufang_images_list
    del kitchen_images_list
    del balcony_images_list
    del livingroom_images_list
    del limian_washroom_images_list
    del limian_kitchen_images_list
    gc.collect()

    print("[Note]模型前向时间:{:.2f} seconds".format(time() - start_time))

    all_entity_bbox = []
    all_entity_class = []
    all_origin_entity_class = []
    all_entity_score = []
    entity_annotation_list = []

    for detection_result in predict_detection_washroom:
        entity_class_score = detection_result[5]
        if entity_class_score <= 0.5:
            continue
        entity_bbox = detection_result[:4]
        height, width = entity_bbox[3] - entity_bbox[1], entity_bbox[2] - entity_bbox[0]
        entity_class = detection_result[4]
        # 检测后处理
        # 便器
        if entity_class in ['closestool']:
            # 置信度较低的便器矫正为others
            if entity_class_score < 0.6:
                entity_class = 'others'
            # 尺寸过大的便器矫正为others
            elif height > CLOSESTOOL_LONG_SIDE_MAX * ratio[1] or width > CLOSESTOOL_LONG_SIDE_MAX * ratio[0]:
                entity_class = 'others'
            # 长边尺寸太小的便器矫正为others
            elif max(height, width) < CLOSESTOOL_LONG_SIDE_MIN * ratio[0]:
                entity_class = 'others'
        # 洗浴器
        if entity_class in ['shower']:
            # 置信度较低的洗浴器矫正为others
            if entity_class_score < 0.5:
                entity_class = 'others'
        all_entity_bbox.append(entity_bbox)
        all_entity_class.append(entity_class)
        all_origin_entity_class.append(entity_class)
        all_entity_score.append(entity_class_score)
        entity_annotation_list.append([])

    for detection_result in predict_detection_bedroom:
        entity_class_score = detection_result[5]
        # if entity_class_score <= 0.5:
        #     continue
        entity_bbox = detection_result[:4]
        height, width = entity_bbox[3] - entity_bbox[1], entity_bbox[2] - entity_bbox[0]
        entity_class = detection_result[4]
        all_entity_bbox.append(entity_bbox)
        all_entity_class.append(entity_class)
        all_origin_entity_class.append(entity_class)
        all_entity_score.append(entity_class_score)
        entity_annotation_list.append([])

    for detection_result in predict_detection_shufang:
        entity_class_score = detection_result[5]
        # if entity_class_score <= 0.5:
        #     continue
        entity_bbox = detection_result[:4]
        height, width = entity_bbox[3] - entity_bbox[1], entity_bbox[2] - entity_bbox[0]
        entity_class = detection_result[4]

        all_entity_bbox.append(entity_bbox)
        all_entity_class.append(entity_class)
        all_origin_entity_class.append(entity_class)
        all_entity_score.append(entity_class_score)
        entity_annotation_list.append([])

    for detection_result in predict_detection_kitchen:
        entity_class_score = detection_result[5]
        # if entity_class_score <= 0.5:
        #     continue
        entity_bbox = detection_result[:4]
        entity_class = detection_result[4]
        all_entity_bbox.append(entity_bbox)
        all_entity_class.append(entity_class)
        all_origin_entity_class.append(entity_class)
        all_entity_score.append(entity_class_score)
        entity_annotation_list.append([])

    for detection_result in predict_detection_balcony:
        entity_class_score = detection_result[5]
        entity_bbox = detection_result[:4]
        entity_class = detection_result[4]
        all_entity_bbox.append(entity_bbox)
        all_entity_class.append(entity_class)
        all_origin_entity_class.append(entity_class)
        all_entity_score.append(entity_class_score)
        entity_annotation_list.append([])

    for detection_result in predict_detection_livingroom:
        entity_class_score = detection_result[5]
        entity_bbox = detection_result[:4]
        entity_class = detection_result[4]
        all_entity_bbox.append(entity_bbox)
        all_entity_class.append(entity_class)
        all_origin_entity_class.append(entity_class)
        all_entity_score.append(entity_class_score)
        entity_annotation_list.append([])
        
    for detection_result in predict_detection_limian_kitchen:
        entity_class_score = detection_result[5]
        entity_bbox = detection_result[:4]
        entity_class = detection_result[4]
        all_entity_bbox.append(entity_bbox)
        all_entity_class.append(entity_class)
        all_origin_entity_class.append(entity_class)
        all_entity_score.append(entity_class_score)
        entity_annotation_list.append([])
        
    for detection_result in predict_detection_limian_washroom:
        entity_class_score = detection_result[5]
        entity_bbox = detection_result[:4]
        entity_class = detection_result[4]
        all_entity_bbox.append(entity_bbox)
        all_entity_class.append(entity_class)
        all_origin_entity_class.append(entity_class)
        all_entity_score.append(entity_class_score)
        entity_annotation_list.append([])

    for cls, ori_cls, bbox, score in zip(all_entity_class, all_origin_entity_class, all_entity_bbox, all_entity_score):
        debug_drawer.draw(cv2.rectangle, border_img_with_wall_copy, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 0, 255),
                          1)
        debug_drawer.draw(cv2.putText, border_img_with_wall_copy, '{} {:.2f}'.format(cls, score),
                          (bbox[0], bbox[1] - 5),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
        debug_drawer.draw(cv2.putText, border_img_with_wall_copy, '{} '.format(ori_cls), (bbox[2], bbox[1] - 5),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 9), 1)
    entity_CAD_coord_list = list(
        map(lambda bbox: convert_bbox_to_CAD_coord(border_coord, bbox, ratio), all_entity_bbox))

    # 检测结果不去除margin
    # # 在保存构件的bbox之前先去除margin
    # all_entity_bbox = [remove_margin(bbox, ext_margin) for bbox in all_entity_bbox]

    border_entity_info['entity_bbox_list_detection'] = all_entity_bbox
    border_entity_info['entity_class_list_detection'] = all_entity_class
    border_entity_info['entity_ori_class_list_detection'] = all_origin_entity_class
    border_entity_info['entity_score_list_detection'] = all_entity_score
    border_entity_info['entity_coord_list_detection'] = entity_CAD_coord_list
    border_entity_info['entity_annotation_list_detection'] = entity_annotation_list

    # 保存中间结果
    img_path_temp = os.path.join(result_path, border_name)

    if rule_index is None:
        save_name = '{}_{}_{}'.format(img_path_temp, drawing_type.value, IMAGE_PRINT_EXTENSION[10])
    else:
        save_name = '{}_{}_rule_{}_{}'.format(img_path_temp, drawing_type.value, rule_index, IMAGE_PRINT_EXTENSION[10])

    debug_drawer.save_to(border_img_with_wall_copy, save_name)
    # 将目标检测的结果保存到image manager
    if SAVE_RECOG_GEN_IMG_ONLINE:
        image_manager.load_to_manager(IMG_DET_RESULT, debug_drawer.get_copy(border_img_with_wall_copy))
        # for debug
        # det = image_manager.load_from_manager(IMG_DET_RESULT)
        # cv2.imwrite("/Users/xuan.ma/Desktop/det.png", det)

    return border_entity_info


def crop_evevation_image(img_copy, img_save_path_by_elevation, save_name):
    """
    剪切立面图
    :param img_copy:
    :param img_save_path_by_elevation:
    :return:
    """
    img_copy_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    cnts, _ = cv2.findContours(img_copy_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    img_bbox = [0, 0, img_copy_gray.shape[1], img_copy_gray.shape[0] - 2000]
    img_cnt = get_contour_from_bbox(img_bbox)
    img_zero = np.zeros_like(img_copy_gray)
    num_elevation = 1
    for cnt in cnts:
        if len(cnt) < 3:
            continue
        cnt_bbox = get_bbox_from_contour(cnt)
        bbox_cnt = get_contour_from_bbox(cnt_bbox)
        cnt_iou1 = get_contours_iou(img_cnt, bbox_cnt, convex=True, approx=True)
        cnt_iou2 = get_contours_iou(bbox_cnt, img_cnt, convex=True, approx=True)
        if cnt_iou1 > 0.9 and cnt_iou2 < 0.8 and cnt_iou2 > 0.04:
            img_zero = cv2.drawContours(img_zero, [cnt], -1, (255, 255, 255), cv2.FILLED)
            # print(cnt_iou1, cnt_iou2)
    cnts, _ = cv2.findContours(img_zero, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    img_crop_list = []
    img_bbox_list = []
    for cnt in cnts:
        image_name = '{}_{}.png'.format(f'{save_name}立面图', num_elevation)
        img_saved_path = os.path.join(img_save_path_by_elevation, image_name)
        img_bbox = get_bbox_from_contour(cnt)
        x1, y1, x2, y2 = img_bbox
        img_crop = img_copy[y1:y2, x1:x2].copy()
        img_crop_list.append(img_crop)
        img_bbox_list.append(img_bbox)
        if DEBUG_MODEL:
            cv2.imencode('.png', img_crop)[1].tofile(img_saved_path)
        num_elevation += 1
        # import matplotlib.pyplot as plt
        # img_zero = np.zeros_like(img_copy_gray)
        # img_zero = cv2.drawContours(img_zero, [cnt], -1, (255, 0, 255), 200)
        # plt.imshow(img_zero)
        # plt.show()
    return img_crop_list, img_bbox_list


def kitchen_detection(kitchen_images_list, kitchen_bbox_list, ext_margin, main_branch_text_list, entity_bbox_dict):
    """
    厨房检测
    Args:
        kitchen_images_list:
        kitchen_bbox_list:
        ext_margin:
        main_branch_text_list:
        entity_bbox_dict:

    Returns:

    """
    # 厨房内的构件进行检测
    predict_detection_kitchen = []
    for kitchen_image, kitchen_bbox in zip(kitchen_images_list, kitchen_bbox_list):
        pred_det_k = tf_restful_detection(
            [kitchen_image], [kitchen_bbox],
            DetectConfig.MODEL_URL[export_env][DetectType.INDOOR_KITCHEN] + DetectConfig.MODEL_URL_SUFFIX[
                DetectType.INDOOR_KITCHEN],
            score_threshold=DetectConfig.SCORE_THRESHOLD[DetectType.INDOOR_KITCHEN])
        # 获取引线文本，纠正检测结果
        entity_bbox_list = [extend_margin(pred[:4], ext_margin) for pred in pred_det_k]
        annotation_list, _ = match_entity_annotation(main_branch_text_list, entity_list=entity_bbox_list,
                                                     img_anno=None, entity_type='vpipe')
        for pi, pred in enumerate(pred_det_k):
            class_idx = pred[4]
            entity_class = DetectConfig.MODEL_CLASS[DetectType.INDOOR_KITCHEN][class_idx]
            entity_class = DetectConfig.LABEL_MAP[DetectType.INDOOR_KITCHEN][entity_class]
            annotation_text = str(annotation_list[pi]) if annotation_list[pi] else ''
            if not annotation_text:
                entity_class = "others"
            elif re.search("热水器", annotation_text) and entity_class not in ["heater"]:
                entity_class = "heater"
            elif re.search("(燃|煤)气表", annotation_text) and entity_class not in ["gas_meter"]:
                entity_class = "gas_meter"
            pred[4] = entity_class

        preds_gas_meter = [pred for pred in pred_det_k if pred[4] == 'gas_meter']
        pred_gas_meter = None
        score_gas_meter = 0
        for pred in preds_gas_meter:
            if pred[-1] > score_gas_meter:
                pred_gas_meter = pred
                score_gas_meter = pred[-1]
            else:
                bbox = extend_margin(pred[:4], 2 * ext_margin)
                entity_bbox_dict['entity_detection_bboxes'].append(bbox)

        preds_heater = [pred for pred in pred_det_k if pred[4] == 'heater']
        pred_heater = None
        score_heater = 0
        for pred in preds_heater:
            if pred[-1] > score_heater:
                pred_heater = pred
                score_heater = pred[-1]
            else:
                bbox = extend_margin(pred[:4], 2 * ext_margin)
                entity_bbox_dict['entity_detection_bboxes'].append(bbox)

        pred_det_k = []
        if pred_gas_meter is not None:
            pred_det_k.append(pred_gas_meter)
        if pred_heater is not None:
            pred_det_k.append(pred_heater)
        predict_detection_kitchen.extend(pred_det_k)

    return predict_detection_kitchen


def shufang_detection(shufang_images_list, shufang_bbox_list, origin_border_entity_info, scale, border_coord, ratio,
                      border_entity_info, img_copy):
    """

    Args:
        shufang_images_list:
        shufang_bbox_list:
        origin_border_entity_info:
        scale:
        border_coord:
        ratio:
        border_entity_info:
        img_copy:

    Returns:

    """
    predict_detection_shufang = []
    # 书房空间内的构件进行检测
    layer_to_check = ["floor_drain_mix", "bed"]
    class_to_check = ["Line", "Polyline", "Polyline2d"]
    origin_entity_dict = get_origin_border_entity_info(origin_border_entity_info, layer_to_check, class_to_check,
                                                       scale, border_coord, ratio)
    line_entity_list = []
    for _, entity_list in origin_entity_dict.items():
        line_entity_list.extend(entity_list)
    line_entity_list = list(filter(lambda x: len(x) == 4, line_entity_list))

    for shufang_image, shufang_bbox in zip(shufang_images_list, shufang_bbox_list):
        # TODO 添加书房空间检测模型
        # pred_det_w = tf_restful_detection([bedroom_image], [bedroom_bbox],
        #     DetectConfig.MODEL_URL[export_env][DetectType.INDOOR_BEDROOM] + DetectConfig.MODEL_URL_SUFFIX[
        #         DetectType.INDOOR_BEDROOM],
        #     score_threshold=DetectConfig.SCORE_THRESHOLD[DetectType.INDOOR_BEDROOM])
        # for pred in pred_det_w:
        #     class_idx = pred[4]
        #     entity_class = DetectConfig.MODEL_CLASS[DetectType.INDOOR_BEDROOM][class_idx]
        #     entity_class = DetectConfig.LABEL_MAP[DetectType.INDOOR_BEDROOM][entity_class]
        #     pred[4] = entity_class
        # print("pred_det_w", pred_det_w)
        # 获取书房内部所有的直线图元
        shufang_line_entity_list = [line for line in line_entity_list if
                                    line_overlap_poly(get_contour_from_bbox(shufang_bbox), line)]

        bed_width_thred1 = int(1250 * ratio[0])
        bed_width_thred2 = int(500000 * ratio[0])  # 目前不用，为了减少计算量，给一个很大的值
        bed_pred_det_w = get_bed_entity(border_entity_info, shufang_line_entity_list, img_copy, bed_width_thred1,
                                        bed_width_thred2)
        pred_det_w = bed_pred_det_w
        # print("pred_det_w", pred_det_w)
        predict_detection_shufang.extend(pred_det_w)

    return predict_detection_shufang


def balcony_detection(balcony_images_list, balcony_bbox_list, ext_margin, main_branch_text_list, entity_bbox_dict):
    """
    阳台检测
    Args:
        balcony_images_list:
        balcony_bbox_list:
        ext_margin:
        main_branch_text_list:
        entity_bbox_dict:

    Returns:

    """
    # 阳台内的构件进行检测
    predict_detection_balcony = []
    for balcony_image, balcony_bbox in zip(balcony_images_list, balcony_bbox_list):
        pred_det_b = tf_restful_detection(
            [balcony_image], [balcony_bbox],
            DetectConfig.MODEL_URL[export_env][DetectType.INDOOR_BALCONY] + DetectConfig.MODEL_URL_SUFFIX[
                DetectType.INDOOR_BALCONY],
            score_threshold=DetectConfig.SCORE_THRESHOLD[DetectType.INDOOR_BALCONY])
        # 获取引线文本，纠正检测结果
        entity_bbox_list = [extend_margin(pred[:4], ext_margin) for pred in pred_det_b]
        annotation_list, _ = match_entity_annotation(main_branch_text_list, entity_list=entity_bbox_list,
                                                     img_anno=None, entity_type='vpipe')
        for pi, pred in enumerate(pred_det_b):
            class_idx = pred[4]
            entity_class = DetectConfig.MODEL_CLASS[DetectType.INDOOR_BALCONY][class_idx]
            entity_class = DetectConfig.LABEL_MAP[DetectType.INDOOR_BALCONY][entity_class]
            # for debug
            # cv2.rectangle(img_copy, tuple(pred[:2]), tuple(pred[2:4]), (255, 255, 0), 3)
            # cv2.putText(img_copy, entity_class, tuple(pred[:2]), cv2.FONT_HERSHEY_SIMPLEX, 1,
            #             (0, 0, 255), 2)
            # cv2.imwrite("/Users/xuan.ma/Desktop/balcony_det_debug.png", img_copy)
            annotation_text = str(annotation_list[pi]) if annotation_list[pi] else ''
            if not annotation_text:
                entity_class = "others"
            elif re.search("热水器", annotation_text) and entity_class not in ["heater"]:
                entity_class = "heater"
            elif re.search("(煤|燃)气表", annotation_text) and entity_class not in ["gas_meter"]:
                entity_class = "gas_meter"
            pred[4] = entity_class

        preds_gas_meter = [pred for pred in pred_det_b if pred[4] == 'gas_meter']
        pred_gas_meter = None
        score_gas_meter = 0
        for pred in preds_gas_meter:
            if pred[-1] > score_gas_meter:
                pred_gas_meter = pred
                score_gas_meter = pred[-1]
            else:
                bbox = extend_margin(pred[:4], 2 * ext_margin)
                entity_bbox_dict['entity_detection_bboxes'].append(bbox)

        # 分类成洗衣机的热水器、热水箱进行矫正
        # if pred_washer is not None:
        #     is_boiler = False
        #     for txt in boiler_text_info_list:
        #         if Iou_temp(txt[:4], pred_washer[:4]) > 0.5:
        #             is_boiler = True
        #             break
        #     if is_boiler:
        #         bbox = extend_margin(pred_washer[:4], 2 * ext_margin)
        #         entity_bbox_dict['entity_detection_bboxes'].append(bbox)
        #         pred_washer = None

        preds_heater = [pred for pred in pred_det_b if pred[4] == 'heater']
        pred_heater = None
        score_heater = 0
        for pred in preds_heater:
            if pred[-1] > score_heater and pred[-1] > 0.9:
                pred_heater = pred
                score_heater = pred[-1]
            else:
                bbox = extend_margin(pred[:4], 2 * ext_margin)
                entity_bbox_dict['entity_detection_bboxes'].append(bbox)

        # 洗衣机和洗面器几乎重合时，取置信度较大的类别
        # if pred_washer is not None and pred_washbasin is not None and \
        #         Iou_temp(pred_washbasin[:4], pred_washer[:4]) > 0.85:
        #     if pred_washbasin[-1] > pred_washer[-1]:
        #         pred_washer = None
        #     else:
        #         pred_washbasin = None

        # other_labels = ['dilou', 'pipe']
        # preds_others = [pred for pred in pred_det_b if pred[4] in other_labels]

        pred_det_b = []
        if pred_gas_meter is not None:
            pred_det_b.append(pred_gas_meter)
        if pred_heater is not None:
            pred_det_b.append(pred_heater)
        # for pred in preds_others:
        #     if pred[-1] < 0.9:
        #         bbox = extend_margin(pred[:4], 2 * ext_margin)
        #         entity_bbox_dict['entity_detection_bboxes'].append(bbox)
        #         continue
        #     pred_det_b.append(pred)
        predict_detection_balcony.extend(pred_det_b)

    return predict_detection_balcony


def livingroom_detection(livingroom_images_list, livingroom_bbox_list, ext_margin, entity_bbox_dict):
    """

    Args:
        livingroom_images_list:
        livingroom_bbox_list:
        ext_margin:
        entity_bbox_dict:

    Returns:

    """
    # 客厅内的构件进行检测
    predict_detection_livingroom = []
    for livingroom_image, livingroom_bbox in zip(livingroom_images_list, livingroom_bbox_list):
        pred_det_l = tf_restful_detection(
            [livingroom_image], [livingroom_bbox],
            DetectConfig.MODEL_URL[export_env][DetectType.INDOOR_LIVINGROOM] + DetectConfig.MODEL_URL_SUFFIX[
                DetectType.INDOOR_LIVINGROOM],
            score_threshold=DetectConfig.SCORE_THRESHOLD[DetectType.INDOOR_LIVINGROOM])
        for pred in pred_det_l:
            class_idx = pred[4]
            entity_class = DetectConfig.MODEL_CLASS[DetectType.INDOOR_LIVINGROOM][class_idx]
            entity_class = DetectConfig.LABEL_MAP[DetectType.INDOOR_LIVINGROOM][entity_class]
            pred[4] = entity_class

        # 目前该版客厅模型只对洗面器分类准确率比较高，其他对象通过后续分类来识别
        pred_det_l_new = []
        for pred in pred_det_l:
            if pred[4] != 'washbasin':
                bbox = extend_margin(pred[:4], 2 * ext_margin)
                entity_bbox_dict['entity_detection_bboxes'].append(bbox)
            elif pred[-1] < 0.98:
                bbox = extend_margin(pred[:4], 2 * ext_margin)
                entity_bbox_dict['entity_detection_bboxes'].append(bbox)
            else:
                pred_det_l_new.append(pred)
        predict_detection_livingroom.extend(pred_det_l_new)

    return predict_detection_livingroom


def washroom_detection(washroom_images_list, washroom_bbox_list, ext_margin, entity_bbox_dict):
    """
    卫生间检测
    Args:
        washroom_images_list:
        washroom_bbox_list:
        ext_margin:
        entity_bbox_dict:

    Returns:

    """
    predict_detection_washroom = []
    # 卫生间空间内的构件进行检测
    for washroom_image, washroom_bbox in zip(washroom_images_list, washroom_bbox_list):
        pred_det_w = tf_restful_detection(
            [washroom_image], [washroom_bbox],
            DetectConfig.MODEL_URL[export_env][DetectType.INDOOR_WASHROOM] + DetectConfig.MODEL_URL_SUFFIX[
                DetectType.INDOOR_WASHROOM],
            score_threshold=DetectConfig.SCORE_THRESHOLD[DetectType.INDOOR_WASHROOM])
        for pred in pred_det_w:
            class_idx = pred[4]
            entity_class = DetectConfig.MODEL_CLASS[DetectType.INDOOR_WASHROOM][class_idx]
            entity_class = DetectConfig.LABEL_MAP[DetectType.INDOOR_WASHROOM][entity_class]
            pred[4] = entity_class
            # for debug
            # cv2.rectangle(img_copy, tuple(pred[:2]), tuple(pred[2:4]), (255, 255, 0), 3)
            # cv2.putText(img_copy, entity_class, tuple(pred[:2]), cv2.FONT_HERSHEY_SIMPLEX, 1,
            #             (0, 0, 255), 2)  # 高度文字红色

        preds_shower = [pred for pred in pred_det_w if pred[4] == 'shower']
        pred_shower = None
        score_shower = 0
        for pred in preds_shower:
            if pred[-1] > score_shower:
                pred_shower = pred
                score_shower = pred[-1]
            else:
                bbox = extend_margin(pred[:4], 2 * ext_margin)
                entity_bbox_dict['entity_detection_bboxes'].append(bbox)

        preds_washer = [pred for pred in pred_det_w if pred[4] == 'washer']
        pred_washer = None
        score_washer = 0
        for pred in preds_washer:
            if pred[-1] > score_washer and pred[-1] > 0.85:
                pred_washer = pred
                score_washer = pred[-1]
            else:
                bbox = extend_margin(pred[:4], 2 * ext_margin)
                entity_bbox_dict['entity_detection_bboxes'].append(bbox)

        preds_bathtub = [pred for pred in pred_det_w if pred[4] == 'bathtub']
        pred_bathtub = None
        score_bathtub = 0
        for pred in preds_bathtub:
            if pred[-1] > score_bathtub:
                pred_bathtub = pred
                score_bathtub = pred[-1]
            else:
                bbox = extend_margin(pred[:4], 2 * ext_margin)
                entity_bbox_dict['entity_detection_bboxes'].append(bbox)

        preds_closestool = [pred for pred in pred_det_w if pred[4] == 'closestool']
        preds_closestool_proceed = []
        while len(preds_closestool) > 0:
            closestool_1 = preds_closestool[0]
            bbox_1 = closestool_1[:4]
            preds_closestool.pop(0)
            closestool_2 = None
            for closestool in preds_closestool:
                bbox_2 = closestool[:4]
                if Iou_temp(bbox_1, bbox_2) > 0:
                    closestool_2 = closestool
                    break
            if closestool_2 is not None:
                preds_closestool.remove(closestool_2)
                xmin = min(closestool_1[0], closestool_2[0])
                ymin = min(closestool_1[1], closestool_2[1])
                xmax = max(closestool_1[2], closestool_2[2])
                ymax = max(closestool_1[3], closestool_2[3])
                score = max(closestool_1[-1], closestool_2[-1])
                closestool_1 = [xmin, ymin, xmax, ymax, closestool_1[4], score]
            preds_closestool_proceed.append(closestool_1)

        special_labels = ['shower', 'washer', 'bathtub', 'closestool', 'washbasin']
        pred_det_w_new = []
        for pred in pred_det_w:
            if pred[4] not in special_labels and pred[-1] <= 0.9:
                bbox = extend_margin(pred[:4], 2 * ext_margin)
                entity_bbox_dict['entity_detection_bboxes'].append(bbox)
            elif pred[4] not in special_labels and pred[-1] > 0.9:
                pred_det_w_new.append(pred)
            elif pred[4] == 'washbasin' and pred[-1] < 0.9:
                bbox = extend_margin(pred[:4], 2 * ext_margin)
                entity_bbox_dict['entity_detection_bboxes'].append(bbox)
            elif pred[4] == 'washbasin' and pred[-1] >= 0.9:
                pred_det_w_new.append(pred)

        pred_det_w = pred_det_w_new + preds_closestool_proceed

        if pred_shower is not None:
            pred_det_w.append(pred_shower)
        if pred_washer is not None:
            pred_det_w.append(pred_washer)
        if pred_bathtub is not None:
            pred_det_w.append(pred_bathtub)

        predict_detection_washroom.extend(pred_det_w)

    return predict_detection_washroom


def limian_washroom_detection(limian_washroom_images_list, limian_washroom_bbox_list):
    """
    立面卫生间
    Args:
        limian_washroom_images_list: 
        limian_washroom_bbox_list: 

    Returns:

    """
    predict_detection_limian_washroom = []
    for limian_washroom_image, limian_washroom_bbox in zip(limian_washroom_images_list, limian_washroom_bbox_list):
        pred_det_l = tf_restful_detection(
            [limian_washroom_image], [limian_washroom_bbox],
            DetectConfig.MODEL_URL[export_env][DetectType.ELEVATION_WASHROOM] + DetectConfig.MODEL_URL_SUFFIX[
                DetectType.ELEVATION_WASHROOM],
            score_threshold=DetectConfig.SCORE_THRESHOLD[DetectType.ELEVATION_WASHROOM])
        for pred in pred_det_l:
            class_idx = pred[4]
            entity_class = DetectConfig.MODEL_CLASS[DetectType.ELEVATION_WASHROOM][class_idx]
            entity_class = DetectConfig.LABEL_MAP[DetectType.ELEVATION_WASHROOM][entity_class]
            pred[4] = entity_class
        predict_detection_limian_washroom.extend(pred_det_l)

    return predict_detection_limian_washroom
    
    
def limian_kitchen_detection(limian_kitchen_images_list, limian_kitchen_bbox_list):
    """
    立面厨房
    Args:
        limain_kitchen_images_list: 
        limian_kitchen_bbox_list: 

    Returns:

    """
    predict_detection_limian_kitchen = []
    for limian_kitchen_image, limian_kitchen_bbox in zip(limian_kitchen_images_list, limian_kitchen_bbox_list):
        pred_det_l = tf_restful_detection(
            [limian_kitchen_image], [limian_kitchen_bbox],
            DetectConfig.MODEL_URL[export_env][DetectType.ELEVATION_KITCHEN] + DetectConfig.MODEL_URL_SUFFIX[
                DetectType.ELEVATION_KITCHEN],
            score_threshold=DetectConfig.SCORE_THRESHOLD[DetectType.ELEVATION_KITCHEN])
        for pred in pred_det_l:
            class_idx = pred[4]
            entity_class = DetectConfig.MODEL_CLASS[DetectType.ELEVATION_KITCHEN][class_idx]
            entity_class = DetectConfig.LABEL_MAP[DetectType.ELEVATION_KITCHEN][entity_class]
            pred[4] = entity_class
        predict_detection_limian_kitchen.extend(pred_det_l)

    return predict_detection_limian_kitchen