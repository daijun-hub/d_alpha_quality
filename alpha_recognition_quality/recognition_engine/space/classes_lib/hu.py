import cv2

from ..space import Space
from typing import List
from ..base_type import SpaceBaseType
from ...border_entity import BorderEntity
from ...utils.utils_space import get_household_entity_list_by_anit_clockwise_seq
from ....common.utils import get_centroid, get_contours_iou, Iou_temp, get_contour_from_bbox, extend_margin_by_side, \
    point_euclidean_distance, anti_clockwise_angle, expand_contour, extend_margin
from shapely.geometry import Polygon
from ....common.utils2 import load_drawing_pkl
from ....common.CONSTANTS import *
from ....common.utils_draw_and_rule import *
from ....config_manager.architecture.drawing_config import DrawingType
from ....config_manager.electric.drawing_config import DrawingType as ele_drawingtype
from ....config_manager.decor_hvac.drawing_config import DrawingType as decor_hvac_drawingtype
from ....config_manager.text_config import TextType
import re
import numpy as np
from ....common.utils_draw_and_rule import get_cnt_center
from ...utils import *


class Hu(Space):
    chinese_name = "户"

    def __init__(self, space_object: Space, border_entity: BorderEntity, household_id) -> None:
        Space.copy(self, space_object)
        # self.border_entity = border_entity
        self.chinese_name = "户"
        self.space_base_type = SpaceBaseType.OTHERS
        # 是板房还是货量房，通过后续的extract_model_house步骤进行明确
        self.is_model_house = False
        # 是否和板房进行了匹配，通过该属性可以对户的匹配进行debug
        self.has_matched_model_house = False
        # 户编号, 相对于每一个图框范围 0, 1, ...
        self.household_id = household_id
        # 自定义属性
        # 为了获取户的层高，需要知道户所在的楼层，要求上层在创建楼栋模型的时候来刷新每一层所有户的楼层属性
        self.floor_num_list: List[str] = border_entity.floor_num_list
        self.rotation_angle = None  # 旋转角度
        self.household_type = None  # 户型
        self.flipped_from_model_house = None  # 与板房对比，是否是镜像户型
        self.household_contours_with_flip = None  # 户翻转轮廓
        # self.translation = None  # 后处理平移参数
        self.living_room_door_base_center = None  # 入户门土建连线的中心
        self.related_door_window_list = None  # 户内门窗类别
        # 碧桂园货板稽核
        self.livingroom_list = []  # 客厅列表
        self.restaurant_list = []  # 客餐厅
        self.bedroom_list = []  # 卧室列表
        self.washroom_list = []  # 卫生间列表
        self.balcony_list = []  # 阳台列表
        self.kitchen_list = []  # 厨房列表
        self.shuiguanjing_list = []  # 套内水管井列表
        self.labeled_height: float = 0.  # 标高
        self.labeled_height_dict = {}
        self.outer_wall_material: str = ""  # 外墙材料
        self.outer_wall_split_style: str = ""  # 外墙分裂方式
        self.wall_contour_list = []  # 墙列表
        self.household_rooms = []  # 户内空间列表
        self.door_list = []  # 门列表
        self.window_list = []  # 窗列表
        self.handrail_list = []  # 栏杆列表
        self.ran_qi_biao_list = []  # 燃气表列表
        self.re_shui_qi_list = []  # 热水器列表
        self.balcony_rain_v_pipe_list = []  # 阳台雨水立管列表
        self.rain_v_pipe_list = [] # 雨水立管列表
        self.washroom_v_pipe_list = []  # 卫生间立管列表
        self.balcony_drain_list = []  # 阳台地漏列表
        self.washroom_drain_list = []  # 卫生间地漏列表
        self.reserved_hole_list = []  # 预留孔洞列表
        self.K_hole_list = []  # K孔列表
        self.P_hole_list = []  # P孔列表
        self.B_hole_list = []  # B孔列表
        self.Q_hole_list = []  # Q孔列表
        self.kitchen_exhaust_pipe_list = []  # 厨房排烟管道 油烟管井
        self.liguan_list = []  # 立管列表
        self.waste_v_pipe_list = []  # 废水立管
        self.sewage_v_pipe_list = []  # 污水立管
        self.ping_mian_lan_gan_list = []  # 平面栏杆
        self.strong_electric_box_list = []  # 强电箱
        self.weak_electric_box_list = []  # 弱电箱
        self.visual_intercom_list = []  # 可视对讲
        self.household_centroid = None  # 户的质心
        self.living_room_door = None  # 入户门
        self.household_direction: List = []  # 户的方向 []
        self._update_known_apartment_property(border_entity)
        self._update_apartment_room_object(border_entity)
        self._update_living_room_door_object(border_entity)
        # 客厅标高，依赖户房间列表
        self.livingroom_mark_height = self.get_mark_height(border_entity)
        # 判断是否为复式户，但是暂不能确定是顶跃（仅在最高楼层是复式）还是叠墅（所有户型都是复式），记录复式户的套内楼梯
        self.is_compound_house = False
        self.is_compound_first_floor = False
        self.stair_center = None
        self.indoor_stair_bbox = None
        self.power_supply_system = ""
        self.plug_list = []
        self.circuit_list = []
        self.outlet_list = []
        self.equip_bound_plate = []
        # 添加户所属楼栋子项，在对比户的外墙材料时需要
        self.subproject_name = border_entity.subproject_name
        self.subproject_num_list = border_entity.subproject_num_list
        # 使用border_entity的简单属性
        self.ratio = border_entity.ratio
        self.major = border_entity.major
        self.drawing_name = border_entity.drawing_name
        self.ext_margin = border_entity.ext_margin
        self.cad_border_id = border_entity.cad_border_id
        self.drawing_type = border_entity.drawing_type
        # 装修暖通
        self.feng_guan_shi_nei_ji_list = []  # 风管式室内机
        self.fen_ti_shi_nei_ji_list = []  # 分体式室内机
        self.shi_wai_ji_list = []  # 室外机列表
        self.fen_ji_shui_qi_list = []
        self.temp_controller_list = []
        self.base_png_id = border_entity.base_png_id
        self.ac_style = None
        self.outline_contour = None

    def get_mark_height(self, border_entity):
        # 获取客厅标高
        living_rooms = [x for x in self.household_rooms if x.chinese_name in ['客厅', "客餐厅"]]
        if len(living_rooms) <= 0:
            print('Error: 没找到客厅')
            return None
        living_room = living_rooms[0]
        height_mark_list = border_entity.mark_object_dict.get('标高符号', [])
        mark_height = None
        for hm in height_mark_list:
            if Iou_temp(hm.bounding_rectangle.list, living_room.bbox) > 0.9:
                mark_height = hm.labeld_type_height_dict.get('建筑标高', None)
                if mark_height:
                    break

        return mark_height

    def get_cross_border_attribs(self, border_entity, building_object):
        # 获取标高属性
        self._get_labeled_height(building_object)
        # 获取外墙材料, 外墙分缝方式
        self._get_outer_wall_material_and_split_style(building_object)
        self._power_supply_system(building_object)
        # 获取空调系统形式
        self._get_ac_style(building_object)

    def _update_known_apartment_property(self, border_entity):
        '''
        获取户已知的属性
        '''
        household = border_entity.special_info_dict["household_list"][self.household_id]
        self.rotation_angle = household.rotation_angle
        self.household_type = household.household_type
        self.household_contours_with_flip = household.household_contours_with_flip
        self.living_room_door_base_center = household.living_room_door_base_center
        self.related_door_window_list = household.related_door_window_list
        self.household_centroid = get_centroid(self.contour.contour)  # 户的质心
        # 户的方向
        self.household_direction = list(self.living_room_door_base_center) + \
                                   list(self.household_centroid)
        # 记录是否是复式户的属性
        self.is_compound_house = household.is_compound_house
        self.is_compound_first_floor = household.is_compound_first_floor
        self.stair_center = household.stair_center
        self.indoor_stair_bbox = household.indoor_stair_bbox
        self.household_transform_params = household.household_transform_params
        # 更新转换参数
        # self.get_translation_params()

    def _update_apartment_room_object(self, border_entity):
        """
        将RoomNode对象替换为Space对象
        """
        household = border_entity.special_info_dict["household_list"][self.household_id]
        space_object_dict = border_entity.space_object_dict
        space_list = []
        another_space_list = []
        household_include_room_name_list = ["储藏室", "卧室", "书房", "客厅", "阳台", "开放式厨房", "家政间", "洗衣房", "衣帽间",
                                            "卫生间", "厨房", "无名称空间", "露台", "套内楼梯间", "飘窗", "保姆间", "菜地", "客餐厅",
                                            ]
        another_include_room_name_list = ["玄关", "卫生间干区"]
        for name, obj_list in space_object_dict.items():
            if name in household_include_room_name_list:
                space_list.extend(obj_list)
            elif name in another_include_room_name_list:
                another_space_list.extend(obj_list)

        # vis = [False] * len(space_list)
        # apartment.household_rooms = household.household_rooms
        # 目前户内空间的列表是RoomNode对象，需要替换为对应空间实例化之后的对象
        print("household rooms", len(household.household_rooms))
        for household_room in household.household_rooms:
            household_room_cnt = household_room.contour
            household_room_name_list = household_room.name_list
            for si, space in enumerate(space_list):
                # if vis[si]: continue
                space_cnt = space.contour.contour
                if get_contours_iou(household_room_cnt, space_cnt) > 0.99 and get_contours_iou(space_cnt,
                                                                                               household_room_cnt) > 0.99 and \
                        (space.chinese_name in household_room_name_list or space.chinese_name in ["无名称空间"]):
                    self.household_rooms.append(space)
                    space.rectified_contour = household_room.rectified_contour
                    space.rectified_contour_flip = household_room.rectified_contour_flip
                    break
        # 玄关和卫生间干区也要加到户里面，
        # entity_info_integration中识别户的时候玄关和卫生间干区还没分割出来
        # 因此只需要判断玄关和卫生间干区有没有在户内
        household_polygon = Polygon(self.contour.contour.squeeze())
        for space in another_space_list:
            space_polygon = Polygon(space.contour.contour.squeeze())
            if household_polygon.contains(space_polygon.buffer(0.1)):
                self.household_rooms.append(space)

        print("apartment rooms", len(self.household_rooms))

    def _update_living_room_door_object(self, border_entity):
        '''
        将ConnectDoor对象改为PingKaiMen对象
        '''
        household = border_entity.special_info_dict["household_list"][self.household_id]
        # apartment.living_room_door = household.living_room_door  # 入户门
        # 将入户门对象转换为平开门对象
        PingKiaMen_list = border_entity.entity_object_dict["平开门"]
        for PingKaimen in PingKiaMen_list:
            if Iou_temp(household.living_room_door.bbox, PingKaimen.bounding_rectangle.list) > 0.95:
                self.living_room_door = PingKaimen
                break

    def get_related_entities(self, border_entity):
        """
        获取相关的构件
        :param border_entity:
        :return:
        """
        self.get_related_hole(border_entity)
        self.get_outline_contour(border_entity)

        # 获取门列表
        self.door_list = self.get_related_door_list(border_entity)

        # 获取墙列表
        self.wall_contour_list = self.get_related_wall(border_entity)

        # 获取窗列表
        self.window_list = self.get_related_window_list(border_entity)

        # 获取平面栏杆
        self.handrail_list = self.get_related_handrail_list(border_entity)

        # 获取立管列表
        self.liguan_list = self.get_related_entity(border_entity, '立管')

        # 获取卫生间立管列表
        self.washroom_v_pipe_list = self.get_room_entity_list(border_entity, "卫生间", "立管")

        # 获取阳台地漏列表
        self.balcony_drain_list = self.get_room_entity_list(border_entity, "阳台", "地漏")

        # 获取卫生间地漏列表
        self.washroom_drain_list = self.get_room_entity_list(border_entity, "卫生间", "地漏")

        # 获取阳台雨水立管
        balcony_rain_v_pipe_list = self.get_room_entity_list(border_entity, "阳台", "阳台雨水立管")
        rain_v_pipe_list = self.get_room_entity_list(border_entity, "阳台", "雨水立管")
        self.balcony_rain_v_pipe_list = balcony_rain_v_pipe_list + rain_v_pipe_list

        # 获取雨水立管
        self.rain_v_pipe_list = self.get_related_entity(border_entity, '雨水立管')

        # 获取厨房排管道（烟道管井）
        self.kitchen_exhaust_pipe_list = self.get_room_entity_list(border_entity, "厨房", "厨房排烟管道")
        # 厨房没获取到导致厨房烟道管井也有问题
        # 因此如果没获取到，直接用户轮廓获取
        if not self.kitchen_exhaust_pipe_list:
            self.kitchen_exhaust_pipe_list = self.get_related_entity(border_entity, "厨房排烟管道")

        # 获取废水立管
        self.waste_v_pipe_list = self.get_related_entity(border_entity, "废水立管")

        # 获取污水立管
        self.sewage_v_pipe_list = self.get_related_entity(border_entity, "污水立管")

        # 获取平面栏杆
        self.ping_mian_lan_gan_list = self.get_related_entity(border_entity, "平面栏杆")

        # 获取燃气表
        self.ran_qi_biao_list = self.get_related_entity(border_entity, "燃气表")

        # 获取热水器
        self.re_shui_qi_list = self.get_related_entity(border_entity, "热水器")

        # 获取阳台
        self.balcony_list = self.get_related_space(border_entity, "阳台")

        # 获取厨房
        self.kitchen_list = self.get_related_space(border_entity, '厨房')

        # 获取卫生间
        self.washroom_list = self.get_related_space(border_entity, '卫生间')

        # 获取插座
        self.plug_list = self.get_related_entity(border_entity, '插座')

        # 获取开关
        self.circuit_list = self.get_related_entity(border_entity, '平面图开关') \
                            # + self.get_related_entity(border_entity, '单刀开关') + self.get_related_entity(border_entity, '双切开关')
                            # + self.get_related_entity(border_entity, '负荷开关')

        # 获取视口
        self.outlet_list = self.get_related_entity(border_entity, '电话插座') + self.get_related_entity(border_entity,
                                                                                                    '电视插座') + self.get_related_entity(
            border_entity, '信息插座')

        # 获取等电位联结板
        self.equip_bound_plate = self.get_related_entity(border_entity, '等电位连接板')

        # 获取客餐厅
        self.restaurant_list = self.get_related_space(border_entity, '客餐厅')

        # 强电箱 弱电箱 可视对讲
        self.strong_electric_box_list = self.get_related_entity(border_entity, "强电箱")
        self.weak_electric_box_list = self.get_related_entity(border_entity, "弱电箱")
        self.visual_intercom_list = self.get_related_entity(border_entity, "可视对讲")

        # 获取套内水管井
        self.shuiguanjing_list = self.get_related_shuiguanjing(border_entity)

        # 装修暖通
        self.feng_guan_shi_nei_ji_list = self.get_related_entity(border_entity, "风管式室内机")
        self.fen_ti_shi_nei_ji_list = self.get_related_entity(border_entity, "分体式室内机")
        self.shi_wai_ji_list = self.get_related_entity(border_entity, "室外机")
        self.deng_ju_list = self.get_related_entity(border_entity, "灯具")
        self.pu_tong_deng_list = self.get_related_entity(border_entity, "普通灯")
        self.fen_ji_shui_qi_list = self.get_related_entity(border_entity, "分集水器")
        self.temp_controller_list = self.get_related_entity(border_entity, "温度控制器")

    def get_related_entity(self, border_entity, entity_name, min_iou=0.5):
        """
        根据构件名字获取构件列表
        Args:
            border_entity:
            entity_name:
            min_iou:

        Returns:

        """
        related_entity_list = []
        entity_list = border_entity.entity_object_dict.get(entity_name, [])
        for entity_obj in entity_list:
            bbox = entity_obj.bounding_rectangle.list
            cnt = get_contour_from_bbox(bbox)
            if get_contours_iou(expand_contour(self.contour.contour, 1000 * border_entity.ratio[0]), cnt) > min_iou:
                related_entity_list.append(entity_obj)
        return related_entity_list

    def get_related_entity_from_list(self, entity_list, min_iou=0):
        """
        获取相关的entity
        Args:
            entity_list:
            min_iou:

        Returns:

        """
        related_entity_list = []
        for i in entity_list:
            if Iou_temp(i.bounding_rectangle, get_bbox_from_contour(self.contour.contour)) > min_iou:
                related_entity_list.append(i)
        return related_entity_list

    def get_related_shuiguanjing(self, border_entity, min_iou=0.5):
        """
        获取水管井列表
        :param border_entity:
        :param min_iou:
        :return:
        """
        # 获取到卫生间和厨房
        related_space_list = []
        shuiguanjing_list = border_entity.space_object_dict.get('套内水管井', [])
        washroom_contour_list = [self.get_unified_contour(i.contour.contour)[0] for i in self.washroom_list]
        washroom_bbox_list = [get_bbox_from_contour(i) for i in washroom_contour_list]
        kitchen_contour_list = [self.get_unified_contour(i.contour.contour)[0] for i in self.kitchen_list]
        kitchen_bbox_list = [get_bbox_from_contour(i) for i in kitchen_contour_list]

        for sgj_obj in shuiguanjing_list:
            sgj_bbox = get_bbox_from_contour(self.get_unified_contour(sgj_obj.contour.contour)[0])
            in_house = False
            for washroom_bbox in washroom_bbox_list:
                if Iou_temp(sgj_bbox, washroom_bbox) > min_iou:
                    related_space_list.append(sgj_obj)
                    in_house = True
                    break
            if in_house:
                continue
            for kitchen_bbox in kitchen_bbox_list:
                if Iou_temp(sgj_bbox, kitchen_bbox) > min_iou:
                    related_space_list.append(sgj_obj)
                    break
        return related_space_list

    def get_related_space(self, border_entity, space_name, min_iou=0.5):
        """
        根据构件名字获取构件列表
        Args:
            border_entity:
            entity_name:
            min_iou:

        Returns:

        """
        related_space_list = []
        space_list = border_entity.space_object_dict.get(space_name, [])
        for space_obj in space_list:
            cnt = space_obj.contour.contour
            if get_contours_iou(expand_contour(self.contour.contour, 800 * border_entity.ratio[0]), cnt) > min_iou:
                related_space_list.append(space_obj)
        return related_space_list

    def get_related_hole(self, border_entity):
        '''
        获取户内预留孔洞，K孔， P孔， B孔，Q孔列表
        '''
        # 获取预留孔洞，K孔，P孔，B孔， Q孔
        reserved_hole_entity_list = border_entity.entity_object_dict["预留孔洞"]
        k_hole_entity_list = border_entity.entity_object_dict.get('预留孔洞K', [])
        p_hole_entity_list = border_entity.entity_object_dict.get('预留孔洞P', [])
        b_hole_entity_list = border_entity.entity_object_dict.get('预留孔洞B', [])
        q_hole_entity_list = border_entity.entity_object_dict.get('预留孔洞Q', [])
        # print("预留孔洞的数量：", len(reserved_hole_entity_list))
        # K孔列表
        self.K_hole_list = get_household_entity_list_by_anit_clockwise_seq(self,
                                                                           k_hole_entity_list,
                                                                           self.living_room_door_base_center)

        # P孔列表
        self.P_hole_list = get_household_entity_list_by_anit_clockwise_seq(self,
                                                                           p_hole_entity_list,
                                                                           self.living_room_door_base_center,
                                                                           800 * max(border_entity.ratio)
                                                                           )

        # B孔列表
        self.B_hole_list = get_household_entity_list_by_anit_clockwise_seq(self, b_hole_entity_list,
                                                                           self.living_room_door_base_center)

        # Q孔列表
        self.Q_hole_list = get_household_entity_list_by_anit_clockwise_seq(self,
                                                                           q_hole_entity_list,
                                                                           self.living_room_door_base_center)

    def get_outline_contour(self, border_entity):
        """获取户的外围轮廓

        Args:
            border_entity (_type_): _description_
        """
        kernel_size = int(border_entity.ratio[0] * 400)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        self.outline_contour = expand_contour_by_cv(self.contour.contour, kernel)

    def get_related_wall(self, border_entity):
        """
        获取户内的墙
        Args:
            border_entity: 图框全量信息

        Returns:户内墙列表

        """
        house_center = get_centroid(self.contour.contour)
        room_indoor_door_base_center_point = self.living_room_door_base_center
        # 空间质心到入空间门中心的基础向量
        base_vector = [room_indoor_door_base_center_point[0] - house_center[0],
                       room_indoor_door_base_center_point[1] - house_center[1]]
        entity_info_list = []
        # 获取墙
        hu_contour_expand = self.outline_contour

        non_bear_wall_list = border_entity.entity_object_dict["墙"]
        for wall in non_bear_wall_list:
            wall_cnt = wall.contour.contour
            wall_center = get_centroid(wall_cnt)
            # expand_wall_cnt = expand_contour(wall_cnt, 20)
            if get_contours_iou(hu_contour_expand, wall_cnt) < 0.2:
                continue
            entity_vector = [wall_center[0] - house_center[0], wall_center[1] - house_center[1]]
            dis = point_euclidean_distance(wall_center, house_center)
            angle = anti_clockwise_angle(base_vector, entity_vector)
            entity_info_list.append([wall, wall_center, dis, angle])
        # 先按照夹角和径向距离进行排序
        entity_info_list.sort(key=lambda x: (x[3], x[2]))
        sorted_entity_list = [entity[0] for entity in entity_info_list]
        return sorted_entity_list

    def get_related_door_list(self, border_entity):
        """
        获取户内的门列表
        Args:
            border_entity: 图框全量信息

        Returns:户内门列表

        """
        related_door_list = []
        door_list = border_entity.entity_object_dict["平开门"] + border_entity.entity_object_dict["推拉门"] + \
                    border_entity.entity_object_dict["门联窗"]
        for related_dw in self.related_door_window_list:
            d_bbox = related_dw[1]
            d_cnt1, d_cnt2 = related_dw[2]
            for door in door_list:
                door_bbox = door.bounding_rectangle.list
                if Iou_temp(d_bbox, door_bbox) > 0.95:
                    door.rectified_contour = d_cnt1
                    door.rectified_contour_flip = d_cnt2
                    related_door_list.append(door)
                    break
        return related_door_list

    # house_center = get_centroid(self.contour.contour)
    # room_indoor_door_base_center_point = self.living_room_door_base_center
    # # 空间质心到入空间门中心的基础向量
    # base_vector = [room_indoor_door_base_center_point[0] - house_center[0],
    #                room_indoor_door_base_center_point[1] - house_center[1]]
    # entity_info_list = []
    # # 获取门
    # door_list = border_entity.entity_object_dict["平开门"] + border_entity.entity_object_dict["推拉门"]
    # for door in door_list:
    #     door_bbox = door.bounding_rectangle.list
    #     if self.living_room_door is not None and Iou_temp(self.living_room_door.bounding_rectangle.list, door_bbox) > 0.95:
    #         continue
    #     door_cnt = get_contour_from_bbox(door_bbox)
    #     if get_contours_iou(self.contour.contour, door_cnt) == 0:
    #         continue
    #     door_center = get_centroid(door_bbox)
    #     entity_vector = [door_center[0] - house_center[0], door_center[1] - house_center[1]]
    #     dis = point_euclidean_distance(door_center, house_center)
    #     angle = anti_clockwise_angle(base_vector, entity_vector)
    #     entity_info_list.append([door, door_center, dis, angle])
    # # 先按照夹角和径向距离进行排序
    # entity_info_list.sort(key=lambda x: (x[3], x[2]))
    # sorted_entity_list = [entity[0] for entity in entity_info_list]
    # return sorted_entity_list

    def get_related_window_list(self, border_entity):
        """
        获取户内的窗列表
        Args:
            border_entity: 图框全量信息

        Returns:户内窗列表

        """
        related_window_list = []
        window_list = border_entity.entity_object_dict["普通窗"] + border_entity.entity_object_dict["凸窗"] + \
                      border_entity.entity_object_dict["百叶"] + border_entity.entity_object_dict["转角窗"]
        piao_chuang_list = border_entity.space_object_dict.get('飘窗', [])
        for window in window_list:
            window_bbox = window.bounding_rectangle.list
            window_cnt = get_contour_from_bbox(window_bbox)
            cnt, cnt_flip = self.get_unified_contour(window_cnt)
            # 使用户的bbox容易将公区的窗户包含到户内
            # if Iou_temp(window_bbox, extend_margin(self.bbox, 100)) > 0.8:
            #     related_window_list.append(window)
            if get_contours_iou(expand_contour(self.contour.contour, 400 * border_entity.ratio[0]), window_cnt) > 0.7:
                related_window_list.append(window)
            else:
                for piao_chuang in piao_chuang_list:
                    if get_contours_iou(expand_contour(self.contour.contour, 500 * border_entity.ratio[0]), piao_chuang.contour.contour) > 0.5 and \
                            get_contours_iou(expand_contour(piao_chuang.contour.contour, 400 * border_entity.ratio[0]), window_cnt) > 0.1:
                        related_window_list.append(window)

        # for related_dw in self.related_door_window_list:
        #     w_bbox = related_dw[1]
        #     w_cnt1, w_cnt2 = related_dw[2]
        #     for window in window_list:
        #         window_bbox = window.bounding_rectangle.list
        #         if Iou_temp(w_bbox, window_bbox) > 0.95:
        #             window.rectified_contour = w_cnt1
        #             window.rectified_contour_flip = w_cnt2
        #             related_window_list.append(window)
        #             break
        return related_window_list

        # house_center = get_centroid(self.contour.contour)
        # room_indoor_door_base_center_point = self.living_room_door_base_center
        # # 空间质心到入空间门中心的基础向量
        # base_vector = [room_indoor_door_base_center_point[0] - house_center[0],
        #                room_indoor_door_base_center_point[1] - house_center[1]]
        # entity_info_list = []
        # # 获取窗
        # window_list = border_entity.entity_object_dict["普通窗"] + border_entity.entity_object_dict["凸窗"] +\
        #               border_entity.entity_object_dict["百叶"] + border_entity.entity_object_dict["转角窗"]
        # for window in window_list:
        #     window_bbox = window.bounding_rectangle.list
        #     extend_win_bbox = extend_margin_by_side(window_bbox, 10, 'long')
        #     window_cnt = get_contour_from_bbox(extend_win_bbox)
        #     if get_contours_iou(self.contour.contour, window_cnt) == 0:
        #         continue
        #     window_center = get_centroid(window_bbox)
        #
        #     entity_vector = [window_center[0] - house_center[0], window_center[1] - house_center[1]]
        #     dis = point_euclidean_distance(window_center, house_center)
        #     angle = anti_clockwise_angle(base_vector, entity_vector)
        #     entity_info_list.append([window, window_center, dis, angle])
        # # 先按照夹角和径向距离进行排序
        # entity_info_list.sort(key=lambda x: (x[3], x[2]))
        # sorted_entity_list = [entity[0] for entity in entity_info_list]
        # return sorted_entity_list

    def get_related_handrail_list(self, border_entity):
        """
        获取户内的栏杆列表
        Args:
            border_entity: 图框全量信息

        Returns:户内栏杆列表

        """
        house_center = get_centroid(self.contour.contour)
        room_indoor_door_base_center_point = self.living_room_door_base_center
        # 空间质心到入空间门中心的基础向量
        base_vector = [room_indoor_door_base_center_point[0] - house_center[0],
                       room_indoor_door_base_center_point[1] - house_center[1]]
        entity_info_list = []
        # 获取窗
        handrail_list = border_entity.entity_object_dict["平面栏杆"]
        for handrail in handrail_list:
            handrail_bbox = handrail.bounding_rectangle.list
            extend_handrail_bbox = extend_margin_by_side(handrail_bbox, 10, 'long')
            handrail_cnt = get_contour_from_bbox(extend_handrail_bbox)
            if get_contours_iou(self.contour.contour, handrail_cnt) == 0:
                continue
            handrail_center = get_centroid(handrail_bbox)

            entity_vector = [handrail_center[0] - house_center[0], handrail_center[1] - house_center[1]]
            dis = point_euclidean_distance(handrail_center, house_center)
            angle = anti_clockwise_angle(base_vector, entity_vector)
            entity_info_list.append([handrail, handrail_center, dis, angle])
        # 先按照夹角和径向距离进行排序
        entity_info_list.sort(key=lambda x: (x[3], x[2]))
        sorted_entity_list = [entity[0] for entity in entity_info_list]
        return sorted_entity_list

    def get_room_entity_list(self, border_entity, room_name, entity_name):
        """
        获取空间内的构件列表
        Args:
            border_entity: 图框全量信息

        Returns:空间内的构件列表

        """
        washroom_list = [room for room in self.household_rooms if room.chinese_name == room_name]
        pipe_list = border_entity.entity_object_dict[entity_name]
        all_pipe_list = []
        for washroom in washroom_list:
            sorted_pipe_list = get_household_entity_list_by_anit_clockwise_seq(washroom, pipe_list,
                                                                               self.living_room_door_base_center)
            all_pipe_list.extend(sorted_pipe_list)
        all_pipe_list.sort(key=lambda x: (x.angle_against_apartment, x.dist_to_apartment_centroid))
        sorted_pipe_list = [pipe for pipe in all_pipe_list]
        return sorted_pipe_list

    def _get_labeled_height(self, building_object):
        '''
        # 获取标高属性
        '''
        print("[Note] 获取户的楼层标高 ... ")
        # self.labeled_height
        for special_drawing_dict in building_object.special_drawing_list:
            section_border_dict = special_drawing_dict.get(DrawingType.SECTION, {})
            section_file_id = section_border_dict.get("file_id", None)
            if section_file_id is not None:
                section_border_entity = load_drawing_pkl(section_file_id)
                # 获取层高信息
                floor_r_height_dict = section_border_entity.special_info_dict.get("floor_r_height", None)
                floor_r_height_bbox = section_border_entity.special_info_dict.get('floor_r_height_bbox', {})
                floor_l_r_height = section_border_entity.special_info_dict.get('floor_l_r_height', None)
                print("floor_r_height_dict", floor_r_height_dict)
                floor_num = None
                for f in self.floor_num_list:
                    if f.isdigit():
                        floor_num = int(f)
                        break
                if floor_r_height_dict is not None and floor_num in floor_r_height_dict:
                    self.labeled_height = floor_r_height_dict[floor_num]
                    self.labeled_height_bbox = floor_r_height_bbox.get(floor_num, [0, 0, 0, 0])
                    print("[Note] labeled_height:{}, labeled_height_bbox:{} ".format(self.labeled_height, self.labeled_height_bbox))
                    self.labeled_height_file_id = section_border_entity.cad_border_id
                    self.labeled_height_pickle_id = section_file_id

                    for f in self.floor_num_list:
                        if f.isdigit():
                            f = int(f)
                        if f in floor_l_r_height:
                            self.labeled_height_dict[f] = floor_l_r_height.get(f)
            # print("labeled_height", self.labeled_height)

    def _get_ac_style(self, building_object):
        '''
        # 空调系统形式
        '''
        print("[Note] 获取户的空调系统形式 ... ")
        self.ac_style_bbox = None
        self.ac_style = None
        for special_drawing_dict in building_object.special_drawing_list:
            if self.ac_style: break
            for drawing_type, info_dict in special_drawing_dict.items():
                if drawing_type in [decor_hvac_drawingtype.DECORATION_AC_DESCRIPTION]:
                    design_file_id = info_dict['file_id']
                    design_border_entity = load_drawing_pkl(design_file_id)
                    # for debug
                    img_manager = design_border_entity.image_manager
                    img_copy = img_manager.load_from_manager(IMG_WITH_WALL_KEY)
                    all_text = design_border_entity.border_text_info[TextType.ALL]
                    ac_style_pattern = "空调采用([\u4e00-\u9fa5]{0,5}式)空调器"
                    for text in all_text:
                        ac_find_res = re.search(ac_style_pattern, text.extend_message)
                        if ac_find_res:
                            self.ac_style = ac_find_res.group(1)
                            self.ac_style_bbox = text.bbox.list
                            self.ac_style_file_id = design_border_entity.cad_border_id
                            self.ac_style_pickle_id = design_file_id
                            # for debug
                            img_copy = draw_chinese(img_copy, [text])
                            cv2.rectangle(img_copy, (self.ac_style_bbox[0], self.ac_style_bbox[1]),
                                                    (self.ac_style_bbox[2], self.ac_style_bbox[3]), (255, 255, 0), 3)
                            cv2.imwrite("hu_ac_style.png", img_copy)
                            break
        print("ac_style", self.ac_style)
        print("ac_style_bbox", self.ac_style_bbox)

    def _get_outer_wall_material_and_split_style(self, building_object):
        '''
        # 获取外墙材料
        '''
        # self.outer_wall_material
        print("[Note] 获取户的外墙材料和分裂方式 ... ")
        for special_drawing_dict in building_object.special_drawing_list:
            for drawing_type, info_dict in special_drawing_dict.items():
                if drawing_type in [DrawingType.EXTERIOR_WALL_MATERIAL_LIST]:
                    material_file_id = info_dict['file_id']
                    material_border_entity = load_drawing_pkl(material_file_id)
                    # 外墙材料表有些情况下分为商业部分和住宅部分两个图框，使用图名过滤掉商业部分
                    if is_business_material_border(material_border_entity.drawing_name):
                        continue
                    image_manager = material_border_entity.image_manager
                    img_h, img_w = image_manager.img_height, image_manager.img_width
                    # for debug
                    img_copy = image_manager.load_from_manager(IMG_WITH_WALL_KEY)
                    border_cell_contours = self._find_table_cells(material_border_entity)
                    ratio = material_border_entity.ratio
                    # print("[Note] border_cell_contours", len(border_cell_contours))
                    text_all = material_border_entity.border_text_info[TextType.ALL]
                    # 有些表格cell里面的文本不是同一个，影响正则匹配
                    # 将同一个cell的文本合并
                    cell_concat_text_list = self.concat_cell_text(border_cell_contours, text_all)
                    # 外墙材料表有些情况下分为商业部分和住宅部分同时在一个图框，找到住宅部分外墙材料表的文本位置
                    text_region_include = [0, 0, img_w, img_h]
                    # 添加函数找到住宅外墙材料表文本区域
                    zhuzhai_pattern = "((住宅|居住|居建|洋房).*外墙材料表)|(外墙材料表.{0,5}(住宅|居住|居建|洋房))"
                    comm_pattern = "((商业|配套|门楼|底商).*外墙材料表)|(外墙材料表.{0,5}(商业|配套|门楼|底商))"
                    text_region_include = self.find_zhuzhai_target_region_bbox(zhuzhai_pattern, comm_pattern, text_all,
                                                                               cell_concat_text_list, text_region_include)
                    if text_region_include is None:
                        continue
                    # for debug
                    # cv2.rectangle(img_copy, (text_region_include[0] + 20, text_region_include[1] + 20),
                    #               (text_region_include[2] - 20, text_region_include[3] - 20), (255, 255, 0), 10)
                    text_all = [text for text in text_all if Iou_temp(text.bbox.list, text_region_include) > 0.5]
                    cell_concat_text_list = [text for text in cell_concat_text_list if Iou_temp(text[:4], text_region_include) > 0.5]
                    print("cell_concat_text_list --> ", len(cell_concat_text_list))
                    self.cell_concat_text_vis = [False for _ in range(len(cell_concat_text_list))]
                    # print("cell_concat_text_vis --> ", len(self.cell_concat_text_vis))
                    border_cell_contours = [cnt for cnt in border_cell_contours if Iou_temp(get_bbox_from_contour(cnt), text_region_include) > 0.5]
                    # for debug
                    # for ci, cell in enumerate(border_cell_contours):
                    #     # print("cell", cell)
                    #     x1, y1, w, h = cv2.boundingRect(cell)
                    #     cv2.polylines(img_copy, [cell], True, (0, 255, 255), 10)
                    #     cv2.putText(img_copy, str(ci), (x1+w//2, y1+h//2), cv2.CHAIN_APPROX_SIMPLE, 2, (0, 0, 255), 3)
                    # cv2.imwrite("table_seg.png", img_copy)

                    ## 查找表头/列索引
                    table_title_name_list = ["使用部位", "材料类型", "做法.*注意事项"]
                    use_pos_bbox, type_bbox, material_warning_bbox = self.find_target_table_title_pos(cell_concat_text_list, table_title_name_list)
                    if use_pos_bbox is None:
                        print("没找到 {} 文本 ... ".format(table_title_name_list[0]))
                        continue
                    # 查找行索引
                    ignore_pattern = "配套|商铺|底商|门楼|入口|门廊|商业|搭配饰线"
                    tabel_row_name_list = ["(二层|板房).*主.*墙", "(上部(主体|建筑|建筑主体)?的?墙身)|主体墙身", "(住宅.*墙身)|(大面积墙身)"]
                    row_text_concat_list = self.find_target_table_row_pos(cell_concat_text_list, use_pos_bbox, tabel_row_name_list, ignore_pattern)
                    print("row_text_concat_list --> ", row_text_concat_list)
                    text_height = abs(use_pos_bbox[3] - use_pos_bbox[1]) if use_pos_bbox else 0
                    type_bbox_ext = extend_margin(type_bbox, text_height) if type_bbox else [0, 0, 0, 0]
                    # 有些情况下 "做法.*注意事项" 这一行多列
                    # 因此不能用整个单元格，而需要使用单元格左边+宽度15000mm
                    if material_warning_bbox:
                        w = material_warning_bbox[2] - material_warning_bbox[0]
                        if w > 15000 * ratio[0]:
                            material_warning_bbox[2] = material_warning_bbox[0] + int(15000 * ratio[0])
                    material_warning_bbox_ext = extend_margin(material_warning_bbox, text_height) if material_warning_bbox else [0,
                                                                                                                                 0,
                                                                                                                                 0,
                                                                                                                                 0]
                    # for debug
                    # cv2.rectangle(img_copy, tuple(material_warning_bbox_ext[:2]), tuple(material_warning_bbox_ext[2:]), (0,255,255), 2)
                    # cv2.imwrite("material_warning_bbox_ext.png", img_copy)

                    find_mat_row = False
                    find_split_row = False
                    for row_text_list in row_text_concat_list:
                        if not row_text_list: continue
                        if find_mat_row and find_split_row: break
                        material_msg_list = []
                        split_msg_list = []
                        for row_text in row_text_list:
                            row_bbox = row_text[:4]
                            row_bbox_ext = extend_margin(row_bbox, text_height)
                            print("Finding 材料类型 cell ... ")
                            target_mat_cnt = self.find_target_cell_contour(border_cell_contours,
                                                                           row_bbox_ext,
                                                                           type_bbox_ext)
                            print("Finding 分缝方式 cell ... ")
                            target_split_cnt = self.find_target_cell_contour(border_cell_contours,
                                                                             row_bbox_ext,
                                                                             material_warning_bbox_ext)

                            if target_mat_cnt is not None:
                                material_msg_list += self.find_cell_text_list(target_mat_cnt, text_all)
                                # for debug
                                # cv2.polylines(img_copy, [target_mat_cnt], True, (255, 0, 0), 10)
                                # # cv2.putText(img_copy, str(ci), (x1, y1), cv2.CHAIN_APPROX_SIMPLE, 2, (0, 0, 255), 3)
                                # cv2.imwrite("target_mat_cnt.png", img_copy)
                            # for debug
                            # for material_msg in material_msg_list:
                            #     text_bbox = material_msg[:4]
                            #     cv2.rectangle(img_copy, (text_bbox[0], text_bbox[1]), (text_bbox[2], text_bbox[3]), (0,255,255), 5)
                            if target_split_cnt is not None:
                                split_msg_list += self.find_cell_text_list(target_split_cnt, text_all)
                                # for debug
                                # cv2.polylines(img_copy, [target_split_cnt], True, (0, 255, 0), 10)
                                # # cv2.putText(img_copy, str(ci), (x1, y1), cv2.CHAIN_APPROX_SIMPLE, 2, (0, 0, 255), 3)
                                # cv2.imwrite("target_split_cnt.png", img_copy)
                        if not find_mat_row:
                            if material_msg_list: find_mat_row = True
                            self.outer_wall_material, self.outer_wall_material_bbox = self.find_outer_wall_material(material_msg_list)
                            # for debug
                            # if self.outer_wall_material is not None:
                            #     img_copy = draw_chinese(img_copy, text_all)
                            #     cv2.rectangle(img_copy, (self.outer_wall_material_bbox[0], self.outer_wall_material_bbox[1]),
                            #                             (self.outer_wall_material_bbox[2], self.outer_wall_material_bbox[3]), (255, 255, 0),
                            #                   3)
                            self.outer_wall_material_file_id = material_border_entity.cad_border_id
                            self.outer_wall_material_pickle_id = material_file_id

                        if not find_split_row:
                            self.outer_wall_split_style, self.outer_wall_split_style_bbox, find_split_row = self.find_outer_wall_split_style(split_msg_list, find_split_row)
                            # for debug
                            # if self.outer_wall_split_style_bbox is not None:
                            #     cv2.rectangle(img_copy,
                            #                   (self.outer_wall_split_style_bbox[0], self.outer_wall_split_style_bbox[1]),
                            #                   (self.outer_wall_split_style_bbox[2], self.outer_wall_split_style_bbox[3]),
                            #                   (0, 255, 255),
                            #                   3)
                            self.outer_wall_split_style_file_id = material_border_entity.cad_border_id
                            self.outer_wall_split_style_pickle_id = material_file_id
                        final_material_border_entity = material_border_entity
                        # for debug
                        # cv2.imwrite("hu_ex_mat_debug.png", img_copy)
        if self.outer_wall_split_style or self.outer_wall_material:
            print("subproject_name", final_material_border_entity.subproject_name)
            print("drawing_name", final_material_border_entity.drawing_name)
        print("outer_wall_split_style", self.outer_wall_split_style)
        print("outer_wall_material", self.outer_wall_material)

    def _split_string(self, s, split_sign_list):
        '''
        字符串切分
        '''
        res = []
        for split_sign in split_sign_list:
            if split_sign in s:
                split_s_list = s.split(split_sign)
                for split_s in split_s_list:
                    res += self._split_string(split_s, split_sign_list)
                return res
        else:
            return [s]

    def find_target_table_title_pos(self, cell_concat_text_list, table_title_name_list):
        '''
        找到表头位置
        '''
        table_title_bbox_list = [None for _ in range(len(table_title_name_list))]
        for ci, text in enumerate(cell_concat_text_list):
            if self.cell_concat_text_vis[ci]: continue
            text_bbox = text[:4]
            text_msg = text[-1]
            for i, table_title_name in enumerate(table_title_name_list):
                if re.search(table_title_name, text_msg):
                    table_title_bbox_list[i] = text_bbox
                    self.cell_concat_text_vis[ci] = True
                    print(f"{table_title_name}cnt id", ci)
                    break
        return table_title_bbox_list

    def concat_cell_text(self, border_cell_contours, text_all):
        '''
        合并表格内部的文本
        '''
        cell_concat_text_list = []
        for cell_contour in border_cell_contours:
            cell_text_list = []
            x, y, w, h = cv2.boundingRect(cell_contour)
            for text in text_all:
                text_bbox = text.bbox.list
                text_msg = text.extend_message
                if get_contours_iou(cell_contour, get_contour_from_bbox(text_bbox)):
                    cell_text_list.append(text_bbox + [text_msg])
            concat_text = self._concat_text(cell_text_list)
            cell_concat_text_list.append([x, y, x + w, y + h, concat_text])
        return cell_concat_text_list

    def find_target_table_row_pos(self, cell_concat_text_list, use_pos_bbox, tabel_row_name_list, ignore_pattern):
        '''
        找到行索引
        '''
        row_bbox_concat_list = [[] for _ in range(len(tabel_row_name_list))]
        cell_concat_text_list_col = list(
            filter(lambda x: use_pos_bbox[0] - 5 <= get_centroid(x[:4])[0] <= use_pos_bbox[2] + 5,
                   cell_concat_text_list))
        for text in cell_concat_text_list_col:
            text_idx = cell_concat_text_list.index(text)
            if self.cell_concat_text_vis[text_idx]: continue
            text_bbox = text[:4]
            text_msg = text[-1]
            # 有些表格行索引也有所需的关键字，需要左右两边的bbox中的文本过滤
            # 根据文本bbox的宽和使用部位的宽判断其左右两边是否还有其他bbox
            text_msg_near = self.find_near_bbox_text(text_bbox, use_pos_bbox, cell_concat_text_list_col)
            if text_msg_near:
                print("text_msg: ", text_msg)
                print("找到杭索引附近的文本: ", text_msg_near)
            # 过滤字段
            # ignore_pattern = "配套|商铺|底商|门楼|入口"
            if re.search(ignore_pattern, text_msg_near + text_msg): continue
            # 在“使用部位”表头下获取“*二层 ** 板房 *”, “*主体 * 墙身 *”, “*上部 * 墙身 *”, “*住宅 * 墙身 *”，
            # 上述字段有多个，则依据板房＞主体 > 上部 > 住宅的优先级取用
            if max(use_pos_bbox[0], text_bbox[0]) > min(use_pos_bbox[2], text_bbox[2]): continue
            for i, tabel_row_name in enumerate(tabel_row_name_list):
                if self.cell_concat_text_vis[text_idx]: continue
                if re.search(tabel_row_name, text_msg):
                    row_bbox_concat_list[i].append(text)
                    self.cell_concat_text_vis[text_idx] = True
        return row_bbox_concat_list

    def find_near_bbox_text(self, text_bbox, use_pos_bbox, cell_concat_text_list):
        use_pos_bbox_width = abs(use_pos_bbox[0] - use_pos_bbox[2])
        text_bbox_width = abs(text_bbox[0] - text_bbox[2])
        tol = 5
        return_text_msg_near = ""
        if abs(text_bbox_width - use_pos_bbox_width) > tol:
            for near_text in cell_concat_text_list:
                near_text_bbox = near_text[:4]
                text_msg_near = near_text[-1]
                near_text_bbox_width = abs(near_text_bbox[0] - near_text_bbox[2])
                if abs(text_bbox_width + near_text_bbox_width - use_pos_bbox_width) < tol and \
                        (abs(near_text_bbox[0] - use_pos_bbox[0]) < tol or abs(
                            near_text_bbox[2] - use_pos_bbox[2]) < tol) and \
                        Iou_temp(extend_margin_by_side(near_text_bbox, tol), text_bbox) > 0:
                    return_text_msg_near = text_msg_near
                    break
        return return_text_msg_near

    def find_target_cell_contour(self, border_cell_contours, row_bbox, col_bbox, col_len = None):
        target_cell_cnt = None
        target_bbox = [int(col_bbox[2]*0.7), row_bbox[1], col_bbox[2], row_bbox[3]]
        target_center = get_centroid(target_bbox)
        # print("border_cell_contours --> ", len(border_cell_contours))
        for ci, cnt in enumerate(border_cell_contours):
            # if self.cell_concat_text_vis[ci]: continue
            # print("ci ", ci)
            cnt_polygon = Polygon(cnt.squeeze())
            target_center_pt = Point(target_center[0], target_center[1])
            # target_mat_center_pt = Point(target_mat_center[0], target_mat_center[1])
            if cnt_polygon.contains(target_center_pt):
                target_cell_cnt = cnt
                self.cell_concat_text_vis[ci] = True
                print("cnt id", ci)
                break
        return target_cell_cnt

    def find_cell_text_list(self, target_cell_cnt, text_all):
        msg_list = []
        for text in text_all:
            text_bbox = text.bbox.list
            text_msg = text.extend_message
            if target_cell_cnt is not None and Iou_temp(text_bbox, get_bbox_from_contour(target_cell_cnt)) > 0.5:
                if re.search("型号", text_msg):
                    print("[Note] find ", text_msg)
                else:
                    text_msg = text_msg.replace(" ", "")
                    text_msg = text_msg.replace("\r", "")
                    text_msg = text_msg.replace("\n", "")
                    msg_list.append(text_bbox + [text_msg.strip()])
        return msg_list

    def _concat_text(self, split_msg_list):
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

    def _find_table_cells(self, border_entity):
        '''
        找到表格中的cell
        '''
        origin_border_entity_info = border_entity.origin_border_entity_info
        space_scale = border_entity.space_scale
        border_coord = border_entity.border_coord
        ratio = border_entity.ratio

        image_manager = border_entity.image_manager
        h, w = image_manager.img_height, image_manager.img_width
        # for debug
        # img_copy = image_manager.load_from_manager(IMG_WITH_WALL_KEY)
        bg = np.zeros((h, w, 3), dtype="uint8")
        layer_to_check = ["engineering_work_table_line"]
        class_to_check = ['Line', 'Polyline', 'Polyline2d']
        table_line_dict = get_origin_border_entity_info_rule(origin_border_entity_info, layer_to_check,
                                                             class_to_check, space_scale, border_coord, ratio)
        line_list = []
        for _, entity_list in table_line_dict.items():
            line_list.extend(entity_list)
        # 过滤弧线
        line_list = list(filter(lambda x: len(x) == 4, line_list))

        for line_slab in line_list:
            if point_euclidean_distance(line_slab[:2], line_slab[2:]) < 1000 * ratio[0]: continue
            cv2.line(bg, tuple(line_slab[:2]), tuple(line_slab[2:]), (255, 255, 255), 1)
        # for debug
        # cv2.imwrite("/Users/xuan.ma/Desktop/bg.png", bg)
        gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)

        if '3.4' in cv2.__version__:
            _, contours_tree, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours_tree, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cells = [contours_tree[i] for i in range(len(contours_tree)) if hierarchy[0][i][3] >= 0]
        cells = [cell for cell in cells if 10 * 10 * ratio[0] * ratio[1] < cv2.contourArea(cell) < (w * h) * 0.6]
        # 过滤宽高过大的cnt
        cells = list(filter(lambda x: cv2.boundingRect(x)[2]< w//2 or cv2.boundingRect(x)[3] < h//2, cells))
        print("[Note] cells ", len(cells))
        # for debug
        # cells = [expand_contour(cell, 20) for cell in cells]
        # for ci, cell in enumerate(cells):
        #     # print("cell", cell)
        #     x1, y1, w, h = cv2.boundingRect(cell)
        #     cv2.polylines(img_copy, [cell], True, (0, 255, 255), 10)
        #     cv2.putText(img_copy, str(ci), (x1, y1), cv2.CHAIN_APPROX_SIMPLE, 2, (0, 0, 255), 3)
        # cv2.imwrite("/Users/xuan.ma/Desktop/table_seg.png", img_copy)
        return cells

    def _power_supply_system(self, building_object):
        for special_drawing_dict in building_object.special_drawing_list:
            info_dict = special_drawing_dict.get(ele_drawingtype.PEIDIAN_PEIDIANXIANG_SYSTEM)
            if info_dict:
                pkl_id = info_dict['file_id']
                pkl = load_drawing_pkl(pkl_id)
                duanluqian_list = pkl.entity_object_dict.get("断路器", [])
                for duanluqian in duanluqian_list:
                    if duanluqian.belong_hu:
                        duanluqi_info = duanluqian.belong_hu
                        if self.household_type in duanluqi_info:
                            self.power_supply_system = duanluqian.power_supply_system
                            break

    def get_unified_contour(self, contour):
        """
        获取该户套内的空间、构件的统一的坐标
        :param contour: 空间、构件的原始contour
        :return: 空间、构件统一之后的 contour 和 同时做了翻转的 contour
        """
        # [
        #     [x1, y1],
        #     [rotation_angle, img_bg.shape[:2]],
        #     [household_x1, household_x1_new],
        #     [household_y1, household_y1_new],
        #     [rotation_angle, [img_new_size, img_new_size]],
        #     [door_cent_new[0], ratio[0], ratio_fixed, center_union[0]],
        #     [door_cent_new[1], ratio[1], ratio_fixed, center_union[1]]
        # ]
        t1, r1, t2_x, t2_y, r2, t3_x, t3_y = self.household_transform_params
        cnt_cp = contour.copy()

        # d_w[2][:, :, 0] -= x1
        # d_w[2][:, :, 1] -= y1
        cnt_cp[:, :, 0] -= t1[0]
        cnt_cp[:, :, 1] -= t1[1]

        # d_w[2] = rotate_contour(d_w[2], rotation_angle, img_bg.shape[:2])
        cnt_cp = rotate_contour(cnt_cp, r1[0], r1[1])

        # d_w[2][:, :, 0] -= household_x1
        # d_w[2][:, :, 0] += household_x1_new
        cnt_cp[:, :, 0] -= t2_x[0]
        cnt_cp[:, :, 0] += t2_x[1]

        # d_w[2][:, :, 1] -= household_y1
        # d_w[2][:, :, 1] += household_y1_new
        cnt_cp[:, :, 1] -= t2_y[0]
        cnt_cp[:, :, 1] += t2_y[1]

        # d_w[2] = rotate_contour(d_w[2], rotation_angle, [img_new_size, img_new_size])
        cnt_cp = rotate_contour(cnt_cp, r2[0], r2[1])

        # d_w[2][:, :, 0] -= door_cent_new[0]
        # d_w[2][:, :, 0] = d_w[2][:, :, 0] / ratio[0] * ratio_fixed
        # d_w[2][:, :, 0] += center_union[0]
        cnt_cp[:, :, 0] -= t3_x[0]
        cnt_cp[:, :, 0] = cnt_cp[:, :, 0] / t3_x[1] * t3_x[2]
        cnt_cp[:, :, 0] += t3_x[3]

        # d_w[2][:, :, 1] -= door_cent_new[1]
        # d_w[2][:, :, 1] = d_w[2][:, :, 1] / ratio[1] * ratio_fixed
        # d_w[2][:, :, 1] += center_union[1]
        cnt_cp[:, :, 1] -= t3_y[0]
        cnt_cp[:, :, 1] = cnt_cp[:, :, 1] / t3_y[1] * t3_y[2]
        cnt_cp[:, :, 1] += t3_y[3]

        # d_w[2] = d_w[2].astype(int)
        # cnt_new = d_w[2].copy()
        # cnt_new[:, :, 1] = 2 * center_union[0] - d_w[2][:, :, 1]
        cnt_cp = cnt_cp.astype(int)
        cnt_cp_flip = cnt_cp.copy()
        cnt_cp_flip[:, :, 1] = 2 * t3_x[3] - cnt_cp[:, :, 1]

        # if self.translation is not None:
        #     flip_status, sub_tx, sub_ty = self.translation
        # 将户轮廓中心点都平移到（4000，4000）
        # (sub_tx, sub_ty), (sub_tx_flip, sub_ty_flip) = self.translation
        # cnt_cp[:, 0, 0] = cnt_cp[:, 0, 0] - sub_tx
        # cnt_cp[:, 0, 1] = cnt_cp[:, 0, 1] - sub_ty
        # cnt_cp_flip[:, 0, 0] = cnt_cp_flip[:, 0, 0] - sub_tx_flip
        # cnt_cp_flip[:, 0, 1] = cnt_cp_flip[:, 0, 1] - sub_ty_flip

        return cnt_cp, cnt_cp_flip

    def reverse_unified_contour(self, unified_contour, isflip=False):
        """
        将套内空间、构件的统一坐标转换回该图框中
        :param unified_contour: 空间、构件的统一contour
        :param is_flip: 配合get_unified_contour中使用的轮廓，转换时需要指定is_flip
        :return: 空间、构件的统一坐标转换回来的contour
        """
        # [
        #     [x1, y1],
        #     [rotation_angle, img_bg.shape[:2]],
        #     [household_x1, household_x1_new],
        #     [household_y1, household_y1_new],
        #     [rotation_angle, [img_new_size, img_new_size]],
        #     [door_cent_new[0], ratio[0], ratio_fixed, center_union[0]],
        #     [door_cent_new[1], ratio[1], ratio_fixed, center_union[1]]
        # ]
        # (sub_tx, sub_ty), (sub_tx_flip, sub_ty_flip) = self.translation
        t1, r1, t2_x, t2_y, r2, t3_x, t3_y = self.household_transform_params
        cnt_cp = unified_contour.copy()
        if isflip:
            cnt_cp_flip = cnt_cp.copy()

            # cnt_cp_flip[:, 0, 0] = cnt_cp_flip[:, 0, 0] + sub_tx_flip
            # cnt_cp_flip[:, 0, 1] = cnt_cp_flip[:, 0, 1] + sub_ty_flip

            cnt_cp_flip[:, :, 1] = 2 * t3_x[3] - cnt_cp_flip[:, :, 1]
            cnt_cp = cnt_cp_flip
        # else:
        #     cnt_cp[:, 0, 0] = cnt_cp[:, 0, 0] + sub_tx
        #     cnt_cp[:, 0, 1] = cnt_cp[:, 0, 1] + sub_ty

        # d_w[2][:, :, 1] -= center_union[1]
        # d_w[2][:, :, 1] = d_w[2][:, :, 1] * ratio[1] / ratio_fixed
        # d_w[2][:, :, 1] += door_cent_new[1]
        cnt_cp[:, :, 1] -= t3_y[3]
        cnt_cp[:, :, 1] = cnt_cp[:, :, 1] * t3_y[1] / t3_y[2]
        cnt_cp[:, :, 1] += t3_y[0]

        # d_w[2][:, :, 0] -= center_union[0]
        # d_w[2][:, :, 0] = d_w[2][:, :, 0] * ratio[0] / ratio_fixed
        # d_w[2][:, :, 0] += door_cent_new[0]
        cnt_cp[:, :, 0] -= t3_x[3]
        cnt_cp[:, :, 0] = cnt_cp[:, :, 0] * t3_x[1] / t3_x[2]
        cnt_cp[:, :, 0] += t3_x[0]

        # d_w[2] = d_w[2].astype(int)
        cnt_cp = cnt_cp.astype(int)

        # d_w[2] = rotate_contour(d_w[2], -rotation_angle, [img_new_size, img_new_size])
        cnt_cp = rotate_contour(cnt_cp, -r2[0], r2[1])

        # d_w[2][:, :, 1] -= household_y1_new
        # d_w[2][:, :, 1] += household_y1
        cnt_cp[:, :, 1] -= t2_y[1]
        cnt_cp[:, :, 1] += t2_y[0]

        # d_w[2][:, :, 0] -= household_x1_new
        # d_w[2][:, :, 0] += household_x1
        cnt_cp[:, :, 0] -= t2_x[1]
        cnt_cp[:, :, 0] += t2_x[0]

        # d_w[2] = rotate_contour(d_w[2], -rotation_angle, img_bg.shape[:2])
        cnt_cp = rotate_contour(cnt_cp, -r1[0], r1[1])

        # d_w[2][:, :, 1] += y1
        # d_w[2][:, :, 0] += x1
        cnt_cp[:, :, 1] += t1[1]
        cnt_cp[:, :, 0] += t1[0]

        return cnt_cp

    def find_outer_wall_material(self, material_msg_list):
        print("[Note] outer_wall_material ", material_msg_list)
        # 排序，可以方便货量对比
        material_msg_list.sort(key=lambda x: (x[1], x[0]))
        outer_wall_material = ','.join([msg[-1] for msg in material_msg_list])
        _xmin_temp, _ymin_temp, _xmax_temp, _ymax_temp = float("inf"), float("inf"), -float("inf"), -float("inf")
        for msg in material_msg_list:
            _xmin_temp = min(_xmin_temp, msg[0])
            _ymin_temp = min(_ymin_temp, msg[1])
            _xmax_temp = max(_xmax_temp, msg[2])
            _ymax_temp = max(_ymax_temp, msg[3])
        outer_wall_material_bbox = [_xmin_temp, _ymin_temp, _xmax_temp, _ymax_temp]
        return outer_wall_material, outer_wall_material_bbox

    def find_outer_wall_split_style(self, split_msg_list, find_split_row):
        split_msg = self._concat_text(split_msg_list)
        print("split_msg ", split_msg)
        pattern = "分缝|通缝|缝宽|缝色"
        if not re.search(pattern, split_msg):
            print(f"没找到 {pattern} 文本... ")
            return None, None, find_split_row
        # num = 10
        # seq_list = list(range(num)) + list([chr(ord("a")+i) for i in range(num)]) + list([chr(ord("A")+i) for i in range(num)])
        # item_split_char1 = "、"
        # item_split_char2 = "."
        # split_sign_list = ["。"]
        # for item_split_num,item_split_char  in list(zip(seq_list, item_split_char1 * len(seq_list))) + list(zip(seq_list, item_split_char2 * len(seq_list))):
        #     split_sign = str(item_split_num) + item_split_char
        #     split_sign_list.append(split_sign)
        # msg_list = self._split_string(split_msg, split_sign_list)
        outer_wall_split_style = None
        outer_wall_split_style_bbox = None
        split_width = ""
        h_split_width = ""
        v_split_width = ""
        split_color = ""
        color_ref = ""
        # for msg in msg_list:
        # 查找缝宽, 颜色和(*缝色|*色号)*参
        if re.search("[^横竖]缝宽", split_msg):
            # search_obj = re.search("[^横竖]缝宽为?(\d*m*)", split_msg)
            search_res_list = re.findall("[^横竖]缝宽为?(\d*m*)", split_msg)
            # print("search_obj", search_obj.group())
            if search_res_list:
                split_width = ",".join(search_res_list)
        if re.search("横缝宽", split_msg):
            search_obj = re.search("横缝宽为?(\d*m*)", split_msg)
            if search_obj:
                h_split_width = search_obj.group(1)
        if re.search("竖缝宽", split_msg):
            search_obj = re.search("竖缝宽为?(\d*m*)", split_msg)
            if search_obj:
                v_split_width = search_obj.group(1)
        if re.search("缝?色", split_msg):
            pattern_list = ["缝色为?([\u4E00-\u9FA5]{1,5}色)，",
                            "[\(\（]([\u4E00-\u9FA5]{1,5}色)[\)\）]",
                            "([\u4E00-\u9FA5]{1,5}色[\u4E00-\u9FA5]{0,5})(回|填)缝"]
            for pi, pattern in enumerate(pattern_list):
                search_res_list = re.findall(pattern, split_msg)
                if search_res_list:
                    # print("search_obj", search_obj.group())
                    # print("search_obj.group(0)", search_obj.group(0))
                    # print("search_obj.group(1)", search_obj.group(1))
                    if pi <= 1:
                        split_color += ",".join([res for res in search_res_list])
                    else:
                        split_color += ",".join([res[0] for res in search_res_list])
                    # break
        if re.search("(缝色|色号)参", split_msg):
            # color_ref = re.search("(缝色|色号)参.*([a-zA-Z0-9]*)", split_msg).group()
            search_obj = re.search("(缝色|色号)参.?[\u4E00-\u9FA5\s]*([a-zA-Z0-9-\s]*)", split_msg)
            if search_obj:
                color_ref = search_obj.group(2)

        final_s_list = list(filter(lambda x: x, [split_width, h_split_width, v_split_width, split_color, color_ref]))
        if final_s_list:
            find_split_row = True
            outer_wall_split_style = ",".join(final_s_list)
            # 找到文本的位置
            _xmin_temp, _ymin_temp, _xmax_temp, _ymax_temp = float("inf"), float("inf"), -float("inf"), -float("inf")
            for msg in split_msg_list:
                _xmin_temp = min(_xmin_temp, msg[0])
                _ymin_temp = min(_ymin_temp, msg[1])
                _xmax_temp = max(_xmax_temp, msg[2])
                _ymax_temp = max(_ymax_temp, msg[3])
            outer_wall_split_style_bbox = [_xmin_temp, _ymin_temp, _xmax_temp, _ymax_temp]
        return outer_wall_split_style, outer_wall_split_style_bbox, find_split_row

    def find_zhuzhai_target_region_bbox(self, zhuzhai_pattern, comm_pattern, text_all, text_concat_list,
                                        text_region_include):
        # 先确定是否有商业外墙材料表和住宅外墙材料表
        zhuzhai_text_bbox = None
        comm_text_bbox = None
        for text in text_concat_list:
            text_bbox = text[:4]
            text_msg = text[-1]
            if re.search(zhuzhai_pattern, text_msg):
                print("text_msg", text_msg)
                zhuzhai_text_bbox = text_bbox
            if re.search(comm_pattern, text_msg):
                print("text_msg", text_msg)
                comm_text_bbox = text_bbox
        # 表格合并问题导致没获取到商业外墙材料表
        # 通过外墙材料表文本外扩获取
        # zhuzhai_pattern = "(住宅|居住|居建|洋房).*外墙材料表|外墙材料表.{0,5}(住宅|居住|居建|洋房)"
        # comm_pattern = "(商业|配套|门楼|底商).*外墙材料表|外墙材料表.{0,5}(商业|配套|门楼|底商)"
        if zhuzhai_text_bbox is None:
            zhuzhai_text_bbox = self.find_target_text_bbox(text_all, zhuzhai_pattern, "住|居|居|洋|外")
        if comm_text_bbox is None:
            comm_text_bbox = self.find_target_text_bbox(text_all, comm_pattern, "商|配|门|底|外")
        if comm_text_bbox is None:
            print("没找到商业外墙材料表 。。。 ")
            return text_region_include

        if zhuzhai_text_bbox is None or comm_text_bbox is None:
            return text_region_include
        # 1. 住宅外墙材料表和商业外墙材料表上下放置
        # bbox在宽度方向的投影出合度大于0.5
        if self.find_line_intersection_len(zhuzhai_text_bbox, comm_text_bbox, proj_dir="width") / abs(
                zhuzhai_text_bbox[2] - zhuzhai_text_bbox[0]) > 0.5:
            # 住宅外墙材料表在上，商业外墙材料表在下
            if zhuzhai_text_bbox[1] < comm_text_bbox[1]:
                text_region_include = [0, 0, text_region_include[2], comm_text_bbox[1]]
                print("住宅外墙材料表在上，商业外墙材料表在下")
                return text_region_include
            # 商业外墙材料表在上，住宅外墙材料表在下
            else:
                text_region_include = [0, zhuzhai_text_bbox[2], text_region_include[2], text_region_include[3]]
                print("商业外墙材料表在上，住宅外墙材料表在下")
                return text_region_include
        # 2. 住宅外墙材料表和商业外墙材料表左右放置
        # bbox在高度方向的投影出合度大于0.5
        if self.find_line_intersection_len(zhuzhai_text_bbox, comm_text_bbox, proj_dir="height") / abs(
                zhuzhai_text_bbox[3] - zhuzhai_text_bbox[1]) > 0.5:
            # 住宅外墙材料表在左，商业外墙材料表在右
            if zhuzhai_text_bbox[0] < comm_text_bbox[2]:
                text_region_include = [0, 0, comm_text_bbox[0], text_region_include[3]]
                print("住宅外墙材料表在左，商业外墙材料表在右")
                return text_region_include
            # 商业外墙材料表在左，住宅外墙材料表在右
            else:
                text_region_include = [zhuzhai_text_bbox[0], zhuzhai_text_bbox[3], text_region_include[2],
                                       text_region_include[3]]
                print("商业外墙材料表在左，住宅外墙材料表在右")
                return text_region_include

    def find_line_intersection_len(self, bbox1, bbox2, proj_dir="width"):
        if proj_dir == "width":
            return abs(max(bbox1[0], bbox2[0]) - min(bbox1[2], bbox2[2]))
        elif proj_dir == "height":
            return abs(max(bbox1[1], bbox2[1]) - min(bbox1[3], bbox2[3]))

    def find_target_text_bbox(self, text_all, full_pattern, pattern):
        target_bbox = None
        kw_msg_list = []
        for text in text_all:
            text_bbox = text.bbox.list
            text_msg = text.extend_message
            if re.search(pattern, text_msg):
                kw_msg_list.append(text_bbox + [text_msg])
        for kw_msg in kw_msg_list:
            kw_msg_bbox = kw_msg[:4]
            # 向右延长bbox
            ext_len = 50 * abs(kw_msg_bbox[2]-kw_msg_bbox[0])
            kw_msg_bbox_ext = [kw_msg_bbox[0], kw_msg_bbox[1], kw_msg_bbox[2]+ext_len, kw_msg_bbox[3]]
            msg_list = []
            for text in text_all:
                text_bbox = text.bbox.list
                text_msg = text.extend_message
                if Iou_temp(text_bbox, kw_msg_bbox_ext):
                    msg_list.append(text_bbox + [text_msg])
            text_concat = self._concat_text(msg_list)
            if re.search(full_pattern, text_concat):
                print("text_concat", text_concat)
                target_bbox = kw_msg_bbox_ext
                break
        return target_bbox

    def get_related_obj(self, entity_list):
        """

        Args:
            entity_list:

        Returns:

        """
        related_obj_list = []
        for entity_obj in entity_list:
            entity_cnt = get_contour_from_bbox(entity_obj.bounding_rectangle.list)
            iou = get_contours_iou(self.contour.contour, entity_cnt)
            if iou > 0:
                related_obj_list.append(entity_obj)

        return related_obj_list

    def get_translation_params(self):
        """
        计算轮廓平移到（4000，4000）后的参数
        Returns:

        """
        cnt, cnt_flip = self.household_contours_with_flip
        x, y = get_cnt_center(cnt)
        diff_x = x - 4000
        diff_y = y - 4000
        cnt[:, 0, 0] = cnt[:, 0, 0] - diff_x
        cnt[:, 0, 1] = cnt[:, 0, 1] - diff_y

        x_flip, y_flip = get_cnt_center(cnt_flip)
        diff_x_flip = x_flip - 4000
        diff_y_flip = y_flip - 4000
        cnt_flip[:, 0, 0] = cnt_flip[:, 0, 0] - diff_x_flip
        cnt_flip[:, 0, 1] = cnt_flip[:, 0, 1] - diff_y_flip

        self.translation = [(diff_x, diff_y), (diff_x_flip, diff_y_flip)]
