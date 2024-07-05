# -*- coding: utf-8 -*-

import re

from ...config_manager.decor_architecture.layer_config import LayerConfig


def is_ignore_layer(layer_name, ignore_words):
    '''
    判断图层中是否含有需忽略的关键字。这里会把ignore_words里面的字符串取upper, 因此调用时
    也要把原始的layer_name取upper后传入。
    Param:
        ignore_words: 需要忽略的关键字
        layer_name: 图层名
    Return:
        True：表示含有忽略字段，该图册需过滤，False：不含有需忽略字段，该图层保留
    '''    
    for layer_sub in ignore_words:
        # 含“车”“车位”图层无需忽略“字”
        if layer_sub == '字' and ('车位' in layer_name or '车' in layer_name):
            continue
        # 墙线不过滤
        if layer_sub == '线' and ('墙线' in layer_name or '窗线' in layer_name or ('虚线' in layer_name and re.search('WIN|DOOR|门|窗', layer_name))):
            continue
        # 只有含“'WIN|DOOR|门|窗”的图层才忽略“号”
        if '号' in layer_sub and re.search('WIN|DOOR|门|窗', layer_name) is None:
            continue
        # 含“配件”“洞口”的图层同时含“空调”“Aircon”需要忽略
        if '配件' in layer_name or '洞口' in layer_name:
            if '空调' in layer_name or 'Aircon'.upper() in layer_name:
                return True
            else:
                pass
        # 其余情况图层含有忽略关键字则返回True
        if re.search(layer_sub.upper(), layer_name):
            return True

    return False


def run(entity_list, all_layer_list, entity_layer_dict=LayerConfig.ENTITY_LAYER_DICT.value):
    """在layer列表内获取entity列表中entity的推荐的layer
           entity_list：需要推荐的构件列表
           layer_list: 一张图纸的全部layers名称列表，从get_layers.py输出获取
           entity_layer_dict: 知识图谱字典，后端可以修改为数据库读取，方便随时更新图谱字典
           return: 返回全部entity对应推荐layer的字典
    """
    layer_rec_list = []
    # 遍历构件列表
    for entity in entity_list:
        item_rec_list = []  # 初始化构件匹配到的图层列表
        layer_info = entity_layer_dict.get(entity, {})  # 获取知识图谱字典中构件关键字和忽略关键字
        if layer_info == {}:
            layer_rec_list.append(list(set(item_rec_list)))  # 去重
            continue
        # layer_info = entity_layer_dict[entity]  # 获取知识图谱字典中构件关键字和忽略关键字
        match_layer_sub = layer_info['layer_sub']  # 构件匹配关键字
        ignore_words = layer_info['ignore_word']  # 构件忽略关键字
        # 遍历匹配关键字，匹配时统一使用字符大写表示（忽略大小写）
        for layer_sub in match_layer_sub:
            layer_sub_upper = layer_sub.upper()
            # 遍历全部图层，在图层中正则搜索匹配关键字，获取图层推荐
            for layer in all_layer_list:
                valid_layer_name_list = layer.split('$')
                valid_layer_name_list.reverse()
                valid_layer_name_list = valid_layer_name_list[:2]
                valid_layer_name_upper_list = [x.upper() for x in valid_layer_name_list]
                for valid_layer_name, layer_upper in zip(valid_layer_name_list, valid_layer_name_upper_list):
                    # filter layer only consist of '地下车库'
                    if '地下车库' in valid_layer_name and entity != 'underground_building':
                        if not re.search(layer_sub_upper, valid_layer_name.replace('地下车库', '').upper()):
                            continue
                    if layer_sub == 'FLOR' and ('SPCL' in layer_upper or 'STRS' in layer_upper):
                        if entity in ['washbasin', 'closestool', 'diamond_bath']:
                            pass
                        else:
                            continue
                    res = re.search(layer_sub_upper, layer_upper)
                    if res:
                        if is_ignore_layer(layer_upper, ignore_words):
                            continue
                        # 对于立管构件，若匹配“pipe”，则要求图层需包含‘vpipe’，‘vert_pipe’
                        if entity == 'pipe':
                            if 'pipe'.upper() in layer_upper and 'vpipe'.upper() not in layer_upper and 'vert_pipe'.upper() not in layer_upper:
                                continue
                        item_rec_list.append(layer)
                        break
        # print("entity", entity)
        # print("layer list", item_rec_list)
        layer_rec_list.append(list(set(item_rec_list)))  # 去重


    rec_dict = dict(zip(entity_list, layer_rec_list))  # 以构件类别为key，匹配到的图层列表为value的字典

    return rec_dict


def main():
    layer_list = ['厨卫', 'C-BORDER', 'A-WIN-TEXT', 'VPIP', 'PIP', '厨卫++', 'abc-VPIPE-abc', 'VPIPE-废水', '0', '图框',
                  '__覆盖_A10-户型A_SEN24I58_设计区$0$AE-WIND', 'AD-NUMB', '字母车位', '子母车位', 'car-字', '车位线', 'abcwall--',
                  'Wall--abc', 'a_pipe', 'abvpipecd', 'door-编号', '编号-vert_pipe', 'X-TTLB-地下车库(100)$0$A-PRKG',
                  'X-TTLB-地下车库(100)$0$A-WIN', '地下车库-车位', 'P-P-L', 'P-Y-L', 'P-J-L', 'P-RM-L', 'P-X-L', 'P-ZP-L',
                  '-ACO-PLTW', '商业快充', '办公慢充', '社会无障碍', '公共泊位', 'XRA-地下车库一层$0$A-CAR_LINE',
                  '136+95+95+136_SJB_2F（架空）$0$S_RBAR_SLAB_PATT（板配筋填充）', '$abc$HYDRANT', '窗沿', 'A-DIM-ELEV',
                  '立管$0$B-立管$0$S_DRAI_FLDR（地漏）', 'A-FLOR-STRS', 'A-FLOR-SPCL', 'A-FLOR-IDEN', 'A-FLOR', '水', 'a水', '水b']
    entity_list = ["window", "elevator_door", "door", "pipe", "elevator_box", "fire_hydrant", "wall", 'border',
                   'segment',
                   'floor_drain', 'pillar', 'floor_drain_mix']

    layer_recomandation = run(entity_list, layer_list)
    for entity in entity_list:
        print('{0}构件在本图的推荐图层为{1}'.format(entity, layer_recomandation[entity]))


if __name__ == '__main__':
    main()
