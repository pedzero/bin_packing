type Color = hex

class Colors:
    colors = {
        "BLUE": 0x295F98,  # BLUE
        "GREY": 0xEAE4DD,  # GREY
        "LIGHT_GREEN": 0xCEDF9F,  # LIGHT_GREEN
        "GOLD_YELLOW": 0xE8B86D,  # GOLD_YELLOW
        "PINK": 0xFF8A8A,  # PINK
        "OCEAN_BLUE": 0xB1AFFF,  # OCEAN_BLUE
        "BROWN": 0x987070,  # BROWN
        "PURPLE": 0xAD88C6,  # PURPLE
        "BLACK": 0X000000,  # BLACK
    }

    _instance = None

    def __init__(self):
        self.color_index = 0
        self.max_color_index = len(self.colors)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_next_color(self):
        current = self.color_index
        self.color_index = (self.color_index + 1) % self.max_color_index
        return list(self.colors.values())[current]

    def get_color_as_tuple(self, hex_color: int):
        red = (hex_color >> 16) & 0xFF
        green = (hex_color >> 8) & 0xFF
        blue = hex_color & 0xFF
        return red, green, blue
