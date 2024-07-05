class BoundingVertex(object):
    """基础外接矩形类"""
    def __init__(self,
                 bbox):
        self.point_1_x = bbox[0][0]
        self.point_1_y = bbox[0][1]
        self.point_2_x = bbox[1][0]
        self.point_2_y = bbox[1][1]
        self.point_3_x = bbox[2][0]
        self.point_3_y = bbox[2][1]
        self.point_4_x = bbox[3][0]
        self.point_4_y = bbox[3][1]

    def __getitem__(self, s):
        return self.list.__getitem__(s)

    @property
    def list(self):
        return [
            [self.point_1_x, self.point_1_y],
            [self.point_2_x, self.point_2_y],
            [self.point_3_x, self.point_3_y],
            [self.point_4_x, self.point_4_y],
        ]
