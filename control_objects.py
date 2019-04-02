import pygame

FONT_SIZE = 30
FONT = pygame.font.Font(pygame.font.match_font("calibri"), FONT_SIZE)

class ShipInfo:
    def __init__(self, game, ship_index):
        pass


class Box:
    def __init__(self, pos, width, height, colour):
        self._pos = list(pos)
        self._width = width
        self._height = height
        self._colour = colour

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

    def draw(self, screen, draw_colour=None):
        if draw_colour is None:
            draw_colour = self._colour
        pygame.draw.rect(screen, draw_colour, self.get_rect())

    def pos_in_bound(self, pos):
        result = (self._pos[0] < pos[0] < self._pos[0] + self._width) and (self._pos[1] < pos[1] < self._pos[1] + self._height)
        print(pos, result)
        return result


class Button(Box):
    def __init__(self, pos, width, height, colour, text, text_col, bind_text, bind_key=None):
        super().__init__(pos, width, height, colour)
        self._text_colour = text_col
        self._text = text
        self._is_clicked = False
        self._bind_text = bind_text
        self._bind_key = bind_key

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text

    def get_text_col(self):
        return self._text_colour

    def set_text_col(self, col):
        self._text_colour = col

    def set_clicked(self, state):
        assert state in (True, False)
        self._is_clicked = state

    def draw(self, screen, draw_colour=None):
        if draw_colour is None:
            if self._is_clicked:
                draw_colour = [i / 2 for i in self._colour]
            else:
                draw_colour = self._colour
        super().draw(screen, draw_colour)
        text_r = FONT.render(self._text, 1, self._text_colour, draw_colour)
        text_size = text_r.get_size()

        text_pos = (self._pos[0] + (self._width / 2) - (text_size[0] / 2),
                    self._pos[1] + ((self._height / 2) - (text_size[1] / 2)))

        screen.blit(text_r, text_pos)

    def get_bind_text(self):
        return self._bind_text

    def get_bind_key(self):
        return self._bind_key