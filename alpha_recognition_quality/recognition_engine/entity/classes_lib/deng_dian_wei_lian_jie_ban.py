from ..base_type import EntityBaseType
from ..entity import ClassifiedEntity, Entity
from ...border_entity import BorderEntity
from ...utils.utils_entity import *
from ....config_manager.decor_electric.drawing_config import DrawingType
from ....common.utils2 import load_drawing_pkl


def _distinct_text(text_list):
    d1 = {(v.extend_message, tuple(v.bbox.list)): v for v in text_list}
    return list(d1.values())


def _trans_unit(heights):
    """统一转为m(米)，如果有多个，按正序排列"""
    res = list()
    for height in heights:
        if height[-1] == 'm':
            height = float(height[:-1]) / 1000
        elif height[-1] == 'c':
            height = float(height[:-1]) / 100
        elif height[-1] == 'd':
            height = float(height[:-1]) / 10
        else:
            height = float(height)
        res.append(height)
    res.sort()
    return res


def filter_headers(enhs, inhs):
    enhs.sort(key=lambda x: x.bbox.list[0])
    inhs.sort(key=lambda x: x.bbox.list[0])
    _heads = list()
    j = 0
    for _enh in enhs:
        # 是否可被替换
        rep_flag = False
        _x = _enh.bbox.list[0]
        for j in range(j, len(inhs)):
            _inh = inhs[j]
            if _inh.bbox.list[0] < _x:
                _tmp_y = _heads[-1].bbox.list[1]
                if rep_flag and _inh.bbox.list[1] > _tmp_y:
                    _heads.pop(-1)
                else:
                    rep_flag = True
                _heads.append(_inh)
                j += 1
            else:
                # 跳到下一个enh时重置标记
                rep_flag = False
                break
        _heads.append(_enh)
    # 头尾相同的话，只留一个
    f_head, l_head = _heads[0], _heads[-1]
    if f_head.extend_message == l_head.extend_message:
        if f_head.bbox.list[1] >= l_head.bbox.list[1]:
            _heads.pop(-1)
        else:
            _heads.pop(0)
    return [(_heads[i], _heads[i + 1], _heads[i].extend_message == enhs[0].extend_message)
            for i in range(0, len(_heads) // 2, 2)]


def _infer_header(equipment_name_heads, install_way_heads):
    """
    根据所有匹配到的表头列（两个表头列须同时出现），从左往右返回表头
        bbox：左上右下
    """
    headers = list()
    # 表格最大可能数
    max_tables = min(len(equipment_name_heads), len(install_way_heads))
    # 按纵坐标排序
    equipment_name_heads.sort(key=lambda t: t.bbox.list[1])
    install_way_heads.sort(key=lambda t: t.bbox.list[1])
    for i in range(max_tables):
        # 按纵坐标一层层拨
        max_head_y_1 = equipment_name_heads[0].bbox.list[1]
        max_head_y_2 = install_way_heads[0].bbox.list[1]
        max_head_y = max(max_head_y_1, max_head_y_2)
        enhs = list(filter(lambda x: x.bbox.list[1] <= max_head_y, equipment_name_heads))
        inhs = list(filter(lambda x: x.bbox.list[1] <= max_head_y, install_way_heads))
        # 一排可能有多个相同表头
        if not enhs or not inhs:
            break
        for _ in enhs:
            equipment_name_heads.pop(0)
        for _ in inhs:
            install_way_heads.pop(0)
        """
        1. 如果都只有一个，直接比较
        2. 否则
            a. 若enhs(inhs)只有一个，保留y最近的inh(enh)
            b. 若都不止一个，则至少有一个：其中所有元素的max_y相同
                i. 如果enhs的max_y相同，则须在enhs两两元素中找一个inh，取max_y最近的
                ii. 反之
        """
        # 如果都只有一个，直接比较
        if len(enhs) == 1 and len(inhs) == 1:
            _enh, _inh = enhs[0], inhs[0]
            if _enh.bbox.list[0] < _inh.bbox.list[0]:
                headers.append((_enh, _inh, True))
            else:
                headers.append((_inh, _enh, False))
        # 若enhs(inhs)只有一个，保留y最近的inh(enh)
        elif len(enhs) == 1:
            inhs.sort(key=lambda x: x.bbox.list[1])
            _enh, _inh = enhs[0], inhs[-1]
        elif len(inhs) == 1:
            enhs.sort(key=lambda x: x.bbox.list[1])
            _enh, _inh = enhs[-1], inhs[0]
        # 若都不止一个，则至少有一个：其中所有元素的max_y相同
        else:
            # 如果enhs的max_y相同，则须在enhs两两元素中找一个inh，取max_y最近的
            if len(set([x.bbox.list[1] for x in enhs])) == 1:
                headers = filter_headers(enhs, inhs)
            else:
                headers = filter_headers(inhs, enhs)
        if not equipment_name_heads or not install_way_heads:
            break
    return headers


# 分类构件
class DengDianWeiLianJieBan(ClassifiedEntity):
    chinese_name = "等电位连接板"

    def __init__(self, entity_object: Entity, border_entity: BorderEntity) -> None:
        ClassifiedEntity.__init__(self, entity_object)

        self.chinese_name = "等电位连接板"
        self.entity_base_type = EntityBaseType.ELECTRIC_DEVICE

        # 安装高度
        # self.install_height_dict = dict()
        height_target_pattern = r'LEB箱.*?安装高度h=(\s*[\d]+[.]?[\d]*\s*[cmd]?)m'
        self.install_height, self.install_height_bbox = get_install_height("等电位|LEB", self.bounding_rectangle.list, border_entity,
                                                 height_target_pattern)

        self.install_height_dict_bbox = dict()
        self.install_height_dict_file_id = None
        self.install_height_dict_pickle_id = None

    def get_cross_border_attribs(self, border_entity, building_object):
        # 等电位安装高度在平面图找，暂时不跨图框
        # try:
        #     self._update_install_height_dict(border_entity, building_object)
        # except Exception:
        #     print('Error: 等电位连接板跨图框属性获取失败')
        pass

    def _update_install_height_dict(self, border_entity, building_object):
        # 遍历特殊图纸类型，《图例及主要设备材料表》中获取安装高度
        # 如果该图纸类型有多个，找到就不用再去其它图框找
        for special_drawing_dict in building_object.special_drawing_list:

            info_dict = special_drawing_dict.get(DrawingType.DECORATION_ELECTRIC_EQUIPMENT_SCHEDULE)
            if not info_dict:
                continue
            file_id = info_dict['file_id']
            _border_entity = load_drawing_pkl(file_id)
            # 板房与货量的subproject_name不一样，只拿一种
            if border_entity.subproject_name != _border_entity.subproject_name:
                continue
            found_flag = self._get_height(file_id, _border_entity)
            if found_flag:
                break

    def _get_height(self, file_id, border_entity_info):
        found_flag = False
        all_text_info = border_entity_info.border_text_info[TextType.ALL]
        # 表格平铺，可能多个表头，按横坐标排序
        equipment_name_heads = [_ for _ in all_text_info if re.search('设备名称', _.extend_message)]
        if not equipment_name_heads:
            return found_flag
        equipment_name_heads = _distinct_text(equipment_name_heads)

        install_way_heads = [_ for _ in all_text_info if re.search('安装方式', _.extend_message)]
        if not install_way_heads:
            return found_flag
        install_way_heads = _distinct_text(install_way_heads)

        header_list = _infer_header(equipment_name_heads, install_way_heads)
        # 所有关键词（等电位）
        keyword_texts = [_ for _ in all_text_info if re.search('等电位|LEB箱', _.extend_message)]
        if not keyword_texts:
            return found_flag
        keyword_texts = _distinct_text(keyword_texts)

        # 只要"设备名称"列的关键词
        filtered_texts = list()
        for _text in keyword_texts:
            _bbox = _text.bbox.list
            flag = None
            for h in header_list:
                if not h[2]:
                    ins_head, eqp_name_head = h[:2]
                else:
                    eqp_name_head, ins_head = h[:2]
                m_bbox = eqp_name_head.bbox.list
                # 横坐标与"设备名称"表头相交
                if not (_bbox[0] > m_bbox[2] or _bbox[2] < m_bbox[0]):
                    # 该关键词找到所在列
                    flag = ins_head
                    break
            if flag:
                filtered_texts.append((_text, flag))
        # 所有安装高度
        install_head_texts = [_ for _ in all_text_info if re.search('h=.*m', _.extend_message)]
        if not install_head_texts:
            return found_flag
        install_head_texts = _distinct_text(install_head_texts)

        # 根据关键词和安装方式表头，获取安装方式
        for target_text, ins_head in filtered_texts:
            raw_bbox = target_text.bbox.list
            eqp_name = target_text.extend_message
            an_bbox = ins_head.bbox.list
            for ih_text in install_head_texts:
                _bbox = ih_text.bbox.list
                if (_bbox[1] + (_bbox[3] - _bbox[1]) / 2) in range(raw_bbox[1], raw_bbox[3]) and \
                        _bbox[0] in range(an_bbox[0] - (an_bbox[2] - an_bbox[0]),
                                          an_bbox[2] + (an_bbox[2] - an_bbox[0])):
                    found_flag = True
                    heights = re.findall(r'h=([\dcmd\\.]*)m', ih_text.extend_message)
                    if heights:
                        hd = self.install_height_dict.get(eqp_name, [])
                        if hd:
                            hd = hd + _trans_unit(heights)
                            hd_bbox = self.install_height_dict_bbox.get(eqp_name)
                            hd_bbox = [min(_bbox[0], hd_bbox[0]),
                                       min(_bbox[1], hd_bbox[1]),
                                       max(_bbox[2], hd_bbox[2]),
                                       max(_bbox[3], hd_bbox[3]),
                                       ]
                            self.install_height_dict_bbox[eqp_name] = hd_bbox
                        else:
                            hd = _trans_unit(heights)
                            self.install_height_dict_bbox[eqp_name] = raw_bbox
                        self.install_height_dict[eqp_name] = hd
                        print(f'找到{eqp_name}的安装高度{heights}')
                    else:
                        print(f'安装方式中未找到h=*m格式文本')
                    # 一个单元格有多个文本匹配
                    # break

        if found_flag:
            for k, v in self.install_height_dict.items():
                self.install_height_dict[k] = sorted(v, key=lambda x: float(x), reverse=True)
            self.install_height_dict_file_id = border_entity_info.cad_border_id
            self.install_height_dict_pickle_id = file_id

        return found_flag
