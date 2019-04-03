import pygame
import time

FONT_SIZE = 30
FONT = pygame.font.Font(pygame.font.match_font("arial"), FONT_SIZE)


class Box:
    def __init__(self, pos, width, height, colour, bind_text="", bind_key=None):
        self._pos = list(pos)
        self._width = width
        self._height = height
        self._colour = colour
        self._last_ping_time = 0
        self._bind_text = bind_text
        self._bind_key = bind_key
        self._enabled = True

    def get_x(self):
        return self._pos[0]

    def set_x(self, x):
        self._pos[0] = x

    def get_y(self):
        return self._pos[1]

    def set_y(self, y):
        self._pos[1] = y

    def get_pos(self):
        return self._pos

    def set_pos(self, pos):
        self._pos = pos

    def get_width(self):
        return self._width

    def set_width(self, width):
        self._width = width

    def get_height(self):
        return self._height

    def set_height(self, height):
        self._height = height

    def get_size(self):
        return self._width, self._height

    def set_size(self, size):
        self._width, self._height = size

    def get_rect(self):
        return self._pos[0], self._pos[1], self._width, self._height

    def get_ping_rect(self):
        return self._pos[0] - 3, self._pos[1] - 3, self._width + 6, self._height + 6

    def draw(self, screen, draw_colour=None):
        if draw_colour is None:
            draw_colour = self._colour

        if not self._enabled:
            draw_colour = [c + ((255 - c) / 2) for c in draw_colour]

        if time.time() - self._last_ping_time < 0.1:
            pygame.draw.rect(screen, [int(round(i / 2)) for i in draw_colour], self.get_ping_rect())

        pygame.draw.rect(screen, draw_colour, self.get_rect())

    def pos_in_bound(self, pos):
        result = (self._pos[0] < pos[0] < self._pos[0] + self._width) and (self._pos[1] < pos[1] < self._pos[1] + self._height)
        return result

    def ping(self):
        if self._enabled:
            self._last_ping_time = time.time()

    def get_bind_text(self):
        if self._enabled:
            return self._bind_text

    def get_bind_key(self):
        if self._enabled:
            return self._bind_key

    def set_enabled(self, state):
        self._enabled = state


class Button(Box):
    def __init__(self, pos, width, height, colour, bind_text, bind_key=None, text="", text_col=(100, 100, 100)):
        super().__init__(pos, width, height, colour, bind_text, bind_key)
        self._text_colour = text_col
        self._text = text
        self._is_clicked = False

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text

    def get_text_col(self):
        return self._text_colour

    def set_text_col(self, col):
        self._text_colour = col

    def set_state(self, state):
        assert state in (True, False)
        self._is_clicked = state

    def get_state(self):
        return self._is_clicked

    def draw(self, screen, draw_colour=None):
        if draw_colour is None:
            if self._is_clicked:
                draw_colour = [i / 2 for i in self._colour]
            else:
                draw_colour = self._colour
        super().draw(screen, draw_colour)
        text_r = FONT.render(self._text, 1, self._text_colour)
        text_size = text_r.get_size()

        text_pos = (self._pos[0] + (self._width / 2) - (text_size[0] / 2),
                    self._pos[1] + ((self._height / 2) - (text_size[1] / 2)))

        screen.blit(text_r, text_pos)


class ToolTip:
    def __init__(self):
        self._pos = [0, 0]
        self._sprites = []

    def set_pos(self, pos):
        self._pos = pos

    def draw(self, screen, sprites=None):
        rect = (self._pos[0], self._pos[1], ) # Todo



class ShipSelector(Box):
    def __init__(self, pos, width, height, colour, bind_text, bind_key, ship_index):
        super().__init__(pos, width, height, colour, bind_text, bind_key)
        self._ship_index = ship_index
        self._history = []
        self._active = False

    def add_history(self, text):
        self._history.append(text)

    def clear_history(self):
        self._history = []

    def get_ship_index(self):
        return self._ship_index

    def set_state(self, state):
        self._active = state

    def get_state(self):
        return self._active

    def draw(self, screen, draw_colour=None):
        super().draw(screen, draw_colour)
