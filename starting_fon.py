import random

import pygame
from coords_coins import *
from main import *

size = width, height = 900, 650
screen = pygame.display.set_mode(size)
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
pygame.display.set_caption('Сollect Сoins')
tile_image = {'wall': load_image('box.png'),
              'empty': load_image('grass.png'),
              'coins': load_image('monet.gif')}
player_image = load_image('mar.png')
tile_width = tile_height = 50


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 900, 700)


class SpriteGroup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for inet in self:
            inet.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_image[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0],
                                               tile_height * self.pos[1])

    def update(self):
        self.kill()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    can_press = []
    for i in range(9):
        can_press.append(eval(f'pygame.K_{i}'))
    intro_text = ["Выбeрите уровень их 3",
                  'Цифрами 1, 2, 3',
                  'Ходить на wasd',
                  "Собери все монетки, чтобы стать миллионером"
                  ]
    fon = pygame.transform.scale(load_image('фон_чрепаха.jpg'), size)
    screen.blit((fon), (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 50
        intro_rect.top = text_coord
        intro_rect.x = 300
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key in can_press:
                    return event.key
                else:
                    pass
        pygame.display.flip()


def load_level(filename):
    filename = filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = '.'
    return new_player, x, y


def move(hero, movement, max_x, max_y, level_map):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1][x] == '.':
            hero.move(x, y - 1)
        elif level_map[y - 1][x] == '*':
            hero.move(x, y - 1)
            Tile('empty', x, y)
    elif movement == 'down':
        if y < max_y - 1 and (level_map[y + 1][x] == '.' or
                              level_map[y + 1][x] == '*'):
            hero.move(x, y + 1)
    elif movement == 'left':
        if x > 0 and (
                level_map[y][x - 1] == '.' or level_map[y][x - 1] == '*'):
            hero.move(x - 1, y)
    elif movement == 'right':
        if x < max_x - 1 and (level_map[y][x + 1] == '.'
                              or level_map[y][x + 1] == '*'):
            hero.move(x + 1, y)

# Название функций и классов говорят сами за себя
