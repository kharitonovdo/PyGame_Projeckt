import pygame
import os
import sys
from starting_fon import *


# Загрузка картинки из файла date


def load_image(name, colorkey=None):
    fullname = os.path.join('../PyGame_Projeckt/data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


if __name__ == '__main__':
    try:
        pygame.init()
        player = None
        run = True
        # Создание карт и выбор карт
        mapa = ''
        levls = {49: 'Map_0_lvl',
                 50: 'Map_1_lvl',
                 51: 'Map_2_lvl'}
        a = start_screen()
        for _ in levls:
            if a in levls:
                mapa = levls[a]
                break
        if mapa == '':
            pass
        # Загрузка уровней и спрайта см. starting_fon
        level_map = load_level(mapa)
        hero, max_x, max_y = generate_level(level_map)
        # счётчик монет 15/15
        text = 0
        # Общий счетчик монет
        count_main = 0
        # Переход на финальное окно
        flag = False
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                # Движение персонажа
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        move(hero, 'up', max_x, max_y, level_map)
                    if event.key == pygame.K_s:
                        move(hero, 'down', max_x, max_y, level_map)
                    if event.key == pygame.K_d:
                        move(hero, 'right', max_x, max_y, level_map)
                    if event.key == pygame.K_a:
                        move(hero, 'left', max_x, max_y, level_map)
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    # Подсчёт общих очков и очков уровня
                    # Столкновение сбор монет, 3 блока анологично
                    if mapa == 'Map_0_lvl':
                        if hero.pos in coords_1_lvl_main_k_copy:
                            text += 1
                            count_main += 1
                            a = coords_1_lvl_main_k_copy.index(hero.pos)
                            screen.blit(load_image('grass.png'),
                                        (coords_1_lvl_copy[a]))
                            del coords_1_lvl_copy[a]
                            del coords_1_lvl_main_k_copy[a]
                    elif mapa == 'Map_1_lvl':
                        if hero.pos in coords_2_lvl_main_k_copy:
                            text += 1
                            count_main += 1
                            a = coords_2_lvl_main_k_copy.index(hero.pos)
                            screen.blit(load_image('grass.png'),
                                        (coords_2_lvl_copy[a]))
                            del coords_2_lvl_copy[a]
                            del coords_2_lvl_main_k_copy[a]
                    elif mapa == 'Map_2_lvl':
                        if hero.pos in coords_3_lvl_main_k_copy:
                            text += 1
                            count_main += 1
                            a = coords_3_lvl_main_k_copy.index(hero.pos)
                            screen.blit(load_image('grass.png'),
                                        (coords_3_lvl_copy[a]))
                            del coords_3_lvl_copy[a]
                            del coords_3_lvl_main_k_copy[a]
            # если ты набрал 15 очков, т.е прошёл уровень то см. дальше
            # 3 анологичных блока

            if text == 15:
                text = 0
                if mapa == 'Map_0_lvl':
                    mapa = 'Map_1_lvl'
                    screen.fill((0, 0, 0))
                    # Смена карты удоление персонажа
                    hero_group.update()
                    level_map = load_level(mapa)
                    hero, max_x, max_y = generate_level(level_map)
                elif mapa == 'Map_1_lvl':
                    mapa = 'Map_2_lvl'
                    if mapa == 'Map_2_lvl':
                        screen.fill((0, 0, 0))
                        # Смена карты удоление персонажа
                        hero_group.update()
                        level_map = load_level(mapa)
                        hero, max_x, max_y = generate_level(level_map)
                elif mapa == 'Map_2_lvl':
                    flag = True
            else:
                # Создание финального окна
                if flag:
                    if count_main != 45:
                        text_end_con = 'Вы собрали не все монетки'
                    else:
                        text_end_con = 'Поздравляем, вы прошли игру!!!'
                    fon = pygame.transform.scale(load_image('фон_чрепаха.jpg'),
                                                 size)
                    screen.blit((fon), (0, 0))
                    font = pygame.font.Font(None, 50)
                    end_t = font.render(text_end_con
                        , True, (0, 100, 5))
                    end_t_coins = font.render(f'Общее количество монет '
                                              f'{count_main} из 45', True,
                                              (0, 100, 5))
                    screen.blit(end_t_coins, (150, 200))
                    screen.blit(end_t, (150, 150))
                else:
                    # видимое кол-во очков на уровне
                    screen.fill(pygame.Color('black'))
                    font = pygame.font.Font(None, 50)
                    text_15 = font.render("/15", True, (0, 0, 0))
                    text_x_15 = 850
                    text_y_15 = 0
                    text_x = 830
                    text_y = 0
                    if text >= 10:
                        text_x = 810
                    text_stroka = font.render(f"{text}", True, (0, 0, 0))
                    screen.fill(pygame.Color('black'))
                    sprite_group.draw(screen)
                    hero_group.draw(screen)
                    screen.blit(text_15, (text_x_15, text_y_15))
                    screen.blit(text_stroka, (text_x, text_y))
                    # Загрузка карт
                    if mapa == 'Map_0_lvl':
                        for i in coords_1_lvl_copy:
                            screen.blit(tile_image['coins'], i)
                    elif mapa == 'Map_1_lvl':
                        for i in coords_2_lvl_copy:
                            screen.blit(tile_image['coins'], i)
                    elif mapa == 'Map_2_lvl':
                        for i in coords_3_lvl_copy:
                            screen.blit(tile_image['coins'], i)
            pygame.display.flip()
        pygame.quit()
    except FileNotFoundError:
        print('Скоро!')
