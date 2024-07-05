from ..space import Space
from ...border_entity import BorderEntity

class BaoMuJian(Space):
    def __init__(self, space_object: Space, border_entity: BorderEntity) -> None:
        Space.copy(self, space_object)
        self.chinese_name = "保姆间"
