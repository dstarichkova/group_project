import pygame
import pygame_gui

import core


# init
import parse_requests

pygame.init()
pygame.font.init()
size = width, height = 650, 500
screen = pygame.display.set_mode(size)
running = True
screen.fill('white')


def search(text):
    search_coords = parse_requests.get_coords(text)
    if search_coords:
        parse_requests.COORDS = [float(i) for i in search_coords.split(',')]
        parse_requests.POINT = parse_requests.COORDS.copy()
        update_map()


# UI
main_ui_manager = core.Manager((width, height), 'data/styles.json')


# Groups
map_sprites = pygame.sprite.Group()
main_sprites = pygame.sprite.Group()
main_text_render = core.AutoTextRender()


# Sprites
def init_main_window():
    update_map()

    def change_mode(mode):
        parse_requests.MAP = mode
        update_map()

    def reset_search(*args):
        parse_requests.POINT = []
        parse_requests.OBJECT_DATA = {}
        search_field.redraw()
        update_map()

    def show_details(*args):
        if parse_requests.OBJECT_DATA:
            game_loop.set_window(details_window)

    def add_postal_code(self, *args):
        if parse_requests.ADD_POSTAL_CODE:
            self.set_text('без почтой')
            parse_requests.ADD_POSTAL_CODE = False
        else:
            self.set_text('с почтой')
            parse_requests.ADD_POSTAL_CODE = True

    def get_obj_description(*args):
        if parse_requests.OBJECT_DATA:
            address = parse_requests.OBJECT_DATA['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
            if parse_requests.OBJECT_DATA['GeoObject']['metaDataProperty']['GeocoderMetaData']['kind'] == 'house' and parse_requests.ADD_POSTAL_CODE:
                address += f" {parse_requests.OBJECT_DATA['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']}"
            return address
        else:
            return 'объект не выбран'

    search_field = pygame_gui.elements.UITextEntryLine(pygame.Rect((10, 10), (130, 30)), main_ui_manager)

    core.Button(pygame.Rect((150, 10), (80, 30)), manager=main_ui_manager, text='искать', on_click=lambda *args: search(search_field.get_text()))
    core.Button(pygame.Rect((240, 10), (80, 30)), manager=main_ui_manager, text='сброс', on_click=reset_search)

    core.Button(pygame.Rect((340, 10), (80, 30)), manager=main_ui_manager, text='карта', on_click=lambda *args: change_mode('map'))
    core.Button(pygame.Rect((440, 10), (80, 30)), manager=main_ui_manager, text='спутник', on_click=lambda *args: change_mode('sat'))
    core.Button(pygame.Rect((540, 10), (80, 30)), manager=main_ui_manager, text='гибрид', on_click=lambda *args: change_mode('skl'))

    core.Button(pygame.Rect((560, 460), (80, 30)), manager=main_ui_manager, text='больше', on_click=show_details)
    core.Button(pygame.Rect((450, 460), (100, 30)), manager=main_ui_manager, text='без почты', on_click=add_postal_code)

    main_text_render.add_text_stream(screen, 10, 467, 15, func=get_obj_description)


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
    auto_text_renders=[main_text_render],
    groups=[map_sprites, main_sprites],
    ui=main_ui_manager,
)


# START WINDOW
start_ui_manager = core.Manager((width, height), 'data/styles.json')
start_sprites = pygame.sprite.Group()
text_render = core.AutoTextRender()


def init_start_window():

    def search_func(self, event):
        game_loop.set_window(main_window)
        search(search_field.get_text())

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


# DETAILS WINDOW
details_ui_manager = core.Manager((width, height), 'data/styles.json')
details_sprites = pygame.sprite.Group()
details_text_render = core.AutoTextRender()


def init_details_window():
    core.Button(pygame.Rect((10, 10), (80, 30)), manager=details_ui_manager, text='назад', on_click=lambda *args: game_loop.set_window(main_window))
    details_text_render.add_text(screen, 100, 15, 15, 'подробнее об объекте', True)

    if parse_requests.OBJECT_DATA:
        details_text_render.add_text(screen, 10, 55, 15, f"адресс: {parse_requests.OBJECT_DATA['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']}")
        kind = parse_requests.OBJECT_DATA['GeoObject']['metaDataProperty']['GeocoderMetaData']['kind']
        details_text_render.add_text(screen, 10, 80, 15, f"вид: {kind}")
        if kind == 'house':
            details_text_render.add_text(screen, 10, 105, 15, f"почтовый код: {parse_requests.OBJECT_DATA['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']}")

details_window = core.Window(
    init_func=init_details_window,
    process_events_func=lambda *args: 0,
    auto_text_renders=[details_text_render],
    groups=[details_sprites],
    ui=details_ui_manager,
)


# GAME LOOP
game_loop = core.GameLoop(screen)
game_loop.set_window(start_window)


game_loop.loop()