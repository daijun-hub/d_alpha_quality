# -*- coding: utf-8 -*-

from enum import Enum

# from rule_engine.single_border_rule import *
from .drawing_config import DrawingType
from .layer_config import LayerConfig


class RuleConfig(Enum):
    # 万科审核规则列表
    VANKE_RULES = {
        DrawingType.XIAOFANG: [501008, 501009, 501035, 501005, 501006, 501007, 503001, 501033, 515008, 501052, 501057,
                               501055, 501056, 501059, 501053, "1502008", "1500003"],
        DrawingType.XIAOFANG_FIRST_FLOOR: [501002, 501001, 501003, 501004, 501008, 501009, 501034, 501035, 501005,
                                           501006, 501007, 503001, 501033, 515008, 501052, 501057, 501055, 501056, 501059,
                                           "1502008", "1500003"],
        DrawingType.XIAOFANG_UNDERGROUND: [501002, 501001, 501003, 501004, 501009, 501008, 503001, 501006, 501033,
                                           515008, 501052, 501057, 501055, 501056, "1502008", "1500003"],
        DrawingType.PEIDIAN_PEIDIANXIANG_SYSTEM: [512001, 507001, 507002, 512002, 511001, 515012, 515016, 515017,
                                                  514004, 514005, 514007, 514019, 501058, 501060, 515025, 515019,
                                                  513005, 515027, 515028, 515029, 515030, 501061, 514010, 515002,
                                                  515006, 515009, 515014, 515033, 515026, 515031, 515013, 515032,
                                                  513007, 516001, 513008, 515015, 514009, 501062, "1502001", "1502002",
                                                  "1502003", "1502010", "1502013", "1502014", "1502018", "1502012",
                                                  "1502021", "1502029", "1502030",
                                                  "1500001", "1502020"],
        DrawingType.PEIDIAN_MAIN_ROUTE_SYSTEM: [],
        DrawingType.DIANQI: [501054, 512001, 514006, 514017, 515001, 514012, 515003, 515021, 515007, 501053, "1502005", "1502017", "1504001"],
        # DrawingType.DIANQI_FIRST_FLOOR: [],
        DrawingType.ZHAOMING: [507003, 505010, 514011, 514016, 514017, 513002, 513003, 513004, 507004, 515018, 515024, 514018, 515007, 515001, 515023, "1500004", "1502016", "1504001"],
        DrawingType.ZHAOMING_FIRST_FLOOR: [505010, 507003, 514011, 513002, 513003, 513004, 507004, 515018, 515024, 514018, 515007, 515001, 515023, "1500004", "1502016", "1504001"],
        DrawingType.ZHAOMING_UNDERGROUND: [505010, 507003, 514011, 513002, 513003, 513004, 507004, 515018, 515024, 515007, 515023, "1502004", "1500004", "1502016"],
        DrawingType.HUXING_DAYANG: [514013, 514017, 514018,514014, 514015],
        DrawingType.FANGLEI: [506005],
        DrawingType.DIANJING_DAYANG: [515001],
        DrawingType.DIANQI_DESIGN: [506002, 506003, "1500002", "1502009", "1502019"],
        DrawingType.QIANGDIAN_DESIGN: [],
        DrawingType.XIAOFANG_DESIGN: ["1502009"],
        DrawingType.RUODIAN_DESIGN: [],
        DrawingType.HUOZAI_AUTO_SYSTEM: [501040, "1502009"],  # 501001, 501002, 501003, 501004 暂时先不审该图纸类型
        DrawingType.STRONG_ELECTRICITY_SITE_PLAN: [],
        DrawingType.WEAK_ELECTRICITY_SITE_PLAN: [],
        DrawingType.PEIDIAN_ROOM_DAYANG: [515004, 515005, 515010],
        DrawingType.GENERATOR_ROOM_DAYANG: [],
        DrawingType.LOW_VOLTAGE_PEIDIAN_SYSTEM: [515012, 515015, 502001, "1502003"],
        DrawingType.HIGH_VOLTAGE_SYSTEM: [],
        DrawingType.BROADCAST: [],
        DrawingType.BROADCAST_SYSTEM: [],
        DrawingType.ELECTRICITY_MONITOR_SYSTEM: [],
        DrawingType.ROOF_FANGLEI: [506001, 506002, 506003, 506004, 506006, 506007, "1500002"],
        DrawingType.NON_ROOF_FANGLEI: [506004, 506007],
        DrawingType.GROUND_CONNECTION: [],
        DrawingType.FIRE_DOOR_MONITOR_SYSTEM: [],
        DrawingType.ELECTRIC_FIRE_MONITOR_SYSTEM: [],
        DrawingType.XIAOFANG_POWER_MONITOR_SYSTEM: [],
        DrawingType.EMERGENCY_ILLUMINATION_SYSTEM: [513002],
        DrawingType.XIAOFANG_CONTROL_ROOM_DAYANG: [],
        DrawingType.EMERGENCY_ILLUMINATION_FIRST_FLOOR: [],
        DrawingType.EMERGENCY_ILLUMINATION: [],
        DrawingType.WEAK_ELECTRICITY: ["1504001"],
        DrawingType.STRONG_ELECTRICITY: ["1504001"],
    }

    # 规则详情
    # REF: https://www.kdocs.cn/p/51356796370?from=docs&source=docsWeb
    CONFIGURATION = {
        "1502001": {
            'name': '电缆大小选择应合理，不能过大选取',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"],
            'operation': ['combination', 'classification', 'text_information', 'segmentation']
        },
        "1502002": {
            'name': '双电源切换开关的额定电流严格按不小于计算电流的1.25倍，并不小于前级断路器整定电流选择，不允许超配。',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["系统图双切开关"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"],
            'operation': ['combination', 'classification', 'text_information', 'segmentation']
        },
        "1502003": {
            'name': '潜水泵漏电保护采用4P型漏电保护电器',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["浪涌保护器"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"] + \
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["系统图双切开关"] + ["wire"],
            'operation': ['combination', 'classification', 'text_information', 'segmentation']
        },
        "1502004": {
            'name': '非机动车坡道及出地下室楼梯间应设照明',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["照明分支回路"] + LayerConfig.BASIC_LAYERS.value["underground_segment"] + \
                      ["elevator_box", "elevator_stair", "podao_edge"] + \
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["插座分支回路"],
            'operation': ['combination', 'classification', 'text_information', "segmentation"]
        },
        "1502005": {
            'name': '对称户型的各自户内的配电箱、弱电箱不可背靠背安装',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱"] + \
                      ['door'],
            'operation': ['combination', 'classification', 'segmentation']
        },
        "1502008": {
            'name': '手动火灾报警按钮设置位置应与声光报警器上下中心对齐安装，位置宜设置在靠近疏散出口的门边，避免设置在整墙的中间位置',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value[
                "火灾自动报警按钮"] + ['door'],
            'operation': ['combination', 'classification', 'segmentation']
        },
        "1502010": {
            'name': '电缆型号选型应合理（消防/无联动功能）采用阻zr',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["浪涌保护器"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value[
                "配电箱子图"] + \
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["系统图双切开关"] + ["wire"],
            'operation': ['combination', 'classification', 'text_information', 'segmentation']
        },
        "1502013": {
            'name': '住宅户内电线采用BV',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value[
                "配电箱子图"],
            'operation': ['combination', 'classification', 'text_information', 'segmentation']
        },
        "1502014": {
            'name': '强电箱需预留插座电源至弱电箱',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value[
                "配电箱子图"],
            'operation': ['combination', 'classification', 'segmentation']
        },
        "1502016": {
            'name': '地上应急照明独立于普通照明',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["普通灯"]
                        + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["应急单管灯"]
                        + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["单管灯"]
                        + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["三管灯"]
                        + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["应急双管灯"]
                        + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["双管灯"]
                        + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["A型应急照明灯"],
            'operation': ['combination', 'classification', 'segmentation', 'text_information']
        },
        "1502017": {
            'name': '对称户型的各自户内的配电箱、弱电箱不可背靠背安装',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value[
                "配电箱"] + \
                      ['door'],
            'operation': ['combination', 'classification', 'segmentation']
        },
        "1500003": {
            'name': '符合下列条件之一的场所，宜选择点型感温火灾探测器；且应根据使用场所的典型应用温度和最高应用温度选择适当类别的感温火灾探测器',
            'entity': LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["感温探测器"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        "1502012": {
            'name': '住宅公共配电系统应预留入户大堂、首层门厅及标准层装修电源备用回路',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value[
                "配电箱子图"],
            'operation': ['combination', 'classification', 'text_information', 'segmentation']
        },
        "1502018": {
            'name': '风机、水泵等电机控制不应选用类似KB0的综合保护器（CPS）、组合式刀熔开关。',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"],
            'operation': ['combination', 'classification', 'text_information', 'segmentation']
        },

        "1502020": {
            'name': '负荷大小、开关大小及电缆大小应匹配',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"],
            'operation': ['combination', 'classification', 'text_information', 'segmentation']
        },

        "1500002": {
            'name': '在可能发生对地闪击的地区，预计雷击次数大于等于0．05次／a小于等于0．25次／a的住宅。应划为第三类防雷建筑物',
            'entity': [],
            'operation': ['text_information']
        },
        "1500004": {
            'name': '机房内应设置检修插座，该插座宜由机房配电箱单独回路配电。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["插座"],
            'operation': ['combination', 'classification', 'segmentation']
        },
        "1504001": {
            'name': '强、弱电箱位置、高度不合适与家私冲突或存在安全隐患',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      ['weak_electric_box', 'strong_electric_box', 'door', 'window'],
            'operation': ['combination', 'classification', 'segmentation']
        },
        501001: {
            'name': '消防控制室、消防值班室、企业消防站里面是否有电话总机',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["电话"] + ['wall', 'segment', 'door', 'window'],
            'operation': ['combination', 'segmentation', 'classification']
        },
        501002: {
            'name': '集中报警系统和控制中心报警系统应设置消防应急广播。',
            'entity': LayerConfig.BASIC_LAYERS.value['basic'] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["消防应急广播"] +
                      ['door', 'window', 'segment'],
            'operation': ['combination', 'segmentation', 'classification']
        },
        501003: {
            'name': '消防控制室、消防值班室或企业消防站等处，应设置可直接报警的外线电话',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["电话"] + ['segment', 'door', 'window'],
            'operation': ['combination', 'segmentation', 'classification']
        },
        501004: {
            'name': '消防控制室应设有用于火灾报警的外线电话。',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["电话"] + ['wall', 'segment', 'door', 'window'],
            'operation': ['combination', 'segmentation', 'classification']
        },
        501005: {
            'name': '消防控制室不应设置在电磁场干扰较强及其他影响消防控制室设备工作的设备用房附近',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] + ['door', 'window'],
            'operation': ['combination', 'segmentation']
        },
        501006: {
            'name': '在宽度小于3m 的内走道顶棚上设置点型探测器时，宜居中布置。感温火灾探测器的安装间距不应超过10m；感烟火灾探测器的安装间距不应超过15m；探测器至端墙的距离，不应大于探测器安装间距的1/2',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["感烟探测器"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value[
                          "感温探测器"] + ['wall', 'window', 'door'],
            'operation': ['combination', 'segmentation', 'classification']
        },
        501007: {
            'name': '点型探测器至墙壁、梁边的水平距离，不应小于0.5m',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["感烟探测器"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value[
                "感温探测器"] + ['wall', 'beam', 'door'] + LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        501008: {
            'name': '点型探测器至空调送风口边的水平距离不应小于1.5m',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + \
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["感烟探测器"] + \
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["感温探测器"] + \
                      ["air_conditioner"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        501009: {
            'name': '火灾光警报器应设置在每个楼层的楼梯口、消防电梯前室。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["光警报器"] +
                      ["door", "window", "elevator_box", "elevator_stair", "elevator_door"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        501033: {
            'name': '点型火灾探测器的设置应符合下列规定: 1 除特殊房间外，探测区域的每个房间应至少设置一只火灾探测器。',
            'entity': LayerConfig.BASIC_LAYERS.value["basic"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["感烟探测器"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["感温探测器"] + ["door", "window"],
            'operation': ["combination", "segmentation", "classification"]
        },
        501034: {
            'name': '区域显示器应设置在出入口等明显便于操作的部位',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["区域显示器"],
            'operation': ['combination']
        },
        501035: {
            'name': '手动火灾报警按钮应设置在明显和便于操作的部位。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["火灾自动报警按钮"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        # 501036: {
        #     'name': '',
        #     'entity': [],
        #     'operation': []
        # },
        501040: {
            'name': '系统总线上应设置总线短路隔离器，每只总线短路隔离器保护的火灾探测器、手动火灾报警按钮和模块等消防设备的总数不应超过32点',
            'entity': LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["总线隔离器"] +
                      ["wire"],
            'operation': ['combination', 'classification']
        },
        501055: {
            'name': '符合下列条件之一的场所，宜选择点型感温火灾探测器；且应根据使用场所的典型应用温度和最高应用温度选择适当类别的感温火灾探测器',
            'entity': LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["感温探测器"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        501056: {
            'name': '点型火灾探测器的设置应符合下列规定',
            'entity': LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["感温探测器"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["感烟探测器"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        501058: {
            'name': '排烟风机的入口处280℃排烟防火阀在关闭后应直接联锁关闭排烟风机',
            'entity': LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"] +
            LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        501059: {
            'name': '消防应急广播扬声器的设置，应符合下列规定',
            'entity': LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["消防应急广播"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        501060: {
            'name': '消防风机应设置专用线路连接至设置在消防控制室内的消防联动控制器的手动控制盘',
            'entity': LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        501052: {
            'name': '疏散通道上各防火门的开启、关闭及故障状态信号应反馈至防火门监控器。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["防火门监控器"] +
                      ["door"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        501054: {
            'name': '手动控制方式，应由防火卷帘两侧设置的手动控制按钮控制防火卷帘的升降。',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["按钮"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["防火卷帘控制器"],
            'operation': ['combination', 'classification']
        },
        501057: {
            'name': '消防专用电话分机，应固定安装在明显且便于使用的部位，并应有区别于普通电话的标识。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["电话"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        503001: {
            'name': '配电室长度超过7m时，应设2个出口，并宜布置在配电室两端。当配电室双层布置时，楼上配电室的出口应至少设一个通向该层走廊或室外的安全出口。配电室的门均应向外开启，但通向高压配电室的门应为双向开启门',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ['door', 'window'],
            'operation': ['combination', 'segmentation', 'classification']
        },
        # 505001: {
        #     'name': '',
        #     'entity': [],
        #     'operation': []
        # },
        505010: {
            'name': '疏散照明灯具应设置在出口',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + \
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["疏散照明灯具"] + \
                      ["door", "window"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        506001: {
            'name': '专设引下线不应少于2根，并应沿建筑物四周和内庭院四周均匀对称布置，其间距沿周长计算不应大于18m。当建筑物的跨度较大，\
                    无法在跨距中间设引下线时，应在跨距两端设引下线并减小其他引下线的间距，专设引下线的平均间距不应大于18m。',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["接闪带"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["专设引下线"],
            'operation': ['combination', 'classification', 'segmentation', 'text_information'],
        },
        506002: {
            'name': '在可能发生对地闪击的地区，预计雷击次数大于0．25次／a的住宅。应划为第二类防雷建筑物',
            'entity': [],
            'operation': ['text_information']
        },
        506003: {
            'name': '在可能发生对地闪击的地区，预计雷击次数大于等于0．05次／a小于等于0．25次／a的住宅。应划为第三类防雷建筑物',
            'entity': [],
            'operation': ['text_information']
        },
        506004: {
            'name': '第二类防雷建筑物外部防雷的措施，宜采用装设在建筑物上的接闪网、接闪带或接闪杆，也可采用由接闪网、接闪带或接闪杆混合组成的接闪器。接闪网、接闪带应按本规范附录B的规定沿屋角、屋脊、屋檐和檐角等易受雷击的部位敷设，并应在整个屋面组成不大于10m×10m或12m×8m的网格；当建筑物高度超过45m时，首先应沿屋顶周边敷设接闪带，接闪带应设在外墙外表面或屋檐边垂直面上，也可设在外墙外表面或屋檐边垂直面外。接闪器之间应互相连接。',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["接闪带"]+["yinxiaxian"],
            'operation': ['combination', 'classification', 'segmentation', 'text_information']
        },
        506005: {
            'name': '第三类防雷建筑物外部防雷的措施宜采用装设在建筑物上的接闪网、接闪带或接闪杆，也可采用由接闪网、接闪带和接闪杆混合组成的接闪器。'
                    '接闪网、接闪带应按本规范附录B的规定沿屋角、屋脊、屋檐和檐角等易受雷击的部位敷设，并应在整个屋面组成不大于20m×20m或24m×16m的网格；'
                    '当建筑物高度超过60m时，首先应沿屋顶周边敷设接闪带，接闪带应设在外墙外表面或屋檐边垂直面上，也可设在外墙外表面或屋檐边垂直面外。接闪器之间应互相连接。',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["接闪带"],
            'operation': ['combination', 'classification', 'segmentation', 'text_information']
        },
        506006: {
            'name': '三类防雷建筑专设引下线不应少于2根，其间距沿周长计算不应大于25m。',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["接闪带"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["专设引下线"],
            'operation': ['combination', 'classification', 'segmentation', 'text_information']
        },
        506007: {
            'name': '专门敷设的接闪器，其布置应符合表5.2.12的规定。',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["接闪带"],
            'operation': ['text_information']
        },
        507001: {
            'name': '电源插座不宜和普通照明灯接在同一分支回路。',
            'entity': LayerConfig.BASIC_LAYERS.value["basic"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"] +
            LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"],
            'operation': ['combination', 'classification']
        },
        507002: {
            'name': '照明分支线路应采用铜芯绝缘电线，分支线截面不应小于1.5mm²',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["系统图单刀开关"] + ["wire"],
            'operation': ['combination', 'classification']
        },
        507003: {
            'name': '除设置单个灯具的房间外，每个房间照明控制开关不宜少于2个',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["平面图开关"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["单管灯"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["双管灯"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["应急单管灯"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["应急双管灯"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["普通灯"] +
                      ["door", "window", "wire"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        507004: {
            'name': '公共和工业建筑非爆炸危险场所通用房间或场所照明功率密度限值应符合表6.3.13的规定',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["单管灯"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["双管灯"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["应急单管灯"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["应急双管灯"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        511001: {
            'name': '每套住宅应设置电源总断路器，总断路器应采用可同时断开相线和中性线的开关电器',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["系统图双切开关"] + ['wire'],
            'operation': ['combination', 'classification']
        },
        512001: {
            'name': '每套住宅应设置配电箱；其电源总开关装置应采用可同时断开相线和中性线的开关电器。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["系统图单刀开关"] + ["door", "window", "wire", "elevator_stair"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        512002: {
            'name': '电气管线应采用穿管暗敷设方式配线，导线应采用铜芯绝缘线，每套住宅进户线截面不应小于10mm²，分支回路截面不应小于2.5mm²',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["系统图单刀开关"] + ["wire"],
            'operation': ['combination', 'classification']
        },
        514007: {
            'name': '住宅建筑单相用电设备由三相电源供配电时，应考虑三相负荷平衡。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        514016: {
            'name': '电梯机房内应至少设置一组单相两孔、三孔电源插座，并宜设置检修电源。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["插座"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        514019: {
            'name': '电梯井道照明宜由电梯机房照明配电箱供电。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"],
            'operation': ['combination', 'segmentation', 'classification']
        },
        513002: {
            'name': '出口标志灯的设置应符合规定。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["灯光疏散指示标志"] +
                      ["door"],
            'operation': ['combination', 'classification','segmentation']
        },
        513003: {
            'name': '楼梯间每层应设置指示该楼层的标志灯。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["楼层标志灯"] +
                      ["door", "window"],
            'operation': ['combination', 'classification', 'segmentation']
        },
        513004: {
            'name': '高层住宅建筑的楼梯间、电梯间及其前室和长度超过20m的内走道，应设置应急照明；中高层住宅建筑的楼梯间、电梯间及其前室和长度超过20m的内走道，宜设置应急照明。应急照明应由消防专用回路供电。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["A型应急照明灯"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["应急单管灯"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["应急双管灯"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["应急三管灯"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["灯光疏散指示标志"],
            'operation': ['combination', 'classification','segmentation']
        },
        513007: {
            'name': '设置在电井内的集中电源不应超过1KW',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"] + ["door", "window"],
            'operation': ['combination', 'classification', 'segmentation']
        },
        513008: {
            'name': '集中电源的输出回路不应超过8路',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"] + ["door", "window"],
            'operation': ['combination', 'classification', 'segmentation']
        },
        514004: {
            'name': '每套住户负荷小于12kW时，应采用单相电源进户;每套住户负荷小于12kW时，每户应设置单相电能表',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"]+
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"],
            'operation': ['combination', 'classification', 'segmentation']
        },
        514005: {
            'name': '每套住户负荷大于等于12kW时，宜采用三相电源进户，每套住户负荷小于12kW时，每户应设置单相电能表。',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"]+
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"],
            'operation': ['combination', 'classification', 'segmentation']
        },
        514006: {
            'name': '高层住宅建筑的楼梯间、电梯间及其前室和长度超过20m的内走道，应设置应急照明；中高层住宅建筑的楼梯间、电梯间及其前室和长度超过20m的内走道，宜设置应急照明。应急照明应由消防专用回路供电。',
            'entity': [],
            'operation': ['combination', 'classification', 'segmentation']
        },
        514010: {
            'name': '柜式空调的电源插座回路应装设剩余电流动作保护器，分体式空调的电源插座回路宜装设剩余电流动作保护器',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"],
            'operation': ['combination', 'classification', 'segmentation']
        },
        514011: {
            'name': '高层住宅建筑的楼梯间、电梯间及其前室和长度超过20m的内走道，应设置应急照明；中高层住宅建筑的楼梯间、电梯间及其前室和长度超过20m的内走道，宜设置应急照明。应急照明应由消防专用回路供电。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["A型应急照明灯"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["应急单管灯"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["应急双管灯"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["应急三管灯"],
            'operation': ['combination', 'classification','segmentation']
        },
        514018: {
            'name': '与卫生间无关的线缆导管不得进入和穿过卫生间。卫生间的线缆导管不应敷设在0、1区内，并不宜敷设在2区内',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["电线"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["插座"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["普通灯"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["平面图开关"],
            'operation': ['combination', 'classification','segmentation']
        },
        515021: {
            'name': '柴油发电机房设计应符合下列规定',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      ['door'],
            'operation': ['combination', 'classification','segmentation']
        },
        515001: {
            'name': '竖井内应设置接地端子或接地干线。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["等电位连接板"],
            'operation': ['combination', 'classification','segmentation']
        },
        515002: {
            'name': '应急电源与正常电源之间，应采取防止并列运行的措施。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"],
            'operation': ['combination', 'classification', 'segmentation']
        },
        515003: {
            'name': '变电所可设置在建筑物的地下层，但不宜设置在最底层。变电所设置在建筑物地下层时，应根据环境要求降低湿度及增设机械通风等。当地下只有一层时，尚应采取预防洪水、消防水或积水从其他渠道浸泡变电所的措施。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            'operation': ['segmentation']
        },
        515004: {
            'name': '成排布置的配电柜长度大于6m时，柜后的通道应设置两个出口。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电柜"],
            'operation': ['combination', 'classification', 'segmentation']
        },
        515005: {
            'name': '成排布置的配电柜，其柜前和柜后的通道净宽不应小于表中的规定。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电柜"] +
                      ["arrow", "window", "door", "annotation_line"],
            'operation': ['combination', 'classification', 'segmentation']
        },
        515006: {
            'name': '对于突然断电比过负荷造成损失更大的线路，不应设置过负荷保护',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            'operation': ['segmentation']
        },
        515009: {
            'name': '消防水泵、防烟风机和排烟风机不得采用变频调速器控制。，不应设置过负荷保护',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            'operation': ['segmentation', 'text_information']
        },
        515010: {
            'name': '变压器外廓（防护外壳）与变压器室墙壁和门的净距不应小于表4.5.9的规定',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["变压器"] +
                      ['door', 'window'],
            'operation': ['combination', 'classification', 'segmentation', 'text_information']
        },
        515012: {
            'name': '电容器应设置接地保护',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["浪涌保护器"],
            'operation': ['combination', 'classification','text_information']
        },
        515014: {
            'name': '各级低压配电箱（柜）宜根据未来发展预留备用回路；',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            'operation': ['segmentation', 'text_information']
        },
        515016: {
            'name': '自动转换开关应标明额定电流;当采用PC级自动转换开关电器时，应能耐受回路的预期短路电流，且ATSE的额定电流不应小于回路计算电流的125%；自动转换开关的额定电流选择偏大',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["系统图双切开关"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"],
            'operation': ['combination', 'classification','segmentation','text_information']
        },
        515017: {
            'name': '对于消防风机等无备用风机的消防设备，当装设了过负荷保护时应报警不跳闸;消防风机的配电应说明采用二类配合',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"],
            'operation': ['combination', 'classification','segmentation','text_information']
        },
        515018: {
            'name': '机房内应设置检修插座，该插座宜由机房配电箱单独回路配电。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["插座"],
            'operation': ['combination', 'classification', 'segmentation']
        },

        514022: {
            'name': '高层住宅建筑的楼梯间、电梯间及其前室和长度超过20m的内走道，应设置应急照明；中高层住宅建筑的楼梯间、电梯间及其前室和长度超过20m的内走道，宜设置应急照明。应急照明应由消防专用回路供电。',
            'entity': [],
            'operation': ['combination', 'classification', 'segmentation']
        },
        515025: {
            'name': '交流充电桩的保护应符合下列规定： 1.设置过负荷保护、短路保护，并应符合本标准第7.6节和第7.7节相关规定；2.设置剩余电流动作保护，应选用额定剩余动作电流不大于30mA的A型RCD。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["漏电断路器"],
            'operation': ['combination', 'classification', 'segmentation']
        },
        515019: {
            'name': '安装在公共区域内的公用交流充电桩应配置电能表，并应符合下列规定：1每个充电接口应独立配备计量装置；',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"],
            'operation': ['combination', 'classification','segmentation']
        },
        513005: {
            'name': '应急照明配电箱或集中电源的输入及输出回路中不应装设剩余电流动作保护器，输出回路严禁接入系统以外的开关装置、插座及其他负载。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + 
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"],
            'operation': ['combination', 'classification','segmentation']
        },
        515027: {
            'name': '电梯、自动扶梯和自动人行道的负荷分级， 应符合本标准附录A民用建筑各类建筑物的主要用电负荷分级的规定。客梯的供电要求应符合下列规定：1 一级负荷的客梯， 应由双重电源的两个低压回路在末端配电箱处切换供电；2 二级负荷的客梯， 宜由低压双回线路在末端配电箱处切换供电， 至少其中一回路应为专用回路；3 自动扶梯和自动人行道应为二级及以上负荷；4 无人乘坐的杂物梯、食梯、运货平台可为三级负荷；5 三级负荷的客梯， 应由建筑物低压配电柜中一路专用回路供电。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["系统图双切开关"],
            'operation': ['combination', 'classification', 'segmentation']
        },
        515028: {
            'name': '电梯、自动扶梯和自动人行道的供电容量， 应按其全部用电负荷确定。向多台电梯供电时， 应计入同时系数。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"],
            'operation': ['combination', 'classification', 'segmentation']
        },
        515029: {
            'name': '电梯、自动扶梯和自动人行道的负荷分级， 应符合本标准附录A民用建筑各类建筑物的主要用电负荷分级的规定。客梯的供电要求应符合下列规定：1 一级负荷的客梯， 应由双重电源的两个低压回路在末端配电箱处切换供电；2 二级负荷的客梯， 宜由低压双回线路在末端配电箱处切换供电， 至少其中一回路应为专用回路；3 自动扶梯和自动人行道应为二级及以上负荷；4 无人乘坐的杂物梯、食梯、运货平台可为三级负荷；5 三级负荷的客梯， 应由建筑物低压配电柜中一路专用回路供电。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"],
            'operation': ['combination', 'classification', 'segmentation']
        },
        515030: {
            'name': '为多台防火卷帘、疏散照明配电箱等消防负荷采用树干式供电时， 宜选择预分支耐火电缆和分支矿物绝缘电缆。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"],
            'operation': ['combination', 'classification', 'segmentation']
        },
        501061: {
            'name': '手动控制方式，应将喷淋消防泵控制箱(柜)的启动、停止按钮用专用线路直接连接至设置在消防控制室内的消防联动控制器的手动控制盘，直接手动控制喷淋消防泵的启动、停止。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"],
            'operation': ['combination', 'classification','segmentation']
        },
        514012: {
            'name': '装有淋雨或浴盆的卫生间应做局部等电位联结。',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                       LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["疏散照明灯具"] + ["door", "window"],
            'operation': ['combination', 'classification', 'segmentation', ]
        },
        514013: {
            'name': '每套住宅的电视插座装设数量不应少于1个。起居室、主卧室应装设电视插座，次卧室宜装设电视插座。',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                       LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["电视插座"] + ["door", "window"],
            'operation': ['combination', 'classification', 'segmentation', ]
        },
        514017: {
            'name': '除厨房、卫生间外，其他功能房应设置至少一个电源插座回路，每一回路插座数量不宜超过10个(组)。',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value['插座分支回路'] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value['插座'],
            'operation': ['combination', 'classification', 'segmentation', ]
        },
        515008: {
            'name': '消火栓旁应设置消火栓按钮',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                       LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["消火栓"] + LayerConfig.DEVICE_ENTITY_LAYER_MAP.value
                      ["消火栓按钮"] + ["door", "window"],
            'operation': ['combination', 'classification', 'segmentation',]
        },
        515032: {
            'name': '末端消防配电箱是否设置了消防电源监控',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["系统图双切开关"],
            'operation': ['combination', 'classification','segmentation']
        },
        515033: {
            'name': '各机房宜采用不间断电源供电，其蓄电池组连续供电时间应符合表23. 5. 1的规定。',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"],
            'operation': ['segmentation', 'text_information']
        },
        514009: {
            'name': '家居配电箱的供电回路应按下列规定配置：1 每套住宅应设置不少于一个照明回路；2 装有空调的住宅应设置不少于一个空调插座回路；3 厨房应设置不少于一个电源插座回路；4 装有电热水器等设备的卫生间，应设置不少于一个电源插座回路；5 除厨房、卫生间外，其他功能房应设置至少一个电源插座回路，每一回路插座数量不宜超过10个(组)',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"],
            'operation': ['combination', 'classification', 'segmentation', 'text_information']
        },
        515023: {
            'name': '照明系统中的每 一单相分支回路电流不宜超过16A, 所 接光源数或LED灯具数不宜超过25个；大型建筑组合灯具每一 单相回路电流不宜超过25A, 光源数最多不宜超过60个；当采用 小功率单颗LED灯时，仅需满足回路电流的规定',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["照明分支回路"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["插座分支回路"],
            'operation': ['combination', 'classification', 'text_information']
        },
        501062: {
            'name': '手动控制方式，应将消火栓泵控制箱(柜)的启动、停止按钮用专用线路直接连接至设置在消防控制室内的消防联动控制器的手动控制盘，并应直接手动控制消火栓泵的启动、停止',
            'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"],
            'operation': ['combination', 'classification', 'segmentation', 'text_information']
        },
        502001: {
            'name': '在低压电网中，宜选用D，yn11接线组别的三相变压器作为配电变压器',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["变压器符号"],
            'operation': ['combination', 'classification', 'text_information']
        },
        515015: {
            'name': 'TN-C-S、TN-S系统中的电源转换开关，应采用切断相导体和中性导体的四级开关',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["系统图双切开关"],
            'operation': ['combination', 'classification', 'text_information']
        },
        501053: {
            'name': '防火卷帘的升降应由防火卷帘控制器控制',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["防火卷帘控制器"] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["卷帘门"],
            'operation': ['combination', 'classification', 'text_information']
        },
        # 515020: {
        #     'name': '机房内应设置储油间， 其总储存量不应超过1m³, 并应采取相应的防火措施',
        #     'entity': LayerConfig.BASIC_LAYERS.value["indoor_segment"] + ["door", "window"],
        #     'operation': ['combination', 'classification', 'segmentation', 'text_information']
        # },
        515024: {
            'name': '电源插座不宜和普通照明灯接在同一分支回路。',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["插座分支回路"] + ["door", "window"],
            'operation': ['combination', 'classification', ]
        },
        515026: {
            'name': '弱电机房配电箱、弱电系统的配电箱应设置浪涌保护器',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                       LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["浪涌保护器"] + ["door", "window"],
            'operation': ['combination', 'classification', ]
        },
        515031: {
            'name': '消防水泵不宜设置自动巡检装置',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                       LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["浪涌保护器"] + ["door", "window"],
            'operation': ['combination', 'classification', ]
        },
        515013: {
            'name': '消防水泵不宜设置自动巡检装置',
            'entity': LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱出线回路"],
            'operation': ['combination', 'classification', ]
        },
        516001: {
            'name': '地下室车库是否有设置CO浓度控制',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["配电箱子图"] + ["door", "window"],
            'operation': ['combination', 'segmentation', 'classification', ]
        },
        514014: {
            'name': '每套住宅的电话插座装设数量不应少于2个。起居室、主卧室、书房应装设电话插座，次卧室、卫生间宜装设电话插座。',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["电话插座"] + ["door", "window"],
            'operation': ['combination', 'classification', 'segmentation', ]
        },
        514015: {
            'name': '每套住宅的信息插座装设数量不应少于1个。书房、起居室、主卧室均可装设信息插座',
            'entity': LayerConfig.BASIC_LAYERS.value['indoor_segment'] +
                      LayerConfig.DEVICE_ENTITY_LAYER_MAP.value["信息插座"] + ["door", "window"],
            'operation': ['combination', 'classification', 'segmentation', ]
        },

    }

