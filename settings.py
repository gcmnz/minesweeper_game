class Settings:
    def __init__(self):
        self.bg_color_1 = (200, 200, 200)
        self.black = (50, 50, 50)
        self.zero_color_black = (180, 180, 180)
        self.bg_color_2 = (50, 50, 50)
        self.white = (200, 200, 200)
        self.zero_color_white = (80, 80, 80)

        self.num_colors = {1: (0, 0, 255),
                           2: (0, 128, 0),
                           3: (255, 0, 0),
                           4: (0, 0, 139),
                           5: (140, 0, 0),
                           6: (72, 209, 204),
                           7: (240, 230, 140),
                           8: (139, 0, 139),
                           }

        self.W, self.H = 800, 600
        self.difficult = 82
        self.fieldsize = '24x15'
        self.theme = self.bg_color_1, self.black, self.zero_color_black
        self.FPS = 30
        self.menu = 1
        self.clicked = 0
