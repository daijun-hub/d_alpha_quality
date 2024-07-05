from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils import *
from ....common.log_manager import LOG
from ....common.utils2 import load_drawing_pkl
from shapely.geometry import LineString, Polygon, MultiLineString, Point
from ....config_manager.architecture.drawing_config import DrawingType as drawing_type_architecture



# 分类构件
class PuTongChuang(ClassifiedEntity):

    chinese_name = "普通窗"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "普通窗"
        self.window_is_outside = judge_outside_window_entity(entity_object.bounding_rectangle.list, border_entity, window_kind='普通窗')  # 判断是否为外窗
        self.window_fire_resistance_level = judge_window_fire_proof_entity(entity_object.bounding_rectangle.list, border_entity, window_kind='普通窗')  # 防火等级
        self.window_number = window_numbering_entity(entity_object.bounding_rectangle.list, border_entity, window_kind='普通窗')  # 窗编号
        self.window_width = window_width_height_entity(entity_object.bounding_rectangle.list, border_entity, window_kind='普通窗')[0]
        self.window_height = window_width_height_entity(entity_object.bounding_rectangle.list, border_entity, window_kind='普通窗')[1]
        self.window_open_area = self.window_width * self.window_height if self.window_width and self.window_height else None  # 窗面积
        self.window_fan_shape_area = None
        self.entity_base_type = EntityBaseType.WINDOW

        # 1022 新增属性
        # 是否是凸窗
        self.is_bay_window = False
        # 宽度
        self.width = self.window_width
        # 高度
        self.height = self.window_height
        # 窗面积
        self.window_open_area = self.window_width * self.window_height if self.window_width and self.window_height else None  # 窗面积
        # 位置
        self.position = get_window_position_entity(self, border_entity)
        # 开启方式:平面图不易获取，跨图获取
        self.open_way = None
        # 防火等级
        self.window_fire_resistance_level = get_window_fire_resistance_level_entity(entity_object.bounding_rectangle.list, border_entity)
        # 是否内窗
        self.is_inner_window = not self.window_is_outside
        # 是否自动排烟窗
        self.is_automatic_smoke_exhaust_window = judge_automatic_smoke_exhaust_window_entity(entity_object.bounding_rectangle.list, border_entity)

        # bgy属性
        self.window_centroid = self._get_window_centroid(entity_object)          # 窗质心
        self.depth = self._get_window_depth(entity_object, border_entity.ratio)  # 窗厚度
        self.window_altitude = None        # 窗台高度
        self.window_open_ways = []         # 开启方式
        self.window_open_direction = []    # 开启方向
        self.lm_window_width = 0        # 规格尺寸之宽度
        self.lm_window_height = 0       # 规格尺寸之高度
        self.division = (0, 0)             # 分隔方式
        self.glass_material = None         # 玻璃材料
        self.glass_color = None            # 玻璃颜色
        self.frame_material = None         # 型材材料
        self.frame_color = None            # 型材颜色
        self.is_axial_symmetry = True     # 是否y轴对称，用在窗编号对比上

    def get_cross_border_attribs(self, border_entity, building_object):

        window_number = self.window_number
        if window_number:
            for special_drawing_dict in building_object.special_drawing_list:
                for drawing_type, info_dict in special_drawing_dict.items():
                    file_id = info_dict['file_id']
                    if drawing_type == drawing_type_architecture.DOOR_WINDOW_DAYANG:
                        dy_border_entity = load_drawing_pkl(file_id)
                        self._get_material(file_id, dy_border_entity)  # 通过表格获得门窗材料和宽高
                        lm_window_obj_list = dy_border_entity.entity_object_dict.get('立面窗', [])
                        for lm_window_obj in lm_window_obj_list:
                            # 立面窗户，编号有多个时，第一个表示原编号，第二个表示镜像编号
                            lm_window_nums = lm_window_obj.window_number
                            if window_number in lm_window_nums:
                                # is_flip为True，表示该窗户与门窗大样表中图例互为镜像
                                is_flip = len(lm_window_nums) == 2 and window_number == lm_window_nums[1]
                                self._get_window_altitude(file_id, dy_border_entity, lm_window_obj)   # 获取窗台高度
                                self._get_window_open_ways(file_id, dy_border_entity, lm_window_obj,
                                                           is_flip)  # 获取规格尺寸、开启方式，开启方向、分隔方式、
                                break

        # 获取窗框颜色（与窗编号无关）
        self._get_color(building_object)

    def _get_window_centroid(self, entity_object):
        cent = None
        bbox = entity_object.bounding_rectangle.list
        cnt = get_contour_from_bbox(bbox)
        if cnt is None:
            return cent
        cen = Polygon(cnt.squeeze()).centroid
        cent = tuple(map(int, [cen.x, cen.y]))

        return cent

    def _get_window_depth(self, entity_object, ratio):
        bbox = entity_object.bounding_rectangle.list
        return int(min((bbox[2] - bbox[0])/ratio[0], (bbox[3] - bbox[1])/ratio[1]))

    def _get_window_altitude(self, file_id, border_entity_info, lm_window_obj):
        # 从门窗大样图拿到窗的高度属性
        ratio = border_entity_info.ratio
        ext_range = int(2000 * ratio[0])
        bg_mark_obj_list = border_entity_info.mark_object_dict['标高符号']
        lm_window_bbox = lm_window_obj.bounding_rectangle.list
        lm_window_ext_bbox = [lm_window_bbox[0] - ext_range, lm_window_bbox[1] - ext_range,
                                lm_window_bbox[2] + ext_range, lm_window_bbox[3] + ext_range]
        lm_window_centroid = get_centroid(lm_window_ext_bbox)
        lm_mark = None
        dis_min = float('inf')
        for bg_mark_obj in bg_mark_obj_list:
            mark_bbox = bg_mark_obj.bounding_rectangle.list
            if Iou_temp(mark_bbox, lm_window_ext_bbox):
                dis = point_euclidean_distance(lm_window_centroid, get_centroid(mark_bbox))
                if dis < dis_min:
                    dis_min = dis
                    lm_mark = bg_mark_obj
        if lm_mark:
            # 因为要求只找到H时代表为0，所以属性labeled_height无法继续使用。
            point_A = get_centroid(lm_mark.bounding_rectangle.list)
            bbox_temp = extend_margin(lm_mark.bounding_rectangle.list, 1000*ratio[0])
            pattern = "-?\d+\.\d+|^H$"
            all_text_info = border_entity_info.border_text_info[TextType.ALL]
            height = border_entity_info.image_manager.img_height
            width = border_entity_info.image_manager.img_width
            n_num = 10  # 图框划分成20*20个网格
            h = np.ceil(height / n_num)  # 网格高度
            w = np.ceil(width / n_num)  # 网格宽度
            all_elevation_text = [text.bbox.list + [text.extend_message]
                                  for text in all_text_info]  # if re.search(pattern, text.extend_message)]
            elevation_text = get_mesh_grid_dict(all_elevation_text, w, h)
            nearby_elevation_text_list = get_grid_range(bbox_temp, elevation_text, w, h)
            min_distance = float("inf")
            return_elevation_info = 0
            H = 0
            for text in nearby_elevation_text_list:
                point_B = text[0:4]
                distance_A_B = point_euclidean_distance(point_A, point_B)
                if distance_A_B < min_distance:
                    return_elevation_info = text[-1]
                    min_distance = distance_A_B
            self.window_altitude = eval(re.search(pattern, return_elevation_info).group()) if re.search(pattern, return_elevation_info) else return_elevation_info
            self.window_altitude_bbox = lm_mark.bounding_rectangle.list
            self.window_altitude_file_id = border_entity_info.cad_border_id
            self.window_altitude_pickle_id = file_id
        print('Note: Window[{}]\'s altitude is [{}]'.format(self.window_number, self.window_altitude))

    def _get_window_open_ways(self, file_id, border_entity_info, lm_window_obj, is_flip):
        try:
            # 从门窗大样图拿到普通窗规格尺寸、开启方式、开启方向、分隔方式
            bbox = lm_window_obj.bounding_rectangle.list
            self.window_open_ways_bbox = bbox
            self.window_open_ways_file_id = border_entity_info.cad_border_id
            self.window_open_ways_pickle_id = file_id
            self.window_open_direction_bbox = bbox
            self.window_open_direction_file_id = border_entity_info.cad_border_id
            self.window_open_direction_pickle_id = file_id
            self.win_size_bbox = bbox
            self.win_size_file_id = border_entity_info.cad_border_id
            self.win_size_pickle_id = file_id
            self.division_bbox = bbox
            self.division_file_id = border_entity_info.cad_border_id
            self.division_pickle_id = file_id
            self.window_open_ways = []         # 开启方式
            self.window_open_direction = []    # 开启方向
            self.lm_window_width = 0
            self.lm_window_height = 0

            ratio = border_entity_info.ratio
            # 以立面窗的范围先挑选一遍附近所有的标注文本（如果能以格点拿则更好）
            ext_bbox = extend_margin(bbox, int(1500 * ratio[0]))
            all_text_info = border_entity_info.border_text_info[TextType.ALL]
            all_text_info = [text for text in all_text_info if text.extend_message.replace('.', '').isdigit() and Iou_temp(ext_bbox, text.bbox.list)]
            ext_range = int(5000 * ratio[0])
            # ----------------------------------根据尺寸线获取窗宽高、分隔方式--------------------------------------------
            ext_bbox1 = [bbox[0], bbox[1], bbox[2], bbox[3] + ext_range]  # 向下外扩
            ext_bbox2 = [bbox[0], bbox[1], bbox[2] + ext_range, bbox[3]]  # 向右外扩
            ext_bbox3 = [bbox[0], max(0, bbox[1] - ext_range), bbox[2], bbox[3]]  # 向上外扩
            ext_bbox4 = [max(0, bbox[0] - ext_range), bbox[1], bbox[2], bbox[3]]  # 向左外扩
            division_width = []
            division_height = []
            for text in all_text_info:
                text_bbox, text_message = text.bbox.list, round(float(text.extend_message))
                if text_message > 50 and ((Iou_temp(ext_bbox1, text_bbox) and ((text_bbox[1] + text_bbox[3]) / 2 > bbox[3]))
                                          or (Iou_temp(ext_bbox3, text_bbox) and ((text_bbox[1] + text_bbox[3]) / 2 < bbox[1]))):
                    division_width.append(text_bbox + [text_message])
                    if text_message > self.lm_window_width:
                        self.lm_window_width = text_message
                if text_message > 50 and ((Iou_temp(ext_bbox2, text_bbox) and ((text_bbox[0] + text_bbox[2]) / 2 > bbox[2]))
                                          or (Iou_temp(ext_bbox4, text_bbox) and ((text_bbox[0] + text_bbox[2]) / 2 < bbox[0]))):
                    division_height.append(text_bbox + [text_message])
                    if text_message > self.lm_window_height:
                        self.lm_window_height = text_message
            for i, text in enumerate(division_width):
                if text[-1] == self.lm_window_width:
                    division_width.pop(i)
                    break
            if division_width:
                division_width = [sorted(division_width, key=lambda x: x[2] - x[0])[-1]]
            else:
                print('error: must have width and yuliu width')
            for i, text in enumerate(division_height):
                if text[-1] == self.lm_window_height:
                    division_height.pop(i)
                    break
            if division_height:
                division_height = [sorted(division_height, key=lambda x: x[3] - x[1])[-1]]
            else:
                print('error: must have height and yuliu height')
            for text in all_text_info:
                text_bbox, text_message = text.bbox.list, round(float(text.extend_message))
                txt_msg = text_bbox + [text_message]
                if division_width and txt_msg not in division_width and text_bbox[1] == division_width[0][1] and text_bbox[3] == division_width[0][3]:
                    division_width.append(txt_msg)
                if division_height and txt_msg not in division_height and text_bbox[0] == division_height[0][0] and text_bbox[2] == division_height[0][2]:
                    division_height.append(txt_msg)
            division_width = list(map(lambda x: x[4], sorted(division_width, key=lambda x: x[0])))
            division_height = list(map(lambda x: x[4], sorted(division_height, key=lambda x: x[1])))
            division_symmetry = True
            for si in range(len(division_width)//2):
                if division_width[si] != division_width[-si]:
                    division_symmetry = False
                    break
            self.division = (division_width, division_height)
            # 若分割因镜像问题，导致审查出问题，放开下面注释，参考"开启方式"修改规则。其它窗类似
            # if is_flip:
            #     self.division = [(self.division[0][::-1], self.division[1]), self.division]
            # else:
            #     self.division = [self.division, (self.division[0][::-1], self.division[1])]
            # ----------------------------------将窗分梃、以获取开启方式、开启方向等属性------------------------------
            space_scale = border_entity_info.space_scale
            border_coord = border_entity_info.border_coord

            height = border_entity_info.image_manager.img_height
            width = border_entity_info.image_manager.img_width
            # 底图
            img_whole = np.zeros((height, width), dtype="uint8")
            # 获取箭头标记
            arrow_list = border_entity_info.mark_object_dict["箭头"]

            # 获取立面窗的图元信息
            origin_border_entity_info = border_entity_info.origin_border_entity_info
            class_to_check = ["Line", "Polyline", "Polyline2d"]
            layer_to_check = ['elevation_window', ]
            line_dict = get_origin_border_entity_info_rule(origin_border_entity_info, layer_to_check, class_to_check,
                                                           space_scale, border_coord, ratio)
            line_list_ori = []
            for _, value in line_dict.items():
                line_list_ori.extend(value)
            line_list = [line for line in line_list_ori if len(line) == 4]

            # 查找线型类型的开闭线图元
            open_layer_to_check = ["elevation_window_open_line"]
            open_line_list = get_origin_border_entity_info_with_style_rule(origin_border_entity_info, open_layer_to_check,
                                                                           class_to_check, space_scale, border_coord, ratio)[open_layer_to_check[0]]
            # 获取bbox里的图元
            line_need = entity_in_bbox(line_list, bbox)
            for line in line_need:
                cv2.line(img_whole, tuple(line[:2]), tuple(line[2:4]), 255, 2)
            # 推拉窗内部分隔需以开启线作梃
            if any([Iou_temp(bbox, extend_margin(arrow.bounding_rectangle.list, 1)) for arrow in arrow_list]):
                open_line_need = entity_in_bbox(list(map(lambda x: x[0], open_line_list)), bbox)
                for line in open_line_need:
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

            # 过滤掉错误的较小门窗
            seg_contours = []
            for contour in seg_contours_ori:
                _bbox = get_bbox_from_contour(contour)
                min_length = min(_bbox[2] - _bbox[0], _bbox[3] - _bbox[1])
                if min_length > 160 * ratio[0]:
                    seg_contours.append(contour)

            # 给扇按质心排序，先左后右，先上后下
            sorted_seg_contours, flip_orders = sort_contour(seg_contours, is_flip=is_flip)
            for contour in sorted_seg_contours:
                # 获取开启类型和方向
                inside_lines = []
                for line in open_line_list:
                    if len(line[0]) != 4:
                        continue
                    if line_overlap_poly(line[0], contour):
                        inside_lines.append(line)
                has_type = False
                for arrow in arrow_list:
                    arrow_bbox = extend_margin(arrow.bounding_rectangle.list, 1)  # 扩大1的原因是目前的箭头是线，不是bbox
                    arrow_cnt = get_contour_from_bbox(arrow_bbox)
                    if get_contours_iou(contour, arrow_cnt) > 0.5:
                        if arrow.start_end_point_list[0][0] < arrow.start_end_point_list[0][2]:
                            self.window_open_ways.append("左推拉")
                            self.window_open_direction.append(None)
                            has_type = True
                            break
                        else:
                            self.window_open_ways.append("右推拉")
                            self.window_open_direction.append(None)
                            has_type = True
                            break
                if has_type:
                    continue
                if len(inside_lines) >= 2:
                    line1, line2 = inside_lines[:2]
                    inside_cross_point = get_line_cross_point(line1[0], line2[0])
                    if inside_cross_point:
                        point1 = get_line_max_point(inside_cross_point, line1[0])
                        point2 = get_line_max_point(inside_cross_point, line2[0])
                        if inside_cross_point[0] < point1[0] and inside_cross_point[0] < point2[0]:
                            self.window_open_ways.append('左平开')
                        elif inside_cross_point[0] > point1[0] and inside_cross_point[0] > point2[0]:
                            self.window_open_ways.append('右平开')
                        elif inside_cross_point[1] < point1[1] and inside_cross_point[1] < point2[1]:
                            self.window_open_ways.append('上悬窗')
                        elif inside_cross_point[1] > point1[1] and inside_cross_point[1] > point2[1]:
                            self.window_open_ways.append('下悬窗')
                        else:
                            self.window_open_ways.append(None)
                    else:
                        self.window_open_ways.append(None)
                    if re.search('DASH', line1[1]):
                        self.window_open_direction.append('inside')
                    else:
                        self.window_open_direction.append('outside')
                    has_type = True
                if has_type:
                    continue
                self.window_open_ways.append(None)
                self.window_open_direction.append(None)
            open_ways_symmetry = True
            for si in range(len(self.window_open_ways)//2):
                if self.window_open_ways[si] != self.window_open_ways[-si]:
                    open_ways_symmetry = False
                    break
            open_direction_symmetry = True
            for si in range(len(self.window_open_direction)//2):
                if self.window_open_direction[si] != self.window_open_direction[-si]:
                    open_direction_symmetry = False
                    break
            self.is_axial_symmetry = division_symmetry and open_ways_symmetry and open_direction_symmetry

            self.window_open_ways = [self.window_open_ways, [self.window_open_ways[i] for i in flip_orders]]
            self.window_open_direction = [self.window_open_direction, [self.window_open_direction[i] for i in flip_orders]]
            print('Note: 普通窗Window[{}]\'s open_ways is [{}], open_direction is [{}],\t\r\ndivision is [{}] win_size:[{}x{}]'.format(
                self.window_number, self.window_open_ways, self.window_open_direction, self.division, self.lm_window_width, self.lm_window_height))
        except Exception as e:
            print(e)
            LOG.error(e)

    # 通过表格获取门窗材料
    def _get_material(self, file_id, border_entity_info):
        if not self.glass_material:
            dw_size_material = border_entity_info.special_info_dict.get('dw_size_material', {})
            if self.window_number in dw_size_material:
                material_text_bbox, material_message = dw_size_material[self.window_number].get('material', [None, ''])
                split_msg = re.split('窗|框|型材', ''.join(re.split('棕色|浅蓝色|蓝色|蓝灰色', material_message)))
                if len(split_msg) > 1:
                    self.frame_material = split_msg[0] + '框'
                    # 去除, mm ()等符号
                    self.glass_material = ''.join(re.split(',|，|m|\(|\（|\)|\）', split_msg[-1]))
                    # 去除框、窗之间可能存在的+
                    if self.glass_material and self.glass_material[0] == '+':
                        self.glass_material = self.glass_material[1:]
                    # 将A替换为空气
                    self.glass_material = self.glass_material.replace('A', '空气')
                    # 若存在数字，则去除常态文字表示；
                    if re.search('[0-9]', self.glass_material):
                        self.glass_material = self.glass_material.replace('中空', '').replace('玻璃', '').replace('普通', '').lower()
                        if re.search('low[-_]e', self.glass_material):
                            self.glass_material = ''.join(re.split('low[-_]e', self.glass_material)) + '+Low_E'
                    self.frame_material_bbox = self.glass_material_bbox = material_text_bbox
                    self.frame_material_file_id = self.glass_material_file_id = border_entity_info.cad_border_id
                    self.frame_material_pickle_id = self.glass_material_pickle_id = file_id
            print('Note: Window[{}]\'s frame_material is [{}], glass_material is [{}]'.format(
                self.window_number, self.frame_material, self.glass_material))

    # 获取窗框或玻璃的颜色
    def _get_color(self, building_object):
        for special_drawing_dict in building_object.special_drawing_list:
            info_dict = special_drawing_dict.get(drawing_type_architecture.EXTERIOR_WALL_MATERIAL_LIST)
            if info_dict:
                file_id = info_dict['file_id']
                border_entity_info = load_drawing_pkl(file_id)
                # 外墙材料表有些情况下分为商业部分和住宅部分两个图框，使用图名过滤掉商业部分
                if is_business_material_border(border_entity_info.drawing_name):
                    continue
                image_manager = border_entity_info.image_manager
                img_h, img_w = image_manager.img_height, image_manager.img_width
                border_cell_contours = self._find_table_cells(border_entity_info)
                ratio = border_entity_info.ratio
                text_all = border_entity_info.border_text_info[TextType.ALL]
                # 有些表格cell里面的文本不是同一个，影响正则匹配
                # 将同一个cell的文本合并
                cell_concat_text_list = self.concat_cell_text(border_cell_contours, text_all)
                # 外墙材料表有些情况下分为商业部分和住宅部分同时在一个图框，找到住宅部分外墙材料表的文本位置
                text_region_include = [0, 0, img_w, img_h]
                zhuzhai_pattern = "((住宅|居住|居建|洋房).*外墙材料表)|(外墙材料表.{0,5}(住宅|居住|居建|洋房))"
                comm_pattern = "((商业|配套|门楼|底商).*外墙材料表)|(外墙材料表.{0,5}(商业|配套|门楼|底商))"
                text_region_include = self.find_zhuzhai_target_region_bbox(zhuzhai_pattern, comm_pattern, text_all,
                                                                               cell_concat_text_list, text_region_include)
                if text_region_include is None:
                    continue
                text_all = [text for text in text_all if Iou_temp(text.bbox.list, text_region_include) > 0.5]
                for text in text_all:
                    glass_match = re.search('玻璃[^框]*?为(.*?)[玻|色]', text.extend_message)
                    if glass_match:
                        self.glass_color = glass_match.groups()[0]
                        self.glass_color_bbox = text.bbox.list
                        self.glass_color_file_id = border_entity_info.cad_border_id
                        self.glass_color_pickle_id = file_id
                    frame_match = re.search('框[^玻璃]*?为(.*?)色', text.extend_message)
                    if frame_match:
                        self.frame_color = frame_match.groups()[0] + '色'
                        self.frame_color_bbox = text.bbox.list
                        self.frame_color_file_id = border_entity_info.cad_border_id
                        self.frame_color_pickle_id = file_id
                        text_bbox = text.bbox.list
                        split_msg_list = []
                        split_msg = ""
                        for txt in text_all:
                            txt_bbox = txt.bbox.list
                            if (0 <= txt_bbox[0] - text_bbox[0]) and (txt_bbox[0] - text_bbox[2] <= text_bbox[2] - text_bbox[0]) and \
                                    (0 <= txt_bbox[1] - text_bbox[1]) and (txt_bbox[1] - text_bbox[3] <= text_bbox[3] - text_bbox[1]):
                                split_msg_list.append(txt.bbox.list + [txt.extend_message])
                        if split_msg_list:
                            line_height = abs(split_msg_list[0][3] - split_msg_list[0][1])
                            split_msg_center_y_list = [get_centroid(split_msg[:4])[1] for split_msg in split_msg_list]
                            vis = [False] * len(split_msg_center_y_list)
                            y_arr = np.array(split_msg_center_y_list)
                            total_text_list = []
                            for yi, y in enumerate(split_msg_center_y_list):
                                if vis[yi]: continue
                                row_text_list = []
                                minor_diff_idxs = np.where(np.abs(y_arr[yi:] - y) < line_height / 2)[0] + yi
                                for idx in minor_diff_idxs:
                                    vis[idx] = True
                                    row_text_list.append(split_msg_list[idx])
                                row_text_list.sort(key=lambda x: x[0])
                                total_text_list.append([y, row_text_list.copy()])
                            total_text_list.sort(key=lambda x: x[0])
                            for center_y, row_text_list in total_text_list:
                                split_msg += "".join([text[-1] for text in row_text_list])

                        color_type = re.search('颜色.*?参[\：\:](.*?)[\。\。]', split_msg)
                        if color_type:
                            self.frame_color = [self.frame_color, color_type.groups()[0]]
                    if self.glass_color and self.frame_color:
                        break
        print('Note: Window[{}]\'s frame_color is [{}], glass_color is [{}]'.format(
            self.window_number, self.frame_color, self.glass_color))

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
        cells = list(filter(lambda x: cv2.boundingRect(x)[2]< w//2 and cv2.boundingRect(x)[3] < h//2, cells))
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

    def find_zhuzhai_target_region_bbox(self, zhuzhai_pattern, comm_pattern, text_all, text_concat_list, text_region_include):
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
        if self.find_line_intersection_len(zhuzhai_text_bbox, comm_text_bbox, proj_dir = "width")/abs(zhuzhai_text_bbox[2]-zhuzhai_text_bbox[0]) > 0.5:
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
        if self.find_line_intersection_len(zhuzhai_text_bbox, comm_text_bbox, proj_dir = "height")/abs(zhuzhai_text_bbox[3]-zhuzhai_text_bbox[1]) > 0.5:
            # 住宅外墙材料表在左，商业外墙材料表在右
            if zhuzhai_text_bbox[0] < comm_text_bbox[2]:
                text_region_include = [0, 0, comm_text_bbox[0], text_region_include[3]]
                print("住宅外墙材料表在左，商业外墙材料表在右")
                return text_region_include
            # 商业外墙材料表在左，住宅外墙材料表在右
            else:
                text_region_include = [zhuzhai_text_bbox[0], zhuzhai_text_bbox[3], text_region_include[2], text_region_include[3]]
                print("商业外墙材料表在左，住宅外墙材料表在右")
                return text_region_include

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

    def find_line_intersection_len(self, bbox1, bbox2, proj_dir = "width"):
        if proj_dir == "width":
            return abs(max(bbox1[0], bbox2[0]) - min(bbox1[2], bbox2[2]))
        elif proj_dir == "height":
            return abs(max(bbox1[1], bbox2[1]) - min(bbox1[3], bbox2[3]))
