# -*- coding: utf-8 -*-

import re
from ...recognition_engine.border_entity import BorderEntity

from ..utils.utils_integration import *
from ..utils.utils_analysis_common import *
from ...config_manager.decor_architecture.drawing_config import DrawingConfig, DrawingType

from ...common.decorator import timer
import cv2


@timer('entity_info_integration')
def run(border_entity_info, result_path, drawing_type):
    """
    :param border_entity_info: 图框构件信息
    :param result_path: 中间结果保存路径
    :param drawing_type: 图框类型
    :return: 更新的border_entity_info
    """

    image_manager = border_entity_info['image_manager']

    border_coord = border_entity_info['border_coord']  # 图框CAD坐标
    ratio = border_entity_info['ratio']  # 毫米转换到像素的比例
    space_scale = border_entity_info['space_scale']  # CAD坐标转换到毫米的比例
    room_info = border_entity_info.get('room_info', []) + border_entity_info.get('small_room_info', [])  # 空间分割信息
    entity_bbox_list = border_entity_info.get('entity_bbox_list', [])  # 构件png坐标
    entity_class_list = border_entity_info.get('entity_class_list', [])  # 构件类别
    border_size = image_manager.img_height, image_manager.img_width  # 图框的尺寸
    border_text_info = border_entity_info['border_text_info']  # 图框文本信息
    entity_num = len(entity_class_list)  # 构件数量
    room_num = len(room_info)  # 空间数量

    print('entity num: {}'.format(entity_num))
    print('room num: {}'.format(room_num))

    # 由于某些后处理并不要求空间和构件同时存在，所以该条件删除
    # # 若没有空间或构件，无法进行空间分割和构件分类后处理
    # if room_num == 0 or entity_num == 0:
    #     print('[NOTE] this drawing has no space or no entity !!!')
    #     return border_entity_info

    ##########################################
    #           根据构件来辅助识别空间
    ##########################################
    # TODO:待添加根据其他家具校正空间，如有马桶的空间是卫生间，有厨具的空间是厨房，有餐桌的空间是餐厅，有沙发的空间是客厅，有床的空间是卧室

    #纠正信报间空间
    border_entity_info = correct_xinbaojian(border_entity_info)

    # 根据排烟管道纠正排烟井
    border_entity_info = correct_paiyanjing(border_entity_info)

    # 根据楼梯构件和电梯厢构件，纠正楼梯间空间和电梯井空间；根据空调构件矫正空调板
    border_entity_info = correct_elevatorRoom_and_stairRoom(border_entity_info)

    # 消防电梯井、消防电梯前室、电梯前室 防烟楼梯前室 其他前室空间名称增加
    # border_entity_info = correct_xiaofang_elevatorRoom_and_frontRoom(border_entity_info)
    border_entity_info = judge_xf_front_room(border_entity_info)
    border_entity_info = judge_front_room_type(border_entity_info)
    # if drawing_type in [DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = get_expand_front_room(border_entity_info)
    # 获取防火墙
    # border_entity_info = get_fire_resistance_wall(border_entity_info)

    # 防烟楼梯前室空间增加
    # border_entity_info = correct_stair_frontRoom(border_entity_info)

    # 套内空间名称增加
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = add_household_room_name_arch_elec(border_entity_info)
    #
    # # 其他前室空间名称增加
    # # border_entity_info = add_other_frontRoom_name(border_entity_info)
    #
    # # 保存门构件的朝向信息
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.BINANCENG, DrawingType.JIFANG,
    #                     DrawingType.DINGCENG, DrawingType.WUMIAN]:
    #     border_entity_info = add_door_orientation_info(border_entity_info)
    #
    # TODO: 根据马桶等构件纠正卫生间等空间
    border_entity_info = add_toilet_info(border_entity_info)
    #
    # # 该逻辑通过获取有两扇门的无名空间即置为走廊不严谨，且目前已通过入户门有获取无名空间的走道逻辑
    # # # 通过逻辑添加走廊空间
    # # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    # #     border_entity_info = add_corridor_info(border_entity_info)
    #
    # # 雨篷空间增加
    # if drawing_type in [DrawingType.SECOND_THIRD_FLOOR]:
    #     border_entity_info = del_origin_yupeng_space(border_entity_info)
    #     border_entity_info = add_yupeng_spaces(border_entity_info)
    #
    # # 屋面层轮廓空间增加
    # if drawing_type in [DrawingType.WUMIAN]:
    #     border_entity_info = add_wumian_contour_space(border_entity_info)
    #
    # # 总图增加用地红线轮廓空间和用地红线图元
    # if drawing_type in [DrawingType.SITE_PLAN_ROAD, DrawingType.SITE_PLAN_BUILDING, DrawingType.XIAOFANG_SITE_PLAN,
    #                     DrawingType.FIRST_FLOOR_SITE_PLAN]:
    #     # 获取用地红线轮廓空间
    #     border_entity_info = add_red_line_room_info(border_entity_info)
    #
    #     # 获取用地红线图元信息，保存在 entity_bbox_dict 中，用于 "用地红线" 标记对象化
    #     red_line_list = get_red_line_pre(border_entity_info)
    #     if len(red_line_list) > 0:
    #         red_line_bbox = get_red_line_bbox(red_line_list)
    #         border_entity_info['entity_bbox_dict']['processed_red_lines'] = [red_line_bbox, red_line_list]
    #
    #     # 获取地库轮廓、地库坡道出入口空间
    #     border_entity_info = add_garage_room_info(border_entity_info)
    #
    #     # 获取回车场空间
    #     return_yard_space_list = get_return_yard_info_pre(border_entity_info)
    #     room_info = border_entity_info.get('room_info', [])
    #     room_info.extend(return_yard_space_list)
    #     border_entity_info['room_info'] = room_info
    #
    #     # 消防登高场地空间
    #     xiaofang_denggao_space_list = get_xiaofang_denggao_area(border_entity_info, result_path)
    #     room_info = border_entity_info.get('room_info', [])
    #     room_info.extend(xiaofang_denggao_space_list)
    #     border_entity_info['room_info'] = room_info
    #
    #     # 获取 基地车行出入口 和 基地人行出入口
    #     border_entity_info = add_space_entry(border_entity_info)
    #
    #     # 为总图类型增加车道边线图层弧形图元轮廓，在后续计算车道空间半径用到
    #     border_entity_info = get_road_arc_ellipse_contour(border_entity_info)
    #
    #     # 为总图类型增加车道中线图层弧形图元轮廓
    #     border_entity_info = get_road_center_arc_ellipse_contour(border_entity_info)
    #
    #     # 为总图类型增加用地红线图层弧形图元轮廓
    #     border_entity_info = get_red_line_arc_ellipse_contour(border_entity_info)
    #
    # # # 其他总图（除了消防总图）增加园区普通车道空间、园区消防车道空间
    # # if drawing_type in [DrawingType.SITE_PLAN_ROAD, DrawingType.SITE_PLAN_BUILDING, DrawingType.FIRST_FLOOR_SITE_PLAN]:
    # #     border_entity_info = add_site_plan_road_room_info(border_entity_info, result_path)
    # #
    # # # 消防总图增加园区消防车道空间
    # # if drawing_type in [DrawingType.XIAOFANG_SITE_PLAN]:
    # #     border_entity_info = add_site_plan_road_room_info(border_entity_info, result_path, is_xiaofang=True)
    #
    # # 防火分区空间增加
    # if drawing_type in [DrawingType.UNDERGROUND]:
    #     # 首先删除空间分割得到的防火分区空间
    #     border_entity_info = remove_fire_prevention_name(border_entity_info)
    #     fire_prevention_room_info_list = get_fire_prevention_info(border_entity_info)
    #     room_info = border_entity_info.get('room_info', [])
    #     room_info.extend(fire_prevention_room_info_list)
    #     border_entity_info['room_info'] = room_info
    #
    # # 对箭头构件进行合并和保存
    # border_entity_info = add_arrow_entity_info(border_entity_info)
    #
    # # 门窗大样图中进行门窗的重新合并
    # if drawing_type in [DrawingType.DOOR_WINDOW_DAYANG]:
    #     border_entity_info = recombine_window_in_dayang_drawing(border_entity_info)
    #
    # # 门窗大样图中立面窗户的开启扇面积属性获取
    # if drawing_type in [DrawingType.DOOR_WINDOW_DAYANG]:
    #     border_entity_info = add_elevation_window_open_area_and_window_number(border_entity_info)
    #
    # # 首层平面图增加 "单元出入口范围" 空间
    # if drawing_type in [DrawingType.INDOOR_FIRST_FLOOR]:
    #     unit_entrance_space = get_unit_entrance_info_pre(border_entity_info)
    #     room_info = border_entity_info.get('room_info', [])
    #     room_info.extend(unit_entrance_space)
    #     border_entity_info['room_info'] = room_info
    #
    # # 地下图纸获取车库范围空间
    # if drawing_type in [DrawingType.UNDERGROUND]:
    #     garage_range_space_info = get_garage_range_info_pre(border_entity_info)
    #     room_info = border_entity_info.get('room_info', [])
    #     room_info.extend(garage_range_space_info)
    #     border_entity_info['room_info'] = room_info
    #
    # # 坡道大样图纸类型获取车库坡道
    # if drawing_type in [DrawingType.PODAO]:
    #     garage_ramp_space_info = get_garage_ramp_info_pre(border_entity_info)
    #     room_info = border_entity_info.get('room_info', [])
    #     room_info.extend(garage_ramp_space_info)
    #     border_entity_info['room_info'] = room_info
    #
    # # 住宅首层无障碍通道获取无障碍坡道空间
    # if drawing_type in [DrawingType.INDOOR_FIRST_FLOOR_ACCESS]:
    #     wza_ramp_space_info = []
    #     arcuated_podao_contours, straight_podao_contours = podao_space_fusion_v2_pre(border_entity_info, "wza_podao")
    #     for cnt in arcuated_podao_contours + straight_podao_contours:
    #         x, y, w, h = cv2.boundingRect(cnt)
    #         bbox = [x, y, x + w, y + h]
    #         wza_ramp_space_info.append([cnt, bbox, ['无障碍坡道']])
    #     room_info = border_entity_info.get('room_info', [])
    #     room_info.extend(wza_ramp_space_info)
    #     border_entity_info['room_info'] = room_info
    #
    # # 住宅平面图和墙身大样图获取平面楼梯踏步，后面用于标记对象化
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.DINGCENG, DrawingType.WUMIAN,
    #                     DrawingType.JIFANG, DrawingType.BINANCENG,
    #                     DrawingType.WALL_DAYANG, DrawingType.UNDERGROUND]:
    #     result_final_list = get_tabu_mark(border_entity_info)
    #     border_entity_info['tabu_mark_list'] = result_final_list
    #
    # # 剖面图、墙身大样图增加栏杆完成面、空间完成面、窗台完成面
    # if drawing_type in [DrawingType.SECTION, DrawingType.WALL_DAYANG]:
    #     border_entity_info = add_completion_surface_pre(border_entity_info)
    #
    # # 获取剖面栏杆可踏面
    # if drawing_type in [DrawingType.WALL_DAYANG]:
    #     border_entity_info = get_ke_ta_mian_info(border_entity_info)
    #
    # # 住宅平面图中添加厨房操作台边线
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = add_kitchen_operate_line(border_entity_info)
    #
    # # 首层平面图增加台阶
    # if drawing_type in [DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = add_step(border_entity_info, result_path)
    #
    # # 楼梯大样图中增加剖面梯段
    # if drawing_type in [DrawingType.STAIR_DAYANG, DrawingType.PODAO]:
    #     border_entity_info = add_plan_profile_stair(border_entity_info, result_path)
    #
    # # 首层、非首层平面图、屋顶层平面图增加建筑轮廓空间
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.DINGCENG,
    #                     DrawingType.WUMIAN, DrawingType.JIFANG, DrawingType.BINANCENG, DrawingType.UNDERGROUND]:
    #     border_entity_info = get_buliding_contour_pre(border_entity_info)
    #
    # # 屋顶/机房层平面图，若一个空间内同时含有电梯厢构件和电梯机房空间文本，优先判断为空间文本指代的空间类型
    # if drawing_type in [DrawingType.DINGCENG, DrawingType.JIFANG]:
    #     border_entity_info = remove_elevatorRoom_name(border_entity_info)
    #
    # # 根据图纸类型，对栏杆进行修改
    # handrail_drawing_type_list = [DrawingType.WALL_DAYANG, DrawingType.STAIR_DAYANG, DrawingType.SECTION,
    #                               DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR_FIRST_FLOOR_NO_SPACE,
    #                               DrawingType.INDOOR, DrawingType.SECOND_THIRD_FLOOR, DrawingType.WUMIAN,
    #                               DrawingType.JIFANG, DrawingType.INDOOR_FIRST_FLOOR_ACCESS, DrawingType.UNDERGROUND,
    #                               DrawingType.UNDERGROUND_BASEMENT, DrawingType.JIANZHU_HUXING_DAYANG, DrawingType.BINANCENG,
    #                               DrawingType.FIRST_FLOOR_SITE_PLAN, DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION,
    #                               DrawingType.DINGCENG]
    # if drawing_type in handrail_drawing_type_list:
    #     border_entity_info = correct_handrail_type(border_entity_info, drawing_type)
    #
    # # 根据住宅平面图纸类型，将通过文本（高护窗栏杆）得到普通窗bbox，加入平面栏杆
    # handrail_drawing_type_list = [DrawingTypeArch.INDOOR_FIRST_FLOOR,
    #                               DrawingTypeArch.INDOOR,  DrawingTypeArch.WUMIAN,
    #                               DrawingTypeArch.JIFANG]
    # if drawing_type in handrail_drawing_type_list:
    #     border_entity_info = add_gaochaung_plan_handrail(border_entity_info, drawing_type)
    #
    # # 楼梯大样图中增加子图区域和矫正栏杆和窗户
    # if drawing_type in [DrawingType.STAIR_DAYANG]:
    #     border_entity_info = add_sub_draw_stair_dayang(border_entity_info, result_path)
    #     border_entity_info = correct_handrail_and_window(border_entity_info, result_path)
    # # 过滤bbox过大的风井
    # border_entity_info = remove_abnormal_fengjing(border_entity_info)
    # # 过滤bbox过小的空间（墙内间隙）
    # border_entity_info = remove_abnormal_room(border_entity_info)
    #
    # # 立面图中elevation_window图层的合并结果不用，可以把bbox去除
    # if drawing_type in [DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION]:
    #     border_entity_info = remove_elevation_window_bbox(border_entity_info)
    #
    # # 非地下图纸中的柱子结果都删除
    # if drawing_type not in [DrawingType.UNDERGROUND, DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = remove_pillar_bbox(border_entity_info)
    #
    # # 剖面图中的普通窗重置为剖面窗
    # if drawing_type in [DrawingType.SECTION, DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION]:
    #     border_entity_info = correct_elevation_window(border_entity_info)
    #
    # # 机房、屋顶平面图中添加对应的楼层离地高度
    # if drawing_type in [DrawingType.JIFANG, DrawingType.DINGCENG]:
    #     target_floor_dict = {DrawingType.JIFANG: 'jf_abs_height', DrawingType.DINGCENG: 'rf_abs_height'}
    #     border_entity_info = add_special_floor_mark_height(border_entity_info, target_floor_dict[drawing_type])
    # # 坡面图中添加层高、楼层数
    # if drawing_type in [DrawingType.SECTION, DrawingType.ELEVATION, DrawingType.SIDE_ELEVATION]:
    #     border_entity_info = add_layer_height(border_entity_info)
    #
    if drawing_type in [DrawingType.DECORATION_PLAN_LAYOUT]:
        # # 识别套内楼梯（客厅内的楼梯，一般出现在复式的一层，且一般只出现在住宅首层和非首层，不出现在机房、屋顶、屋面层）
        # border_entity_info = get_indoor_stair(border_entity_info)
        # # 识别套内楼梯间（独立的楼梯间，但与客厅、卧室、卫生间、书房等直接相连，一般出现在复式的一层、二层、三层）
        # border_entity_info = get_indoor_stair_room(border_entity_info)
        # 获取所有户门列表，将其放入属性中供后续使用
        border_entity_info['indoor_door_info_list'] = get_entrance_door_pre_decoration(border_entity_info)

    # # 平面图中走道空间获取，同时处理敞开楼梯间
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = correct_zoudao(border_entity_info)
    #
    # # 平面图中获取凹廊空间
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = get_ao_lang_info(border_entity_info)
    #
    # # 平面图中判断阳台细分类型，封闭阳台和开敞阳台
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.DINGCENG, DrawingType.WUMIAN,
    #                     DrawingType.JIFANG, DrawingType.BINANCENG]:
    #     border_entity_info = judge_balcony_type_pre(border_entity_info)
    #
    # # 平面图中获取开敞外廊和封闭走廊
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.DINGCENG, DrawingType.WUMIAN,
    #                     DrawingType.JIFANG, DrawingType.BINANCENG]:
    #     border_entity_info = get_open_corridor_pre(border_entity_info)
    #
    # # # 平面图中对电井的分类进行细化
    # # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.DINGCENG, DrawingType.WUMIAN,
    # #                     DrawingType.JIFANG, DrawingType.BINANCENG]:
    # #     border_entity_info = get_open_corridor_pre(border_entity_info)
    #
    # # 公共空间名称增加
    # border_entity_info = add_public_room_name_arch_elec(border_entity_info)
    #
    # # 强弱电井名称增加
    # border_entity_info = add_qiangruo_dianjing_name(border_entity_info)
    #
    # 获取已被切割开的卫生间干区的小空间置为卫生间干区
    if drawing_type in [DrawingType.DECORATION_PLAN_LAYOUT]:
        border_entity_info = add_washroom_dry_area_info(border_entity_info)

    # # "配电间"只在"住宅地下平面图"和"住宅首层平面图"中有
    # border_entity_info = filter_distribution_room(border_entity_info)
    #
    # # "热水机房"只在"住宅机房层平面图"和"住宅屋顶层平面图"中有
    # border_entity_info = filter_thermal_room(border_entity_info)
    #
    # # "排风机房"只在"住宅地下平面图"中有
    # border_entity_info = filter_ventilation_room(border_entity_info)
    #
    # # "加压机房"只在"住宅地下平面图"和"住宅机房层平面图"中有
    # border_entity_info = filter_compression_room(border_entity_info)
    #
    # # "排烟机房"只在"住宅地下平面图"和"住宅机房层平面图"中有
    # border_entity_info = filter_emission_room(border_entity_info)
    #
    # # "住宅首层平面图"和"住宅标准层平面图"中的"卧室"分类成"主卧"和"其他卧室"
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = classify_bedroom(border_entity_info)
    #
    # # TODO: !!! 将完整空间的后处理代码放在该位置前面 !!!
    #
    if drawing_type in [DrawingType.DECORATION_PLAN_LAYOUT]:
        # 构建空间拓扑图
        border_entity_info = build_room_graph_pre(border_entity_info, result_path)

    # recognize households
    if drawing_type in [DrawingType.DECORATION_PLAN_LAYOUT]:
        border_entity_info = get_household_list_pre(border_entity_info, result_path)
        border_entity_info = get_unit_list_pre(border_entity_info)
        border_entity_info = get_building_pre(border_entity_info)

    # # TODO: !!! 将空间细划分的后处理代码放在该位置后面 !!!
    #
    # # 对走道和大堂之间没有门隔开的情况分割走道和大堂
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = seperate_zoudao_and_lobby(border_entity_info)
    #     border_entity_info = seperate_zoudao_and_elevator_hall(border_entity_info)
    #     # 对卫生间和客厅之间没有门隔开的情况分割卫生间和客厅
    #     border_entity_info = separate_toilet_and_living_room(border_entity_info)
    #
    # # 对大堂和电梯厅之间没有门隔开的情况分割大堂和电梯厅
    # if drawing_type in [DrawingType.UNDERGROUND]:
    #     border_entity_info = seperate_lobby_and_elevator_hall(border_entity_info)
    # # 公共空间名称增加
    # border_entity_info = add_public_room_name_arch_elec(border_entity_info)
    #
    # # 平面图中楼梯间平台区域
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.DINGCENG, DrawingType.WUMIAN,
    #                     DrawingType.JIFANG, DrawingType.BINANCENG]:
    #     border_entity_info = get_stair_room_platform(border_entity_info)
    #
    # # 屋顶层平面图获取建筑的最大长，宽
    # if drawing_type in [DrawingType.DINGCENG]:
    #     border_entity_info = get_building_width_length(border_entity_info)
    #
    # # 住宅平面图中获取玄关、卫生间干区区域
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = get_household_hallway_and_washroom_dry_regions(border_entity_info)
    #
    # # 地下图纸中添加标高的获取
    # if drawing_type in [DrawingType.UNDERGROUND, DrawingType.PODAO]:
    #     border_entity_info = get_elevation_mark_in_underground(border_entity_info)
    #
    # # 平面图中获取所有外窗
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.DINGCENG, DrawingType.WUMIAN,
    #                     DrawingType.JIFANG, DrawingType.BINANCENG]:
    #     border_entity_info = get_outer_windows_pre(border_entity_info)
    #
    # # 平面图阳台中的"洗面器"/"洗脸盆"修改为"污水盆"
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.DINGCENG, DrawingType.WUMIAN,
    #                     DrawingType.JIFANG, DrawingType.BINANCENG]:
    #     border_entity_info = correct_sewage_sinks(border_entity_info)
    #
    # # 将飘窗空间从卧室|客厅|开放式厨房|卫生间|厨房|书房中分割出来
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = sep_Bay_window_room(border_entity_info)
    #
    # # 平面图中飘窗识别
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.DINGCENG,
    #                     DrawingType.BINANCENG]:
    #     border_entity_info = get_Bay_window_room(border_entity_info)
    #
    # # 平面图中添加封闭楼梯间、敞开楼梯间、防烟楼梯间、剪刀楼梯间的识别
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.DINGCENG, DrawingType.JIFANG,
    #                     DrawingType.BINANCENG]:
    #     border_entity_info = get_stair_room_info(border_entity_info)
    #
    # # 平面图中添加安全出口构件
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.DINGCENG,
    #                     DrawingType.JIFANG]:
    #     border_entity_info = get_emergency_exit_info(border_entity_info)
    #
    # # 获取门附近的门垛
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = get_men_duo_info(border_entity_info)
    #
    # # 添加卫生间排风井
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = get_washroom_pfj_info(border_entity_info)
    #
    # # 添加厨房油烟井
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = get_kitchen_yyj_info(border_entity_info)
    #
    # # 添加套内水管井空间
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = get_architect_pipe_room(border_entity_info)
    #
    # # 获取建筑面积标注
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.UNDERGROUND]:
    #     border_entity_info = get_arch_area_text_info(border_entity_info)
    #
    # 获取尺寸标注
    border_entity_info = get_all_anno_size_info(border_entity_info)
    #
    # # 获取门窗编号
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.UNDERGROUND]:
    #     border_entity_info = get_door_and_window_number_info(border_entity_info)
    #
    # # 获取建筑剖面标注
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.UNDERGROUND]:
    #     border_entity_info = get_arch_section_anno_info(border_entity_info)
    #
    # # 获取建筑索引
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.UNDERGROUND]:
    #     border_entity_info = get_arch_index_info(border_entity_info)
    #
    # # 纠正风井空间
    # border_entity_info = correct_fengjing_Room(border_entity_info)
    #

    # # 添加非承重墙构件

    # # 添加墙构件

    # border_entity_info = get_nobear_wall(border_entity_info)
    #
    # # 添加非机动车坡道信息、截水沟剖面
    # if drawing_type in [DrawingType.PODAO]:
    #     border_entity_info = get_podao_info(border_entity_info)
    #     border_entity_info = get_jieshuigou_info(border_entity_info)
    #
    # # 获取风井百叶(住宅平面图)
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = get_feng_jing_bai_ye_info(border_entity_info)
    #
    # # 走道空间同时置为走廊空间
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = duplicate_zoudao_to_zoulang(border_entity_info)
    #
    # # 空调板空间同时置为空调机位空间
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = duplicate_kongtiaoban_to_kongtiaojiwei(border_entity_info)
    #
    # # 添加与厨房相连的阳台为设备阳台
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = add_equipment_balcony_info(border_entity_info)
    #
    # # # 添加太阳能板位空间
    # # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    # #     border_entity_info = add_solar_spaces(border_entity_info)
    #
    # # 设备平台区分为户内和公区
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = judge_equipment_platform_type(border_entity_info)
    #
    # # 获取上人屋面信息
    # if drawing_type in [DrawingType.JIFANG]:
    #     border_entity_info = get_accessible_roof_info(border_entity_info)
    #
    # # 纠正变配电室
    # if drawing_type in [DrawingType.UNDERGROUND, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = correct_bian_pei_dian_shi_info(border_entity_info)
    #
    # # 建筑雨水立管开发
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR, DrawingType.DINGCENG,
    #                     DrawingType.WUMIAN, DrawingType.JIFANG, DrawingType.JIANZHU_HUXING_DAYANG]:
    #     border_entity_info = get_rain_pipe_info(border_entity_info)
    #
    # # 对门进行新分类子母门、双开门、单开门
    # border_entity_info = get_new_door_type_info(border_entity_info)
    #
    # # 将空间转换为构件
    # border_entity_info = convert_space_to_entity(border_entity_info)
    #
    # # 添加淋浴间
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = get_shower_house(border_entity_info)
    #
    #
    # # 纠正洗衣机地漏
    # if drawing_type in [DrawingType.INDOOR_FIRST_FLOOR, DrawingType.INDOOR, DrawingType.JIANZHU_HUXING_DAYANG]:
    #     border_entity_info = correct_xi_yi_di_lou_info(border_entity_info)
    #
    # # 添加排水沟
    # if drawing_type in [DrawingType.INDOOR_FIRST_FLOOR, DrawingType.UNDERGROUND]:
    #     border_entity_info = get_paishuigou_info(border_entity_info)
    #
    # # 添加橱柜
    # if drawing_type in [DrawingType.INDOOR, DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = get_kitchen_cabinet_info(border_entity_info)

    # 添加散水
    # if drawing_type in [DrawingType.INDOOR_FIRST_FLOOR]:
    #     border_entity_info = get_san_shui_info(border_entity_info)


    ##########################################
    #           根据空间来校正构件识别
    ##########################################
    ##########################################
    #        重构材料表/说明中的文字信息         #
    ##########################################
    # if drawing_type in [DrawingType.DECORATION_SANITARY_SCHEDULE]:
    #     border_entity_info = get_text_in_cell_aligned(border_entity_info)


    return border_entity_info


# 空间信息过滤
def room_info_filting(drawing_type, border_entity_info: BorderEntity):
    """

    Args:
        drawing_type: 图纸类型
        border_entity_info: 图框全量信息

    Returns:
        更新后的图纸全量信息
    """
    space_filter_config = DrawingConfig.SPACE_FILTER_CONFIG.value
    if drawing_type in space_filter_config:
        new_room_info = []
        for room in border_entity_info.room_info:
            for room_kw in space_filter_config[drawing_type]:
                room_name = str(room.name_list)
                if re.search(room_kw, room_name):
                    new_room_info.append(room)
        border_entity_info.room_info = new_room_info
    return border_entity_info
