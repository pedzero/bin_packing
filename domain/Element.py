from domain.Color import Color
from domain.Color import Colors


class Element:
    def __init__(self, size: float, color: Color = None):
        self.size = size
        self.color = color if color else Colors.instance().get_next_color()
