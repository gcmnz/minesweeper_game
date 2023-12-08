import sys
from interface import *
from settings import Settings
from backend import *

settings = Settings()

pygame.init()
screen = pygame.display.set_mode((settings.W, settings.H))
pygame.display.set_caption('MineSweeper')
clock = pygame.time.Clock()

FONT = pygame.font.SysFont('Comic sans ms', int(settings.W / 20))
FONT_2 = pygame.font.SysFont('Comic sans ms', int(settings.W / 40))
FONT_3 = pygame.font.SysFont('Comic sans ms', int(settings.W / 30))

bomb_x16_image = pygame.image.load('images/bomb_x16.png')
bomb_x20_image = pygame.image.load('images/bomb_x20.png')
bomb_x30_image = pygame.image.load('images/bomb_x30.png')
bomb_x40_image = pygame.image.load('images/bomb_x40.png')
bomb_img = bomb_x20_image

flag_x16_image = pygame.image.load('images/flag_x16.png')
flag_x20_image = pygame.image.load('images/flag_x20.png')
flag_x30_image = pygame.image.load('images/flag_x30.png')
flag_x40_image = pygame.image.load('images/flag_x40.png')
flag_img = flag_x20_image
icon = pygame.image.load('images/icon.ico')

pygame.display.set_icon(icon)

game_surface = pygame.Surface((settings.W, settings.H))
main_menu_surface = pygame.Surface((settings.W, settings.H))
options_menu_surface = pygame.Surface((settings.W, settings.H))
game_surface.fill(settings.theme[0])
main_menu_surface.fill(settings.theme[0])
options_menu_surface.fill(settings.theme[0])

btn_startgame = Button('Start game', 3)
btn_options = Button('Options', 3)
btn_exit = Button('Exit', 3)

btn_restart = Button('Restart', 1)

btn_easy = Button('Easy', 1)
btn_medium = Button('Medium', 3)
btn_hard = Button('Hard', 1)
btn_1200x900 = Button('1200x900', 1)
btn_800x600 = Button('800x600', 3)
btn_32x20 = Button('32x20', 1)
btn_24x15 = Button('24x15', 3)
btn_16x10 = Button('16x10', 1)
btn_white = Button('white', 3)
btn_black = Button('black', 1)

btn_back = Button('Back', 3)

tv_you_won = TextView('You won!')
tv_bombs = TextView('Bombs: ')
tv_difficult = TextView('Difficult')
tv_resolution = TextView('Resolution')
tv_fieldsize = TextView('Fieldsize')
tv_theme = TextView('Theme')
tv_pausemenu = TextView('Pause menu')

main_menu_buttons = [btn_startgame, btn_options, btn_exit]
options_menu_buttons = [btn_easy, btn_medium, btn_hard, btn_1200x900, btn_800x600,
                        btn_32x20, btn_24x15, btn_16x10, btn_white, btn_black, btn_back]

difficult = settings.difficult
fieldsize = settings.fieldsize

theme = settings.bg_color_1, settings.black

game_field = GameField()
minefield = Map(int(settings.fieldsize.split('x')[0]), int(settings.fieldsize.split('x')[1]), bomb_img,
                flag_img, settings.difficult)

while True:

    if settings.W == 800:
        if settings.fieldsize == '32x20':
            flag_img = flag_x16_image
            bomb_img = bomb_x16_image
        elif settings.fieldsize == '24x15':
            flag_img = flag_x20_image
            bomb_img = bomb_x20_image
        elif settings.fieldsize == '16x10':
            flag_img = flag_x30_image
            bomb_img = bomb_x30_image
    elif settings.W == 1200:
        if settings.fieldsize == '32x20':
            flag_img = flag_x20_image
            bomb_img = bomb_x20_image
        elif settings.fieldsize == '24x15':
            flag_img = flag_x30_image
            bomb_img = bomb_x30_image
        elif settings.fieldsize == '16x10':
            flag_img = flag_x40_image
            bomb_img = bomb_x40_image

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if settings.menu == 2:

                    if difficult != settings.difficult:
                        settings.difficult = difficult
                        settings.clicked = 0
                        minefield.player_map = []
                        minefield.flag_map = []
                        game_surface.fill(settings.theme[0])
                        tv_bombs.text = 'Bombs: 0'

                    if fieldsize != settings.fieldsize:
                        settings.fieldsize = fieldsize
                        settings.clicked = 0
                        minefield.x, minefield.y = int(settings.fieldsize.split('x')[0]), int(
                            settings.fieldsize.split('x')[1])
                        minefield.player_map = []
                        minefield.flag_map = []
                        game_surface.fill(settings.theme[0])
                        tv_bombs.text = 'Bombs: 0'

            settings.menu = abs(settings.menu - 1)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 1:
                if settings.menu == 0:
                    if mouse_pos[1] > game_field.fieldborder:
                        x = int(mouse_pos[0] / game_field.size)
                        y = int((mouse_pos[1] - game_field.fieldborder) / game_field.size)
                        if (x, y) not in minefield.flag_map:
                            if settings.clicked == 0:
                                minefield.generateFinallyMap(x, y, settings.difficult)
                                tv_bombs.text = f'Bombs: {minefield.bombs}'

                            settings.clicked += 1
                            if (x, y) not in minefield.player_map:
                                minefield.player_map.append((x, y))

                            if minefield.finally_map[y][x] == 'Б':
                                for i in range(minefield.x):
                                    for j in range(minefield.y):
                                        if (i, j) not in minefield.player_map and (i, j) not in minefield.flag_map:
                                            minefield.player_map.append((i, j))
                            elif minefield.finally_map[y][x] == 0:
                                minefield.openAround(y, x)

                    else:
                        if on_click(btn_restart.coord, mouse_pos):
                            settings.clicked = 0
                            minefield.player_map = []
                            minefield.flag_map = []
                            tv_bombs.text = 'Bombs: 0'

                if settings.menu == 1:
                    for button in main_menu_buttons:
                        if on_click(button.coord, mouse_pos):
                            if button == btn_startgame:
                                settings.menu = 0
                            elif button == btn_options:
                                settings.menu = 2
                            else:
                                sys.exit()

                elif settings.menu == 2:
                    for button in options_menu_buttons:
                        if on_click(button.coord, mouse_pos):

                            if button == btn_easy:
                                difficult = 88
                                btn_easy.width = 3
                                btn_medium.width = 1
                                btn_hard.width = 1
                            elif button == btn_medium:
                                difficult = 82
                                btn_easy.width = 1
                                btn_medium.width = 3
                                btn_hard.width = 1
                            elif button == btn_hard:
                                difficult = 77
                                btn_easy.width = 1
                                btn_medium.width = 1
                                btn_hard.width = 3

                            elif button == btn_1200x900:
                                btn_800x600.width = 1
                                btn_1200x900.width = 3
                                settings.W, settings.H = 1200, 900

                                screen = pygame.display.set_mode((settings.W, settings.H))
                                game_surface = pygame.Surface((settings.W, settings.H))
                                main_menu_surface = pygame.Surface((settings.W, settings.H))
                                options_menu_surface = pygame.Surface((settings.W, settings.H))

                                game_surface.fill(settings.theme[0])
                                main_menu_surface.fill(settings.theme[0])
                                options_menu_surface.fill(settings.theme[0])

                                FONT = pygame.font.SysFont('Comic sans ms', int(settings.W / 20))
                                FONT_2 = pygame.font.SysFont('Comic sans ms', int(settings.W / 40))
                                FONT_3 = pygame.font.SysFont('Comic sans ms', int(settings.W / 30))

                            elif button == btn_800x600:
                                btn_800x600.width = 3
                                btn_1200x900.width = 1
                                settings.W, settings.H = 800, 600

                                screen = pygame.display.set_mode((settings.W, settings.H))
                                game_surface = pygame.Surface((settings.W, settings.H))
                                main_menu_surface = pygame.Surface((settings.W, settings.H))
                                options_menu_surface = pygame.Surface((settings.W, settings.H))

                                game_surface.fill(settings.theme[0])
                                main_menu_surface.fill(settings.theme[0])
                                options_menu_surface.fill(settings.theme[0])

                                FONT = pygame.font.SysFont('Comic sans ms', int(settings.W / 20))
                                FONT_2 = pygame.font.SysFont('Comic sans ms', int(settings.W / 40))
                                FONT_3 = pygame.font.SysFont('Comic sans ms', int(settings.W / 30))

                            elif button == btn_32x20:
                                fieldsize = '32x20'
                                btn_32x20.width = 3
                                btn_24x15.width = 1
                                btn_16x10.width = 1
                            elif button == btn_24x15:
                                fieldsize = '24x15'
                                btn_32x20.width = 1
                                btn_24x15.width = 3
                                btn_16x10.width = 1
                            elif button == btn_16x10:
                                fieldsize = '16x10'
                                btn_32x20.width = 1
                                btn_24x15.width = 1
                                btn_16x10.width = 3
                            elif button == btn_white:
                                btn_white.width = 3
                                btn_black.width = 1
                                settings.theme = settings.bg_color_1, settings.black, settings.zero_color_black
                                game_surface.fill(settings.theme[0])
                                main_menu_surface.fill(settings.theme[0])
                                options_menu_surface.fill(settings.theme[0])
                            elif button == btn_black:
                                btn_white.width = 1
                                btn_black.width = 3
                                settings.theme = settings.bg_color_2, settings.white, settings.zero_color_white
                                game_surface.fill(settings.theme[0])
                                main_menu_surface.fill(settings.theme[0])
                                options_menu_surface.fill(settings.theme[0])
                            elif button == btn_back:
                                settings.menu = 1

                                if difficult != settings.difficult:
                                    settings.difficult = difficult
                                    settings.clicked = 0
                                    minefield.player_map = []
                                    minefield.flag_map = []
                                    game_surface.fill(settings.theme[0])
                                    tv_bombs.text = 'Bombs: 0'

                                if fieldsize != settings.fieldsize:
                                    settings.fieldsize = fieldsize
                                    minefield.x, minefield.y = int(settings.fieldsize.split('x')[0]), int(
                                        settings.fieldsize.split('x')[1])
                                    settings.clicked = 0
                                    minefield.player_map = []
                                    minefield.flag_map = []
                                    game_surface.fill(settings.theme[0])
                                    tv_bombs.text = 'Bombs: 0'

            elif event.button == 3:
                if settings.menu == 0:
                    if mouse_pos[1] > game_field.fieldborder:
                        x = int(mouse_pos[0] / game_field.size)
                        y = int((mouse_pos[1] - game_field.fieldborder) / game_field.size)
                        if (x, y) not in minefield.player_map:
                            if (x, y) in minefield.flag_map:
                                minefield.flag_map.remove((x, y))
                            else:
                                minefield.flag_map.append((x, y))

    if settings.menu == 0:
        screen.blit(game_surface, (0, 0))
        game_surface.fill((settings.theme[0]))

        btn_restart.output(game_surface, settings.theme[1],
                           (settings.H * 1.05, settings.H / 30, settings.H / 4, settings.H / 10),
                           (settings.W / 1200 * 987, settings.H / 20), FONT_3)

        tv_bombs.output(game_surface, (0, 0), settings.theme[1], FONT_3)
        if set(minefield.flag_map) == set(minefield.bomb_map) and len(minefield.bomb_map) > 1:
            tv_you_won.output(game_surface, (settings.W * 0.4, settings.H * 0.03), settings.theme[1], FONT)

        game_field.output(game_surface, settings.W, settings.H, fieldsize, settings.theme[1])
        minefield.output(game_surface, game_field,
                         pygame.font.SysFont('Comic sans ms', int(800 / (100 / (game_field.size // 11)))), bomb_img,
                         flag_img, settings.num_colors, settings.theme[2])

        pygame.draw.line(game_surface, settings.theme[1], (0, game_field.fieldborder),
                         (settings.W, game_field.fieldborder), 3)

    elif settings.menu == 1:
        screen.blit(main_menu_surface, (0, 0))
        main_menu_surface.fill(settings.theme[0])

        btn_startgame.output(main_menu_surface, settings.theme[1],
                             (settings.W * 0.3, settings.H / 6, settings.W / 2.5, settings.H / 6),
                             (settings.W * 29 / 80, settings.H * 120 / 600), FONT)
        btn_options.output(main_menu_surface, settings.theme[1],
                           (settings.W * 0.3, settings.H * 5 / 12, settings.W / 2.5, settings.H / 6),
                           (settings.W * 0.4, settings.H * 270 / 600), FONT)
        btn_exit.output(main_menu_surface, settings.theme[1],
                        (settings.W * 0.3, settings.H * 2 / 3, settings.W / 2.5, settings.H / 6),
                        (settings.W * 266 / 600, settings.H * 420 / 600), FONT)

        tv_pausemenu.output(main_menu_surface, (settings.W * 6 / 7, settings.H * 0.94), settings.theme[1], FONT_2)

    elif settings.menu == 2:
        screen.blit(options_menu_surface, (0, 0))
        options_menu_surface.fill(settings.theme[0])

        btn_easy.output(options_menu_surface, settings.theme[1],
                        (settings.W / 9.6, settings.H / 4, settings.W / 6, settings.H / 10),
                        (settings.W * 74 / 480, settings.H * 0.27), FONT_2)
        btn_medium.output(options_menu_surface, settings.theme[1],
                          (settings.W / 9.6, settings.H * 23 / 60, settings.W / 6, settings.H / 10),
                          (settings.W * 26 / 192, settings.H * 242 / 600), FONT_2)
        btn_hard.output(options_menu_surface, settings.theme[1],
                        (settings.W / 9.6, settings.H * 31 / 60, settings.W / 6, settings.H / 10),
                        (settings.W * 74 / 480, settings.H * 322 / 600), FONT_2)

        btn_1200x900.output(options_menu_surface, settings.theme[1],
                            (settings.W / 2.4, settings.H / 4, settings.W / 6, settings.H / 10),
                            (settings.W * 53 / 120, settings.H * 0.275), FONT_2)
        btn_800x600.output(options_menu_surface, settings.theme[1],
                           (settings.W / 2.4, settings.H * 23 / 60, settings.W / 6, settings.H / 10),
                           (settings.W * 43 / 96, settings.H * 49 / 120), FONT_2)

        btn_32x20.output(options_menu_surface, settings.theme[1],
                         (settings.W * 35 / 48, settings.H / 4, settings.W / 6, settings.H / 10),
                         (settings.W * 923 / 1200, settings.H * 11 / 40), FONT_2)
        btn_24x15.output(options_menu_surface, settings.theme[1],
                         (settings.W * 35 / 48, settings.H * 23 / 60, settings.W / 6, settings.H / 10),
                         (settings.W * 923 / 1200, settings.H * 245 / 600), FONT_2)
        btn_16x10.output(options_menu_surface, settings.theme[1],
                         (settings.W * 35 / 48, settings.H * 31 / 60, settings.W / 6, settings.H / 10),
                         (settings.W * 923 / 1200, settings.H * 325 / 600), FONT_2)

        btn_white.output(options_menu_surface, settings.theme[1],
                         (settings.W / 12, settings.H * 0.8, settings.W / 7, settings.H / 15),
                         (settings.W / 8.3, settings.H * 0.808), FONT_2)
        btn_black.output(options_menu_surface, settings.theme[1],
                         (settings.W / 12, settings.H * 0.88, settings.W / 7, settings.H / 15),
                         (settings.W / 8.3, settings.H * 0.888), FONT_2)

        btn_back.output(options_menu_surface, settings.theme[1],
                        (settings.W * 0.375, settings.H * 47 / 60, settings.W / 4, settings.H / 7.5),
                        (settings.W * 7 / 16, settings.H * 48 / 60), FONT)

        tv_difficult.output(options_menu_surface, (settings.W * 7 / 80, settings.H * 124 / 1200), settings.theme[1],
                            FONT)
        tv_resolution.output(options_menu_surface, (settings.W * 31 / 80, settings.H * 124 / 1200), settings.theme[1],
                             FONT)
        tv_fieldsize.output(options_menu_surface, (settings.W * 56 / 80, settings.H * 124 / 1200), settings.theme[1],
                            FONT)
        tv_theme.output(options_menu_surface, (settings.W / 17, settings.H * 0.7), settings.theme[1], FONT)
        tv_pausemenu.output(options_menu_surface, (settings.W * 6 / 7, settings.H * 0.94), settings.theme[1], FONT_2)

    pygame.display.update()
    clock.tick(settings.FPS)
