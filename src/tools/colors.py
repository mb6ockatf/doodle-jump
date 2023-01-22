"""Colors class"""
from random import choice


class Colors:
    """Class to handle groups of colors"""
    def __init__(self):
        black_white = {"black": (16, 16, 16), "white": (240, 240, 240)}
        self.dark = {"dark_purple": (49, 11, 71),
                     "dark_grey": (57, 68, 79),
                     "dark_green": (14, 98, 67),
                     "dark_yellow": (207, 184, 32)}
        self.light = {"light_blue": (104, 195, 248),
                      "light_green": (153, 232, 89)}
        self.vivid = {"blue": (40, 81, 184),
                      "purple": (120, 18, 120),
                      "grey": (143, 143, 161),
                      "yellow": (236, 234, 156),
                      "green": (24, 180, 24),
                      "brown": (107, 59, 27),
                      "red": (170, 45, 14),
                      "orange": (235, 118, 45)}
        self.all_colors = black_white | self.dark | self.light | self.vivid

    def __getitem__(self, key: str) -> tuple:
        return self.all_colors[key]

    def get_random_paint(self, source=None) -> tuple:
        """
        return random paint from given dict
        if no resource provided, returns value from self.all_colors
        """
        if source is None:
            source = self.all_colors
        all_values = list(source.values())
        return choice(all_values)
