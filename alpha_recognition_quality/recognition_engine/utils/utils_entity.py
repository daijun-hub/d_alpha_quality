# -*- coding: utf-8 -*-
import cv2

from ...common.utils_draw_and_rule import *
from ...common.CONSTANTS import wall_thickness_CAD
from ...common.utils import *
from ...config_manager.architecture.drawing_config import DrawingType
from ...config_manager.text_config import TextType
from shapely.geometry import LineString, Polygon, MultiLineString, Point, MultiPoint, MultiPolygon
from .utils_objectification_common import *
from scipy import ndimage
from skimage import filters
from skimage.morphology import disk

# ######################################################
#                        陈耀整理                       #
# ######################################################


# 获取门的宽度
def door_width_entity(bbox, border_entity_info, text_cls):
    """

    Args:
        bbox: 传入的门的外接矩形框
        border_entity_info: 图层全量信息
        text_cls: 文本信息

    Returns:
        门宽度信息
    """
    pattern = "\d{2}"
    # text_cls = door_nearby_text(bbox, border_entity_info, extend_margin=1000)
    door_width_info = None
    if text_cls is None:
        return door_width_info

    info_about_width = re.findall(pattern, text_cls.extend_message)
    if info_about_width:
        info_about_width = info_about_width[0]
        if info_about_width.startswith("0"):
            door_width_info = int(info_about_width[-1]) / 10
        else:
            door_width_info = int(info_about_width) / 10
    return door_width_info


# 获取门的高度
def door_height_entity(bbox, border_entity_info, text_cls):
    """

    Args:
        bbox: 传入的门的外接矩形框
        border_entity_info: 图层全量信息
        text_cls: 文本信息

    Returns:
        门的高度
    """

    pattern = "\d{2}[a-z|\.]?\d{2}"
    # text_cls = door_nearby_text(bbox, border_entity_info, extend_margin=1000)
    door_height_info = None
    if text_cls is None:
        return door_height_info

    info_about_height = re.findall(pattern, text_cls.extend_message)
    if info_about_height:
        info_about_height = info_about_height[0][-2:]
        if info_about_height.startswith("0"):
            door_height_info = int(info_about_height[-1]) / 10
        else:
            door_height_info = int(info_about_height) / 10

    return door_height_info


# 判断防火门防火等级
def door_fm_entity(bbox, border_entity_info, text_cls):
    """
    Args:
        bbox:传入的门的外接矩形框
        border_entity_info:图层全量信息
        text_cls:文本信息
    Returns:
        门的防火等级
    """
    # text_cls = door_nearby_text(bbox, border_entity_info, extend_margin=1000)

    cls_dic = {"甲级": "JFM|甲", "乙级": "YFM|乙", "丙级": "BFM|丙"}
    door_fm_info = None
    if text_cls is None:
        return door_fm_info

    for key, value in cls_dic.items():
        if re.search(value, text_cls.extend_message):
            door_fm_info = key
            break
    return door_fm_info


# 判断门用途属性
def door_usage_entity(bbox, border_entity_info):
    """
    Args:
        bbox:传入的门的外接矩形框
        border_entity_info:图层全量信息
        extend_margin:文本信息
    Returns:
        门的用途属性
    """
    room_info = border_entity_info.room_info
    door_usage_info_str = "其他门"
    # 鉴于目前户门定义还是有问题，通过老函数逻辑判定是否是户门，是户门的不走门函数逻辑
    indoor_door_info_list = border_entity_info.special_info_dict.get('indoor_door_info_list', [])
    for door in indoor_door_info_list:
        if door is not None and bbox[:4] == door[:4]:
            # return '户门'
            door_usage_info_str = '户门'
    # 获得每个门的朝向线信息
    direction = get_door_direction_info_entity([bbox], border_entity_info)[0]
    # print('direction', direction)
    if direction and door_usage_info_str != '户门':
        usg_A, usg_B = "", ""
        point_A = direction[0:2]
        point_B = direction[2:4]
        Flag_A = 0  # 为A找到一个空间
        Flag_B = 0  # 为B 找到一个空间
        for room in room_info:
            # 对于多边形
            try:
                poly = room.contour.contour
                poly_obj = Polygon(poly.squeeze())  # shapely用法
                if not Flag_A:
                    if Point(point_A).within(poly_obj):
                        usg_A = "".join(room.name_list)
                        Flag_A = 1
                if not Flag_B:
                    if Point(point_B).within(poly_obj):
                        usg_B = "".join(room.name_list)
                        Flag_B = 1
                if Flag_A and Flag_B:
                    break
            except:
                continue
        # 因为目前有部分空间分割问题(图纸+空间分割技术问题)，导致玄关和卫生间连成一块，所以做出特别处理
        if re.search('玄关', usg_A):
            usg_A = ''.join(usg_A.split('卫生间'))
        if re.search('玄关', usg_B):
            usg_B = ''.join(usg_B.split('卫生间'))
        # 先判断单一侧房间即可决定门用途的。包括阳台之于阳台门，卫生间之于卫生间门，厨房之于厨房门，楼梯间之于楼梯间门，设备用房、管道井之于管井门
        determine_relationship = {"阳台门": "阳台", "卫生间门": "卫生间", "厨房门": "厨房", "楼梯间门": "楼梯间", "管井门": "设备|管道|管井"}
        for door, determine in determine_relationship.items():
            if re.search(determine, usg_A + usg_B):
                door_usage_info_str = door
                break
        if door_usage_info_str == "其他门":
            # 需要两侧一起参与判定的门：客厅|走道+卧室=卧室门，套内or玄关+非套内=户门，前室+非楼梯间=前室门，大堂+室外=单元门
            # 目前确定的排位顺序有：卧室门须在户门之前识别(针对卧室-走道门)，户门须在前室门之前识别(针对前室-玄关门)
            determine_relationship = {"卧室门": ["客厅|走道", True, "卧室", True],
                                      # "户门": ["套内空间|玄关", True, "套内空间|平面图建筑轮廓", False],
                                      "前室门": ["前室", True, "楼梯间", False], "单元门": ["大堂", True, "", True]}

            def match(pattern, string, not_reverse=True):
                result = True if re.search(pattern, string) else False
                return result if not_reverse else not result

            for door, determine in determine_relationship.items():
                if (match(determine[0], usg_A, determine[1]) and match(determine[2], usg_B, determine[3])) or \
                        (match(determine[0], usg_B, determine[1]) and match(determine[2], usg_A, determine[3])):
                    door_usage_info_str = door

                    break
    # print('[Debug] usg_A:{} usg_B:{} door_usage:{}'.format(usg_A, usg_B, door_usage_info_str))
    return door_usage_info_str, direction


# 获取门的朝向信息
def door_towards_direction_entity(bbox, border_entity_info):
    """
        Args:
            bbox:传入的门的外接矩形框
            border_entity_info:图层全量信息
        Returns:
            门的朝向：空间
        """
    room_info = border_entity_info.room_info
    cnt_bbox = get_contour_from_bbox(bbox)
    door_towards_info = None
    for room in room_info:
        if get_contours_iou(room.contour.contour, cnt_bbox) > 0.8:
            door_towards_info = "".join(room.name_list)
            break
    return door_towards_info


# 获取门的门扇类型
def door_leaf_number_entity(bbox, border_entity_info, kind="平开门"):
    """

    Args:
        bbox: 传入的门的外接矩形框
        border_entity_info: 图层全量信息
        kind: 门的类别

    Returns:
        门扇类型
    """
    attribute = None
    origin_border_entity_info = border_entity_info.origin_border_entity_info
    scale = border_entity_info.space_scale
    ratio = border_entity_info.ratio
    border_coord = border_entity_info.border_coord
    if kind == "平开门":
        circle_to_check = ['Ellipse', 'Circle']
        arc_to_check = ['Arc', 'Polyline', 'Polyline2d']
        layer_to_check = ["door", "window"]
        arc_info_dict = get_origin_border_entity_info_rule(origin_border_entity_info, layer_to_check,
                                                           arc_to_check, scale, border_coord, ratio)
        arc_info_list = []
        for layer, e_list in arc_info_dict.items():
            arc_info_list.extend(e_list)
        arc_info_list = [arc for arc in arc_info_list if len(arc) == 8]

        circle_info_dict = get_origin_border_entity_info_rule(origin_border_entity_info, layer_to_check,
                                                              circle_to_check, scale, border_coord, ratio)
        circle_info_list = []
        for layer, e_list in circle_info_dict.items():
            circle_info_list.extend(e_list)

        door_arc_list = arc_info_list + circle_info_list
        # 在bbox里面的arc
        arc_need = entity_in_bbox(door_arc_list, bbox)
        if len(arc_need) == 1:
            attribute = "单扇"
        elif len(arc_need) == 2:
            if arc_need[0][-2] == arc_need[-1][-2]:  # 半径相同
                attribute = "双扇"
            else:
                attribute = "子母"
        elif len(arc_need) >= 3:
            attribute = "多扇"
    # else:#推拉门

    return attribute


# 获取门的开启角度
def door_angle_entity(bbox, border_entity_info):
    """

    Args:
        bbox: 传入的门的外接矩形框
        border_entity_info: 图层全量信息

    Returns:
        门的开启角度
    """
    attribute = None
    angle = 0
    origin_border_entity_info = border_entity_info.origin_border_entity_info
    scale = border_entity_info.space_scale
    ratio = border_entity_info.ratio
    border_coord = border_entity_info.border_coord

    class_to_check = ['Arc']
    arc_info_list = \
        get_origin_border_entity_info_rule(origin_border_entity_info, ["door"], class_to_check, scale, border_coord,
                                           ratio)["door"]
    # 在bbox里面的arc
    arc_need = entity_in_bbox(arc_info_list, bbox)
    for arc in arc_need:
        angle_temp = arc[-1]
        angle = max(angle_temp, angle)
    if angle < 89:
        attribute = "小角"
    elif angle > 91:
        attribute = "大角"
    else:
        attribute = "直角"
    return attribute


def cross_point(line1, line2):
    """
    返回两线段所在直线的交点。若不相交，则返回None。
    Args:
        line1: 线段1，格式为[Point1.x, Point1.y, Point2.x, Point2.y]
        line2: 线段2，格式为[Point3.x, Point3.y, Point4.x, Point4.y]
    """

    def get_arg(line):
        # 由两点得直线的标准方程 ax+by=c
        x0, y0 = line[:2]
        x1, y1 = line[2:4]
        return y1 - y0, x0 - x1, x0 * y1 - y0 * x1

    a0, b0, c0 = get_arg(line1)
    a1, b1, c1 = get_arg(line2)
    dd = a0 * b1 - a1 * b0
    if abs(dd) < 1e-6:
        return None
    return (int((c0 * b1 - c1 * b0) / dd), int((a0 * c1 - a1 * c0) / dd))


def judge_evacuating_door(bbox, border_entity_info):
    """
    判断首层平面图的疏散外门
    Args:
        bbox: 门的bbox
        border_entity_info: 建筑底图的

    Returns:
        是否是疏散外门
    """
    room_info = border_entity_info.room_info
    plan_building_outline = None
    for room in room_info:
        if re.search('平面图建筑轮廓', ''.join(room.name_list)):
            plan_building_outline = room
            break
    if plan_building_outline is not None:
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        # 将门的外框向内缩小短边的1/4
        door_bbox_shrink = extend_margin(bbox, -min(w, h) // 4)

        if get_contours_iou(plan_building_outline.contour.contour, get_contour_from_bbox(door_bbox_shrink)) < 0.1:
            return True
        else:
            return False
    else:
        return False


def door_leaf_orientation(bbox, border_entity_info, kind="平开门"):
    """
    返回门扇侧点和非门扇侧点，由门扇侧指向非门扇侧。对于平开门而言，直线侧为门扇侧，另一侧为非门扇侧。
    Args:
        bbox: 传入的门的外接矩形框
        border_entity_info: 图层全量信息
        kind: 门的类别

    Returns:
        点集。形式为[point1,point2]，point1代表门扇侧，point2代表非门扇侧
    """
    points = [[], []]
    arc_to_check = ['Arc', 'Polyline', 'Polyline2d']
    circle_to_check = ['Ellipse', 'Circle']
    origin_border_entity_info = border_entity_info.origin_border_entity_info
    door_lists = list(
        map(lambda x: x.list, border_entity_info.single_line_door_window_list + border_entity_info.door_base_coords))
    scale = border_entity_info.space_scale
    ratio = border_entity_info.ratio
    border_coord = border_entity_info.border_coord
    arc_info_list = get_origin_border_entity_info_rule(origin_border_entity_info, ["door"], arc_to_check, scale,
                                                       border_coord, ratio)["door"]
    arc_info_list = [arc for arc in arc_info_list if len(arc_info_list) == 8]
    circle_info_list = get_origin_border_entity_info_rule(origin_border_entity_info, ["door"], circle_to_check, scale,
                                                          border_coord, ratio)["door"]
    door_arc_list = arc_info_list + circle_info_list

    # 在bbox里面的arc
    arc_need = entity_in_bbox(door_arc_list, bbox)
    bbox_extend = extend_margin(bbox, 5)
    # bbox对应的门连线
    single_line = list(filter(lambda x: line_overlap_poly(bbox_extend, x), door_lists))
    if (kind == '平开门') and arc_need and single_line:
        if len(arc_need) > 1:
            print('error_bbox:', bbox, 'error_arc:', arc_need)
            arc_need = [arc_need[0]]
        if len(single_line) > 1:  # 目前发现会出现两条门连线实际是一条直线，所以只需要选择1条
            print('error_bbox:', bbox, 'error_line:', single_line)
            single_line = [single_line[0]]

        single_line = single_line[0]
        arc_line = arc_need[0]
        # 因为门连线是画出来的，和弧线不相交，相差几个像素点，所以用线段所在直线交点解决
        arc_point = cross_point(single_line[:4], arc_line[:4])
        if arc_point:
            points[1] = (arc_point[0], arc_point[1])
            distance0 = point_euclidean_distance(single_line[:2], points[1])
            distance1 = point_euclidean_distance(single_line[2:4], points[1])
            points[0] = tuple(single_line[:2]) if distance0 > distance1 else tuple(single_line[2:4])
    return points


# 获取门是否需要消防连通控制
def door_xiaofang_control(bbox, border_entity_info):
    """

    Args:
        bbox: 传入的门的bbox
        border_entity_info: 图框全量信息

    Returns:
        更新了门消防连通控制属性的图框全量信息
    """
    # 获取空间信息
    need_control = False
    room_info = border_entity_info.room_info
    drawing_type = border_entity_info.drawing_type
    ####目前逻辑##################################################
    public_area_name_list = ['凹廊','大堂','电梯前室','独立前室','防烟楼梯前室','过廊',
                             '合用前室','连廊','楼梯间','门斗','其他前室','前厅','消防电梯前室','走道']
    public_area_list = []
    for room in room_info:
        for public_area_name in public_area_name_list:
            if re.search(public_area_name, " ".join(room.name_list)):
                public_area_list.append(room)
                # print("公共空间: ", room.name_list)
    # # 获取门朝向线信息
    door_orientation = get_door_direction_info_entity([bbox], border_entity_info)
    if door_orientation[0] == None:
        return False
    door_line = door_orientation[0][:4]
    # # 判断门朝向线和上述公共空间其中两个空间相交
    # count_p = 0
    # 如果只判断空间数量，那么一个空间可能有多个名字，导致出错
    # 因此改为判断门朝向线的是起终点是否分别在两个上述工区之内，如是则消防联动控制为True
    is_start_pt_in_public_area = False
    is_end_pt_in_public_area = False
    for room in public_area_list:
        if is_start_pt_in_public_area and is_end_pt_in_public_area:
            break
        # if line_overlap_poly(room.contour.contour, door_line):
        # 判端起点
        if not is_start_pt_in_public_area and Polygon(np.array(room.contour.contour).squeeze()).contains(Point(door_line[0], door_line[1])):
            # print("room_name: ", room.name_list)
            # count_p += 1
            is_start_pt_in_public_area = True
        # 判断终点
        if not is_end_pt_in_public_area and Polygon(np.array(room.contour.contour).squeeze()).contains(Point(door_line[2], door_line[3])):
            is_end_pt_in_public_area = True
    #print("is_start_pt_in_public_area, is_end_pt_in_public_area", is_start_pt_in_public_area, is_end_pt_in_public_area)
    if is_start_pt_in_public_area and is_end_pt_in_public_area:
        need_control = True
    ####初始逻辑##################################################
    # # 分别获取前室空间、走道空间、楼梯间、和其它空间
    # front_room = []
    # stair_room = []
    # zoudao = []
    # other_room = []
    # need_control = False
    # for room in room_info:
    #     if re.search("合用前室|独立前室|消防电梯前室", " ".join(room.name_list)):
    #         front_room.append(room.contour.contour)
    #         # print("前室: ", room.name_list)
    #     elif re.search("走道", " ".join(room.name_list)):
    #         zoudao.append(room.contour.contour)
    #         # print("走道: ", room.name_list)
    #     elif "楼梯间" in room.name_list:
    #         stair_room.append(room.contour.contour)
    #         # print("楼梯间: ", room.name_list)
    #     elif re.search("平面图建筑轮廓", " ".join(room.name_list)):
    #         continue
    #     elif re.search("楼梯间", " ".join(room.name_list)):
    #         continue
    #     else:
    #         other_room.append(room)
    # # 获取门朝向线信息
    # door_orientation = get_door_direction_info_entity([bbox], border_entity_info)
    # if door_orientation[0] == None:
    #     return False
    # door_line = door_orientation[0][:4]
    # # 判断朝向线是否和其它空间相交，若相交则不需要连通控制
    # for room in other_room:
    #     if line_overlap_poly(room.contour.contour, door_line):
    #         # print("room_name: ", room.name_list)
    #         need_control = False
    #         return need_control
    # # 判断门朝向线和前室、楼梯间、走道以及户外是否在其中两个空间相交
    # count_f = 0
    # for room in front_room:
    #     if line_overlap_poly(room, door_line):
    #         count_f += 1
    # count_s = 0
    # for room in stair_room:
    #     if line_overlap_poly(room, door_line):
    #         count_s += 1
    # count_z = 0
    # for room in zoudao:
    #     if line_overlap_poly(room, door_line):
    #         count_z += 1
    # # print(count_s, " ", count_z, " ", count_f)
    # if drawing_type in [DrawingType.INDOOR_FIRST_FLOOR]:
    #     if count_s > 1:
    #         return True
    # if count_f > 1 or count_s > 1 or count_z > 1 or count_f + count_s + count_z < 2:
    #     need_control = False
    # else:
    #     need_control = True
    return need_control


# 获取管径
def pipe_diameter_entity(line, border_entity_info):
    """

    Args:
        line: 传入的线
        border_entity_info:图层全量信息

    Returns:
        管径

    """
    # start_end_point_list
    bbox = get_line_coord_by_order(line)
    return_text_info = None
    pattern = "D[NE]?\d+"
    ratio = border_entity_info.ratio
    bbox_horizon = 400 * ratio[0]
    bbox_verticle = 1000 * ratio[0]
    all_text_list = border_entity_info.border_text_info_with_bound_vertex[TextType.ALL]
    # 得到所有文本的四个顶点坐标、长边倾斜角度、底边中点坐标、文本内容
    all_text_new_list = []
    for all_text in all_text_list:
        p1, p2, p3, p4 = all_text.bbox.list
        content = all_text.extend_message
        text_contour = np.array([[p1], [p2], [p3], [p4]])
        text_center = get_centroid(text_contour)
        # print('-----》》》》text_contour', text_contour)
        if point_euclidean_distance(p1, p2) > point_euclidean_distance(p2, p3):
            text_angle = getLineDeg([p1[0], p1[1], p2[0], p2[1]])
        else:
            text_angle = getLineDeg([p2[0], p2[1], p3[0], p3[1]])
        if re.search(pattern, content):
            all_text_new_list.append([[p1, p2, p3, p4], text_angle, text_center, content])
    line_angel = getLineDeg(line)
    min_distance = float("inf")
    point_A = get_centroid(bbox)
    bbox_temp = extend_rect_entity(bbox, line_ext=bbox_horizon, direction='long', double_side=(True, True))

    for text in all_text_new_list:
        point_B = get_centroid(text[0])
        distance_A_B = None
        # 文本方向应该与构件方向一致
        if abs(line_angel - text[1]) < 2:

            # 垂直构件
            if 89 <= abs(line_angel) <= 91:
                bbox_temp = extend_rect_entity(bbox_temp, line_ext=bbox_verticle, direction='short',
                                               double_side=(True, True))
                bbox_temp = get_bbox_from_contour_entity(np.array(bbox_temp))
                if Iou_temp(bbox_temp, text[0]):
                    distance_A_B = abs(point_A[0] - point_B[0])
            # 水平构件
            elif 0 <= abs(line_angel) <= 1:
                bbox_temp = extend_rect_entity(bbox_temp, line_ext=bbox_verticle, direction='short',
                                               double_side=(True, True))
                bbox_temp = get_bbox_from_contour_entity(np.array(bbox_temp))
                if Iou_temp(bbox_temp, text[0]):
                    distance_A_B = abs(point_A[1] - point_B[1])
            # 倾斜构件
            else:
                text_cnt = get_contour_from_bbox(text[0])
                if get_contours_iou(bbox_temp, text_cnt):
                    distance_A_B = abs(point_A[1] - point_B[1])

            if distance_A_B is not None and distance_A_B < min_distance:
                min_distance = distance_A_B
                return_text_info = eval(re.search("\d+", text[-1]).group())

    return return_text_info


# 获取用地红线
def get_red_line_entity(border_entity_info):
    """

    Args:
        border_entity_info: 图层全量信息

    Returns:
        用地红线信息

    """
    space_scale = border_entity_info.space_scale
    border_coord = border_entity_info.border_coord
    ratio = border_entity_info.ratio
    origin_border_entity_info = border_entity_info.origin_border_entity_info

    class_to_check_road = ["Line", 'Polyline', 'Polyline2d', 'Arc']
    if 'red_line' in origin_border_entity_info.keys():  # 用地红线
        layer_to_check = ['red_line']
        # 从origin_border_entity_info转换并提取line/arc在png中坐标
        entity_info_all = get_origin_border_entity_info_rule(origin_border_entity_info, layer_to_check,
                                                             class_to_check_road,
                                                             space_scale, border_coord, ratio)
        red_line_info = entity_info_all.get(layer_to_check[0])
    else:
        layer_to_check = ['red_line_sub']  # 红线图层
        entity_info_all = get_origin_red_line_info_pre(
            origin_border_entity_info, layer_to_check, class_to_check_road, space_scale, border_coord, ratio)
        red_line_info = entity_info_all.get(layer_to_check[0])

    return red_line_info


# 扩大bbox用于合并
def extend_margin_by_direction_entity(bbox, margin, direction='left_right'):
    """

    Args:
        bbox: 构件外接矩形框
        margin: 外扩间距
        direction: 外扩方向

    Returns:
        外扩后的矩形框
    """
    if direction == 'left_right':
        return [bbox[0] - margin, bbox[1], bbox[2] + margin, bbox[3]]
    elif direction == "up":
        return [bbox[0], bbox[1] - margin, bbox[2], bbox[3]]
    elif direction == "down":
        return [bbox[0], bbox[1], bbox[2], bbox[3] + margin]
    elif direction == "left":
        return [bbox[0] - margin, bbox[1], bbox[2], bbox[3]]
    elif direction == "right":
        return [bbox[0], bbox[1], bbox[2] + margin, bbox[3]]
    else:
        return [bbox[0], bbox[1] - margin, bbox[2], bbox[3] + margin]


# 获取倾斜矩形的最小外接矩形
def get_bbox_from_coord_entity(coord):
    """

    Args:
        coord: 图形坐标

    Returns:
        矩形框
    """
    point_sorted_x = sorted(coord, key=lambda x: x[0])
    point_sorted_y = sorted(coord, key=lambda x: x[1])

    return [point_sorted_x[0][0], point_sorted_y[0][1], point_sorted_x[-1][0], point_sorted_y[-1][1]]


# 返回一个轮廓的最小外接矩形
def get_bbox_from_contour_entity(contour):
    """

    Args:
        contour: 轮廓

    Returns:
        最小外接矩形框

    """
    x, y, w, h = cv2.boundingRect(contour)

    return [x, y, x + w, y + h]


def get_ordered_point_entity(rect):
    """

    Args:
        rect: four point of a rectangle, lean rect or bbox shape

    Returns:
        按照顺序排列的四个点坐标
    """
    #### 先判断是否是正矩形 ####
    if len(rect) == 1:
        point_left, point_up, point_right, point_down = rect[0], rect[0], rect[0], rect[0]
    elif len(rect) == 2:
        rect = sorted(rect, key=lambda x: x[0])
        k = get_point_skew(rect[0], rect[1])
        if k <= 0:
            point_left, point_up, point_right, point_down = rect[0], rect[1], rect[1], rect[0]
        else:
            point_left, point_up, point_right, point_down = rect[0], rect[0], rect[1], rect[1]

    elif len(rect) == 4:
        normal = judgment_rectangle(rect)
        x = [x[0] for x in rect]
        y = [y[1] for y in rect]
        if normal:
            point_left = [min(x), max(y)]
            point_up = [min(x), min(y)]
            point_right = [max(x), min(y)]
            point_down = [max(x), max(y)]
        else:
            point_sorted_x = sorted(rect, key=lambda x: x[0])
            point_sorted_y = sorted(rect, key=lambda x: x[1])

            point_left = point_sorted_x[0]
            point_right = point_sorted_x[-1]
            point_up = point_sorted_y[0]
            point_down = point_sorted_y[-1]
    else:
        print('输入的格式有问题请检查！！！')
        return None

    return [point_left, point_up, point_right, point_down]


# 外扩矩形
def extend_rect_entity(lean_rect, line_ext=100, direction='long', double_side=(True, True)):
    """
    外扩矩形的长边或短边，支持按 短边/长边 上边/下边
    Param:
        lean_rect: four point of a rectangle
        line_ext: abs length value for long-side to extend
        direction: str, 'long' or 'short'
        double_side: (True, True), 是否上面扩，是否下面扩
    Return:
        extended four point of a rectangle
    """

    # 倾斜矩形的顶点排序：最左侧，最上侧，最右侧，最下侧
    point_left, point_up, point_right, point_down = get_ordered_point_entity(lean_rect)

    # 计算最左侧的顶点与最上侧的顶点的连线的斜率
    if list(point_left) != list(point_up):
        skew = get_point_skew(point_left, point_up)
    else:
        skew = 1 / (get_point_skew(point_right, point_up) + 0.001)

    # get length in right triangle
    y_ext = line_ext / np.sqrt(1 + skew * skew)
    x_ext = np.sqrt(line_ext * line_ext - np.power(y_ext, 2))

    if y_ext < 0:
        x_ext = - x_ext

    y_ext = int(y_ext)
    x_ext = int(x_ext)

    if point_euclidean_distance(point_up, point_left) > point_euclidean_distance(point_up, point_right):
        # bbox here is height < width
        if direction == 'long':
            if double_side[0]:
                point_up = [point_up[0] - x_ext, point_up[1] - y_ext]
                point_left = [point_left[0] - x_ext, point_left[1] - y_ext]

            if double_side[1]:
                point_right = [point_right[0] + x_ext, point_right[1] + y_ext]
                point_down = [point_down[0] + x_ext, point_down[1] + y_ext]

        elif direction == 'short':
            if double_side[0]:
                point_up = [point_up[0] + y_ext, point_up[1] - x_ext]
                point_right = [point_right[0] + y_ext, point_right[1] - x_ext]
            if double_side[1]:
                point_down = [point_down[0] - y_ext, point_down[1] + x_ext]
                point_left = [point_left[0] - y_ext, point_left[1] + x_ext]
        else:
            print('illegal direction')
            return lean_rect

    else:  # bbox here is height > width
        if direction == 'long':
            if double_side[0]:  # bbox right side here is up
                point_up = [point_up[0] + y_ext, point_up[1] - x_ext]
                point_right = [point_right[0] + y_ext, point_right[1] - x_ext]
            if double_side[1]:  # bbox left side here is down
                point_down = [point_down[0] - y_ext, point_down[1] + x_ext]
                point_left = [point_left[0] - y_ext, point_left[1] + x_ext]

        elif direction == 'short':
            if double_side[0]:
                point_up = [point_up[0] - x_ext, point_up[1] - y_ext]
                point_left = [point_left[0] - x_ext, point_left[1] - y_ext]
            if double_side[1]:
                point_down = [point_down[0] + x_ext, point_down[1] + y_ext]
                point_right = [point_right[0] + x_ext, point_right[1] + y_ext]
        else:
            print('illegal direction')
            return lean_rect

    return [list(map(int, point)) for point in [point_left, point_up, point_right, point_down]]


def get_outside_lianlang_contour(border_entity_info):
    """
    :param border_entity_info:图框全量信息
    :return: 开敞的连廊的轮廓数组
    """
    open_lianlang_cnt_list = []

    room_info = border_entity_info.room_info

    border_coord = border_entity_info.border_coord
    ratio = border_entity_info.ratio
    space_scale = border_entity_info.space_scale
    origin_border_entity_info = border_entity_info.origin_border_entity_info
    # 获取栏杆构件的线
    layer_to_check = ['elevation_handrail']
    class_to_check = ['Line', 'Polyline', 'Polyline2d']
    rail_line_dict = get_origin_border_entity_info_rule(origin_border_entity_info,
                                                        layer_to_check,
                                                        class_to_check, space_scale,
                                                        border_coord, ratio)
    rail_line_list = []
    for layer, entity_list in rail_line_dict.items():
        rail_line_list.extend(entity_list)
    rail_line_list = list(filter(lambda x: len(x) == 4, rail_line_list))
    # 查找有栏杆的连廊
    for room in room_info:
        room_cnt = room.contour.contour
        if re.search("连廊", " ".join(room.name_list)):
            for line in rail_line_list:
                ext_line = extend_margin(line, 20)
                ext_line_cnt = get_contour_from_bbox(ext_line)
                if get_contours_iou(room_cnt, ext_line_cnt) > 0:
                    open_lianlang_cnt_list.append(room_cnt)
                    break
    return open_lianlang_cnt_list


# 窗的属性 是否为外窗 适用于'普通窗', '转角窗', '门联窗','凸窗', '剖面窗'
def judge_outside_window_entity(win_bbox, border_entity_info, window_kind='普通窗'):
    """
    :param bbox: 窗户的bbox
    :param border_entity_info:
    :return: 窗户是否是外窗
    """
    room_info = border_entity_info.room_info
    ratio = border_entity_info.ratio
    outer_window_bbox_list = border_entity_info.special_info_dict.get('outer_window_bbox_list', [])
    all_text_info = border_entity_info.border_text_info[TextType.ALL]
    # 通风排烟平面图用到独立前室|楼梯间|合用前室的外窗属性
    pattern = "客厅|卧室|厨房|卫生间|书房|储藏室|衣帽间|独立前室|楼梯间|合用前室|主卧|次卧"
    space_text_list = [text.bbox.list for text in all_text_info if re.search(pattern, text.extend_message)]
    ext_margin = int(1000 * ratio[0])
    outside_attributes = 0

    # 开敞的连廊cnt_list
    open_lianlang_cnt_list = get_outside_lianlang_contour(border_entity_info)

    if win_bbox in outer_window_bbox_list:
        outside_attributes = 1
        return outside_attributes

    # 获取窗对象相邻的两侧空间，如果其中一侧不与任何空间相邻，则该窗对象为外窗，属性值为1，否则属性值为0
    if window_kind in ['普通窗', '转角窗', '门联窗']:
        # 窗户沿着长边进行外扩
        w, h = win_bbox[2] - win_bbox[0], win_bbox[3] - win_bbox[1]
        if w > h:
            left_ext_region = extend_margin_by_direction_entity(win_bbox, ext_margin, direction='up')
            right_ext_region = extend_margin_by_direction_entity(win_bbox, ext_margin, direction='down')
        else:
            left_ext_region = extend_margin_by_direction_entity(win_bbox, ext_margin, direction='left')
            right_ext_region = extend_margin_by_direction_entity(win_bbox, ext_margin, direction='right')
        left_ext_region = get_contour_from_bbox(left_ext_region)
        right_ext_region = get_contour_from_bbox(right_ext_region)
        left_connect = False
        right_connect = False
        for room in room_info:
            ignore_room = False
            if re.search("天井|屋面|平面图建筑轮廓", " ".join(room.name_list)):
                continue
            room_con = room.contour.contour
            for open_room_cnt in open_lianlang_cnt_list:
                if get_contours_iou(open_room_cnt, room_con) > 0.5:
                    ignore_room = True
                    break
            if ignore_room:
                continue
            if get_contours_iou(room_con, left_ext_region) > 0.3:
                left_connect = True
            if get_contours_iou(room_con, right_ext_region) > 0.3:
                right_connect = True
        if not left_connect or not right_connect:
            outside_attributes = 1
    # 在墙身大样图中获取窗图层内容，保留合并后尺寸宽度小于500mm的窗bbox，长边外扩2400，底部短边外扩1100mm范围内有空间文本，判断为是外窗，属性值为1，否则属性值为0
    elif window_kind in ['凸窗', '剖面窗']:
        longside_shift_length = int(1200 * ratio[0])
        shortside_shift_length = int(1100 * ratio[1])
        # 窗户长边各外扩1.2米, 下底边外扩1.1米, 上底边不外扩
        window_region = [win_bbox[0] - longside_shift_length,
                         win_bbox[1],
                         win_bbox[2] + longside_shift_length,
                         win_bbox[3] + shortside_shift_length]
        # 若外扩区域与外窗文本相交, 则该窗为外窗
        have_space_text = False
        for text_info in space_text_list:
            if bbox_intersect_bbox_object(text_info[:4], window_region):
                have_space_text = True
                break
        if have_space_text:
            outside_attributes = 1
    return outside_attributes


# 窗的防火等级属性值判断
def judge_window_fire_proof_entity(win_bbox, border_entity_info, window_kind='普通窗'):
    """
    :param win_bbox: 窗户的bbox
    :param border_entity_info: 图框信息综合
    :param window_kind: 窗户类型
    :return: 防火等级
    """
    # 获取窗构件的外接矩形，四周外扩3m范围内查找是否含“FC *”+4
    # 位数字的文本，若该文本中含有：
    # ①“甲”文本，属性值为甲级
    # ②“乙”文本，属性值为乙级
    # ③不属于以上两种情况的，属性值为丙级
    if window_kind not in ['普通窗', '转角窗', '凸窗']:
        return None
    ratio = border_entity_info.ratio
    all_text_info = border_entity_info.border_text_info[TextType.ALL]
    ext_winbbox = extend_margin(win_bbox, int(ratio[0] * 3000))
    pattern = "FC.*\d{4}"
    fire_proof_level = "丙级"
    for text in all_text_info:
        text_bbox, text_message = text.bbox.list, text.extend_message
        if Iou_temp(ext_winbbox, text_bbox) > 0 and re.search(pattern, text_message):
            if "甲" in text_message:
                fire_proof_level = "甲级"
                break
            if "乙" in text_message:
                fire_proof_level = "乙级"
                break
    return fire_proof_level


def window_numbering_entity(win_bbox, border_entity_info, window_kind='普通窗'):
    """
    :param win_bbox: 窗户的bbox
    :param border_entity_info: 图框信息综合
    :param window_kind: 窗户类型
    :return: 窗户编号
    """
    # 适用对象：普通窗、转角窗、凸窗、立面窗
    # 实现流程：
    # 获取窗构件的外接矩形，将其沿与长边垂直的方向两边外扩1m，在该范围内查找是否与含“C *”+4
    # 位数字的文本相交，将文字书写方向与长边方向平行的文本整体作为窗构件的编号
    ratio = border_entity_info.ratio
    # 窗户的外扩范围
    WINDOW_EXTEND = 1000
    window_number = None
    if window_kind not in ['普通窗', '转角窗', '凸窗', '立面窗', '门联窗', '百叶']:
        return window_number
    # 窗户中心
    win_center = get_centroid(win_bbox)
    # 文本
    all_text_info = border_entity_info.border_text_info[TextType.ALL]
    all_text_list = [text.bbox.list + [text.extend_message] for text in all_text_info]
    f_text_list = get_f_text_list(all_text_list)
    extend_win_box = extend_margin(win_bbox, int(WINDOW_EXTEND * ratio[0]))
    # bgy二层平面图C11，倾斜普通窗，按照长边垂直方向找不到
#    extend_win_box = extend_margin_by_side_object(win_bbox, int(WINDOW_EXTEND * ratio[0]), 'long')
    min_dis = float('inf')
    for text in all_text_info:
        text_bbox, text_message = text.bbox.list, text.extend_message
        text_center = get_centroid(text_bbox)
        if Iou_temp(extend_win_box, text_bbox) > 0 and re.search(LIMIAN_NUMBER_PATTERN, text_message):
            dis_win_text = point_euclidean_distance(text_center, win_center)
            if dis_win_text < min_dis:
                window_number = text_message
                min_dis = dis_win_text
    win_dis = float('inf')
    f_win_number = None
    for f_text in f_text_list:
        f_center, f_message = f_text[:4], f_text[-1]
        dis_f_text = point_euclidean_distance(f_center, win_center)
        if dis_f_text < win_dis:
            f_win_number = f_message
            win_dis = dis_f_text
    if win_dis < min_dis:
        window_number = f_win_number

    return window_number


##获取窗户的宽度和高度属性
def window_width_height_entity(win_bbox, border_entity_info, window_kind='普通窗'):
    """
    :param win_bbox: 窗户的bbox
    :param border_entity_info: 图框信息综合
    :param window_kind: 窗户类型
    :return: 窗户的宽和高
    """
    win_width = None
    win_height = None
    if window_kind not in ['普通窗', '转角窗', '凸窗', '立面窗', '门联窗']:
        return win_width, win_height
    window_number = window_numbering_entity(win_bbox, border_entity_info, window_kind)
    if window_number is not None:
        if re.search(r'\d{2}[a-z]?\d{2}', window_number):
            num_str = re.search(r'\d{2}[a-z]?\d{2}', window_number).group()
            if re.search('[a-z]', window_number):
                num = num_str.replace(re.search('[a-z]', window_number).group(), '')
                win_width = int(num[:2]) / 10
                win_height = int(num[2:]) / 10
            if re.search(r'\d{4}', window_number):
                num = re.search(r'\d{4}', window_number).group()
                win_width = int(num[:2]) / 10
                win_height = int(num[2:]) / 10

    return win_width, win_height


def get_door_direction_info_entity(
        door_bbox_list, border_entity_info, default_len=810, shorter_line=False, img_debug=None):
    '''
    获取每个门的朝向信息
    Param:
        door_bbox_list: 需要获取朝向的所有门构件, list, [[x1,y1,x2,y2], ...]
        border_entity_info: 包含该图框所有信息的一个字典
        default_len：默认的朝向线的长度
        shorter_line：是否使用较短的朝向线
        img_debug：用于debug的图片
    Return:
        direction_info: 包含每个门构件的朝向线和方向角的列表,
                        list, [[x1,y1,x2,y2,deg], ...]
    '''
    # 由于现在获取的门的bbox是remove_margin之后的，所以需要margin添加回来，再获取其土建连线
    ext_margin = border_entity_info.ext_margin
    ext_door_bbox_list = [extend_margin(bbox, 2 * ext_margin) for bbox in door_bbox_list]

    ratio = border_entity_info.ratio
    # 朝向线过滤短于0.5米的(门的土建宽度一般在0.8米左右)
    door_base_coords = [l.list for l in border_entity_info.door_base_coords if
                        line_length_in_reality(l.list, ratio) >= 0.5]

    # 对门的朝向线的半长进行初始化，可以用于倾斜的门；对于水平或竖直的门，再根据门的长宽和朝向线的方向将朝向线长度调小
    # 之所以将朝向线的长度尽量调小，是因为朝向线会用来判断是否与某个区域相交，若区域很小，朝向线会贯穿该区域，并与另一个区域相交
    r = float(default_len * ratio[0])

    direction_info = []

    for door_bbox in ext_door_bbox_list:
        width_door = door_bbox[2] - door_bbox[0]
        height_door = door_bbox[3] - door_bbox[1]
        door_base = None
        direction_line = None

        # 匹配出门的土建连线
        intercept_length = 0
        for l in door_base_coords:
            inter_line = line_intercept_by_poly(l, door_bbox)
            if inter_line is None and point_in_bbox(l[:2], door_bbox) and point_in_bbox(l[2:], door_bbox):
                inter_line = l
            if inter_line is not None:
                length = line_length_in_reality(inter_line, ratio)
                if length > intercept_length:
                    door_base = l[:]
                    intercept_length = length

        if door_base is None:
            direction_info.append(None)
            continue

        # 可视化匹配的土建连线，用于debug
        if img_debug is not None:
            cv2.line(img_debug, tuple(door_base[:2]), tuple(door_base[2:4]),
                     (0, 0, 255), 5)

        # 门的中心点
        x0, y0 = get_centroid(door_bbox)

        k, _ = getLineParam(door_base)
        # if img is not None:
        #     # debug
        #     cv2.line(img, (door_base[0], door_base[1]), (door_base[2], door_base[3]), (180, 105, 255), 3)
        # 门的土建连线为竖直的(门的朝向线为水平的)
        if k is None:
            if shorter_line:
                r = float(width_door / 2 + 150 * ratio[0])
            direction_line = [int(x0 - r), y0, int(x0 + r), y0]
        # 门的土建连线为水平的(门的朝向线为竖直的)
        elif k == 0:
            if shorter_line:
                r = float(height_door / 2 + 150 * ratio[0])
            direction_line = [x0, int(y0 - r), x0, int(y0 + r)]
        # 门的土建连线是倾斜的(门的朝向线也是倾斜的)，此时朝向线的半长用默认的值
        else:
            # 门的朝向线的斜率
            kk = -1.0 / k
            alpha = 1.0 / math.sqrt(1 + kk ** 2)
            if kk > 0:
                dx = alpha * r
                dy = alpha * kk * r
                direction_line = [int(x0 - dx), int(y0 - dy),
                                  int(x0 + dx), int(y0 + dy)]

            else:
                dx = alpha * r
                dy = -1 * alpha * kk * r
                direction_line = [int(x0 - dx), int(y0 + dy),
                                  int(x0 + dx), int(y0 - dy)]

        direction_info.append(direction_line + [getLineDeg(direction_line)])

    return direction_info


# # 得到线段的轮廓表示
def get_line_coord_by_order_entity(bbox):
    """

    Args:
        bbox: 矩形框

    Returns:
        四个点的坐标
    """
    return [[bbox[0], bbox[1]], [bbox[2], bbox[3]], [bbox[2], bbox[3]], [bbox[0], bbox[1]]]


# 判断一个四边形是否是正矩形
def judgment_rectangle_entity(rect):
    """
    #### 判断一个四边形是否是正矩形###
    :param rect: [[],[],[],[]]
    :return: bool
    """
    side1 = [np.array(rect[1]), np.array(rect[0])]
    side2 = [np.array(rect[3]), np.array(rect[0])]
    angle = int(angle_between_segment2(side1, side2))
    k1 = get_point_skew(rect[0], rect[1])
    k2 = get_point_skew(rect[0], rect[3])
    ####### 2条边一条是水平另一条是竖直的 ########
    if ((abs(k1) > 100 and abs(k2) < 0.1) or (abs(k1) < 0.1 and abs(k2) > 100)) and abs(90 - angle) < 5:
        return True
    else:
        return False


def get_window_attribute_entity(bbox, border_entity_info):
    """
    获取立面窗属性
    Args:
        bbox: 外接矩形框
        border_entity_info: 图框全量信息

    Returns:
        window_devide: 门窗分隔档数
        window_attri: 门窗属性
        open_num: 开扇数量
    """

    # 返回结果字典
    result = dict()
    # 图框基本信息
    ratio = border_entity_info.ratio
    space_scale = border_entity_info.space_scale
    border_coord = border_entity_info.border_coord
    # 标记对象化信息
    mark_object_dict = border_entity_info.mark_object_dict
    # 图框高宽比
    height = border_entity_info.image_manager.img_height
    width = border_entity_info.image_manager.img_width
    # 底图
    img_whole = np.zeros((height, width), dtype="uint8")
    # 获取箭头标记
    arrow_list = border_entity_info.mark_object_dict["箭头"]

    # 获取里面窗内的图元信息
    origin_border_entity_info = border_entity_info.origin_border_entity_info
    class_to_check = ["Line", "Polyline", "Polyline2d"]
    layer_to_check = ["door", "window", "wall"]
    line_dict = get_origin_border_entity_info_rule(origin_border_entity_info, layer_to_check,
                                                   class_to_check, space_scale, border_coord, ratio)
    line_list_ori = []
    for _, value in line_dict.items():
        line_list_ori.extend(value)
    line_list = [line for line in line_list_ori if len(line) == 4]

    # 获取bbox里的图元
    line_need = entity_in_bbox(line_list, bbox)
    for line in line_need:
        cv2.line(img_whole, tuple(line[:2]), tuple(line[2:4]), 255, 2)

    # 查找每个窗户的内轮廓
    edges = cv2.Canny(img_whole, 20, 255)
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (14, 20), (-1, -1))

    # 闭运算，连接有间隙的轮廓
    opened = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, element, iterations=1)

    # Find contours
    if '3.4' in cv2.__version__:
        _, contours_tree, hierarchy = cv2.findContours(opened, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours_tree, hierarchy = cv2.findContours(opened, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    holes = [contours_tree[i] for i in range(len(contours_tree)) if hierarchy[0][i][3] >= 0]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    seg_contours_ori = []
    for hole in holes:
        new_contour = contour_morphology(hole, kernel, cv2.MORPH_CLOSE)
        seg_contours_ori.append(new_contour)

    # cv2.imwrite("/Users/zhengcijie/bgy.png", img_whole)
    # 过滤掉错误的较小门窗
    seg_contours = []
    for contour in seg_contours_ori:
        bbox = get_bbox_from_contour(contour)
        min_length = min(bbox[2] - bbox[0], bbox[3] - bbox[1])
        if min_length > 160 * ratio[0]:
            seg_contours.append(contour)

    # 查找带线型类型的开闭线图元
    open_layer_to_check = ["elevation_window_open_line"]
    open_line_list = get_origin_border_entity_info_with_style_rule(origin_border_entity_info, open_layer_to_check,
                                                                   class_to_check, space_scale, border_coord, ratio)[
        "elevation_window_open_line"]
    # 取门窗水平线，查找最左上端的基准点
    base_line = [100, 100, 200, 100]
    horiz_line = []
    for line in line_need:
        horiz_line.append(line[:2])
        horiz_line.append(line[2:])
    horiz_line.sort(key=lambda x: x[1])
    horiz_line.sort(key=lambda x: x[0])
    if horiz_line:
        base_point = horiz_line[0][:2]
    else:
        base_point = bbox[:2]
    # print("base point: ", base_point)

    # 获取相对基准点的轮廓信息，轮廓中心点信息以及每一扇的开启方式、类型的信息
    relative_contours = []
    contour_attr = []
    open_num = 0
    center_list = []
    for contour in seg_contours:
        abs_bbox = get_bbox_from_contour(contour)
        contour_attr = []
        # 轮廓中心点
        center = get_centroid(contour)
        center_list.append(center)
        # 相对中心点
        relative_center = tuple([center[0] - base_point[0], center[1] - base_point[1]])
        # 相对轮廓坐标
        relative_contour = contour - base_point
        result[relative_center] = [relative_contour, abs_bbox]
        # 获取开启类型和方向
        has_type = False
        for line in open_line_list:
            if line_overlap_poly(line[0], contour):
                if re.search("DASH", line[1]):
                    contour_attr = ["pingkai", "inside"]
                else:
                    contour_attr = ["pingkai", "outside"]
                open_num += 1
                has_type = True
                result[relative_center].extend(contour_attr)
                break
        if has_type:
            continue
        for arrow in arrow_list:
            arrow_bbox = arrow.bounding_rectangle.list
            arrow_cnt = get_contour_from_bbox(arrow_bbox)
            if get_contours_iou(contour, arrow_cnt) > 0.5:
                contour_attr = ["tuila", None]
                result[relative_center].extend(contour_attr)
                has_type = True
                break
        if has_type:
            continue
        contour_attr = ["fixed", None]

        result[relative_center].extend(contour_attr)

    # 计算门窗分隔道数
    # 矩形框的高和宽
    bbox_height = bbox[3] - bbox[1]
    bbox_width = bbox[2] - bbox[0]

    # 轮廓中心点按照竖向进行排序
    center_list.sort(key=lambda x: x[1])
    line_ver = []
    line_hor = []
    # 获取水平方向穿过轮廓中心点的间隔
    if len(center_list) != 0:
        line_hor = [[base_point[0], center_list[0][1], base_point[0] + bbox_width, center_list[0][1]]]
        cur_point = center_list[0][1]
        for i in range(1, len(center_list)):
            if abs(cur_point - center_list[i][1]) < 10:
                continue
            else:
                cur_point = center_list[i][1]
                line_hor.append([base_point[0], cur_point, base_point[0] + bbox_width, cur_point])

    center_list.sort(key=lambda x: x[0])
    if len(center_list) != 0:
        line_ver = [[center_list[0][0], base_point[1], center_list[0][0], base_point[1] + bbox_height]]
        cur_point = center_list[0][0]
        for i in range(1, len(center_list)):
            if abs(cur_point - center_list[i][0]) < 10:
                continue
            else:
                cur_point = center_list[i][0]
                line_hor.append([cur_point, base_point[1], cur_point, base_point[1] + bbox_height])
    # print("line_v: ", line_ver)
    # print("line_h: ", line_hor)
    #
    # print("contour num: ", len(seg_contours))
    # 计算竖直向最大档数
    max_h = 0
    for line in line_hor:
        tmp = 0
        for contour in seg_contours:
            if line_overlap_poly(contour, line):
                tmp += 1
        max_h = max(max_h, tmp)
    # 计算水平向最大档数
    max_v = 0
    for line in line_ver:
        tmp = 0
        for contour in seg_contours:
            if line_overlap_poly(contour, line):
                tmp += 1
        max_v = max(max_v, tmp)
    # print("max_h: ", max_h, " max_v: ", max_v)
    return [max_v, max_h], result, open_num


def get_inside_window(bbox, border_entity_info):
    """
    获取每个立面窗内的小窗面
    Args:
        bbox: 外接矩形框
        border_entity_info: 图框全量信息
    Returns:
        inside_windows: 小窗面的集合
    """
    all_inside_windows = border_entity_info.special_info_dict.get('inside_li_mian', [])
    inside_windows = []
    for inside_window in all_inside_windows:
        if Iou_temp(inside_window, bbox) > 0.5:
            inside_windows.append(inside_window)
    return inside_windows


def get_door_open_region_contour(bbox, border_entity_info):
    """
    获取平开门的开启范围
    :param bbox: 平开门的bbox
    :param border_entity_info: 图框全量信息
    :return: door_open_region_contour，开启范围
    """
    border_coord = border_entity_info.border_coord
    space_scale = border_entity_info.space_scale
    ratio = border_entity_info.ratio
    image_manager = border_entity_info.image_manager
    height, width = image_manager.img_height, image_manager.img_width
    background_image = np.zeros((height, width, 3), dtype=np.uint8)  # 绘制底图
    origin_border_entity_info = border_entity_info.origin_border_entity_info

    # 首先获取所有门的弧线图元
    check_layer = ['door', 'window', 'elevator_door', 'emergency_door']
    arc_entity_list = list()
    class_to_check = ['Polyline', 'Polyline2d', 'Arc', 'Ellipse']
    arc_info_dict = get_origin_border_entity_info_rule(origin_border_entity_info, check_layer,
                                                       class_to_check, space_scale, border_coord, ratio)
    for layer, entity_list in arc_info_dict.items():
        arc_entity_list.extend(entity_list)
    # Polyline中有line，需要过滤
    arc_entity_list = list(filter(lambda x: len(x) == 8 or len(x) == 11, arc_entity_list))

    arc_in_list = entity_in_bbox(arc_entity_list, bbox)
    for entity in arc_in_list:
        if len(entity) == 8:
            st_point = entity[0:2]  # 起点坐标
            end_point = entity[2:4]  # 终点坐标
            center_point = entity[4:6]  # 圆心坐标
            cv2.line(background_image, tuple(st_point), tuple(center_point), (255, 255, 255), 1)
            cv2.line(background_image, tuple(end_point), tuple(center_point), (255, 255, 255), 1)

            radius = entity[-2]  # 半径
            arc_angle = entity[-1]  # 圆心角
            st_vector = center_point + st_point  # 起点和圆心组成向量
            end_vector = center_point + end_point  # 终点和圆心组成向量

            # 角度小于10度的弧线画直线
            if abs(arc_angle) < 10:
                cv2.line(background_image, tuple(st_point), tuple(end_point), (255, 255, 255), 1)
            else:
                # 角度在180左右的弧线单独处理，根据经验这种角的起始点和终止点是解析正确的
                if 170 < abs(arc_angle) < 190:
                    if arc_angle > 0:
                        st_vector = end_vector
                    start_vector_angle = get_png_vector_angle(st_vector)
                # 根据经验其他角的起始点和终止点可能是解析错误的，所以首先对起始点和终止点进行一步额外的判定
                else:
                    start_vector_angle = get_png_vector_angle(st_vector)  # 获取角度
                    end_vector_angle = get_png_vector_angle(end_vector)  # 获取角度
                    if start_vector_angle > end_vector_angle:
                        start_vector_angle, end_vector_angle = end_vector_angle, start_vector_angle

                    if abs(end_vector_angle - start_vector_angle - abs(arc_angle)) > 20:
                        start_vector_angle, end_vector_angle = end_vector_angle, start_vector_angle + 360

                # 画图是以起始点的角度开始，画出圆心角大小的圆弧
                cv2.ellipse(background_image, tuple(center_point), (radius, radius), start_vector_angle, 0,
                            abs(arc_angle), (255, 255, 255), 1)
        elif len(entity) == 11:
            x1, y1, x2, y2, center_x, center_y, long_radius, short_radius, angle, start_angle, end_angle = entity
            center_point = [center_x, center_y]
            arc_angle = end_angle - start_angle
            st_point = [x1, y1]  # 起点坐标
            end_point = [x2, y2]  # 终点坐标
            cv2.line(background_image, tuple(st_point), tuple(center_point), (255, 255, 255), 1)
            cv2.line(background_image, tuple(end_point), tuple(center_point), (255, 255, 255), 1)

            # 角度小于10度的弧线画直线
            if abs(arc_angle) < 10:
                cv2.line(background_image, (x1, y1), (x2, y2), (255, 255, 255), 1)
            else:
                # 首先找到png坐标系中真正的起始角度和终止角度
                start_vector = center_point + [x1, y1]  # 起点和圆心组成向量
                end_vector = center_point + [x2, y2]  # 起点和圆心组成向量
                start_vector_angle = get_png_vector_angle(start_vector)  # 获取角度
                end_vector_angle = get_png_vector_angle(end_vector)  # 获取角度
                if start_vector_angle > end_vector_angle:
                    start_vector_angle, end_vector_angle = end_vector_angle, start_vector_angle

                if abs(end_vector_angle - start_vector_angle - arc_angle) > 20:
                    start_vector_angle, end_vector_angle = end_vector_angle, start_vector_angle + 360

                # 用cad中的起始角度（png中的终止角度）验证长轴方向向量起始角的正确性
                st_angle_cad = angle - start_angle
                angle_diff = abs(st_angle_cad - end_vector_angle)
                angle_diff = angle_diff - angle_diff // 360 * 360
                if angle_diff > 20:
                    angle = angle + 180
                st_angle = start_vector_angle - angle
                cv2.ellipse(background_image, tuple(center_point), (long_radius, short_radius), angle, st_angle,
                            st_angle + arc_angle, (255, 255, 255), 1)

    gray = cv2.cvtColor(background_image, cv2.COLOR_BGR2GRAY)
    del background_image
    gc.collect()
    edges = cv2.Canny(gray, 20, 255)
    del gray
    gc.collect()
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5), (-1, -1))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, element, iterations=1)
    del edges
    gc.collect()
    # 提取轮廓
    if '3.4' in cv2.__version__:
        _, contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    del closed
    gc.collect()
    door_open_region_contour = contours[0] if len(contours) > 0 else None

    return door_open_region_contour


def get_breaker_pole(bbox, border_entity_info):
    """
    获取断路器极数
    Args:
        bbox: 外接矩形框
        border_entity_info: 图框全量信息
    Returns:
        pole: 极数
    """
    ratio = border_entity_info.ratio
    breaker_bbox = [bbox[0], bbox[1] - int(1000 * ratio[0]), bbox[2], bbox[3]] # 断路器向上外扩
    text_all = border_entity_info.border_text_info[TextType.ALL]
    text_pole = [i for i in text_all if re.search(r'\/\dP', i.extend_message)]
    breaker_parameter_tmp = []
    pole = ''
    for text in text_pole:
        if Iou_temp(text.bbox.list, breaker_bbox):
            breaker_parameter_tmp.append(text)
    breaker_parameter_tmp.sort(key=lambda x: x.bbox.list[1])
    if breaker_parameter_tmp:
        pole = breaker_parameter_tmp[-1].extend_message.split('/')[-1]
    return pole


def get_power_system(pole):
    """
    Args:
        pole: 断路器极数
    Returns:
        power_system: 电源制式
    """
    power_system = ""
    if pole:
        if pole[0] in ['1', '2']:
            power_system = "单相"
        elif pole[0] in ['3', '4']:
            power_system = '三相'
    return power_system


def get_door_base_line_entity(door_bbox, border_entity):
    door_base_line_dict = border_entity.special_info_dict.get('door_base_line_dict', {})
    return door_base_line_dict.get(tuple(door_bbox), None)


def get_door_direction_line_entity(door_bbox, border_entity):
    door_direction_line_dict = border_entity.special_info_dict.get('door_direction_line_dict', {})
    return door_direction_line_dict.get(tuple(door_bbox), None)


def rectify_oblique_rooms(oblique_household_img):
    """
    计算户型或公共空间的倾斜角度
    :param oblique_household_img: 倾斜的户型图或公共空间图
    :return: rotation_angle，户型或公共空间的倾斜角度
    """
    rotation_angle = 0
    gray = cv2.cvtColor(oblique_household_img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 0)
    if len(lines[0]) == 0:
        return rotation_angle
    for rho, theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
    if x1 == x2 or y1 == y2:
        return rotation_angle
    t = float(y2 - y1) / (x2 - x1)
    rotation_angle = math.degrees(math.atan(t))
    if rotation_angle > 45:
        rotation_angle = -90 + rotation_angle
    elif rotation_angle < -45:
        rotation_angle = 90 + rotation_angle
    return rotation_angle


def rotate_contour(contour, rotation_angle, img_h_w):
    """
    将一个轮廓绕图片中心点进行旋转
    :param contour: 原始轮廓
    :param rotation_angle: 旋转角度
    :param img_h_w: 图片的高和宽
    :return: cnt_cp，旋转之后的轮廓
    """
    height, width = img_h_w
    png_cent_x, png_cent_y = [width // 2, height // 2]
    cnt_cp = contour.copy()
    for i in range(cnt_cp.shape[0]):
        x2, y2 = png_cent_x, png_cent_y
        x1, y1 = list(cnt_cp[i][0])
        # 将图像坐标转换到平面坐标
        y1 = height - y1
        y2 = height - y2
        x = int((x1 - x2) * np.cos(np.pi / 180.0 * rotation_angle) -
                (y1 - y2) * np.sin(np.pi / 180.0 * rotation_angle) + x2)
        y = int((x1 - x2) * np.sin(np.pi / 180.0 * rotation_angle) +
                (y1 - y2) * np.cos(np.pi / 180.0 * rotation_angle) + y2)
        # 将平面坐标转换到图像坐标
        y = height - y
        cnt_cp[i][0] = np.array([x, y])
    return cnt_cp


def neighbours(y_origin, x_origin, image):
    """
    定义像素周围的八个相邻点
    :param y_origin: 参考点行坐标
    :param x_origin: 参考点列坐标
    :param image: 图片
    :return: 八个相邻点的像素值
    """
    # print('--> ', (x_origin, y_origin))
    x_1, y_1, x1, y1 = y_origin - 1, x_origin - 1, y_origin + 1, x_origin + 1
    return [image[x_1][x_origin], image[x_1][y1], image[y_origin][y1], image[x1][y1],
            image[x1][x_origin], image[x1][y_1], image[y_origin][y_1], image[x_1][y_1]]


def transitions(neighbours):
    """
    计算邻域中像素从0变化到1的次数
    :param neighbours: 八个相邻点的像素值
    :return: 邻域中像素从0变化到1的次数
    """
    n = neighbours + neighbours[0:1]
    return sum((n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]))


def zhang_suen(image):
    """
    Zhang-Suen 细化算法
    :param image: 原始图片
    :return: 细化之后的图片
    """
    image_thinned = image.copy()
    changing1 = changing2 = 1
    while changing1 or changing2:
        changing1 = []
        rows, columns = image_thinned.shape
        for x in range(1, rows - 1):
            for y in range(1, columns - 1):
                p2, p3, p4, p5, p6, p7, p8, p9 = n = neighbours(x, y, image_thinned)
                if (image_thinned[x][y] == 1 and 2 <= sum(n) <= 6 and transitions(n) == 1 and
                        p2 * p4 * p6 == 0 and p4 * p6 * p8 == 0):
                    changing1.append((x, y))
        for x, y in changing1:
            image_thinned[x][y] = 0
        changing2 = []
        for x in range(1, rows - 1):
            for y in range(1, columns - 1):
                p2, p3, p4, p5, p6, p7, p8, p9 = n = neighbours(x, y, image_thinned)
                if (image_thinned[x][y] == 1 and 2 <= sum(n) <= 6 and transitions(n) == 1 and
                        p2 * p4 * p8 == 0 and p2 * p6 * p8 == 0):
                    changing2.append((x, y))
        for x, y in changing2:
            image_thinned[x][y] = 0
    return image_thinned


def get_nearby_points_coords(point):
    """
    获取参考点周围八个点的坐标
    :param point: 参考点
    :return: 八个邻域点的坐标
    """
    x, y = point
    return [[x, y-1], [x+1, y-1], [x+1, y], [x+1, y+1], [x, y+1], [x-1, y+1], [x-1, y], [x-1, y-1]]


def rotate_point(point, rotation_angle, img_h_w):
    """
    将一个点绕图片中心点进行旋转
    :param point: 原始点坐标
    :param rotation_angle: 旋转角度
    :param img_h_w: 图片的高和宽
    :return: point_new，旋转之后的点
    """
    height, width = img_h_w
    png_cent_x, png_cent_y = [width // 2, height // 2]
    x2, y2 = png_cent_x, png_cent_y
    x1, y1 = point
    # 将图像坐标转换到平面坐标
    y1 = height - y1
    y2 = height - y2
    x = int((x1 - x2) * np.cos(np.pi / 180.0 * rotation_angle) -
            (y1 - y2) * np.sin(np.pi / 180.0 * rotation_angle) + x2)
    y = int((x1 - x2) * np.sin(np.pi / 180.0 * rotation_angle) +
            (y1 - y2) * np.cos(np.pi / 180.0 * rotation_angle) + y2)
    # 将平面坐标转换到图像坐标
    y = height - y
    point_new = [x, y]
    return point_new


def get_cross_point_list_pre(poly_1, poly_2, use_buffer=True):
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


def get_room_end_points(room_contour, img_h_w):
    """
    获取一个空间的所有中心线端点
    :param room_contour: 空间轮廓
    :param img_h_w: 图框高、宽
    :return: end_inter_point_list_origin，空间的中心线端点
    :return: cnt_center_line_origin，空间的中心线轮廓
    """
    height, width = img_h_w
    room_contour_cp = room_contour.copy()

    # # for debug
    # img_bg = np.zeros((height, width, 3), dtype=np.uint8)
    # cv2.fillPoly(img_bg, [room_contour], (255, 255, 255))
    # cv2.imwrite('test.png', img_bg)
    x_origin, y_origin, w_origin, h_origin = cv2.boundingRect(room_contour_cp)
    center_origin = [x_origin + w_origin // 2, y_origin + h_origin // 2]
    img_size = int(1.5 * max(w_origin, h_origin))
    img_origin = np.zeros((img_size, img_size, 3), dtype=np.uint8)
    room_contour_cp[:, :, 0] -= center_origin[0]
    room_contour_cp[:, :, 0] += img_size // 2
    room_contour_cp[:, :, 1] -= center_origin[1]
    room_contour_cp[:, :, 1] += img_size // 2

    cv2.fillPoly(img_origin, [room_contour_cp], (255, 255, 255))
    rotation_angle = rectify_oblique_rooms(img_origin)
    rectified_img_origin = ndimage.rotate(img_origin, rotation_angle, reshape=False)
    room_contour_rotated = rotate_contour(room_contour_cp, rotation_angle, (img_size, img_size))
    x_rotated, y_rotated, w_rotated, h_rotated = cv2.boundingRect(room_contour_rotated)
    room_contour_rotated[:, :, 0] -= x_rotated
    room_contour_rotated[:, :, 0] += 100
    room_contour_rotated[:, :, 1] -= y_rotated
    room_contour_rotated[:, :, 1] += 100
    room_contour_rotated_poly = Polygon(room_contour_rotated.squeeze())
    room_contour_rotated_poly = room_contour_rotated_poly.convex_hull

    rectified_img_origin_new = rectified_img_origin[y_rotated-100:y_rotated+h_rotated+100, x_rotated-100:x_rotated+w_rotated+100]
    img_size_max = max(w_rotated+200, h_rotated+200)

    scale = 4
    while img_size_max // scale > 500:
        scale *= 2
    img_resized = cv2.resize(rectified_img_origin_new, ((w_rotated+200) // scale, (h_rotated+200) // scale))
    image = Image.fromarray(cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)).convert('L')
    img_original = filters.median(image, disk(5))
    bw_original = img_original > 10

    bw_skeleton = zhang_suen(bw_original)
    bw_skeleton = np.invert(bw_skeleton)
    bw_skeleton = bw_skeleton + 0

    skeleton = np.zeros((bw_skeleton.shape[0], bw_skeleton.shape[1], 3), np.uint8)
    for i in range(bw_skeleton.shape[0]):
        for j in range(bw_skeleton.shape[1]):
            if bw_skeleton[i][j] == 0:
                skeleton[i][j] = 255, 255, 255

    skeleton_resized = cv2.resize(skeleton, ((w_rotated+200), (h_rotated+200)), interpolation=cv2.INTER_NEAREST)
    gray = cv2.cvtColor(skeleton_resized, cv2.COLOR_BGR2GRAY)
    _, thres = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    if "3.4" in cv2.__version__:
        _, contours, hierarchy = cv2.findContours(thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, hierarchy = cv2.findContours(thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt_center_line = contours[0] if len(contours) > 0 else None

    end_points = []
    all_points_origin = []
    for y in range(1, bw_skeleton.shape[0] - 1):
        for x in range(1, bw_skeleton.shape[1] - 1):
            if bw_skeleton[y][x] == 0:
                all_points_origin.append([x, y])
                ns = neighbours(y, x, bw_skeleton)
                if sum(ns) == 7:
                    end_points.append([x, y])

    near_end_points = []
    for point in end_points:
        p_list = [point]
        # 找到临近的第五个点的坐标
        for i in range(5):
            p_ref = p_list[-1]
            ns = neighbours(p_ref[1], p_ref[0], bw_skeleton)
            neighbour_coords = get_nearby_points_coords(p_ref)
            idx_list = np.where(np.array(ns) == 0)[0]
            p_to_add_list = [neighbour_coords[idx] for idx in idx_list if neighbour_coords[idx] not in p_list]
            p_list.append(p_to_add_list[0])
        near_end_points.append(p_list[-1])

    end_points = (np.array(end_points) * scale).tolist()
    near_end_points = (np.array(near_end_points) * scale).tolist()
    all_points = (np.array(all_points_origin) * scale).tolist()

    # 和空间轮廓的交点
    end_inter_point_list = []
    for e_p, n_e_p in zip(end_points, near_end_points):
        x = n_e_p[0] + (e_p[0] - n_e_p[0]) * 10
        y = n_e_p[1] + (e_p[1] - n_e_p[1]) * 10
        end_line_poly = LineString([[x, y], [n_e_p[0], n_e_p[1]]])
        inter_point_list = get_cross_point_list_pre(end_line_poly, room_contour_rotated_poly, use_buffer=False)
        end_inter_point = [[int(p[0]), int(p[1])] for p in inter_point_list if [int(p[0]), int(p[1])] != n_e_p][0]
        end_inter_point_list.append(end_inter_point)

    end_points = np.array(end_points)
    end_points[:, 0] += (x_rotated - 100)
    end_points[:, 1] += (y_rotated - 100)
    end_points = end_points.tolist()
    end_inter_point_list = np.array(end_inter_point_list)
    end_inter_point_list[:, 0] += (x_rotated - 100)
    end_inter_point_list[:, 1] += (y_rotated - 100)
    end_inter_point_list = end_inter_point_list.tolist()
    if cnt_center_line is not None:
        cnt_center_line[:, :, 0] += (x_rotated - 100)
        cnt_center_line[:, :, 1] += (y_rotated - 100)

    # # for debug
    # if cnt_center_line is not None:
    #     cv2.fillPoly(rectified_img_origin, [cnt_center_line], (0, 255, 255))
    # for e_p, e_i_p in zip(end_points, end_inter_point_list):
    #     cv2.line(rectified_img_origin, tuple(e_p), tuple(e_i_p), (0, 255, 255), 10)
    # cv2.imwrite('cnt_center_line_rectified.png', rectified_img_origin)  # for debug

    cnt_center_line_rotated = rotate_contour(cnt_center_line, -rotation_angle, (img_size, img_size))
    end_inter_point_list_rotated = []
    end_point_list_rotated = []
    for e_p, e_i_p in zip(end_points, end_inter_point_list):
        e_p_new = rotate_point(e_p, -rotation_angle, (img_size, img_size))
        end_point_list_rotated.append(e_p_new)
        e_i_p_new = rotate_point(e_i_p, -rotation_angle, (img_size, img_size))
        end_inter_point_list_rotated.append(e_i_p_new)
        # cv2.line(img_origin, tuple(e_p_new), tuple(e_i_p_new), (0, 255, 255), 10)  # for debug

    # # for debug
    # cv2.fillPoly(img_origin, [cnt_center_line_rotated], (0, 255, 255))
    # cv2.imwrite('cnt_center_line_img_origin.png', img_origin)

    end_inter_point_list_origin = []
    end_point_list_origin = []
    for e_p_rotated, e_i_p_rotated in zip(end_point_list_rotated, end_inter_point_list_rotated):
        x_new_e_i_p = e_i_p_rotated[0] - img_size // 2 + center_origin[0]
        y_new_e_i_p = e_i_p_rotated[1] - img_size // 2 + center_origin[1]
        x_new_e_p = e_p_rotated[0] - img_size // 2 + center_origin[0]
        y_new_e_p = e_p_rotated[1] - img_size // 2 + center_origin[1]
        end_inter_point_list_origin.append([x_new_e_i_p, y_new_e_i_p])
        end_point_list_origin.append([x_new_e_p, y_new_e_p])

        # # for debug
        # cv2.line(img_bg, tuple([x_new_e_p, y_new_e_p]), tuple([x_new_e_i_p, y_new_e_i_p]), (0, 255, 255), 10)

    cnt_center_line_origin = cnt_center_line_rotated.copy()
    cnt_center_line_origin[:, :, 0] -= img_size // 2
    cnt_center_line_origin[:, :, 0] += center_origin[0]
    cnt_center_line_origin[:, :, 1] -= img_size // 2
    cnt_center_line_origin[:, :, 1] += center_origin[1]
    # # for debug
    # cv2.fillPoly(img_bg, [cnt_center_line_origin], (0, 255, 255))
    # for p in end_inter_point_list_origin:
    #     cv2.circle(img_bg, tuple(p), 5, (0, 255, 0), -1)
    # cv2.imwrite('cnt_center_line_img_bg.png', img_bg)

    return end_inter_point_list_origin, cnt_center_line_origin


def get_anzhu_number(entity_object, border_entity):
    """
    获取结构暗柱的名称编号
    :param entity_object:
    :param border_entity:
    :return:
    """
    name_number = None
    ratio = border_entity.ratio
    anzhu_contour = entity_object.contour.contour
    anzhu_bbox = entity_object.bounding_rectangle.list
    if anzhu_contour is None:
        return name_number
    yinzhu_obj_list = border_entity.mark_object_dict['引注']
    print(f'---> num {len(yinzhu_obj_list)} yinzhu found !')
    yinzhu_candidate_list = [yinzhu for yinzhu in yinzhu_obj_list if re.search('[GY]BZ', ''.join(yinzhu.labeled_text))]
    for yinzhu in yinzhu_candidate_list:
        start_point = yinzhu.annotation_start_point
        start_point_area = [start_point[0] - 2, start_point[1] - 2,
                            start_point[0] + 2, start_point[1] + 2]
        if get_contours_iou(anzhu_contour, get_contour_from_bbox(start_point_area)) > 0:
            name_number = yinzhu.labeled_text
            break

    if name_number is None:
        extend_range = int(800 * ratio[0])
        az_ext_bbox = [anzhu_bbox[0] - extend_range, anzhu_bbox[1] - extend_range,
                       anzhu_bbox[2] + extend_range, anzhu_bbox[3] + extend_range]
        all_text_info = border_entity.border_text_info[TextType.ALL]
        need_text_list = [text for text in all_text_info if re.search('[GY]BZ', text.extend_message)]
        candidate_text_list = [text for text in need_text_list if Iou_temp(text.bbox.list, az_ext_bbox) > 0]
        # 找到暗柱的质心
        cent = None
        if len(anzhu_contour) < 3:
            cenx = anzhu_contour[:,0,0].mean()
            ceny = anzhu_contour[:,0,1].mean()
            cent = tuple(map(int, [cenx, ceny]))
        else:
            cen = Polygon(anzhu_contour.squeeze()).centroid
            cent = tuple(map(int, [cen.x, cen.y]))
        min_dist = float('inf')
        for candidate_text in candidate_text_list:
            candidate_text_bbox = candidate_text.bbox.list
            text_center = [(candidate_text_bbox[0] + candidate_text_bbox[2]) // 2,
                           (candidate_text_bbox[1] + candidate_text_bbox[3]) // 2]
            if point_euclidean_distance(cent, text_center) < min_dist:
                min_dist = point_euclidean_distance(cent, text_center)
                name_number = candidate_text.extend_message

    return name_number


def get_zongjin_attribs(search_area, candidate_text_list):
    """
    在目标区域寻找文本以得到纵筋的相关属性
    :param search_area:
    :param candidate_text_list:
    :return:
    """
    zongjin_num = []
    zongjin_diameter = []
    for zongjin_text in candidate_text_list:
        zongjin_text_bbox = zongjin_text.bbox.list
        if Iou_temp(zongjin_text_bbox, search_area) > 0:
            text_content = zongjin_text.extend_message
            text_partial_list = re.split('\+', text_content)
            for text_partial in text_partial_list:
                text_partial_before = re.split('%%132', text_partial)[0]
                text_partial_after = re.split('%%132', text_partial)[1]
                zongjin_num.append(eval(text_partial_before))
                zongjin_diameter.append(eval(text_partial_after))

    return zongjin_num, zongjin_diameter


def get_gujin_attribs(search_area, candidate_text_list):
    """
    在目标区域寻找文本以得到箍筋的相关属性
    :param search_area:
    :param candidate_text_list:
    :return:
    """
    gujin_diameter = []
    gujin_distance = []
    for gujin_text in candidate_text_list:
        gujin_text_bbox = gujin_text.bbox.list
        if Iou_temp(gujin_text_bbox, search_area) > 0:
            text_content = gujin_text.extend_message
            text_partial_list = re.split('\+', text_content)
            for text_partial in text_partial_list:
                text_partial_before = re.split('@', text_partial)[0]
                text_partial_after = re.split('@', text_partial)[1]
                num_list_before = re.findall('\d+', text_partial_before)
                num_list_after = re.findall('\d+', text_partial_after)
                gujin_diameter.append(eval(num_list_before[-1]))
                gujin_distance.append(eval(num_list_after[0]))

    return gujin_diameter, gujin_distance


def get_qiangshen_number(entity_object, border_entity):
    """
    获取结构墙身的名称编号
    :param entity_object:
    :param border_entity:
    :return:
    """
    name_number = None
    ratio = border_entity.ratio
    qiangshen_contour = entity_object.contour.contour
    qiangshen_bbox = entity_object.bounding_rectangle.list
    if qiangshen_contour is None:
        return name_number
    all_text_info = border_entity.border_text_info[TextType.ALL]
    need_text_list = [text for text in all_text_info if re.search('未.*注明.*墙[身体]均[为按]', text.extend_message)]
    if len(need_text_list) > 0:
        need_text = need_text_list[0]
        text_content = need_text.extend_message
        name_number_candidate = re.split('均[为按]', text_content)[1]
        if re.search('Q', name_number_candidate):
            name_number = name_number_candidate
            print('---> 未注明墙身均为: ', name_number)
    # 先在墙身引线或者墙身旁边查找
    yinzhu_obj_list = border_entity.mark_object_dict['引注']
    print(f'---> num {len(yinzhu_obj_list)} yinzhu found !')
    yinzhu_candidate_list = [yinzhu for yinzhu in yinzhu_obj_list if re.search('Q[-_]?\d', ''.join(yinzhu.labeled_text))]
    yinzhu_ok = False
    for yinzhu in yinzhu_candidate_list:
        start_point = yinzhu.annotation_start_point
        start_point_area = [start_point[0] - 2, start_point[1] - 2,
                            start_point[0] + 2, start_point[1] + 2]
        if get_contours_iou(qiangshen_contour, get_contour_from_bbox(start_point_area)) > 0:
            name_number = yinzhu.labeled_text
            yinzhu_ok = True
            break
    if not yinzhu_ok:
        if qiangshen_bbox is None:
            return name_number
        extend_range = int(600 * ratio[0])
        # 沿短边方向外扩
        if abs(qiangshen_bbox[0] - qiangshen_bbox[2]) > abs(qiangshen_bbox[1] - qiangshen_bbox[3]):  # 水平
            qs_ext_bbox = [qiangshen_bbox[0], qiangshen_bbox[1] - extend_range,
                           qiangshen_bbox[2], qiangshen_bbox[3] + extend_range]
        else:
            qs_ext_bbox = [qiangshen_bbox[0] - extend_range, qiangshen_bbox[1],
                           qiangshen_bbox[2] + extend_range, qiangshen_bbox[3]]

        cadidate_text_list = [text for text in all_text_info if re.search('Q[-_]?\d', text.extend_message)]
        target_text_list = [text for text in cadidate_text_list if Iou_temp(text.bbox.list, qs_ext_bbox) > 0]
        # 找到墙身的质心
        cen = Polygon(qiangshen_contour.squeeze()).centroid
        cent = tuple(map(int, [cen.x, cen.y]))
        min_dist = float('inf')
        for candidate_text in target_text_list:
            candidate_text_bbox = candidate_text.bbox.list
            text_center = [(candidate_text_bbox[0] + candidate_text_bbox[2]) // 2,
                           (candidate_text_bbox[1] + candidate_text_bbox[3]) // 2]
            if point_euclidean_distance(cent, text_center) < min_dist:
                min_dist = point_euclidean_distance(cent, text_center)
                name_number = candidate_text.extend_message

    return name_number


def get_intersect_area_table(name_num_bbox, target_bbox, table_bbox):
    """
    找到相交区域
    :param name_num_bbox:
    :param target_bbox:
    :param table_bbox:
    :return:
    """
    intersect_bbox = None
    if name_num_bbox is None or target_bbox is None:
        return intersect_bbox
    if target_bbox[1] > name_num_bbox[1]:
        candidate_bbox1 = [name_num_bbox[0], name_num_bbox[1], name_num_bbox[2], table_bbox[3]]
        candidate_bbox2 = [target_bbox[0], target_bbox[1], table_bbox[2], target_bbox[3]]
    else:
        candidate_bbox1 = [target_bbox[0], target_bbox[1], table_bbox[2], target_bbox[3]]
        candidate_bbox2 = [name_num_bbox[0], name_num_bbox[1], table_bbox[2], name_num_bbox[3]]

    intersect_min = list((max(candidate_bbox1[i], candidate_bbox2[i]) for i in range(0, 2)))
    intersect_max = list((min(candidate_bbox1[i], candidate_bbox2[i]) for i in range(2, 4)))
    intersect_bbox = intersect_min + intersect_max

    return intersect_bbox


def get_qiangshen_bar_info(bar_text):
    """
    从目标文本中拿到筋信息
    :param bar_text:
    :return:
    """
    diameter = []
    distance = []
    if re.search('/', bar_text):
        text_partial_list = re.split('/', bar_text)
        for text_partial in text_partial_list:
            if re.search('@', text_partial):
                text_partial_before = re.split('@', text_partial)[0]
                text_partial_after = re.split('@', text_partial)[1]
                num_list_before = re.findall(r"\d+", text_partial_before)
                num_list_after = re.findall(r"\d+", text_partial_after)
                if len(num_list_before) > 0:
                    diameter.append(eval(num_list_before[0]))
                if len(num_list_after) > 0:
                    distance.extend([eval(num_list_after[0]), eval(num_list_after[0])])
            else:
                num_list = re.findall(r"\d+", text_partial)
                if len(num_list) > 0:
                    diameter.append(eval(num_list[0]))
    else:
        text_partial_before = re.split('@', bar_text)[0]
        text_partial_after = re.split('@', bar_text)[1]
        num_list_before = re.findall(r"\d+", text_partial_before)
        num_list_after = re.findall(r"\d+", text_partial_after)
        if len(num_list_before) > 0:
            diameter = [eval(num_list_before[0])]
        if len(num_list_after) > 0:
            distance = [eval(num_list_after[0])]

    return diameter, distance


def find_max_contour(contour_list):
    """
    :param contour_list: 轮廓列表
    :return: 面积最大的轮廓
    """

    if not contour_list:
        return []
    contour_list = sorted(contour_list, key=lambda x: cv2.contourArea(x), reverse=True)
    max_contour = contour_list[0]
    return max_contour


def get_ban_peijin_lines(border_entity):
    """
    拿到所有板的配筋线
    :param border_entity:
    :return:
    """
    ban_peijin_line_dict = defaultdict(list)
    ratio = border_entity.ratio
    all_text = border_entity.border_text_info[TextType.ALL]
    height, width = border_entity.image_manager.img_height, border_entity.image_manager.img_width
    # debug
    # img_without_wall = border_entity.image_manager.load_from_manager('border_image_with_wall')
    # 拿到所有的板构件
    ban_obj_list = border_entity.entity_object_dict['结构板']
    print(f'Note: num {len(ban_obj_list)} ban found !!')
    if len(ban_obj_list) == 0:
        return ban_peijin_line_dict
    origin_border_entity_info = border_entity.origin_border_entity_info
    space_scale = border_entity.space_scale
    ratio = border_entity.ratio
    border_coord = border_entity.border_coord
    layer_to_check = ['other_layers', 'beam', 'pillar', 'wall']
    class_to_check = ["Line", 'Polyline', 'Polyline2d']
    entity_info_info_dic = get_origin_border_entity_info_rule(origin_border_entity_info, layer_to_check,
                                                              class_to_check,
                                                              space_scale, border_coord, ratio)
    line_list = []
    for layer, entity_list in entity_info_info_dic.items():
        line_list.extend(entity_list)
    # Polyline中有arc，需要过滤
    line_list = list(filter(lambda x: len(x) == 4, line_list))
    print('Note: candidate line num: {}'.format(len(line_list)))
    wall_thickness_pixel = int(200 * ratio[0])

    for ban_obj in ban_obj_list:
        background = np.zeros((height, width, 3), dtype=np.uint8)
        ban_contour = ban_obj.contour.contour
        ban_bbox = ban_obj.bounding_rectangle.list
        cv2.fillPoly(background, [ban_contour], (255, 255, 255))

        gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        kernel_size = int(wall_thickness_pixel) + 3
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        image = cv2.morphologyEx(gray, cv2.MORPH_ERODE, kernel)
        # Find contours
        if '3.4' in cv2.__version__:
            _, contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            continue
        final_contour = find_max_contour(contours)
        # cv2.fillPoly(img_without_wall, [final_contour], (255, 255, 255), 1)
        for line in line_list:
            if line_intercept_by_poly(line, final_contour):
                # 过滤掉所有相交叉的线
                xiaojiao = False
                for _line in ban_peijin_line_dict[ban_obj]:
                    if get_segment_cross_point(_line, line):
                        ban_peijin_line_dict[ban_obj].remove(_line)
                        xiaojiao = True
                if xiaojiao is True:
                    continue
                # 过滤掉周围没有文本的线
                has_text = False
                ext_range = int(250 * ratio[0])
                if abs(line[2] - line[0]) < 3:  # 竖直
                    line_bbox = [line[0] - ext_range, line[1], line[2] + ext_range, line[3]]
                else:
                    line_bbox = [line[0], line[1] - ext_range, line[2], line[3] + ext_range]

                for text in all_text:
                    text_bbox = text.bbox.list
                    if Iou_temp(text_bbox, line_bbox) > 0:
                        ban_peijin_line_dict[ban_obj].append(line)
                        # cv2.line(img_without_wall, (line[0], line[1]), (line[2], line[3]), (180, 105, 255), 5)
                        has_text = True
                        break
                # 考虑到小短斜线
                if not has_text:
                    line_length_ = line_length(line)
                    ban_short_line = min(abs(ban_bbox[2] - ban_bbox[0]), abs(ban_bbox[3] - ban_bbox[1]))
                    if line_length_ < ban_short_line:
                        ban_peijin_line_dict[ban_obj].append(line)
                        # cv2.line(img_without_wall, (line[0], line[1]), (line[2], line[3]), (180, 105, 255), 5)

    # cv2.imwrite("ban.png", img_without_wall)

    return ban_peijin_line_dict


def get_breaker_hu(bbox, border_entity_info):
    """
    获取断路器极数
    Args:
        bbox: 外接矩形框
        border_entity_info: 图框全量信息
    Returns:
        pole: 极数
    """
    ratio = border_entity_info.ratio
    breaker_bbox = bbox # 断路器向上外扩
    peidianxiang_zitu_list = [room for room in border_entity_info.room_info if "配电箱子图" in room.name_list]
    text_all = [text.bbox.list + [text.extend_message] for text in border_entity_info.border_text_info[TextType.ALL]]
    text_pole = [i for i in text_all if re.search('^户型', i[-1])]
    fina_text = None
    for text in text_pole:
        if "配电箱系统图" in text[-1]:
            fina_text = text
            break
        else:
            text = get_joint_bbox(text, text_all, ratio)
            if "配电箱系统图" in text[-1]:
                fina_text = text
                break
            #默认系统图字样和户型字样在一排
    belong_hu = ""
    for peidianxiang_zitu in peidianxiang_zitu_list:
        bbox_peidian = peidianxiang_zitu.bbox.list
        text_info = None
        if fina_text:
            text_bbox = fina_text[:4]
            if Iou_temp(remove_margin(bbox_peidian, margin= int(2000*ratio[0])), text_bbox):
                text_info = fina_text[-1]

        if text_info:
            extend_bbox = remove_margin(bbox_peidian, margin= int(5000*ratio[0]))
            if Iou_temp(extend_bbox, breaker_bbox) and text_info:
                belong_hu = text_info

    return belong_hu


def get_joint_bbox(center_bbox, border_text_info, ratio):
    """
    Param:
        center_bbox: 待比较的中心文本框, type: list, [x1, y1, x2, y2, 'text']
        border_text_info: 解析出的图框所有文本信息
    Return:
        merged_bbox: 合并后的文本框, type: list, [x1, y1, x2, y2, 'text']
    """
    left_bboxes_list, right_bboxes_list = list(), list()
    left_merged_bbox = list()
    merged_bbox = list()
    # print("border_text_info:", border_text_info)
    x1, _, x2, _ = center_bbox[0], center_bbox[1], center_bbox[2], center_bbox[3]
    distance = (x2 - x1) / len(center_bbox[-1]) * 10
    for _, text_info in enumerate(border_text_info):
        if abs(text_info[1] - center_bbox[1]) < 300 * ratio[0]:   # 纵坐标相同
            print(text_info)
            # 文本框在center_bbox左边
            if text_info[2] <= x2 and text_info[0] < x1 and abs(x1 - text_info[0]) < 6 * distance:
                left_bboxes_list.append(text_info)
            # 文本框在center_bbox右边
            if text_info[0] >= x1  and text_info[2] > x2 and abs(text_info[0] - x2) < 6 * distance:
                right_bboxes_list.append(text_info)

    if left_bboxes_list:
        left_bboxes_list.sort(key=lambda x: x[0], reverse=True)  # 横坐标降序排列
        # 合并文本框
        for text_info in left_bboxes_list:
            # 横坐标差距——30个字符宽度
            if abs(text_info[2] - center_bbox[0]) < distance:
                # 合并center_bbox和text_info文本框
                temp_bbox = [text_info[0], text_info[1], center_bbox[2], center_bbox[3],
                             text_info[-1] + center_bbox[-1]]
                center_bbox = temp_bbox
        left_merged_bbox = center_bbox
    else:
        left_merged_bbox = center_bbox

    if right_bboxes_list:
        right_bboxes_list.sort(key=lambda x: x[0], reverse=False)  # 横坐标升序排列
        for text_info in right_bboxes_list:
            # 横坐标差距——10个字符宽度
            if abs(text_info[0] - left_merged_bbox[2]) < 2 * distance:
                # 合并left_merged_bbox和text_info文本框
                temp_bbox = [left_merged_bbox[0], left_merged_bbox[1], text_info[2], text_info[3],
                             left_merged_bbox[-1] + text_info[-1]]
                left_merged_bbox = temp_bbox
        merged_bbox = left_merged_bbox
    else:
        merged_bbox = left_merged_bbox

    return merged_bbox


def get_entity_label_number(bbox, border_entity_info, extend_margin=1800, map_label=None):
    """
    获取构件编号
    Args:
        bbox: contour
        border_entity_info:
        extend_margin:
        map_label: 匹配附近编号的正则
    Returns:
    匹配的属性
    """
    ratio = border_entity_info.ratio
    extend_margin = int(extend_margin * ratio[0])
    point_center = get_centroid(bbox)
    bbox_temp = [point_center[0] - extend_margin, point_center[1] - extend_margin, point_center[0] + extend_margin,
                point_center[1] + extend_margin]
    all_text_info = border_entity_info.border_text_info_with_bound_vertex[TextType.ALL]

    nearby_text_origin = entity_in_bbox_update(all_text_info, bbox_temp)
    if not nearby_text_origin:
        # print("解析结果中，没有获取在矩形中的文本")
        return None

    pattern = map_label
    if isinstance(map_label, list):
        res = []
        for label in map_label:
            label_text_info = [text for text in nearby_text_origin if re.search(label, text.extend_message)]
            len_label_info = len(label_text_info)
            if len_label_info >= 1:
                res.append(label_text_info[0].extend_message)
        if res:
            return res
        else:
            return None

    label_text_info = [text for text in nearby_text_origin if re.search(pattern, text.extend_message)]

    len_label_info = len(label_text_info)
    if len_label_info == 0:
        return None
    elif len_label_info >= 1:
        return label_text_info[0].extend_message


def get_entity_nearby_entity(bbox, border_entity_info, extend_margin=1800, map_label=None):
    """
    获取构件编号
    Args:
        bbox: contour
        border_entity_info:
        extend_margin:
        map_label: 匹配附近构件名称
    Returns:
    匹配的属性
    """
    ratio = border_entity_info.ratio
    extend_margin = int(extend_margin * ratio[0])
    point_center = get_centroid(bbox)
    bbox_temp = [point_center[0] - extend_margin, point_center[1] - extend_margin, point_center[0] + extend_margin,
                 point_center[1] + extend_margin]
    entity_bbox_list = [entity for entity in border_entity_info.entity_bbox_list if entity.entity_class == map_label]
    nearby_entity_list = [entity.bounding_rectangle for entity in entity_bbox_list
                          if abs(entity.bounding_rectangle.list[0] - entity.bounding_rectangle.list[2]) > 2 and
                             abs(entity.bounding_rectangle.list[1] - entity.bounding_rectangle.list[3]) > 2 ]

    nearby_entity_origin = entity_in_bbox_update(nearby_entity_list, bbox_temp)
    return nearby_entity_origin


def get_elevator_bottom_depth(bbox, border_entity_info, extend_margin=1800):
    """
    获取构件编号
    Args:
        bbox: contour
        border_entity_info:
        extend_margin:
        map_label: 匹配附近编号的正则
    Returns:
    匹配的属性
    """
    ratio = border_entity_info.ratio
    extend_margin = int(extend_margin * ratio[0])
    point_center = get_centroid(bbox)
    bbox_temp = [point_center[0] - extend_margin, point_center[1] - extend_margin, point_center[0] + extend_margin,
                 point_center[1] + extend_margin]
    nearby_entity_list = border_entity_info.mark_object_dict.get("标高符号", [])

    nearby_entity_list = [entity.bounding_rectangle.list + [entity.labeled_height] for entity in nearby_entity_list if entity.labeled_height]

    nearby_entity_origin = entity_in_bbox_update(nearby_entity_list, bbox_temp)
    if not nearby_entity_origin:
        return None
    text_num_dict = defaultdict(int)
    for entity in nearby_entity_list:
        text_num_dict[entity[4]] += 1
    floor_height = sorted(text_num_dict.items(), key=lambda x: x[1], reverse=True)[0][0]

    elevator_height = nearby_entity_origin[0][4]

    return abs(float(elevator_height) - float(floor_height))


def get_floor_label_height(bbox, border_entity_info):
    all_height_mark_list = border_entity_info.mark_object_dict.get("标高符号", [])
    if all_height_mark_list:
        all_height_mark_list = [list(get_centroid(mark.bounding_rectangle.list)) + [mark.labeled_height] for mark in all_height_mark_list]
        point_center = get_centroid(bbox)
        # 找一个距离最近的标高作为此楼层标2

        sorted_mark_list = sorted(all_height_mark_list, key=lambda x: point_euclidean_distance(point_center, x[:2]))
        print("----------------debug--------------")
        print(sorted_mark_list)
        return sorted_mark_list[0][2]

    return None

def get_space_label_height(bbox, border_entity_info):
    all_height_mark_list = border_entity_info.mark_object_dict.get("标高符号", [])
    all_height_mark_list = [mark for mark in all_height_mark_list if Iou_temp(mark.bounding_rectangle.list, bbox)]
    if all_height_mark_list:
        all_height_mark_list = [list(get_centroid(mark.bounding_rectangle.list)) + [mark.labeled_height] for mark in
                                all_height_mark_list]
        return sorted(all_height_mark_list, key=lambda x:x[-1])[0][-1]
    return None


def get_door_open_direction_entity(direction_line, base_line):
    """
    根据门的朝向线和门的bbox
    Args:
        direction_line:门朝向线
        base_line:门基线
    Returns:门朝向门弧的法线
    """
    direction = None
    if direction_line is None or base_line is None:
        return None
    p1, p2 = direction_line[:2], direction_line[2:]
    p1_1 = point_project_on_line(p1, base_line)
    p2_2 = point_project_on_line(p2, base_line)
    dis_1 = point_euclidean_distance(p1_1, p1)
    dis_2 = point_euclidean_distance(p2_2, p2)
    if dis_1 > dis_2:
        direction = p2 + p1
    else:
        direction = p1 + p2
    return direction


def get_door_axis_entity(entity_object, border_entity):
    """
    获取门轴信息

    Args:
        entity_bbox: 构件bbox
        border_entity: 图框全量信息
    Returns:
        门轴列表
    """
    door_axis_list = []
    base_line = entity_object.door_base_line
    entity_bbox = entity_object.bounding_rectangle.list
    print("==========", "base_line: ", base_line, entity_object.chinese_name)
    if base_line is None:
        return door_axis_list
    # 图框基本信息
    ratio = border_entity.ratio
    space_scale = border_entity.space_scale
    border_coord = border_entity.border_coord
    origin_border_entity_info = border_entity.origin_border_entity_info

    # 获取门窗图层的直线和弧线图元
    door_layer_to_check = ["door", "window", "elevator_door"]
    line_class = ["Line", "Polyline", "Polyline2d"]

    line_dict = get_origin_border_entity_info_rule(origin_border_entity_info, door_layer_to_check, line_class,
                                                   space_scale, border_coord, ratio)
    line_list = []
    for _, line in line_dict.items():
        line_list.extend(line)
    line_list = [line for line in line_list if len(line) == 4]

    # 过滤门板线的长度阈值
    line_in_bbox = entity_in_bbox(line_list, entity_bbox)
    # 选取长度大于200mm的直线
    line_need_list = [line for line in line_in_bbox if point_euclidean_distance(line[:2], line[2:]) > 200 * ratio[0]]
    # 过滤掉平行于门基线的直线
    line_need_list = [line for line in line_need_list if angle_between_segment2(np.array([line[:2], line[2:]]),
                                                                np.array([base_line[:2], base_line[2:]])) > 10]
    # 门基线的中点获取
    base_center = get_centroid(base_line)

    door_axis_1, door_axis_2 = None, None
    p1, p2 = base_line[:2], base_line[2:]
    min_dis_1, min_dis_2 = float("inf"), float("inf")
    for line in line_need_list:
        p1_1 = point_project_on_line(p1, line)
        dis_1 = point_euclidean_distance(p1, p1_1)
        if dis_1 < min_dis_1:
            min_dis_1 = dis_1
            door_axis_1 = line
        p2_2 = point_project_on_line(p2, line)
        dis_2 = point_euclidean_distance(p2, p2_2)
        if dis_2 < min_dis_2:
            min_dis_2 = dis_2
            door_axis_2 = line

    if entity_object.chinese_name in ["子母门", "双开门"]:
        if door_axis_1 is not None:
            door_axis_list.append(door_axis_1)
        if door_axis_2 is not None:
            door_axis_list.append(door_axis_2)
    elif entity_object.chinese_name in ["单开门"]:
        if door_axis_1 is not None and door_axis_2 is not None:
            if min_dis_2 > min_dis_1:
                door_axis_list.append(door_axis_1)
            else:
                door_axis_list.append(door_axis_2)
    return door_axis_list


def get_door_open_status_entity(entity_object, border_entity):
    """
    获取门的开启状态属性

    Args:
        entity_object: 构件对象
        border_entity: 图框全量信息

    Returns:
        门的开启状态
    """
    open_status = "常闭"
    text_info = border_entity.border_text_info[TextType.ALL]
    status_text_bbox = [text.bbox.list for text in text_info if re.search("常开", text.extend_message)]
    entity_bbox = entity_object.bounding_rectangle.list
    extend_entity_bbox = extend_margin(entity_bbox, 20)
    for text_bbox in status_text_bbox:
        if Iou_temp(text_bbox, extend_entity_bbox) > 0:
            open_status = "常开"
            break
    return  open_status


def judge_door_is_guanjing_door(entity_object, border_entity):
    """
    判断门是否是管井门

    Args:
        entity_object: 构件对象
        border_entity: 图框全量信息

    Returns:
        是否是管井门
    """
    is_guanjing_door = False
    door_direction_line = entity_object.door_direction_line
    if door_direction_line is None:
        return is_guanjing_door
    room_info = border_entity.room_info
    guanjing_room_list = [room for room in room_info if re.search("井", "".join(room.name_list))]
    for room in guanjing_room_list:
        if line_overlap_poly(door_direction_line, room.contour.contour):
            is_guanjing_door = True
            break
    return is_guanjing_door


def get_window_position_entity(entity_object, border_entity):
    """
    获取窗户的位置

    Args:
        entity_object: 构件对象
        border_entity: 图框全量信息

    Returns:
        窗户位置
    """
    position = None
    bbox = entity_object.bounding_rectangle.list
    door_base_coords = border_entity.door_base_coords

    for coord in door_base_coords:

        if line_overlap_poly(get_contour_from_bbox(bbox), coord.list):
            position = coord.list
            print("coord: ", position)
            break
    return position


def get_window_fire_resistance_level_entity(bbox, border_entity):
    """
    获取门的防火属性

    Args:
        bbox: 外接矩形框
        border_entity: 图框全量信息

    Returns:
        窗防火属性
    """
    level = None
    text_info = border_entity.border_text_info[TextType.ALL]
    F_text = [text for text in text_info if re.search("F", text.extend_message)]
    jia_text = [text for text in text_info if re.search("甲", text.extend_message)]
    yi_text = [text for text in text_info if re.search("乙", text.extend_message)]
    extend_bbox = extend_margin(bbox, 30)
    has_F = False
    for text in F_text:
        if Iou_temp(text.bbox.list, extend_bbox) > 0:
            has_F = True
            break
    if not has_F:
        return level
    min_jia_text_dis = float('inf')
    has_jia_text = False
    window_center = get_centroid(bbox)
    for text in jia_text:
        if Iou_temp(text.bbox.list, extend_bbox) > 0:
            has_jia_text = True
            text_center = get_centroid(text.bbox.list)
            dis = point_euclidean_distance(text_center, window_center)
            if min_jia_text_dis < dis:
                min_jia_text_dis = dis
    min_yi_text_dis = float('inf')
    has_yi_text = False
    window_center = get_centroid(bbox)
    for text in yi_text:
        if Iou_temp(text.bbox.list, extend_bbox) > 0:
            has_yi_text = True
            text_center = get_centroid(text.bbox.list)
            dis = point_euclidean_distance(text_center, window_center)
            if min_yi_text_dis < dis:
                min_yi_text_dis = dis
    if has_jia_text and has_yi_text:
        if min_yi_text_dis < min_jia_text_dis:
            level = 'F乙'
        else:
            level = 'F甲'
    elif has_jia_text:
        level = 'F甲'
    elif has_yi_text:
        level = 'F乙'
    else:
        level = "FC"
    return level


def judge_automatic_smoke_exhaust_window_entity(bbox, border_entity):
    """
    获取窗是否自动排烟属性

    Args:
        bbox:外接矩形框
        border_entity:图框全量信息

    Returns:
        是否自动排烟属性
    """
    automatic_smoke_exhaust = False
    text_info = border_entity.border_text_info[TextType.ALL]
    target_text = [text for text in text_info if re.search("排烟", text.extend_message)]
    extend_bbox = extend_margin(bbox, 30)
    for text in target_text:
        if Iou_temp(text.bbox.list, extend_bbox) > 0:
            automatic_smoke_exhaust = True
            break
    return automatic_smoke_exhaust


def get_entity_nearby_text(bbox, border_entity_info, extend_margin=1800, map_label=None):
    """
    获取构件编号
    Args:
        bbox: contour
        border_entity_info:
        extend_margin:
        map_label: 匹配附近编号的正则
    Returns:
    匹配的属性
    """
    ratio = border_entity_info.ratio
    extend_margin = int(extend_margin * ratio[0])
    bbox_temp = [bbox[0] - extend_margin, bbox[1] - extend_margin, bbox[2] + extend_margin,
                 bbox[3] + extend_margin]
    all_text_info = border_entity_info.border_text_info_with_bound_vertex[TextType.ALL]

    nearby_text_origin = entity_in_bbox_update(all_text_info, bbox_temp)
    if not nearby_text_origin:
        # print("解析结果中，没有获取在矩形中的文本")
        return None

    pattern = map_label

    label_text_info = [text for text in nearby_text_origin if re.search(pattern, text.extend_message)]

    len_label_info = len(label_text_info)
    if len_label_info == 0:
        return None
    elif len_label_info >= 1:
        return label_text_info


def get_form(bbox, border_entity_info, kind=""):
    """
    碧桂园期被产品要求开发，函数为获取构件的形式属性，用途为区分同一构件的不同图例。方式为依赖构件的原始图元，比如开关构件附近的几根长线-短线，插座附近的文本
    Args:
        bbox: 传入的构件的外接矩形框
        border_entity_info: 图层全量信息
        kind: 构件的类别(chinese_name)
    Returns:
        形式属性
    """
    form = None
    margin = border_entity_info.ext_margin
    bbox = extend_margin(bbox, margin)
    if kind in ['负荷开关', '平面图开关', '单刀开关', '双切开关']:
        # 开关区分图例，用到 1、与圆相连的长线数目；2、与长线相连的短线数目；3、短线和长线相交的方式(以图例举证，单联单控开关为'vert',
        # 新风机开关为'divide', 空调线控器为'cross')；4、开关附近可能存在的文本。
        form = [0, 0, '', None]
        switch_circle_list = []
        switch_line_list = []
        origin_border_entity_info = border_entity_info.origin_border_entity_info
        space_scale = border_entity_info.space_scale
        border_coord = border_entity_info.border_coord
        ratio = border_entity_info.ratio
        text_all = border_entity_info.border_text_info[TextType.ALL]
        layers_to_check = ["device_switch", "device_light"]
        circle_entity_dict = get_origin_border_entity_info_rule(
            origin_border_entity_info, layers_to_check, ['Circle', 'Ellipse'], space_scale, border_coord, ratio)
        line_entity_dict = get_origin_border_entity_info_rule(origin_border_entity_info, layers_to_check,
                                                              ['Line', 'Polyline', 'Polyline2d'],
                                                              space_scale, border_coord, ratio)
        for _, entity_list in line_entity_dict.items():
            switch_line_list.extend(entity_list)
        switch_line_list = list(filter(lambda x: len(x) == 4, switch_line_list))
        for _, entity_list in circle_entity_dict.items():
            for entity in entity_list:
                if len(entity) == 3:  # 'Circle'
                    switch_circle_list.append(entity)
                elif len(entity) == 11:  # 'Ellipse'
                    if (entity[0] == entity[2]) and (entity[1] == entity[3]) and (entity[6] == entity[7]) and \
                            (entity[-1] - entity[-2] == 360):
                        switch_circle_list.append(entity[4:7])
        switch_circle_list = [[temp[0] - temp[2], temp[1] - temp[2], temp[0] + temp[2], temp[1] + temp[2]]
                              for temp in switch_circle_list]
        circle_inside = entity_in_bbox(switch_circle_list, bbox)
        line_inside = entity_in_bbox(switch_line_list, bbox)
        line_string = list(map(lambda x: LineString([x[:2], x[2:4]]), line_inside))
        text_near = None
        if len(circle_inside) > 1:
            # 尽管在分类时候靠近的开关拆分成了若干个，但拆分后的外扩轮廓仍可能包含另一个，所以用事先拆分前的对应关系来寻找此拆分后的bbox对应的圆心
            more_circles_switch = border_entity_info.special_info_dict.get('abnormal_switch', {}).get('more_circles_switch', [])
            if bbox in more_circles_switch:
                circle_inside = [border_entity_info.special_info_dict.get('abnormal_switch', {})['real_circle'][more_circles_switch.index(bbox)]]
        if len(circle_inside) == 1:
            # 先找寻与中心圆相连的长线数量
            poly_obj = Polygon(get_contour_from_bbox(circle_inside[0]).squeeze())
            long_lines = list(filter(lambda x: x.intersects(poly_obj), line_string))
            form[0] = len(long_lines)
            # 再找寻与长线相连的短线数量
            short_lines = []
            for long_line in long_lines:
                for short_line in line_string:
                    # 因为短线实际可能并不相交，设计师画的时候差距一两个像素点的位置，所以不直接判断是否相交；
                    if short_line in long_lines:
                        continue
                    x, y = long_line.xy
                    long_line_cnt = np.array([[[x[0], y[0]]], [[x[1], y[1]]]], dtype=np.int32)
                    long_line_cnt = expand_contour(long_line_cnt, 1, 'open')
                    if short_line.intersects(Polygon(long_line_cnt.squeeze())):
                        short_lines.append(short_line)
            form[1] = len(short_lines)
            # 找寻开关附近可能存在的文本
            for text in text_all:
                if text.extend_message in ['L', 'C', 'Y']:
                    if Iou_temp(bbox, text.bbox.list):
                        if text_near:
                            print('form_error-1: has two message', bbox, text.extend_message, text_near)
                        text_near = text.extend_message
            form[2] = 'vert'
            form[3] = text_near
            # if len(short_lines) + len(long_lines) != len(line_inside):
            #     print('form_error0:', bbox, line_inside, list(map(lambda x:x.xy, long_lines)), list(map(lambda x:x.xy, short_lines)))
        elif len(circle_inside) == 0:
            print('form_error1:应是人体感应开关？', bbox, circle_inside, line_inside)
        else:
            print('form_error2:不该存在超过2个圆的开关，应被分为两个以上', bbox, 'lines_num:', line_inside)

    elif kind in ['插座', ]:
        # 插座区分图例，产品说用文本实现
        text_all = border_entity_info.border_text_info[TextType.ALL]
        for text in text_all:
            if text.extend_message in ['F', 'Y', 'R', 'C', 'D', 'XD', 'KX', 'B', 'J', 'WBL', 'XW', 'XD', 'T', 'X', 'P',
                                       'DR', 'W', 'Z', 'W', 'MJ', 'K1', 'K2', 'K3', 'U', 'L', 'D']:
                if Iou_temp(bbox, text.bbox.list):
                    if form:
                        print('form_error3: has two message', bbox, text.extend_message, form)
                    form = text.extend_message
    # print('form_get:', bbox, form)
    return form

def get_door_label_number(bbox, border_entity_info, extend_margin=1800, map_label=None):
    """
    获取构件编号
    Args:
        bbox: contour
        border_entity_info:
        extend_margin:
        map_label: 匹配附近编号的正则
    Returns:
    匹配的属性
    """
    image_manager = border_entity_info.image_manager
    # for debug
    # img_debug = image_manager.load_from_manager(IMG_WITH_WALL_KEY)
    # cv2.rectangle(img_debug, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 255, 0), 5)
    # cv2.imwrite("/Users/xuan.ma/Desktop/door_number.png", img_debug)
    ratio = border_entity_info.ratio
    extend_margin = int(extend_margin * ratio[0])
    point_center = get_centroid(bbox)
    bbox_temp = [point_center[0] - extend_margin, point_center[1] - extend_margin, point_center[0] + extend_margin,
                point_center[1] + extend_margin]
    all_text_info = border_entity_info.border_text_info_with_bound_vertex[TextType.ALL]

    nearby_text_origin = entity_in_bbox_update(all_text_info, bbox_temp)
    if not nearby_text_origin:
        # print("解析结果中，没有获取在矩形中的文本")
        return None

    pattern = map_label
    if isinstance(map_label, list):
        res = []
        for label in map_label:
            label_text_info = [text for text in nearby_text_origin if re.search(label, text.extend_message)]
            len_label_info = len(label_text_info)
            if len_label_info >= 1:
                res.append(label_text_info[0].extend_message)
        if res:
            return res
        else:
            return None

    label_text_info = [text for text in nearby_text_origin if re.search(pattern, text.extend_message)]

    len_label_info = len(label_text_info)
    if len_label_info == 0:
        return None
    elif len_label_info >= 1:
        label_text_info.sort(key=lambda x: point_euclidean_distance(point_center, get_centroid(x.bbox.list)), reverse=False)

        first_label = label_text_info[0].extend_message
        # 防火门编号有时会分开
        fhm_tag = 'FM|FHM'
        fh_level = '甲|乙|丙'
        fh_level_with_num = '[甲乙丙]\d{1, 2}'
        if re.search(fhm_tag, first_label) and not re.search(fh_level, first_label):
            # 需要将nearby_text_origin排序，确保找到FM|FHM最近的fh_level文本
            nearby_text_origin.sort(key=lambda x: point_euclidean_distance(point_center, get_centroid(x.bbox.list)), reverse=False)
            for text_info in nearby_text_origin:
                if re.search(fh_level_with_num, text_info.extend_message):
                    label_info = first_label + text_info.extend_message
                    return label_info
                elif re.search(fh_level, text_info.extend_message):
                    # 获取甲乙丙附近的数字
                    level_extend_margin = int(800 * ratio[0])
                    level_point_center = get_centroid(text_info.bbox.list)
                    level_text_bbox = [level_point_center[0] - level_extend_margin, level_point_center[1] - level_extend_margin, level_point_center[0] + level_extend_margin,
                                level_point_center[1] + level_extend_margin]

                    nearby_num_text_info = entity_in_bbox_update(all_text_info, level_text_bbox)
                    if not nearby_num_text_info:
                        # TODO: 验证是否有这种门编号
                        label_info = first_label + text_info.extend_message
                        return label_info
                    else:
                        num_infos = [text for text in nearby_text_origin if re.search('^\d{1,2}$', text.extend_message)]
                        if num_infos == []:
                            continue
                        num_infos.sort(key=lambda x: point_euclidean_distance(level_point_center, get_centroid(x.bbox.list)), reverse=False)
                        num_info = num_infos[0].extend_message
                        label_info = first_label + text_info.extend_message + num_info

                        return label_info
        else:
            return first_label

def get_dx_position_entity(entity_object, border_entity, extend_margin=1800):
    """
    获取电箱的位置

    Args:
        entity_object: 构件对象
        border_entity: 图框全量信息

    Returns:
        电箱位置
    """
    pattern = "^\d{1,}$"
    bbox = entity_object.bounding_rectangle.list
    point_center = get_centroid(bbox)
    ratio = border_entity.ratio
    extend_margin = int(extend_margin * ratio[0])
    bbox_temp = [point_center[0] - extend_margin, point_center[1] - extend_margin, point_center[0] + extend_margin,
                 point_center[1] + extend_margin]
    # all_text_info = border_entity.border_text_info_with_bound_vertex[TextType.ALL]
    all_text_info = border_entity.mark_object_dict.get('尺寸标注', [])

    label_text_info = [text for text in all_text_info if re.search(pattern, text.extend_message)]

    len_label_info = len(label_text_info)
    if len_label_info == 0:
        return None
    elif len_label_info >= 1:
        label_text_info.sort(key=lambda x: point_euclidean_distance(point_center, get_centroid(x.bounding_rectangle.list)),
                             reverse=False)

        first_text = get_centroid(label_text_info[0].bounding_rectangle.list)
        if first_text[0] in range(bbox_temp[0], bbox_temp[2]) and first_text[1] in range(bbox_temp[1], bbox_temp[3]):
            first_label = label_text_info[0].extend_message
        else:
            return None

    return first_label


def trans_unit(height_str: str):
    """
    h = 1230.12 mm 转为 1.23012m
    :param height_str: 正则提取的文本 "1230.12 m"
    :return:
    """
    height_str = height_str.strip()
    if height_str[-1] == 'm':
        height = float(height_str[:-1].strip()) / 1000
    elif height_str[-1] == 'c':
        height = float(height_str[:-1].strip()) / 100
    elif height_str[-1] == 'd':
        height = float(height_str[:-1].strip()) / 10
    else:
        height = float(height_str.strip())
    return height


def get_metric_from_remark(border_entity, target_pattern):
    all_text_info = border_entity.border_text_info[TextType.ALL]
    target_texts = [_ for _ in all_text_info if re.search(target_pattern, _.extend_message)]
    height = None
    if target_texts:
        height_str = re.findall(target_pattern, target_texts[0].extend_message)[0]
        height = trans_unit(height_str)
    else:
        print(f'Not found the match text, pattern is "{target_pattern}"]!')
    return height, target_texts[0].bbox.list if target_texts else None

def get_metric_from_remark_v2(chinese_name, border_entity, target_pattern):
    """
    将目标文本上下3行的文本合并之后在继续正则匹配
    """
    height = None
    height_bbox = None
    all_text_info = border_entity.border_text_info[TextType.ALL]
    target_text_list = [_ for _ in all_text_info if re.search(chinese_name, _.extend_message)]
    for target_text in target_text_list:
        target_bbox = target_text.bbox.list
        text_height = abs(target_bbox[1] - target_bbox[3])
        target_bbox_ext = extend_margin_by_direction(target_bbox, 3 * text_height, direction="up_down")
        bbox_ext_include_text_list = [_ for _ in all_text_info if Iou_temp(_.bbox.list, target_bbox_ext)]
        # 有些数据文本和整个文本是分离的，导致没获取到
        # 需要加进来一起合并
        bbox_ext_include_text_list = [_ for _ in all_text_info
                                      if any([Iou_temp(extend_margin_by_direction(text.bbox.list, 10*text_height, direction="left_right"), _.bbox.list)>0. for text in bbox_ext_include_text_list])]
        # 按文本左上角的位置将文本进行上下排序
        # 注意不在一起的文本的位置不是完全一样，需要判断是否一行
        merge_text = concat_text([text.bbox.list+[text.extend_message] for text in bbox_ext_include_text_list])
        if re.search(target_pattern, merge_text):
            print("merge_text", merge_text)
            height_str = re.findall(target_pattern, merge_text)[0]
            height = trans_unit(height_str)
            for text in bbox_ext_include_text_list:
                if re.search(height_str, text.extend_message):
                    height_bbox = text.bbox.list
                    break
            break
    return height, height_bbox

def get_install_height(chinese_name, bbox, border_entity, target_pattern):
    """
    平面图中没引线的，可以从设备表中获取，但设备表中分类较细，难度较大
    因此，货板比对时，只比有引线标注的和文本说明的，暂不比对设备表
    """
    height = None
    height_bbox = None
    # 获取所有虚框
    dash_border_list = border_entity.special_info_dict['dash_border_list']
    # 判断该构件是否在某个虚框中
    outer_border = None
    for dash_border in dash_border_list:
        iou = Iou_temp(extend_margin(bbox, 10), dash_border)
        if iou > 0.9:
            outer_border = dash_border
            print(f'\033[1;33m 找到构件所在虚框 {dash_border} \033[0m')
            break

    # 获取引线
    anno_line_list = border_entity.special_info_dict['annotation_info_list']
    height_pattern = r'h\s*=\s*([\d]+[.]?[\d]*\s*[cmd]?)m'
    min_iou = 0.01
    target_text = None
    for line_l, text_l, main_end_point in anno_line_list:
        # line_l格式为：(支线，主线)，文本在主线两侧
        branch_line = line_l[0]
        target_text_list = [t for t in text_l if re.search(height_pattern, t)]
        if len(target_text_list) == 0:
            continue

        if outer_border is not None:
            # 在虚框的构件，用虚框找引线
            iou = point_in_bbox(main_end_point, extend_margin(outer_border, 10))
        else:
            iou = point_in_bbox(main_end_point, extend_margin(bbox, 10))
        if iou > min_iou:
            min_iou = iou
            target_text = target_text_list[0]
    if target_text:
        height_str = re.findall(height_pattern, target_text)[0]
        height = trans_unit(height_str)
        height_bbox = bbox
        print(f'\033[1;32m 从平面图引线中获取 {chinese_name} 安装高度{height}m \033[0m')
    else:
        height, height_bbox = get_metric_from_remark(border_entity, target_pattern)
        if height is None:
            print("文本换行有可能导致正则匹配失败, 将目标文本上下两行的文本连接起来尝试匹配 ...")
            height, height_bbox = get_metric_from_remark_v2(chinese_name, border_entity, target_pattern)
        print(f'\033[1;31m 从备注文本中获取 {chinese_name} 安装高度{height}m \033[0m')
    return height, height_bbox

def get_distance_to_wall(chinese_name,bbox, border_entity):
    """
    从电气平面图的尺寸标注中，获取离墙距离
    """
    len_mark_list = border_entity.mark_object_dict['尺寸标注']

    min_iou = 0.1
    target_text = None
    for mark in len_mark_list:
        mark_bbox = mark.bounding_rectangle.list
        iou = Iou_temp(mark_bbox, bbox)
        if iou > min_iou:
            min_iou = iou
            target_text = mark.extend_message
    if target_text:
        try:
            distance = float(target_text.strip())/1000
            print(f'\033[1;32m 从平面图标注中获取 {chinese_name} 离墙边距离{distance}m \033[0m')
        except:
            print(f'Error: {target_text} 转数字出错')
            distance = None
    else:
        print(f'\033[1;31m {chinese_name} 未找到对应的尺寸标注 \033[0m')
        distance = None
    return distance


def sort_contour(seg_contours, is_flip=False, threshold=50):
    """
    将contour按中心点排序。如果为镜像状态（左右镜像），x调整为降序排列
    一定误差范围内，认为x,y相同
        若key为（x0, y0) ，则value中为阈值范围内的点{(x, y)|abs(x-x0)<t,abs(y-y0)<t}
    :return 排好顺序的contour和镜像的排序
    注意：中心点直接取平均
    """
    centroid_contour_dict = dict()
    centroid_group_dict = dict()
    for seg_contour in seg_contours:
        bbox = get_bbox_from_contour(seg_contour)
        c_x = (bbox[0] + bbox[2])/2
        c_y = (bbox[1] + bbox[3])/2
        centroid_contour_dict[(c_x, c_y)] = seg_contour
        if not centroid_group_dict:
            centroid_group_dict[(c_x, c_y)] = [(c_x, c_y)]
        else:
            find_flag = False
            for k, v in centroid_group_dict.items():
                # 先确定x是否在某个key的阈值范围内
                if abs(c_x - k[0]) < threshold:
                    # 再确定y是否也在这个key对应的y的阈值范围内
                    if abs(c_y - k[1]) < threshold:
                        # 认为两点重合，不需排序
                        v.append((c_x, c_y))
                    else:
                        centroid_group_dict[(k[0], c_y)] = [(c_x, c_y)]
                    find_flag = True
                    break
            if not find_flag:
                centroid_group_dict[(c_x, c_y)] = [(c_x, c_y)]
    # 对分组的key排序，将对应的contour按顺序拿出
    if is_flip:
        grouped_keys = sorted(list(centroid_group_dict.keys()), key=lambda x: (-x[0], x[1]))
        flip_keys = sorted(list(centroid_group_dict.keys()), key=lambda x: (x[0], x[1]))
    else:
        grouped_keys = sorted(list(centroid_group_dict.keys()), key=lambda x: (x[0], x[1]))
        flip_keys = sorted(list(centroid_group_dict.keys()), key=lambda x: (-x[0], x[1]))

    # print(f'grouped_keys: {list(grouped_keys)}')
    sorted_seg_contours = [centroid_contour_dict[v] for x in grouped_keys for v in centroid_group_dict[x]]
    return sorted_seg_contours, [grouped_keys.index(x) for x in flip_keys]

def get_cfyyj_w_h(entity_obj, border_entity_info):
    '''
    获取长和宽
    '''
    width, height = None, None
    contour = None
    bbox = entity_obj.bounding_rectangle.list
    ratio = border_entity_info.ratio
    origin_border_entity_info = border_entity_info.origin_border_entity_info
    scale = border_entity_info.space_scale
    border_coord = border_entity_info.border_coord
    # for debug
    img_manager = border_entity_info.image_manager
    img_copy = img_manager.load_from_manager(IMG_WITH_WALL_KEY)
    img_w, img_h = img_manager.img_width, img_manager.img_height
    line_to_check = ['Line', 'Polyline', 'Polyline2d']
    layer_to_check = ["kitchen_exhaust_pipe", "floor_drain_mix"]
    line_info_dict = get_origin_border_entity_info_rule(origin_border_entity_info, layer_to_check,
                                                       line_to_check, scale, border_coord, ratio)
    line_info_list = []
    for layer, e_list in line_info_dict.items():
        line_info_list.extend(e_list)
    line_info_list = [line for line in line_info_list if len(line) == 4]

    # for debug
    # for line in line_info_list:
    #     cv2.line(img_copy, (line[0], line[1]), (line[2], line[3]), (255, 255, 0), 1)
    # cv2.imwrite("lines.png", img_copy)

    bbox_line_info_list = []
    for line in line_info_list:
        line_len = point_euclidean_distance(line[:2], line[2:])
        if line_len > 1000 * ratio[0]: continue
        flag, intersection = line_overlap_poly(get_contour_from_bbox(bbox), line, need_intersections=True)
        if (flag and intersection.length/line_len > 0.5) or entity_in_bbox([line], bbox):
            bbox_line_info_list.append(line)

    # for debug
    # for line in bbox_line_info_list:
    #     cv2.line(img_copy, (line[0], line[1]), (line[2], line[3]), (0, 255, 255), 1)
    # cv2.imwrite("bbox_lines.png", img_copy)

    _, _, contour = find_contour_w_h(bbox_line_info_list, img_copy)

    bbox_line_deg_list = [getLineDeg(line) for line in bbox_line_info_list]
    # vertical_line_pair_list = []
    # 找到相互垂直的直线对
    line_num = len(bbox_line_deg_list)
    vis = [False] * line_num
    for i in range(line_num):
        line_i = bbox_line_info_list[i]
        same_degrees_idx_list = [i]
        v_degress_idx_list = []
        # vertical_line_dict = {}
        for j in range(i + 1, line_num):
            if vis[j]: continue
            line_j =  bbox_line_info_list[j]
            if abs(point_euclidean_distance(line_i[:2], line_i[2:])/point_euclidean_distance(line_j[:2], line_j[2:]) - 1) < 0.05: continue
            if abs(bbox_line_deg_list[i] - bbox_line_deg_list[j]) < 5:
                same_degrees_idx_list.append(j)
                vis[j] = True
            elif abs(abs(bbox_line_deg_list[i] - bbox_line_deg_list[j]) - 90) < 5:
                v_degress_idx_list.append(j)
                vis[j] = True
        if v_degress_idx_list:  # and len(v_degress_idx_list + same_degrees_idx_list) > 2
            # 有些边会被分为多个线段徐阿哟将其连接起来
            # 直接将直线划到背景图上找轮廓， 在计算宽高
            line_1_list = [bbox_line_info_list[i] for i in v_degress_idx_list]
            line_1 = max(line_1_list, key=lambda x: point_euclidean_distance(x[:2], x[2:]))
            width = point_euclidean_distance(line_1[:2], line_1[2:]) / ratio[0]
            line_2_list = [bbox_line_info_list[j] for j in same_degrees_idx_list]
            line_2 = max(line_2_list, key=lambda x: point_euclidean_distance(x[:2], x[2:]))
            height = point_euclidean_distance(line_2[:2], line_2[2:]) / ratio[1]
            print(f"Get w,h by enentity {width, height} mm")
            # for debug
            # cv2.line(img_copy, (line_1[0], line_1[1]), (line_1[2], line_1[3]), (0, 255, 255), 3)
            # cv2.line(img_copy, (line_2[0], line_2[1]), (line_2[2], line_2[3]), (255, 255, 0), 3)
            # cv2.imwrite("cfydgj_w_h.png", img_copy)

            # _, _, contour = find_contour_w_h(line_1_list + line_2_list, img_copy)
            # cnt_width /= ratio[0]
            # cnt_height /= ratio[1]
            # print(f"Get w,h by contour {cnt_width, cnt_height} mm")
            # width = min(min(width, height), min(cnt_width, cnt_height))
            # height = max(max(width, height), max(cnt_width, cnt_height))
            break

    return ((min(width, height), max(width, height)), contour) if width is not None and height is not None else (None, None)

def find_contour_w_h(line_list, img_copy):
    '''
    直接将直线划到背景图上找轮廓， 在计算宽高
    '''
    bg = np.zeros_like(img_copy, dtype = np.uint8)
    for line in line_list:
        cv2.line(bg, (line[0], line[1]), (line[2], line[3]), (255, 255, 255), 1)
    bg_gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("bg_gray.png", bg_gray)
    edges = cv2.Canny(bg_gray, 50 , 100)
    # cv2.imwrite("edges.png", edges)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    # cv2.imwrite("closed.png", closed)
    if '3.4' in cv2.__version__:
        _, contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) >= 1:
        # print("getting more than 1 contour ... ")
        contour = max(contours, key = lambda x: cv2.contourArea(x))
        peri = cv2.arcLength(contour, True)
        app_conotur = cv2.approxPolyDP(contour, 0.05 * peri, True)
        # _, (w, h), _ = cv2.minAreaRect(contour)
        return None, None, app_conotur
    return None, None, None

def concat_text(split_msg_list):
    '''
    将文本合并在一起
    split_msg_list: [[x1, y1, x2, y2, text], ... ]
    '''
    # 直接排序有问题，特别是尺寸数据和文本不为同一个文本，坐标有偏差，导致文本合并问题
    # split_msg_list.sort(key=lambda x: (x[1], x[0]))
    # split_msg = "".join([msg[-1] for msg in split_msg_list])
    if not split_msg_list: return ""
    line_height = abs(split_msg_list[0][3] - split_msg_list[0][1])
    # 先根据文本中心确认有几行文本
    split_msg_center_y_list = [get_centroid(split_msg[:4])[1] for split_msg in split_msg_list]
    # row_y_list = []
    vis = [False] * len(split_msg_center_y_list)
    y_arr = np.array(split_msg_center_y_list)
    total_text_list = []
    for yi, y in enumerate(split_msg_center_y_list):
        if vis[yi]: continue
        row_text_list = []
        minor_diff_idxs = np.where(np.abs(y_arr[yi:] - y) < line_height / 2)[0] + yi
        # print("minor_diff_idxs", minor_diff_idxs)
        for idx in minor_diff_idxs:
            vis[idx] = True
            row_text_list.append(split_msg_list[idx])
        row_text_list.sort(key=lambda x: x[0])
        total_text_list.append([y, row_text_list.copy()])
        # row_y_list.append(y)
    # # 从上到下户获取每一行的文本
    total_text_list.sort(key=lambda x: x[0])
    split_msg = ""
    for center_y, row_text_list in total_text_list:
        split_msg += "".join([text[-1] for text in row_text_list])
    return split_msg