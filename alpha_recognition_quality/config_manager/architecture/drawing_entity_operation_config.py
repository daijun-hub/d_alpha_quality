from enum import Enum

from .drawing_config import DrawingType


class Entity_Operation_Config(Enum):
    entity_operation_config = {
        DrawingType.IGNORE: {'entities': [], 'operations': []},
        DrawingType.INDOOR: {
            'entities': ['wall',
                         'pillar',
                         'decorative',
                         'segment',
                         'segment_extra',
                         # 'elevation_handrail',
                         # 'dayang_handrail',
                         'plan_handrail',
                         'door',
                         'elevation_mark',
                         'arrow',
                         'axis_net',
                         'elevator_box',
                         'elevator_door',
                         'window',
                         'pipe',
                         'fire_hydrant',
                         # 'pipe_barrier',
                         'floor_drain',
                         'floor_drain_mix',
                         'air_conditioner',
                         'air_conditioner_mix',
                         # 'emergency_door',
                         # 'podao_edge',
                         # 'gutter',
                         # 'washbasin',
                         # 'diamond_bath',
                         'wall_hatch',
                         # 'closestool',
                         # 'podao',
                         'kitchen_exhaust_pipe',
                         # 'elevator_stair',
                         # 'mailbox',
                         'yu_liu_kong_dong',
                         "annotation",
                         'annotation_line',
                         # 'fen_ji_shui_qi'
                         ],
            'operations': ['combination',
                           'classification',
                           'segmentation',
                           'text_information']},
        DrawingType.UNDERGROUND: {
            'entities': ['wall',
                         'axis_net',
                         'pillar',
                         'annotation',
                         'stair_dayang_plan_stair',
                         'stair_dayang_profile_stair',
                         # 'elevation_handrail',
                         # 'plan_handrail',
                         'door',
                         'window',
                         'elevator_stair',
                         'elevator_box',
                         'parking',
                         'fire_hydrant',
                         'emergency_door',
                         'road',
                         'fire_road',
                         'car_lane',
                         'segment',
                         'segment_extra',
                         'dayang_handrail',
                         'elevator_door',
                         'wall_hatch',
                         'pipe',
                         'floor_drain',
                         'floor_drain_mix',
                         'air_conditioner_mix',
                         'gutter',
                         'water_pit'],
            'operations': ['combination',
                           'classification',
                           'segmentation']},
        DrawingType.INDOOR_FIRST_FLOOR: {
            'entities': ['wall',
                         'pillar',
                         'segment',
                         'segment_extra',
                         # 'elevation_handrail',
                         # 'dayang_handrail',
                         'plan_handrail',
                         'door',
                         # 'elevation_mark',
                         'arrow',
                         'axis_net',
                         'elevator_box',
                         'elevator_door',
                         'window',
                         # 'elevate_biaogao',
                         'annotation',
                         'annotation_line',
                         # 'pipe',
                         'fire_hydrant',
                         # 'pipe_barrier',
                         'air_conditioner',
                         # 'floor_drain',
                         'floor_drain_mix',
                         'air_conditioner_mix',
                         'wall_hatch',
                         # 'emergency_door',
                         # 'podao_edge',
                         # 'gutter',
                         # 'podao',
                         # 'indoor_access',
                         # 'washbasin',
                         # 'closestool',
                         # 'diamond_bath',
                         # 'stair_dayang_plan_stair',
                         # 'podao_extra',
                         # 'separator',
                         'kitchen_exhaust_pipe',
                         # 'mailbox',
                         # 'elevator_stair',
                         # 'lobby_platform_border',
                         'yu_liu_kong_dong',
                         # 'san_shui',
                         # 'fen_ji_shui_qi'
                         ],
            'operations': ['combination',
                           'classification',
                           'segmentation']},
        DrawingType.INDOOR_FIRST_FLOOR_NO_SPACE: {
            'entities': ['wall',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'door',
                         'axis_net',
                         'floor_drain',
                         'floor_drain_mix',
                         'elevator_box',
                         'pipe',
                         'window',
                         'air_conditioner_mix',
                         'annotation_line',
                         'elevator_stair',
                         'mailbox',
                         'elevator_door'],
            'operations': ['combination',
                           'segmentation',
                           'classification']},
        DrawingType.SITE_PLAN_ROAD: {
            'entities': ['wall',
                         'axis_net',
                         'parking',
                         'road',
                         'fire_road',
                         'border',
                         'red_line',
                         'red_line_sub',
                         'building',
                         'elevation_mark',
                         'car_lane',
                         'road_center_line',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'garage',
                         'window',
                         'door',
                         'extinguishing_ascend_field',
                         'garage_exit',
                         'garage_podao_exit',
                         'basement_contour',
                         'annotation_line'],
            'operations': ['combination',
                           'classification',
                           'segmentation',
                           'text_information']},
        DrawingType.SITE_PLAN_BUILDING: {
            'entities': ['building',
                         'red_line',
                         'red_line_sub',
                         'road_center_line',
                         'road',
                         'fire_road',
                         'underground_building',
                         'border',
                         'car_lane',
                         'wall',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'axis_net',
                         'parking',
                         'window',
                         'door',
                         'annotation_line',
                         'garage_exit',
                         'basement_contour',
                         'garage_podao_exit',
                         'extinguishing_ascend_field',
                         'axis_grid'],
            'operations': ['combination', 'classification', 'segmentation']},
        DrawingType.ELEVATION: {
            'entities': ['elevation_window',
                         'decoration',
                         'wall',
                         'axis_net',
                         'window',
                         'elevation_handrail',
                         'dayang_handrail',
                         'completion_surface',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'plan_handrail',
                         'door',
                         'elevator_box',
                         'fire_hydrant',
                         'elevation_mark',
                         'elevate_biaogao'],
            'operations': ['combination', 'classification']},
        DrawingType.SIDE_ELEVATION: {
            'entities': ['elevation_window',
                        #  'mentou',
                         'decoration',
                         'wall',
                         'axis_net',
                         'window',
                         'elevation_handrail',
                         'dayang_handrail',
                         'completion_surface'],
            'operations': ['combination', 'classification']},
        DrawingType.UNDERGROUND_DINGBAN: {
            'entities': ['pillar_cap'],
            'operations': []},
        DrawingType.UNDERGROUND_BASEMENT: {
            'entities': ['floor_drain',
                         'pipe',
                         'plan_handrail',
                         'elevator_box',
                         'floor_drain_mix',
                         'window',
                         'air_conditioner_mix',
                         'door',
                         'elevator_stair',
                         'elevator_door'],
            'operations': []},
        DrawingType.PUZHUANG: {
            'entities': ['border', 'pave'],
            'operations': []},
        DrawingType.PAISHUI: {
            'entities': ['wall',
                         'axis_net',
                         'floor_drain',
                         'floor_drain_mix',
                         'door',
                         'pipe'],
            'operations': ['combination', 'segmentation', 'classification']},
        DrawingType.WALL_DAYANG: {
            'entities': ['elevation_handrail',
                         'elevation_window',
                         'structure',
                         'wall_hatch',
                         'door',
                         'window',
                         'wall',
                         'axis_net',
                         'completion_surface',
                         'dayang_handrail',
                         'pillar',
                         'annotation',
                         'stair_dayang_plan_stair',
                         'stair_dayang_profile_stair',
                         'plan_handrail',
                         'air_conditioner',
                         'segment',
                         'segment_extra',
                         'elevation_mark'],
            'operations': ['combination', 'classification', 'segmentation']},
        DrawingType.SECOND_THIRD_FLOOR: {
            'entities': ['wall',
                         'axis_net',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'second_third_space',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'annotation_line',
                         'door',
                         'window',
                         'floor_drain',
                         'pipe',
                         'elevator_box',
                         'floor_drain_mix',
                         'air_conditioner_mix',
                         'elevator_stair',
                         'mailbox',
                         'elevator_door'],
            'operations': ['combination', 'segmentation', 'classification']},
        DrawingType.INDOOR_FIRST_FLOOR_ACCESS: {
            'entities': ['wall',
                         'axis_net',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'indoor_access',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'door',
                         'window',
                         'podao',
                         'arrow',
                         'podao_extra',
                         'separator',
                         'gutter',
                         'mailbox',
                         'elevator_door',
                         'elevation_mark'],
            'operations': ['combination', 'segmentation', 'classification']},
        DrawingType.PODAO: {
            'entities': ['wall',
                         'pillar',
                         'podao',
                         'podao_extra',
                         'separator',
                         'gutter',
                         'filling',
                         'podao_mark',
                         'podao_edge',
                         'road_center_line',
                         'car_lane',
                         'door'],
            'operations': ['combination', 'segmentation', 'classification']},
        DrawingType.STAIR_DAYANG: {
            'entities': ['wall',
                         'pillar',
                         'annotation',
                         'stair_dayang_plan_stair',
                         'stair_dayang_profile_stair',
                         'elevation_handrail',
                         'plan_handrail',
                         'elevator_door',
                         'fire_hydrant',
                         'axis_net',
                         'segment',
                         'segment_extra',
                         'dayang_handrail',
                         'door',
                         'window',
                         'pipe',
                         'annotation_line',
                         'elevator_box',
                         'elevation_window',
                         'elevator_stair'],
            'operations': ['combination', 'segmentation', 'classification']},
        DrawingType.BUILDING_DESIGN: {
            'entities': ['wall',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'building',
                         'engineering_work_table_line'],
            'operations': ['text_information']},
        DrawingType.EXTERIOR_WALL_MATERIAL_LIST: {
            'entities': ['wall',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'building',
                         'engineering_work_table_line'],
            'operations': ['text_information']},
        DrawingType.ENGINEERING_WORK: {
            'entities': ['engineering_work_table_line'],
            'operations': ['text_information']},
        DrawingType.DINGCENG: {
            'entities': ['wall',
                         'axis_net',
                         'door',
                         'pipe',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'window',
                         'elevator_stair',
                         'elevator_box',
                         "air_conditioner"
                         ],
            'operations': ['combination', 'segmentation', 'classification']},
        DrawingType.WUMIAN: {
            'entities': ['wall',
                         'axis_net',
                         'door',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'building',
                         'pipe',
                         'elevator_stair',
                         'floor_drain',
                         'elevator_box',
                         'floor_drain_mix',
                         'window',
                         'elevator_door',
                         "annotation_line",
                         'kitchen_exhaust_pipe',
                         ],
            'operations': ['combination', 'segmentation', 'classification']},
        DrawingType.SECTION: {
            'entities': ['wall',
                         'axis_net',
                         'pillar',
                         'wall_hatch',
                         'door',
                         'parking',
                         'segment',
                         'segment_extra',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'window',
                         'stair_dayang_profile_stair',
                         'elevation_window',
                         'stair_dayang_plan_stair',
                         'elevation_mark'],
            'operations': ['combination', 'segmentation', 'classification']},
        DrawingType.JIFANG: {
            'entities': ['wall',
                         'axis_net',
                         'door',
                         'pipe',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'elevator_stair',
                         'floor_drain',
                         'elevator_box',
                         'floor_drain_mix',
                         'window',
                         'elevator_door',
                         "annotation_line",
                         'kitchen_exhaust_pipe',
                         ],
            'operations': ['combination', 'segmentation', 'classification']},
        DrawingType.XIAOFANG_SITE_PLAN: {
            'entities': ['wall',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'window',
                         'door',
                         'road_center_line',
                         'road',
                         'fire_road',
                         'red_line',
                         'red_line_sub',
                         'extinguishing_ascend_field',
                         'building',
                         'garage_exit',
                         'garage_podao_exit',
                         'axis_net',
                         'annotation_line'],
            'operations': ['combination',
                           'segmentation',
                           'classification',
                           'text_information']},
        DrawingType.FIRST_FLOOR_SITE_PLAN: {
            'entities': ['wall',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'door',
                         'window',
                         'stair_dayang_plan_stair',
                         'elevator_box',
                         'elevator_stair',
                         'building',
                         'extinguishing_ascend_field',
                         'road_center_line',
                         'road',
                         'fire_road',
                         'elevator_door'],
            'operations': ['combination', 'classification', 'segmentation']},
        DrawingType.DOOR_WINDOW_DAYANG: {
            'entities': [
                         'elevation_window',
                         'elevation_window_open_line',
                         'arrow',
                         "elevation_mark",
                         "engineering_work_table_line"],
            'operations': ['combination', 'segmentation', 'classification']},
        DrawingType.JIANZHU_HUXING_DAYANG: {
            'entities': ['wall',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'window',
                         'door',
                         'washbasin',
                         'closestool',
                         'diamond_bath',
                         'floor_drain_mix',
                         'arrow',
                         'annotation_line',
                         'floor_drain',
                         'pipe',
                         'elevator_box',
                         'air_conditioner_mix',
                         'elevator_stair',
                         'elevator_door'],
            'operations': ['combination', 'segmentation', 'classification']},
        DrawingType.BINANCENG: {
            'entities': ['wall',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'door',
                         'window',
                         'elevator_box',
                         'fire_hydrant',
                         'floor_drain',
                         'pipe',
                         'floor_drain_mix',
                         'elevator_stair',
                         'elevator_door'],
            'operations': ['combination', 'classification', 'segmentation']},
        DrawingType.INDOOR_BATHROOM: {
            'entities': [],
            'operations': []},
        DrawingType.EXTERIOR_WALL_MATERIAL_LIST: {
            'entities': ['wall',
                         'pillar',
                         'segment',
                         'segment_extra',
                         'elevation_handrail',
                         'dayang_handrail',
                         'plan_handrail',
                         'building',
                         'engineering_work_table_line'],
            'operations': ['text_information']},
    }