class Line(object):
    """基础线段类"""
    def __init__(self,
                 line):
        self.point_1_x = line[0]
        self.point_1_y = line[1]
        self.point_2_x = line[2]
        self.point_2_y = line[3]

    def __getitem__(self, s):
        return self.list.__getitem__(s)

    @property
    def list(self):
        return [self.point_1_x, self.point_1_y, self.point_2_x, self.point_2_y]
