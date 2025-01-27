def entity_en2cn(entity):
    d = {
        "other": "其他",
        "border": "图框",
        "pipe": "立管",
        "vpipe": "立管",
        "life_supply_vpipe": "生活给水立管",
        "sewage_vpipe": "污水立管",
        "waste_vpipe": "废水立管",
        "rain_vpipe": "雨水立管",
        "sprinkler_vpipe": "喷淋立管",
        "hydrant_vpipe": "消火栓立管",
        "condensate_vpipe": "冷凝水立管",
        "ventilate_vpipe": "通气立管",
        "window": "普通窗",
        "elevator_door": "电梯门",
        "door": "平开门",
        "elevator": "电梯",
        "parking": "停车位",
        "normal_parking": "普通停车位",
        "fire_hydrant": "消火栓",
        "renfang_door": "人防门",
        "other_door": "普通门",
        "wall": "墙",
        "pillar": "柱子",
        "elevator_box": "电梯厢",
        "equip_door": "设备管井门",
        "fire_box": "消火栓",
        "combine_door": "普通门",
        "tuila_door": "推拉门",
        "xiaohuoshuan": "消火栓",
        "guanjingmen": "设备管井门",
        "fire_hydrants": "消火栓",
        "entry_door": "入户门",
        "kitchen_door": "厨房门",
        "washroom_door": "卫生间门",
        "segment": "-",
        "evacuating_door": "疏散门",
        "drain": "地漏",
        "balcony_door": "阳台门",
        "floor_drain": "地漏",
        "floor_drain_mix": "厨卫",
        # "air_conditioner": "空调",
        "air_conditioner_ins": "空调内机",
        "air_conditioner_out": "空调外机",
        "cd_parking": "充电车位",
        "entry": "车行出入口",
        "podao": "坡道",
        "limianchuang": "立面窗",
        "car_entry": "车行出入口",
        "people_entry": "人行出入口",
        "gutter": "水沟",
        "elevation_handrail": "栏杆",
        "pave_passage": "人行道",
        "arc_podao": "弧形坡道",
        "pillar_cap": "柱帽",
        "truck_parking": "货车位",
        "inside_air_conditioner": "空调内机",
        "bedroom_door": "卧室门",
        "stair_door": "楼梯间门",
        "dilou": "地漏",
        "washbasin": "洗手盆",
        # 地上分类补充
        "others": "其他",
        "zhexianchuang": "折线窗",
        "paiqikou": "排气口",
        "paishuikou": "排水口",
        "stair": "楼梯",
        "shower": "淋浴器",
        "washer": "洗衣机",
        "baiye": "百叶窗",
        "diamond_bath": "钻石淋浴",
        "menlianchuang": "门连窗",
        "closestool": "马桶",
        # 地下分类补充
        "juanlianmen": "卷帘门",
        "wza_cd_parking": "无障碍充电停车位",
        "wza_parking": "无障碍车位",
        "louti": "楼梯",
        "shuijing": "水井",
        "famen": "阀门",
        # 电气
        "light_alarm": "声光警报器",
        "light_alarm_fire_button": "声光警报器和手动报警按钮",
        "flat_switch": "平面图开关",
        "flat_switch_evacuation_signs": "平面图开关和疏散指示标志",
        "flat_switch_double": "平面图开关",
        "temperature": "感温探测器",
        "smoke": "感烟探测器",
        "broadcast": "消防应急广播",
        "hydrant_button": "消火栓按钮",
        "fire_button": "手动报警按钮",
        "evacuation_signs": "疏散指示标志",
        "lamps": "普通灯",
        "lamps_flat_switch": "普通灯和平面图开关",
        "phone": "消防电话",
        "switch_single": "单刀开关",
        "switch_double": "双切开关",
        "distribution_box": "配电箱",
        "bus_isolator": "总线隔离器",
        "area_display": "区域显示器",
        "emergency_lighting": "应急照明灯",
        "emergency_lighting_flat_switch": "应急照明灯和平面图开关",
        "emergency_lighting_evacuation_signs": "应急照明灯和疏散指示标志",
        "yinxiaxian": "引下线",
        "bus_isolator_smoke": "总线隔离器和感烟探测器",
        # 给排水
        "signal_valve": "信号阀",
        "casing": "套管",
        "exhaust_valve": "排气阀",
        "check_point": "检查口",
        "pump_connector": "水泵接合器",
        "water_tank": "生活水箱",
        "water_meter": "水表",
        "fire_hydrants_plumbing": "系统消火栓",
        "fire_extinguisher": "灭火器",
        "fire_extinguisher_fire_hydrants": "消火栓和灭火器",
        "system_dilou": "系统地漏",
        "alarm_valve": "报警阀",
        "system_alarm_valve": "系统报警阀",
        "vent_cap": "通气帽",
        "vent_cap_circle": "通气帽",
        "reducing_valve": "减压阀",
        "stop_valve": "截止阀",
        "butterfly_valve": "蝶阀",
        "sluice_valve": "闸阀",
        "rain_bucket_side": "雨水斗侧排",
        "rain_bucket_full": "雨水斗全排",
        "toilet": "马桶",
        "check_well": "检查井",
        "sprinkler": "喷头",
        "flow_indicator": "水流指示器",
        "elevation_symbol": "标高符号",
        "pressure_meter": "压力表",
        # 暖通
        "fang_huo_fa_150": "150°防火阀",
        "pai_yan_fang_huo_fa_280": "280°排烟防火阀",
        "fang_huo_fa_70": "70°防火阀",
        "co_tan_ce_qi": "CO探测器",
        "xia_song_feng_kou": "下送风口",
        "ce_qiang_bu_feng_kou": "侧墙补风口",
        "ce_song_jia_ya_feng_kou": "侧送加压风口",
        "ce_song_pai_yan_jian_pai_feng_kou": "侧送排烟兼排风口",
        "quan_re_jiao_huan_qi": "全热交换器",
        "nei_chen_jin_shu_feng_guan": "内衬金属风管",
        "fen_ti_kong_tiao": "分体空调",
        "fen_ji_shui_qi": "分集水器",
        "jia_ya_feng_ji": "加压风机",
        "ya_cha_chuan_gan_qi": "压差传感器",
        'bi_shi_zhou_liu_feng_ji': "壁式轴流风机",
        "duo_ye_feng_kou": "多叶风口",
        "zhan_shi_pai_feng_ji": "战时排风机",
        "zhan_shi_song_feng_ji": "战时送风机",
        "shou_dong_kai_qi_zhuang_zhi": "手动开启装置",
        "pai_yan_jian_pai_feng_ji": "排烟兼排风机",
        "pai_yan_feng_ji": "排烟风机",
        "pai_feng_ji": "排风机",
        "xin_feng_ji": "新风机",
        "zhi_hui_fa": "止回阀",
        "mao_jin_nuan_qi_jia": "毛巾暖气架",
        "shui_guan_tao_guan": "水管套管",
        "xie_ya_fa": "泄压阀",
        "xiao_sheng_qi": "消声器",
        "ran_qi_bi_hua_lu": "燃气壁挂炉",
        "dian_dong_feng_fa": "电动风阀",
        "kong_tiao_hui_feng_kou": "空调回风口",
        "you_dao_feng_ji": "诱导风机",
        "song_bu_feng_ji": "送补风机",
        "feng_ji_pan_guan": "风机盘管",
        "feng_guan_shang_xia_fan": "风管上下翻",
    }

    return d.get(entity, "其他")
