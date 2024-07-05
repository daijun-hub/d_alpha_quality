class BoundingRectangle(object):
    """基础外接矩形类"""
    def __init__(self,
                 bbox):
        self.top_left_x = bbox[0]
        self.top_left_y = bbox[1]
        self.bottom_right_x = bbox[2]
        self.bottom_right_y = bbox[3]
        if self.top_left_x > self.bottom_right_x:
            self.top_left_x, self.bottom_right_x = self.bottom_right_x, self.top_left_x
        if self.top_left_y > self.bottom_right_y:
            self.top_left_y, self.bottom_right_y = self.bottom_right_y, self.top_left_y

    def __getitem__(self, s):
        return self.list.__getitem__(s)

    def __repr__(self) -> str:
        return str(self.list)

    @property
    def list(self):
        return [self.top_left_x, self.top_left_y, self.bottom_right_x, self.bottom_right_y]
