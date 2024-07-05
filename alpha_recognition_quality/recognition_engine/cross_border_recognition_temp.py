import gc

import cv2, re
import numpy as np
from shapely.geometry import Point, MultiPoint, MultiLineString, MultiPolygon, LineString, Polygon

from .space.classes_lib.bu_shang_ren_wu_mian import BuShangRenWuMian
from ..common.utils import point_euclidean_distance, extend_line, contour_area_in_reality, get_contours_iou, get_line_cross_point
from .base.bounding_rectangle import BoundingRectangle
from .base.contour import Contour
from .space.classes_lib.jia_kong_kong_jian import JiaKongKongJian
from .space.space import Space


def get_max_bbox_index(bbox_list):
    """
    获取最大的bbox的索引
    """
    max_length = 0
    ind = 0
    for i, bbox in enumerate(bbox_list):
        bbox_length = point_euclidean_distance(bbox[:2], bbox[2:])
        if bbox_length > max_length:
            max_length = bbox_length
            ind = i
    return ind


def get_cross_point_list(poly_1, poly_2, use_buffer=True):
    """
    获取交点列表
    :param poly_1: POLYGON对象1
    :param poly_2: POLYGON对象2
    :param use_buffer: 是否加buffer
    :return: 交点列表
    """
    # poly_1 = poly_1.convex_hull
    # poly_2 = poly_2.convex_hull
    if use_buffer:
        poly_1 = poly_1.buffer(0.001)  # 加一个较小的buffer
        poly_2 = poly_2.buffer(0.001)  # 加一个较小的buffer
    # print(poly_1.is_valid)
    # print(poly_2.is_valid)

    intersection_point_list = []
    intersection_point = poly_1.intersection(poly_2)
    # print('---> intersection_point type', type(intersection_point))

    if intersection_point.is_empty:
        intersection_point_list = []
    elif isinstance(intersection_point, Point):
        intersection_point_list.extend(list(intersection_point.coords))
    elif isinstance(intersection_point, LineString):
        intersection_point_list.extend(list(intersection_point.coords))
    elif isinstance(intersection_point, MultiPoint):
        for points in list(intersection_point):
            intersection_point_list.extend(list(points.coords))
    elif isinstance(intersection_point, MultiLineString):
        for lines in list(intersection_point):
            intersection_point_list.extend(list(lines.coords))
    elif isinstance(intersection_point, Polygon):
        cent = intersection_point.centroid
        intersection_point_list = [[int(cent.x), int(cent.y)]]
    elif isinstance(intersection_point, MultiPolygon):
        cent_x_list = []
        cent_y_list = []
        for poly in list(intersection_point):
            cent = poly.centroid
            cent_x_list.append(cent.x)
            cent_y_list.append(cent.y)
        # 求均值
        cent_x = int(np.mean(cent_x_list))
        cent_y = int(np.mean(cent_y_list))
        intersection_point_list = [[cent_x, cent_y]]

    return intersection_point_list


def get_paired_axis_line(axis_net_line_list_U, axis_net_line_num_list_U, axis_net_line_list_D,
                         axis_net_line_num_list_D):
    axis_num_index_U = []
    for i, axis_num in enumerate(axis_net_line_num_list_U):
        if axis_num in axis_net_line_num_list_D:
            axis_num_index_U.append(i)
    inter_point_U = None
    axis_num_value = []
    for i in axis_num_index_U:
        axis_line1 = axis_net_line_list_U[i]
        for j in axis_num_index_U:
            if j == i:
                continue
            axis_line2 = axis_net_line_list_U[j]
            break_point = get_line_cross_point(axis_line1, axis_line2)
            if break_point is None:
                continue
            else:
                axis_num_value = [axis_net_line_num_list_U[i], axis_net_line_num_list_U[j]]
                inter_point_U = [int(break_point[0]), int(break_point[1])]
                break
        if inter_point_U is not None:
            break
    if inter_point_U is None:
        print("[NOTE]该组平面图未找到相交的轴网，无法有效映射！！")
        return None, None

    axis_line_D_1 = axis_net_line_list_D[axis_net_line_num_list_D.index(axis_num_value[0])]
    axis_line_D_2 = axis_net_line_list_D[axis_net_line_num_list_D.index(axis_num_value[1])]
    break_point_D = get_line_cross_point(axis_line_D_1, axis_line_D_2)
    # print("line_1: ", axis_num_value[0], " ", axis_num_value[1])
    if break_point_D is None:
        print("[NOTE]两个平面图的轴网信息无法对应！！")
        return None, None
    inter_point_D = [int(break_point_D[0]), int(break_point_D[1])]
    return inter_point_U, inter_point_D


def get_overhead_sapce_info(border_entity_1, border_entity_2):
    overhead_space_list = []
    ratio = border_entity_1.ratio
    # 分别获取两个图框的轴网
    axis_net_bbox_list_1 = border_entity_1.axis_net_bbox_list
    axis_net_line_list_1 = border_entity_1.axis_net_line_list
    axis_net_num_list_1 = border_entity_1.axis_net_line_num_list

    axis_net_bbox_list_2 = border_entity_2.axis_net_bbox_list
    axis_net_line_list_2 = border_entity_2.axis_net_line_list
    axis_net_num_list_2 = border_entity_2.axis_net_line_num_list

    # 判断是否都有轴网
    if len(axis_net_bbox_list_1) == 0 or len(axis_net_bbox_list_2) == 0:
        print("[NOTE]一层或二层没有轴网，导致无法映射来获取架空层。")
        return overhead_space_list
    # 获取两组轴网的最大bbox索引
    ind_1 = get_max_bbox_index(axis_net_bbox_list_1)
    ind_2 = get_max_bbox_index(axis_net_bbox_list_2)
    # 通过索引获取相应的轴网
    axis_net_num_1 = axis_net_num_list_1[ind_1]
    axis_net_line_1 = axis_net_line_list_1[ind_1]
    axis_net_num_2 = axis_net_num_list_2[ind_2]
    axis_net_line_2 = axis_net_line_list_2[ind_2]

    # 获取图框一的图像管理器信息
    image_manager_1 = border_entity_1.image_manager
    img_height, img_width = image_manager_1.img_height, image_manager_1.img_width
    image_manager_2 = border_entity_1.image_manager
    img_height_2, img_width_2 = image_manager_2.img_height, image_manager_2.img_width
    # 获取两个轴网对应的参考交点
    inter_point_1, inter_point_2 = get_paired_axis_line(axis_net_line_1, axis_net_num_1, axis_net_line_2,
                                                        axis_net_num_2)
    if inter_point_1 is None or inter_point_2 is None:
        print("[Note]没有找到对应的轴网交点。")
        return overhead_space_list

    # 分别获取平面图建筑轮廓
    building_contour_list_1 = border_entity_1.space_object_dict["平面图建筑轮廓"]
    building_contour_list_2 = border_entity_2.space_object_dict["平面图建筑轮廓"]
    if len(building_contour_list_1) == 0 or len(building_contour_list_2) == 0:
        print("[Note]图框一或图框二没有平面图建筑轮廓！！")
        return overhead_space_list
    relative_building_contour_list_2 = []
    for building_contour_2 in building_contour_list_2:
        relative_building_contour_2 = building_contour_2.contour.contour - inter_point_2 + inter_point_1
        relative_building_contour_list_2.append(relative_building_contour_2)
    print("1: ", inter_point_1, " 2: ", inter_point_2)
    # 将两个图框的轮廓分别画到底图上
    img_temp = np.zeros((img_height, img_width, 3), dtype="uint8")
    for relative_building_contour_2 in relative_building_contour_list_2:
        cv2.fillPoly(img_temp, [relative_building_contour_2], (255, 255, 255))
    for building_contour_1 in building_contour_list_1:
        cv2.fillPoly(img_temp, [building_contour_1.contour.contour], (0, 0, 0))
    gray = cv2.cvtColor(img_temp, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("/Users/shanks/Desktop/jiakongceng.png", img_temp)
    del img_temp
    gc.collect()
    gray = gray.astype(np.uint8)
    if '3.4' in cv2.__version__:
        _, contours, hierarchy = cv2.findContours(gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, hierarchy = cv2.findContours(gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    del gray
    gc.collect()
    d = hierarchy[:, :, 2].tolist() if hierarchy is not None else []
    # 筛选轮廓并查找内轮廓
    for i, cnt in enumerate(contours):
        inner_contours_list = []
        cnt_area = contour_area_in_reality(cnt, ratio)
        if cnt_area < 10:
            continue
        for j in d:
            if j == i:
                inner_contours_list.append(contours[j])
        # 实例化架空空间
        contour_o = Contour(cnt, border_entity_1.ratio)
        bbox_o = BoundingRectangle(cv2.boundingRect(cnt))
        space_object = Space(contour_o, bbox_o, ["架空空间"])
        overhead_space = JiaKongKongJian(space_object, border_entity_1, inner_contours_list)
        overhead_space_list.append(overhead_space)

    # cv2.imwrite("/Users/zhengcijie/Desktop/jiakongceng.png", img_temp)

    return overhead_space_list


def get_unaccessible_root_space(border_entity_1, border_entity_2):
    """
    通过跨图将机房层功能性空间映射到屋顶层得到不上人屋面
    Args:
        border_entity_1: 机房层图框全量信息
        border_entity_2: 屋顶层图框全量信息
    Returns: 不上人屋面空间对象列表
    """
    # 初始化返回的空间列表
    space_list = []
    # 如果两个层的图框全量信息不是同时存在，则不进行查找空间
    if border_entity_1 is None or border_entity_2 is None:
        return space_list
    # 分别获取两个图框的轴网
    axis_net_bbox_list_1 = border_entity_1.axis_net_bbox_list
    axis_net_line_list_1 = border_entity_1.axis_net_line_list
    axis_net_num_list_1 = border_entity_1.axis_net_line_num_list

    axis_net_bbox_list_2 = border_entity_2.axis_net_bbox_list
    axis_net_line_list_2 = border_entity_2.axis_net_line_list
    axis_net_num_list_2 = border_entity_2.axis_net_line_num_list

    # 判断是否都有轴网
    if len(axis_net_bbox_list_1) == 0 or len(axis_net_bbox_list_2) == 0:
        print("[NOTE]机房层或屋顶层没有轴网，导致无法映射来获取不上人屋面。")
        return space_list
    # 获取两组轴网的最大bbox索引
    ind_1 = get_max_bbox_index(axis_net_bbox_list_1)
    ind_2 = get_max_bbox_index(axis_net_bbox_list_2)
    # 通过索引获取相应的轴网
    axis_net_num_1 = axis_net_num_list_1[ind_1]
    axis_net_line_1 = axis_net_line_list_1[ind_1]
    axis_net_num_2 = axis_net_num_list_2[ind_2]
    axis_net_line_2 = axis_net_line_list_2[ind_2]

    # 获取图框一的图像管理器信息
    image_manager_1 = border_entity_1.image_manager
    img_height, img_width = image_manager_1.img_height, image_manager_1.img_width
    image_manager_2 = border_entity_1.image_manager
    img_height_2, img_width_2 = image_manager_2.img_height, image_manager_2.img_width
    # 获取两个轴网对应的参考交点
    inter_point_1, inter_point_2 = get_paired_axis_line(axis_net_line_1, axis_net_num_1, axis_net_line_2,
                                                        axis_net_num_2, img_width, img_height, img_width_2,
                                                        img_height_2)
    if inter_point_1 is None or inter_point_2 is None:
        print("[Note]没有找到对应的轴网交点。")
        return space_list
    room_info_2 = border_entity_2.room_info
    room_info_1 = border_entity_1.room_info
    # 过滤出机房层的功能性空间
    filter_room_info_1 = [room for room in room_info_1 if re.search("机房|楼梯间|水箱间|井|烟道", "".join(room.name_list))]
    # 从机房层向屋顶层映射，找到屋顶对应机房层功能性空间的空间为不上人屋面
    contour_list = []
    for room_2 in room_info_2:
        room_2_cnt = room_2.contour.contour
        related_room_2_cnt = room_2_cnt - inter_point_2
        for room_1 in filter_room_info_1:
            room_1_cnt = room_1.contour.contour
            related_room_1_cnt = room_1_cnt - inter_point_1
            if get_contours_iou(related_room_2_cnt, related_room_1_cnt) > 0.3:
                # 实例化一个新的不上人屋面对象
                new_space_cnt = Contour(room_2_cnt, border_entity_2.ratio)
                new_space_bbox = BoundingRectangle(cv2.boundingRect(room_2_cnt))
                space_object = Space(new_space_cnt, new_space_bbox, ["不上人屋面"])
                root_object = BuShangRenWuMian(space_object, border_entity_2)
                space_list.append(root_object)
                break
    return space_list