from .architecture.drawing_config import DrawingType as JZType
from .plumbing.drawing_config import DrawingType as GPSType

class EntityStorageConfig:

    # 属性字段映射表
    attribute_map = {
        "chinese_name": "elementName",
        # "contour": "elementProfile",
        "bounding_rectangle": "elementPosition",

        "window_width": "elementWidth",
        "door_wall_width": "elementWidth",
        "window_height": "elementHeight",
        "door_height": "elementHeight",

        "lead_mark": "elementMark"
    }

    # 不返回的属性
    attribute_filter = {
        "entity_base_type",
        "entity_class",
        "CAD_bounding_rectangle",
        "origin_class",
        "score",
        "processed_gbes"
    }

    # 不返回的构件
    filted_entities = {
        "照明插座分支回路"
    }

    # 构件id映射表
    storage_id_dict = {
        "平面图开关": 50047,
        "熔断器": 50046,
        "A型应急照明灯": 50045,
        "应急双管灯": 50044,
        "应急单管灯": 50043,
        "双管灯": 50042,
        "单管灯": 50041,
        "普通灯": 50040,
        "变压器符号": 50039,
        "配电箱出线回路": 50038,
        "插座分支回路": 50037,
        "照明分支回路": 50036,
        "按钮": 50035,
        "防火卷帘控制器": 50034,
        "防火门监控器": 50033,
        "浪涌保护器 ": 50032,
        "变压器": 50031,
        "信息插座": 50030,
        "电话插座": 50029,
        "电视插座": 50028,
        "插座": 50027,
        "等电位连接板": 50026,
        "配电柜": 50025,
        "楼层标志灯": 50024,
        "负荷开关": 50023,
        "热继电器": 50022,
        "接触器": 50021,
        "漏电断路器": 50020,
        "断路器": 50019,
        "电表": 50018,
        "灯具": 50017,
        "接闪带": 50016,
        "引下线": 50015,
        "总线隔离器": 50014,
        "配电箱": 50013,
        "区域显示器": 50012,
        "疏散指示标志": 50011,
        "消防应急广播": 50010,
        "消防电话": 50009,
        "声光报警器": 50008,
        "感温探测器": 50007,
        "感烟探测器": 50006,
        "手动报警按钮": 50005,
        "消火栓按钮": 50004,
        "双切开关": 50003,
        "单刀开关": 50002,
        "电线": 50001,
        "其他门": 10001,
        "平开门": 10002,
        "电梯门": 10003,
        "密闭门": 10004,
        "弹簧门": 10005,
        "卷帘门": 10006,
        "折叠门": 10007,
        "推拉门": 10008,
        "其他窗": 10009,
        "普通窗": 10010,
        "转角窗": 10011,
        "凸窗": 10012,
        "百叶窗": 10013,
        "剖面窗": 10014,
        "立面窗": 10015,
        "门联窗": 10016,
        "大样楼梯剖面梯段": 10017,
        "直跑楼梯": 10018,
        "双跑楼梯": 10019,
        "剪刀楼梯": 10020,
        "其他楼梯": 10021,
        "电梯轿厢": 10022,
        "剖面栏杆": 10023,
        "立面栏杆": 10024,
        "平面栏杆": 10025,
        "普通停车位": 10026,
        "充电停车位": 10027,
        "无障碍车位": 10028,
        "货车停车位": 10029,
        "普通地漏": 10030,
        "洗衣机地漏": 10031,
        "侧排地漏": 10032,
        "立管": 30043,
        "厨房排烟管道": 10035,
        "台阶": 10036,
        "减速带": 10037,
        "洗面器": 10038,
        "洗浴器": 10039,
        "便器": 10040,
        "洗涤槽": 10041,
        "炉灶": 10042,
        "冰箱": 10043,
        "空调内机": 10044,
        "空调外机": 10045,
        "洗衣机": 10046,
        "信报箱": 10047,
        "截水沟": 10048,
        "预留孔洞": 10049,
        "柱子": 10050,
        "柱帽": 10051,
        "水泵接合器": 30001,
        "排气阀": 30002,
        "消火栓横管": 30003,
        "污水横管": 30004,
        "废水横管": 30005,
        "排水横管": 30006,
        "生活给水横管": 30007,
        "雨水横管": 30008,
        "喷淋横管": 30009,
        "冷水横管": 30010,
        "热水横管": 30011,
        "进水横管": 30012,
        "通气横管": 30013,
        "检查口": 30014,
        "通气帽": 30015,
        "灭火器": 30016,
        "系统消火栓": 30017,
        "生活水箱": 30018,
        "套管": 30019,
        "地漏": 30020,
        "系统地漏": 30021,
        "报警阀": 30022,
        "检查井": 30024,
        "喷头": 30025,
        "水流指示器": 30026,
        "水表": 30028,
        "阀门": 30029,
        "雨水斗侧排": 30030,
        "雨水斗全排": 30031,
        "截止阀": 30032,
        "减压阀": 30033,
        "冷凝水横管": 30034,
        "喷头-系统": 30035,
        "闸阀": 30036,
        "蝶阀": 30037,
        "压力表": 30038,
        "消火栓": 10034,
        "消火栓和灭火器": 30040,
        "雨水回用给水横管": 30041,
        "实心墙": 30042,
        "生活给水立管": 30044,
        "消火栓立管": 30045,
        "喷淋立管": 30046,
        "室外消火栓-总图": 30047,
        "雨水立管": 30048,
        "污水立管": 30049,
        "废水立管": 30050,
        "冷凝水立管": 30051,
        "末端试水装置-系统": 30054,
        "末端试水装置-平面": 30055,
        "清扫口": 30056,
        "集水坑": 30058,
        "雨水井": 30059,
        "溢流口": 30061,
        "其他立管": 30062,
        "系统报警阀": 30063
    }

    # 构件属性--中台枚举类型值
    storage_enum_dict = {
        "平开门": {
            "door_fire_resistance_level": ["甲级", "乙级", "丙级"],
            "door_usage": ["卧室门", "卫生间门", "厨房门", "阳台门", "户门", "单元门", "楼梯间门", "前室门", "其它门"]
        },
        "配电箱出线回路": {
            "disconnector_type": ["断路器", "漏电断路器", "0"]
        }
    }

    # 构件去重iou大于0取较大bbox构件列表
    iou_filter_zero_entities = []

    # 构件去重iou最大最小阈值
    iou_filter_threshold = {
        "default": {
            "max_threshold": 0.95,
            "min_threshold": 0.7
        },
        "地漏": {
            "max_threshold": 0.69,
            "min_threshold": 0.45
        },
        "普通地漏": {
            "max_threshold": 0.69,
            "min_threshold": 0.45
        },
        "洗面器": {
            "max_threshold": 0.3,
            "min_threshold": 0.3
        },
        "洗浴器": {
            "max_threshold": 0.3,
            "min_threshold": 0.3
        },
        "便器": {
            "max_threshold": 0.3,
            "min_threshold": 0.3
        },
        "洗涤槽": {
            "max_threshold": 0.3,
            "min_threshold": 0.3
        },
        "炉灶": {
            "max_threshold": 0.3,
            "min_threshold": 0.3
        },
        "冰箱": {
            "max_threshold": 0.3,
            "min_threshold": 0.3
        },
        "洗衣机": {
            "max_threshold": 0.3,
            "min_threshold": 0.3
        }

    }

    # 分类构件中不走iou去重的特殊构件，一般是构件数量太多会造成超时的构件,构件：数量阈值
    ignore_iou_classified_entities = {
        "喷头": 500
    }




class SpaceStorageConfig:

    # 属性字段映射表
    attribute_map = {
        "chinese_name": "spaceName",
        "area": "spaceArea",
        "bbox": "spacePosition",
        "contour": "spaceProfile"
    }

    # 属性字段过滤集合
    attribute_filter = {
        "space_base_type",
        "name_list",
        "is_small_room",
    }

    # 空间id映射表
    storage_id_dict = {
        "道路": 10001,
        "客厅": 10002,
        "卧室": 10003,
        "书房": 10004,
        "卫生间": 10005,
        "厨房": 10006,
        "阳台": 10007,
        "餐厅": 10008,
        "玄关": 10009,
        "电梯前室": 10010,
        "防烟楼梯前室": 10011,
        "合用前室": 10012,
        "其他前室": 10013,
        "楼梯间": 10014,
        "电梯井": 10015,
        "走廊": 10016,
        "连廊": 10017,
        "大堂": 10018,
        "墙体": 10019,
        "排烟井": 10020,
        "风井": 10021,
        "水井": 10022,
        "电井": 10023,
        "电缆井": 10024,
        "水表井": 10025,
        "管道井": 10026,
        "消防控制室": 10027,
        "总图地上水泵房": 10028,
        "总图地下水泵房": 10029,
        "仓库": 10030,
        "设备用房": 10031,
        "附建公共用房": 10032,
        "储藏室": 10033,
        "锅炉房": 10034,
        "车库范围": 10035,
        "单元出入口范围": 10036,
        "避难间": 10037,
        "烧水间": 10038,
        "衣帽间": 10039,
        "配电房": 10040,
        "开关房": 10041,
        "发电机房": 10042,
        "消防水泵房": 10043,
        "生活水泵房": 10044,
        "弱电机房": 10045,
        "露台": 10046,
        "无障碍坡道": 10047,
        "入口平台": 10048,
        "屋面层轮廓": 10049,
        "雨篷": 10051,
        "非弧形车库坡道": 10052,
        "门廊": 10053,
        "园区普通车道": 10054,
        "园区消防车道": 10055,
        "总图建筑轮廓": 10056,
        "地库轮廓": 10057,
        "用地红线轮廓": 10058,
        "地库坡道出入口": 10059,
        "基地车行出入口": 10060,
        "基地人行出入口": 10061,
        "消防登高场地": 10062,
        "回车场": 10064,
        "变电站": 10065,
        "调压站": 10066,
        "垃圾房": 10067,
        "报警阀间": 10068,
        "化粪池": 10069,
        "电气机房": 10070,
        "通信机房": 10071,
        "电梯机房": 10072,
        "储油间": 10073,
        "消防风机房": 10074,
        "普通风机房": 10075,
        "弧形车库坡道": 10076,
        "公共空间": 30001,
        "盥洗室": 30002,
        "淋浴间": 30003,
        "贵重商品仓库": 30004,
        "防火分区": 30006,
        "贮存食品库房": 30007,
        "套内空间": 30008,
        "套内水管井": 30009,
        "消防电梯前室": 30010,
        "配电箱子图": 50001
    }

    # 有些空间是某个专业特有的，不在其他专业返回，如套内空间和公共空间是给排水特有的，不在建筑和电气专业返回
    major_ignore_space = {
        "建筑": ["套内空间", "公共空间", "消防电梯前室"],
        "电气": ["套内空间", "公共空间", "消防电梯前室"],
        "给排水": []
    }


class MarkStorageConfig:

    # 属性字段映射表
    attribute_map = {
        "chinese_name": "markName",
        "bounding_rectangle": "markPosition",
    }

    # 属性字段过滤集合
    attribute_filter = {
        "_gbe_list",
        "entity_base_type",
        "start_end_point_list"
    }

    # 属性字段过滤集合中，仍需返回的构件集合
    attribute_filter_exception = {
        "start_end_point_list":{
            "栏杆完成面",
            "空间完成面",
            "窗台完成面",
            "墙线",
            "厨房操作台边线"
        }
    }

    # 标记id映射表
    storage_id_dict = {
        "标高符号": 10001,
        "箭头": 10002,
        "引注": 10003,
        "折断线": 10004,
        "地下车库车道线": 10005,
        "地上道路线": 10006,
        "完成面": 10007,
        "园区出入口": 10008,
        "墙线": 10009,
        "墙填充": 10010,
        "平面楼梯踏步": 10011,
        "厨房操作台边线": 10012,
        "用地红线": 10013,
        "空间完成面": 10014,
        "窗台完成面": 10015,
    }


class ProjectInfoStorageConfig:

    storage_id_dict = {
        "building_position": 10001,
        "building_height": 10002,
        "building_fire_resistance_level": 10003,
        "building_type": 10004,
        "indoor_pollution_limit_sheet": 10005,

        "extinguisher_parameter_sheet": 30001,
    }

    architecture_list = ["building_position", "building_height", "building_fire_resistance_level", "building_type", "indoor_pollution_limit_sheet"]
    plumbing_list = ["extinguisher_parameter_sheet"]

    architecture_drawing_type_dict = {
        JZType.BUILDING_DESIGN.value: -1,
        JZType.SITE_PLAN_BUILDING.value: 1,
        JZType.FIRST_FLOOR_SITE_PLAN.value: 1
    }

    plumbing_drawing_type_set = {
        GPSType.GEIPAISHUI_DESIGN.value
    }