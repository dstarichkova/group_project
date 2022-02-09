import pygame
import pygame_gui

import core


# init
import parse_requests

pygame.init()
pygame.font.init()
size = width, height = 650, 450
screen = pygame.display.set_mode(size)
running = True
screen.fill('white')


# UI
main_ui_manager = core.Manager((width, height), 'data/styles.json')


# Groups
map_sprites = pygame.sprite.Group()
main_sprites = pygame.sprite.Group()


# Sprites
def init_main_window():
    update_map()

    def search_func(self, event):
        print(search_field.get_text())
        # тут будет функция поиска

    def change_mode(mode):
        parse_requests.MAP = mode
        update_map()

    search_field = pygame_gui.elements.UITextEntryLine(pygame.Rect((10, 10), (230, 30)), main_ui_manager)

    core.Button(pygame.Rect((240, 10), (80, 30)), manager=main_ui_manager, text='искать', on_click=search_func)

    core.Button(pygame.Rect((340, 10), (80, 30)), manager=main_ui_manager, text='карта', on_click=lambda *args: change_mode('map'))
    core.Button(pygame.Rect((440, 10), (80, 30)), manager=main_ui_manager, text='спутник', on_click=lambda *args: change_mode('sat'))
    core.Button(pygame.Rect((540, 10), (80, 30)), manager=main_ui_manager, text='гибрид', on_click=lambda *args: change_mode('skl'))


def update_map():
    map_sprites.empty()
    if parse_requests.MAP == 'skl':
        parse_requests.MAP = 'sat'
        parse_requests.update_image()
        core.ImageSprite(map_sprites, 'map.png', 0, 0, 650, 450)
        parse_requests.MAP = 'skl'
    parse_requests.update_image()
    core.ImageSprite(map_sprites, 'map.png', 0, 0, 650, 450)


# MAIN WINDOW CREATING
def main_window_process_events(self, event):
    if event.type == pygame.KEYDOWN:
        keys = [i for i, e in enumerate(pygame.key.get_pressed()) if e and i in [75] + list(range(78, 83))]
        if keys:
            if 75 in keys and parse_requests.SPN >= 0:
                parse_requests.SPN /= 2
            elif 78 in keys and parse_requests.SPN < 50:
                parse_requests.SPN *= 2
            else:
                move = parse_requests.SPN
                if 82 in keys and parse_requests.COORDS[1] + move < 100:
                    parse_requests.COORDS[1] += move
                if 81 in keys and parse_requests.COORDS[1] - move > -100:
                    parse_requests.COORDS[1] -= move
                if 80 in keys:
                    parse_requests.COORDS[0] -= move
                if 79 in keys:
                    parse_requests.COORDS[0] += move
            update_map()

main_window = core.Window(
    init_func=init_main_window,
    process_events_func=main_window_process_events,
    auto_text_renders=[],
    groups=[map_sprites, main_sprites],
    ui=main_ui_manager,
)


# START WINDOW
start_ui_manager = core.Manager((width, height), 'data/styles.json')
start_sprites = pygame.sprite.Group()
text_render = core.AutoTextRender()


def init_start_window():

    def search_func(self, event):
        print(search_field.get_text())
        # тут будет функция поиска

    search_field = pygame_gui.elements.UITextEntryLine(pygame.Rect((165, 210), (230, 30)), start_ui_manager)

    core.Button(pygame.Rect((415, 210), (80, 30)), manager=start_ui_manager, text='искать', on_click=search_func)
    core.Button(pygame.Rect((275, 270), (100, 30)), manager=start_ui_manager, text='к карте', on_click=lambda *args: game_loop.set_window(main_window))
    text_render.add_text(screen, 270, 150, 30, 'поиск', True)


start_window = core.Window(
    init_func=init_start_window,
    process_events_func=lambda *args: 0,
    auto_text_renders=[text_render],
    groups=[start_sprites],
    ui=start_ui_manager,
)


# GAME LOOP
game_loop = core.GameLoop(screen)
game_loop.set_window(start_window)


game_loop.loop()