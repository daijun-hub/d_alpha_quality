# -*- coding: utf-8 -*-

from enum import Enum


class ClassifyType(Enum):
    # ENUM = MODEL_NAME
    HVAC = "hvac"


class ClassifyConfig:

    MODEL_CLASS = {
        ClassifyType.HVAC: [
            "fang_huo_fa_150",  # 150°防火阀
            "pai_yan_fang_huo_fa_280",  # 280°排烟防火阀
            "fang_huo_fa_70",  # 70°防火阀
            "co_tan_ce_qi",  # CO探测器
            "xia_song_feng_kou",  # 下送风口
            "ce_qiang_bu_feng_kou",  # 侧墙补风口
            "ce_song_jia_ya_feng_kou", # 侧送加压风口
            "ce_song_pai_yan_jian_pai_feng_kou", # 侧送排烟兼排风口
            "quan_re_jiao_huan_qi",  # 全热交换器
            "nei_chen_jin_shu_feng_guan",  # 内衬金属风管
            "fen_ti_kong_tiao",  # 分体空调
            "fen_ji_shui_qi",  # 分集水器
            "jia_ya_feng_ji",  # 加压风机
            "ya_cha_chuan_gan_qi",  # 压差传感器
            'bi_shi_zhou_liu_feng_ji', # 壁式轴流风机
            "duo_ye_feng_kou",  # 多叶风口
            "zhan_shi_pai_feng_ji",  # 战时排风机
            "zhan_shi_song_feng_ji",  # 战时送风机
            "shou_dong_kai_qi_zhuang_zhi",  # 手动开启装置
            "pai_yan_jian_pai_feng_ji",  # 排烟兼排风机
            "pai_yan_feng_ji",  # 排烟风机
            "pai_feng_ji",  # 排风机
            "xin_feng_ji",  # 新风机
            "zhi_hui_fa",  # 止回阀
            "mao_jin_nuan_qi_jia",  # 毛巾暖气架
            "shui_guan_tao_guan",  # 水管套管
            "xie_ya_fa",  # 泄压阀
            "xiao_sheng_qi",  # 消声器
            "ran_qi_bi_hua_lu",  # 燃气壁挂炉
            "dian_dong_feng_fa", # 电动风阀
            "kong_tiao_hui_feng_kou",  # 空调回风口
            "you_dao_feng_ji",  # 诱导风机
            "song_bu_feng_ji",  # 送补风机
            "feng_ji_pan_guan",  # 风机盘管
            "feng_guan_shang_xia_fan",  # 风管上下翻
        ],
    }
    
    
    # 通过图层、尺寸等后处理获取的构件如下：
    # 'overflow_hole'   溢流口
    # 'water_tank',    # 水箱
    # 'sprinkler'      # 喷头
    # 'check_well'     # 检查井

    MODEL_URL = {
        "prd": {
            ClassifyType.HVAC: "http://124.70.184.163:8505"
        },
        "test": {
            ClassifyType.HVAC: "http://124.70.184.163:8505"
        },
        "pre": {
            ClassifyType.HVAC: "http://124.70.184.163:8505"
        },
        "dev": {
            ClassifyType.HVAC: "http://124.70.184.163:8505"
        }
    }

