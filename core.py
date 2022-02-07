import datetime
import os
import random
import sys
import pygame
import pygame_gui


# images
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# fonts
def get_font(size, bold=False):
    return pygame.font.Font(f'data/fonts/{"bold-" if bold else ""}font.ttf', size)


def create_text(screen, x, y, size, text='', bold=False):
    text = get_font(size, bold).render(str(text), False, (0, 0, 0))
    screen.blit(text, (x, y))


# mixins
class OnClickMixin:

    def on_click(self, event, *args):
        if 'on_click_func' in self.__dict__:
            self.on_click_func(self, event, *args)


# classes
class EmptyClass: pass


class GameLoop:

    def __init__(self, screen):
        self.screen = screen
        self.window = None
        self.clock = pygame.time.Clock()

    def loop(self):
        running = True
        while running and self.window:
            time_delta = self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.window.process_events(event)
            self.screen.fill('white')
            self.window.draw()
            self.window.update(time_delta)
            pygame.display.flip()
        pygame.quit()

    def set_window(self, window):
        if self.window:
            self.window.clear()
        self.window = window
        self.window.init()
        self.window.clock = self.clock
        self.window.screen = self.screen


class Window:

    def __init__(self, ui=None, init_func=None, process_events_func=None, update_func=None, groups=[], auto_text_renders=[]):
        self.screen = None
        self.clock = None
        self.ui = ui
        self.process_events_func = process_events_func
        self.update_func = update_func
        self.auto_text_renders = auto_text_renders
        self.groups = groups
        if init_func:
            self.init_func = init_func

    def init(self):
        if 'init_func' in self.__dict__:
            self.init_func()


    def draw(self):
        if self.screen:
            [group.draw(self.screen) for group in self.groups]
            [text.render() for text in self.auto_text_renders]
            self.ui.draw_ui(self.screen)

    def process_events(self, event):
        if self.screen and self.process_events_func:
            self.process_events_func(self, event)
            self.ui.process_events(event)

    def update(self, time_delta):
        if self.screen:
            self.ui.update(time_delta)
            if self.update_func:
                self.update_func(self, time_delta)

    def clear(self):
        self.screen = None
        self.clock = None
        for group in self.groups:
            for sprite in group:
                sprite.kill()
        for sprite in self.ui.ui_group:
            sprite.kill()
        for text in self.auto_text_renders:
            text.clear()


class AutoTextRender:

    __init__ = lambda self: self.__setattr__('lst', list())
    add_text = lambda self, *args, **kwargs: self.lst.append(lambda: create_text(*args, **kwargs))
    add_text_stream = lambda self, *args, func, **kwargs: self.lst.append(
        lambda: create_text(*args, text=func(), **kwargs))
    render = lambda self: [func() for func in self.lst]
    clear = lambda self: self.__setattr__('lst', list())


# ui
class Manager(pygame_gui.UIManager):

    def process_events(self, event: pygame.event.Event):
        super().process_events(event)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for obj in self.ui_group:
                    if event.ui_element == obj:
                        obj.on_click(event)


class Button(pygame_gui.elements.UIButton, OnClickMixin):

    def __init__(self, *args, **kwargs):
        self.default_name = kwargs['text']
        self.on_click_func = kwargs['on_click']
        del kwargs['on_click']
        super().__init__(*args, **kwargs)

    def reset_text(self):
        self.set_text(self.default_name)


# sprites
class ImageSprite(pygame.sprite.Sprite):

    def __init__(self, group, name, x, y, w, h, colorkey=None):
        super().__init__([group])
        self.image = pygame.transform.scale(load_image(name, colorkey), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y