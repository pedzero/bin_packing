type Color = hex


class Colors:
    _colors = [
        0X295F98,  # BLUE
        0XEAE4DD,  # GREY
        0XCEDF9F,  # LIGHT_GREEN
        0XE8B86D,  # GOLD_YELLOW
        0XFF8A8A,  # PINK
        0XB1AFFF,  # OCEAN_BLUE
        0X987070,  # BROWN
        0XAD88C6,  # PURPLE
    ]

    _instance = None

    def __init__(self):
        self.color_index = 0
        self.max_color_index = len(self._colors) - 1

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_next_color(self):
        current = self.color_index
        self.color_index += 1
        return current % self.max_color_index
