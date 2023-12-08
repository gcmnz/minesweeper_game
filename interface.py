import pygame


class Widget:
    def __init__(self, text):
        self.text = text


class Button(Widget):

    def __init__(self, text, width):
        super().__init__(text)
        self.textsize = None
        self.textcoord = None
        self.coord = None
        self.color = None
        self.surface = None
        self.width = width

    def output(self, surface, color, coord, textcoord, textsize):
        self.surface = surface
        self.color = color
        self.coord = coord
        self.textcoord = textcoord
        self.textsize = textsize
        pygame.draw.rect(self.surface, self.color, self.coord, self.width)
        self.surface.blit(self.textsize.render(self.text, True, self.color), self.textcoord)


class TextView(Widget):

    def __init__(self, text):
        super().__init__(text)
        self.textsize = None
        self.textcolor = None
        self.textcoord = None
        self.surface = None

    def output(self, surface, textcoord, textcolor, textsize):
        self.surface = surface
        self.textcoord = textcoord
        self.textcolor = textcolor
        self.textsize = textsize

        self.surface.blit(self.textsize.render(self.text, True, self.textcolor), self.textcoord)


class GameField:
    def __init__(self):

        self.color = None
        self.fieldborder = None
        self.y = None
        self.x = None
        self.fieldsize = None
        self.H = None
        self.W = None
        self.surface = None
        self.size = 50

    def output(self, surface, W, H, fieldsize, color):
        self.surface = surface
        self.W = W
        self.H = H
        self.fieldsize = fieldsize
        self.color = color
        self.x, self.y = int(self.fieldsize.split('x')[0]), int(self.fieldsize.split('x')[1])
        self.fieldborder = self.H / 6
        self.size = (self.W * (self.H - self.fieldborder) / self.x / self.y) ** 0.5
        for i in range(1, self.x + 1):
            pygame.draw.line(self.surface, self.color, (self.size * i, self.fieldborder), (self.size * i, self.H))
        for j in range(1, self.y + 1):
            pygame.draw.line(self.surface, self.color, (0, self.size * j + self.fieldborder),
                             (self.W, self.size * j + self.fieldborder))
