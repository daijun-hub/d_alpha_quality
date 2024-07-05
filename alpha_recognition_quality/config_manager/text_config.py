from enum import Enum


class TextType(Enum):
    DOOR = "door_text"
    ROOM = "room_text"
    PARKING = "parking_text"  # 非机动车停车位文本，比如"自行车数量"
    PARKING_VEHICLE = "parking_vehicle_text"  # 机动车停车位文本，比如"车库"、"停车"
    NUMBER = "number_text"  # 纯数字文本，比如"621"
    HOUSING_HEIGHT = "housing_height_text"  # 楼栋高度文本，eg: "H=99.2M"
    HOUSING_FLOOR = "housing_floor_text"  # 总平图以外的图纸类型的楼栋层数文本，eg: "3F"
    ELEVATION_DRAWING_FLOOR = "elevation_drawing_floor_text"  # 立面图图纸类型的楼层数文本，eg: "3F"，不含40层以上的楼层文本
    ELEVATION_DRAWING_ELEVATION = "elevation_drawing_elevation_text"  # 立面图图纸类型的建筑标高文本，eg: "60.200"，不含100以上的标高文本
    BUILDING_FLOOR = "building_floor_text"  # 总平图的楼栋层数文本
    HOUSING_TYPE = "housing_type_text"  # 楼栋类型文本，eg: "变电站"
    HOUSING_UNDERGROUND = "housing_underground_text"  # 总平图地下建筑标注文本
    HOUSING_NAME = "housing_name_text"  # 比如"52#"，"D5-12号楼"
    HOUSING_ENTRANCE = "housing_entrance_text"  # 住宅出入口文本
    HOUSING_MARKING = "housing_marking_text"  # 住宅标注文本
    AIRCON = "aircon_text"  # text for air_conditioner, eg:AC, F1
    PODAO = "podao_text"  # 坡道文本
    PARKING_EXIT = "parking_exit_text"  # 车库出口文本
    GUTTER = "gutter_text"  # 排水沟标注文本
    ELEVATION = "elevation_text"
    ELEVATION_TEXTURE = "elevation_texture_text" # 立面材质图例文本
    PAISHUI = "paishui_text"  # 标示水井间的文字 如“水”“S”“水井”
    INDOOR_FIRST_FLOOR_ELEVATION = "indoor_first_floor_elevation_text"  # 首层标高相关文本
    UNDERGROUND_ELEVATION = "underground_elevation_text"  # 地下标高相关文本
    DRAWING_TAG = 'drawing_tag_text'  # 图纸的图签信息 如“图号/图别”
    SHANGKONG = 'shangkong_text'  # 卧室上空文本
    TRUCK_PAKRING = 'truck_parking_text'  # 货车停车位
    YUPENG = 'yupeng_text'  # 雨棚
    ALL = 'all_text'# 所有文字信息
    INDOOR_FIRST_FLOOR_PODAO = "indoor_first_floor_podao"  # 地上无障碍坡道, 1:5~30 or 无障碍坡道
    ASCENT = "ascent_text"  # 登高场地文本，比如"消防登高场地"
    SILENT = "silent_text"  # 隔音墙
    MANAGER_ROOM = "manager_room_text"  # 管理人员室 如"门卫室"、"消防控制室"
    DAYANG_BUILDING_FLOOR = "dayang_building_floor"  # 墙身大样图楼层文本"
    GALLERY = "gallery"  # 外廊｜内天井｜上人**屋面
    BUS_ISOLATOR = "bus_isolator_text"  # 总线隔离器 "SI"、"G"
    DISTRIBUTION_BOX = "distribution_box_text"  # 配电箱 "HE","AT","AL","AP','ALE'
    AREA_DISPLAY = "area_display_text"  # 区域显示器 "D"
    EVACUATION_SIGNS = "evacuation_signs_text"  # 灯光疏散指示标志 "E"或"S"
    EMERGENCY_LIGHTING = "emergency_lighting_text"  # 疏散照明灯具 "E"
    FLOOR_INDICATOR_LIGHT = "floor_indicator_light_text" # 楼层标志灯 有“F"或“楼层指示”的文本
    INFORMATION_SOCKET = "information_socket_text" # 信息插座 TD、TO
    TELEVISION_SOCKET = "television_socket_text" # 电视插座 TV
    TELEPHONE_SOCKET = "telephone_socket_text" # 电话插座 TP
    ELECTRICITY_METER = "electricity_meter_text" # 电表 矩形，含“EM”或者”AW’,“kwh”或“wh”或“dds”或“dts”的文本（不区分大小写）
    FIRE_PROOF_DOOR_MONITOR = "fire_proof_door_monitor_text" # 防火门监控器.      矩形中含“DC”或“DO”或“FHM”或“FM”文本
    FIRE_RESISTANT_SHUTTER_CONTROLLER = "fire_resistant_shutter_controller_text" # 防火卷帘控制器.  矩形框，内部有FJL、RS、JL、JLM、FJ、FHJL
    EQUIPOTENTIAL_JUNCTION_PLATE = "equipotential_junction_plate_text" # 等电位连接板.      矩形框，内有“LEB”、“MEB”文本
    FLOW_INDICATOR = "flow_indicator_text"  # 水流指示器 "L"
    MAILBOX = 'mailbox_text' # 信报箱   包含"信报箱"
    
# list, 包含TextType的所有成员变量         
All_TextType = [item[1] for item in TextType.__dict__['_member_map_'].items()]


class TitleTextType(Enum):
    title_keyword = {
        "ProjectManager": "PROJECTMANAGER",
        "DrawingName": "(图名|图.*名|图纸名称|图纸内容|DRAW.*TITLE|DRAWINGNAME|DWG.*TITLE|^TITLE|PROJECTDESIGNTITLE|SHEET.*TITLE|^DRAWING$)",
        "ProjectName": r"(^项目名称|^工程项目|^PRO.*NAME|^工程名称|^PROJECTTITLE|^ENGINEERING|^PROJECT|^JOBTITLE)$(?!.*NO)",
        "Major": r"^(.*专业$|.*MAJOR$|DISCIPLINE$|SPECIALITY$|.*DEPT)(?!.*BY)",
        "Date": r"^(日期|DATE|FINISHINGDATE)$",
        "Version": r"(.*版本|.*版次|VERSION|VER.*NO|VISION|.*REV|VER.|EDITION.*NO)(?!.*BY)(?!.*RECORD)",
        "DrawingType": r"(图别|DRAWINGCATEGORIES|.*CATEGORY|DRAW.*TYPE|DWG.*TYPE|.*STYLE|DWG.*SORT|DRAW.*SORT|TYPE)",
        "SubProject": r"(子项|子项名称|子项.*名称|ITEMNAME|SUB.*|SUB.*NAME|SUBITEM|ITEM|单项工程)$",
        "DrawingScale":r"(比例|SCALE)$",
        "DesignPhase": r"(阶段|STATUS|STAGE|DESIGNPHASE|PHASE)",
        "DrawingNumber": r"(图号|图.*号|序.*号|DWGNO|DRAWING.*NO|DWG.*NO|DWG.*NUMBER|DRAWING.*NUMBER|DRAWING.*N0|SHEET.*NO)",
        "DesignNumber": "(设计.*号|项目.*号|DESIGN.*NO|PRO.*NO)",
        "ConstructionUnit": "(建设单位|.*CLIENT|OWNER.*NAME|OWNER|顾客)",
        "OtherSignatory ": "(.*修改.*|.*BY.*|.*助理|.*经理|.*组审|.*CHECK|审核|审定|VERIFIED|DESIGNER|设计人|负责人|制图人|所长|SUPERINTENDENT|业主|.*CHIEF|主持人)"
    }

    ignore_title_keyword = {
        # (?!.*人)
        "IgnoreKeyword": "(.*编码|^号$|CONTRACT|MAPSHEET|专业审查人|分号|^总图$|PLAN|会签|COORDINATION|^商铺$|方案|版权|^UNIT$|未经许可|许可|^验证签字$|^工号$|^MM$|^工程号$|^NAME$|^单位$|^DESIGN$|^CO.$|^GROUP$|^N0.$|^N0$|^NO.$|^NO$|^LTD$|工程设计资质证书编号|不得以比例尺度量|.*负责.*|^图幅$|^设总$|^说明$|图纸使用说明|会签栏|ISSUE|出图|编号|^NO.$|^委托方$|^REMARK$|.*备注.*|^制图$|^DRAWE$|^档案号$|盖章|SEAL|^JOBNO$|^工程编号$|REVISEDRECORD|ARCHIVES|EDITION|归档纪录|项目负责|校对|^设计$|审批编号|施工图设计|WORKDRAWING|工程主持人|批准|个人执业章|REGISTERED|附注|方案主创|方案设计|DESCRIPTION|CO-OPERATEDWITH|合作设计单位)"
    }