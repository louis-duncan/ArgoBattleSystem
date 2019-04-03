import pygame
import time

FONT_SIZE = 30
FONT = pygame.font.Font(pygame.font.match_font("arial"), FONT_SIZE)

NUMBER_KEYS = (pygame.K_1,
               pygame.K_2,
               pygame.K_3,
               pygame.K_4,
               pygame.K_5,
               pygame.K_6
               )


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

    def get_relative_pos(self, pos):
        return (self._pos[0] + pos[0]), (self._pos[1] + pos[1])

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
        result = (self._pos[0] < pos[0] < self._pos[0] + self._width) and (
                    self._pos[1] < pos[1] < self._pos[1] + self._height)
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
        self._sprite_size = 50
        self._boarder_thickness = 2
        self._margin = 5

    def draw(self, screen, objects=None):
        pos = pygame.mouse.get_pos()
        if objects is None or len(objects) == 0:
            return

        width = (self._sprite_size * len(objects)) + (2 * self._margin)
        height = self._sprite_size + (2 * self._margin)
        rect = (pos[0], pos[1], width, height)
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         rect)
        for i, o in enumerate(objects):
            s = o.get_sprite(self._sprite_size)
            s_size = s.get_size()
            range_start_pos = ((s_size[0] / 2) - (self._sprite_size / 2),
                               (s_size[1] / 2) - (self._sprite_size / 2))
            screen.blit(s,
                        (pos[0] + self._margin + (i * self._sprite_size), pos[1] + self._margin),
                        (range_start_pos[0], range_start_pos[1],
                         self._sprite_size, self._sprite_size))
        pygame.draw.rect(screen,
                         (0, 0, 0),
                         rect,
                         self._boarder_thickness)


class ShipSelector(Box):
    def __init__(self, pos, width, height, colour, bind_text, bind_key, ship):
        super().__init__(pos, width, height, colour, bind_text, bind_key)
        self._ship = ship
        self._history = ["FW", "FW", "FW", "FW", "FW", "FW", "FW", "FW", "FW", "FW", "FW", "FW", "FW", "FW", "FW", "FW",  "FW", "FW", "FW", "FW", "FW", "FW", "FW", "FW", "FW", "FW", "FW", "FW",]
        self._active = False
        self._margin = 5
        self._icon_size = 50
        self._name_font = pygame.font.Font(pygame.font.match_font("arial"), 30, bold=1)
        self._history_font = pygame.font.Font(pygame.font.match_font("arial"), 20)

    def add_history(self, text):
        self._history.append(text)

    def pop_history(self, index=-1):
        if index == -1:
            index = len(self._history)
        return self._history.pop(index)

    def clear_history(self):
        self._history = []

    def get_ship(self):
        return self._ship

    def set_selected(self, state):
        self._active = bool(state)

    def get_selected(self):
        return self._active

    def draw(self, screen, draw_colour=None):
        super().draw(screen, draw_colour)
        if self._active:
            border_col = (0, 0, 0)
            border_thickness = 3
        else:
            border_col = (100, 100, 100)
            border_thickness = 1
        pygame.draw.rect(screen,
                         border_col,
                         (self._pos[0], self._pos[1], self._width, self._height),
                         border_thickness)

        icon_pos = self.get_relative_pos((self._margin, self._margin))
        r_image = self._ship.get_sprite(self._icon_size)
        r_image_size = r_image.get_size()
        icon_crop_start = ((r_image_size[0] / 2) - (self._icon_size / 2),
                           (r_image_size[1] / 2) - (self._icon_size / 2))
        screen.blit(r_image, icon_pos, (icon_crop_start[0], icon_crop_start[1], self._icon_size, self._icon_size))

        r_name = self._name_font.render(self._ship.get_description(), 1, (0, 0, 0), (255, 255, 255))
        name_pos = self.get_relative_pos((self._icon_size + (self._margin * 2), self._margin))
        screen.blit(r_name, name_pos)

        history_width = self._width - (4 * self._margin) - self._icon_size

        lines = self._flow_text(list(self._history), ", ", history_width)
        line_pos = [name_pos[0], name_pos[1] + r_name.get_size()[1]]
        for l in lines:
            r_line = self._history_font.render(l, 1, (0, 0, 0), (255, 255, 255))
            screen.blit(r_line, line_pos)
            line_pos[1] += r_line.get_size()[1] + self._margin

    def _flow_text(self, words, sep, width):
        lines = []
        if len(words) == 0:
            return lines
        new_line = words.pop(0)
        while len(words) > 0:
            next_word = words.pop(0)
            with_next = new_line + sep + next_word
            if self._history_font.size(with_next)[0] <= width:
                new_line = with_next
            else:
                lines.append(new_line)
                new_line = next_word
        if new_line != "":
            lines.append(new_line)
        return lines
