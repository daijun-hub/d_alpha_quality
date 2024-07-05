from enum import Enum


class MultiBorderPipelineType(Enum):
    TYPE_A = 'A'   # 主副图，借助副图对主图进行审查
    TYPE_B = 'B'   # 住宅平面图上下层
    TYPE_C = 'C'   # 建筑说明图，全部返回
    TYPE_D = 'D'   # 将属于同一项目的、所有的、规则中需要的图纸类型的图框全部返回，但是不做图纸类型完整性检查
