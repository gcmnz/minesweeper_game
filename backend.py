import random

import pygame


def getKey(arr):
    values = list(arr.values())
    index = values.index(1)
    return list(arr)[index]


def on_click(arr, pos):
    return arr[0] < pos[0] < arr[0] + arr[2] and arr[1] < pos[1] < arr[1] + arr[3]


class Map:
    def __init__(self, x, y, bomb_image, flag_image, difficult):
        self.x = x
        self.y = y
        self.finally_map = []
        self.player_map = []
        self.flag_map = []
        self.bomb_map = []
        self.bomb_image = bomb_image
        self.flag_image = flag_image
        self.bombs = 0
        self.fontsize = None
        self.difficult = difficult

    def generateFinallyMap(self, mouse_x, mouse_y, difficult):
        self.difficult = difficult
        self.__generateBombMap()
        self.bombs = 0
        self.finally_map[mouse_y][mouse_x] = 0

        for i in range(self.y):
            for j in range(self.x):
                if self.finally_map[i][j] != 'Б':
                    self.finally_map[i][j] = (self.checkAround(i, j))
                else:
                    self.bombs += 1

    def __generateBombMap(self):
        self.bomb_map = []
        self.finally_map = []
        temp = []
        for i in range(self.y):
            for j in range(self.x):
                if random.randrange(1, 101) // self.difficult:
                    temp.append('Б')
                    self.bomb_map.append((j, i))
                else:
                    temp.append(0)
            self.finally_map.append(temp)
            temp = []

    def checkAround(self, a, b):
        num = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if self.finally_map[a + i][b + j] == 'Б':
                        if a == 0 and i == -1 or b == 0 and j == -1:
                            continue
                        elif a == self.y and i == 1 or b == self.x and j == 1:
                            continue
                        num += 1
                except IndexError:
                    continue
        return num

    def openAround(self, a, b):
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if a == 0 and i == -1 or b == 0 and j == -1:
                        continue
                    if a+i == self.y or b+j == self.x:
                        continue
                    if (b+j, a+i) not in self.player_map:
                        self.player_map.append((b+j, a+i))
                        if self.finally_map[a+i][b+j] == 0:
                            self.openAround(a+i, b+j)
                except IndexError:
                    continue

    def output(self, surface, Field, font, bomb_image, flag_image, font_color, empty_color):
        self.bomb_image = bomb_image
        self.flag_image = flag_image
        self.fontsize = Field.size
        for i, j in self.player_map:
            if self.finally_map[j][i] == 'Б':
                surface.blit(self.bomb_image,
                             (Field.size * (i + 0.22), j * Field.size + Field.fieldborder + Field.size / 5))
            elif self.finally_map[j][i] == 0:
                zero_surface = pygame.Surface((Field.size-3, Field.size-3))
                zero_surface.fill(empty_color)
                surface.blit(zero_surface, (i*Field.size+2, j*Field.size + Field.fieldborder+2))

            else:
                surface.blit(font.render(str(self.finally_map[j][i]), True, font_color[self.finally_map[j][i]]),
                             (Field.size * (i + 0.3), j * Field.size + Field.fieldborder))

        for i, j in self.flag_map:
            surface.blit(self.flag_image,
                         (Field.size * (i + 0.22), j * Field.size + Field.fieldborder + Field.size / 5))
