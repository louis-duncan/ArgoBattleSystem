import random

from assets import *
from control_objects import *

import pygame
import easygui

pygame.init()


class Game:
    def __init__(self, grid_width, grid_height, board_pos, cell_size):
        self._tool_tip = ToolTip()
        self._ships = []
        self._objects = []
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._board_pos = board_pos
        self._cell_size = cell_size
        self._round = 1
        self._font = pygame.font.Font(pygame.font.match_font("arial"), 30, bold=1)
        self._history = []
        self._control_objects = []
        self._selected_ship = 0
        self._coord_pos = (self._board_pos[0], self._board_pos[1] + (self._grid_height * self._cell_size) + 5)

    def get_objects_in_space(self, grid_ref=None, x=None, y=None):
        if grid_ref is not None:
            x, y = grid_to_coord(grid_ref)
        else:
            pass
        found_ships = []
        found_objects = []
        for s in self._ships:
            if s.get_x() == x and s.get_y() == y:
                found_ships.append(s)
        for o in self._objects:
            if o.get_x() == x and o.get_y() == y:
                found_objects.append(o)
        return found_ships, found_objects

    def add_ship(self, location):
        name = easygui.enterbox("Enter Ship Name:", "New Ship", "Ship " + str(len(self._ships) + 1))
        if name is None:
            return
        colour = easygui.buttonbox("Choose ship colour:", "New Ship", [], images=COLOUR_SQUARE_PATHS)
        if colour is None:
            return None
        direction = easygui.buttonbox("Choose ship colour:", "New Ship", [], images=DIRECTION_SQUARE_PATHS)
        if direction is None:
            return None
        if "random" in direction:
            direction = random.randint(0, 7)
        else:
            direction = DIRECTION_SQUARE_PATHS_IN_ORDER.index(direction)
        new_ship = Ship(name, direction, location, COLOURS[COLOUR_SQUARE_PATHS.index(colour)])
        self._ships.append(new_ship)
        return self._ships.index(new_ship)

    def add_object(self, new_object):
        self._objects.append(new_object)
        return self._objects.index(new_object)

    def remove_ship(self, index):
        p = self._ships.pop(index)

    def remove_object(self, index):
        p = self._objects.pop(index)

    def move_ship(self, index):
        if self._selected_ship >= len(self._ships):
            return None
        trail_index = self.add_object(TravelTrail("Created By {}".format(self._ships[index].get_description()),
                                                  self._ships[index].get_direction(),
                                                  self._ships[index].get_pos(),
                                                  self._ships[index].get_colour()))
        self._ships[index].move()
        self._add_history(("create", trail_index))
        self._add_history(("move", index))

    def turn_ship(self, index, direction, history=True):
        if self._selected_ship >= len(self._ships):
            return None
        self._ships[index].turn(direction)
        if history:
            self._history.append(("turn", index, direction))

    def _purge_objects(self):
        i = 0
        while i < len(self._objects):
            if self._objects[i].get_ttl() == 0:
                self._objects.remove(self._objects[i])
            else:
                i += 1

    def _decrement_ttls(self):
        for o in self._objects:
            o.decrement_ttl()

    def get_round(self):
        return self._round

    def tick(self):
        if len(self._history) == 0:
            return
        self._decrement_ttls()
        self._purge_objects()
        self._round += 1
        self._history = []

    def draw_board(self, screen):
        for y in range(self._grid_height + 1):
            start_pos = [self._board_pos[0], self._board_pos[1] + (self._cell_size * y) - 1]
            end_pos = [start_pos[0] + (self._cell_size * self._grid_width), start_pos[1]]
            pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 2)

        for x in range(self._grid_width + 1):
            start_pos = [self._board_pos[0] + (self._cell_size * x) - 1, self._board_pos[1]]
            end_pos = [start_pos[0], start_pos[1] + (self._cell_size * self._grid_height)]
            pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 2)

        for x in range(self._grid_width):
            char = self._font.render(str(x + 1), 1, (0, 0, 0,), (255, 255, 255))
            width, height = char.get_size()
            x = self._board_pos[0] + (self._cell_size * x) + (self._cell_size / 2) - (width / 2)
            y = self._board_pos[1] - (self._cell_size / 2) - (height / 2)
            screen.blit(char, (x, y))

        for y in range(self._grid_height):
            char = self._font.render(chr(y + 65), 1, (0, 0, 0), (255, 255, 255))
            width, height = char.get_size()
            x = self._board_pos[0] - (self._cell_size / 2) - (width / 2)
            y = self._board_pos[1] + (y * self._cell_size) + (self._cell_size / 2) - (height / 2)
            screen.blit(char, (x, y))

        mouse_over = self.coord_at_pos(pygame.mouse.get_pos())
        if mouse_over is not None:
            coord_text = "({}{})".format(chr(mouse_over[1] + 65), mouse_over[0] + 1)
        else:
            coord_text = "(---)"
        coord_text_img = self._font.render(coord_text, 1, (0, 0, 0), (255, 255, 255))
        screen.blit(coord_text_img, self._coord_pos)

        round_text_img = self._font.render("Round: {}".format(self._round), 1, (0, 0, 0), (255, 255, 255))
        screen.blit(round_text_img,
                    ((self._coord_pos[0] + (self._grid_width * self._cell_size)) - round_text_img.get_size()[0],
                     self._coord_pos[1]))

    def draw_assets(self, screen):
        for o in self._objects + self._ships:
            x, y = o.get_pos()
            image_size = self._cell_size * .9
            image = o.get_sprite(round(image_size))
            r_image_size = image.get_size()
            scaled_pos = (
                round((x * self._cell_size) + self._board_pos[0]) + ((self._cell_size / 2) - (image_size / 2)),
                round((y * self._cell_size) + self._board_pos[1]) + ((self._cell_size / 2) - (image_size / 2)))
            crop_pos = ((r_image_size[0] / 2) - (image_size / 2),
                        (r_image_size[1] / 2) - (image_size / 2))
            screen.blit(image, scaled_pos, (crop_pos[0], crop_pos[1], image_size, image_size))

    def add_control_object(self, control_obj):
        self._control_objects.append(control_obj)
        return self._control_objects.index(control_obj)

    def draw_control_objects(self, screen):
        for o in self._control_objects:
            o.draw(screen)

    def _add_history(self, history_item):
        self._history.append(history_item)

    def undo(self):
        if len(self._history) == 0:
            return
        history_item = self._history.pop()
        if history_item[0] == "move":
            self._ships[history_item[1]].move(-1)
            self.undo()
        elif history_item[0] == "create":
            self.remove_object(history_item[1])
        elif history_item[0] == "turn":
            if history_item[2] == "left":
                self.turn_ship(history_item[1], "right", False)
            elif history_item[2] == "right":
                self.turn_ship(history_item[1], "left", False)
            else:
                pass

    def draw(self, screen):
        self.update_co_enables()
        self.draw_assets(screen)
        self.draw_control_objects(screen)
        self.draw_board(screen)
        self.draw_tool_tip(screen)

    def update_co_enables(self):
        state = len(self._ships) > 0
        for co in self._control_objects:
            co.set_enabled(state)

    def get_clicked(self, pos):
        i = len(self._control_objects) - 1
        found = False
        while i >= 0 and found is False:
            if self._control_objects[i].pos_in_bound(pos):
                found = True
            else:
                i -= 1
        if found:
            return i
        else:
            return None

    def set_clicked(self, index, state=True):
        self._control_objects[index].set_state(state)

    def clear_clicks(self):
        for co in self._control_objects:
            co.set_state(False)

    def get_co_by_key(self, key):
        for co in self._control_objects:
            if co.get_bind_key() == key:
                return self._control_objects.index(co)

    def enact_bind(self, bind_text):
        if bind_text == "next_turn":
            return self.tick()
        elif bind_text == "left":
            self.turn_ship(self._selected_ship, "left")
        elif bind_text == "right":
            self.turn_ship(self._selected_ship, "right")
        elif bind_text == "up":
            self.move_ship(self._selected_ship)
        elif bind_text == "add_ship":
            self.add_ship()
        else:
            return False

    def get_co_bind_text(self, co_index):
        return self._control_objects[co_index].get_bind_text()

    def set_ship_select(self, ship_index):
        if ship_index < len(self._ships):
            self._selected_ship = ship_index
        else:
            pass

    def get_ship_select(self):
        return self._selected_ship

    def get_co_state(self, co_index):
        return self._control_objects[co_index].get_state()

    def ping_co(self, co_index):
        self._control_objects[co_index].ping()

    def coord_at_pos(self, pos):
        x, y = (((pos[0] - self._board_pos[0]) // self._cell_size),
                ((pos[1] - self._board_pos[1]) // self._cell_size))
        if 0 <= x < self._grid_width and 0 <= y < self._grid_height:
            return x, y
        else:
            return None

    def draw_tool_tip(self, screen):
        if self._tool_tip is None or self.coord_at_pos(pygame.mouse.get_pos()) is None:
            return
        pos = pygame.mouse.get_pos()
        ships, objects = self.get_objects_in_space(x=self.coord_at_pos(pos)[0], y=self.coord_at_pos(pos)[1])
        self._tool_tip.draw(screen, ships + objects)


def enact_bind(bind_text):
    return False


def is_adjacent(point1, point2):
    if type(point1) is str:
        x1, y1 = grid_to_coord(point1)
        x2, y2 = grid_to_coord(point2)
    else:
        x1, y1 = point1
        x2, y2 = point2
    return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1


def grid_to_coord(grid_ref):
    return int(grid_ref[1:]) - 1, ord(grid_ref[0].upper()) - 65


def main():
    board_height = 20
    board_width = 20
    cell_size = 45

    game = Game(board_width, board_height, (cell_size, cell_size), cell_size)

    controls_area = ((board_width + 1) * cell_size + 5,  # x
                     5,  # y
                     600,  # width
                     ((board_height + 1) * cell_size) + 35)  # height

    screen_size = (((board_width + 1) * cell_size) + controls_area[2] + 10,
                   max([((board_height + 1) * cell_size) + 5, controls_area[3] + 10]))

    # Create Game Control Objects
    button_height = 70

    next_turn_button = Button((controls_area[0], controls_area[1] + controls_area[3] - button_height),
                              controls_area[2],
                              button_height,
                              (255, 0, 0),
                              "next_turn",
                              pygame.K_SPACE,
                              "Next Turn",
                              (255, 255, 255))
    left_button = Button((controls_area[0],
                          next_turn_button.get_y() - (button_height + 5)),
                         round((next_turn_button.get_width() - 10) / 3),
                         button_height,
                         (150, 150, 150),
                         "left",
                         pygame.K_LEFT,
                         "◄",
                         (0, 0, 0)
                         )
    up_button = Button((controls_area[0] + left_button.get_width() + 5,
                        next_turn_button.get_y() - (button_height + 5)),
                       left_button.get_width(),
                       button_height,
                       (150, 150, 150),
                       "up",
                       pygame.K_UP,
                       " ▲",
                       (0, 0, 0)
                       )
    right_button = Button((controls_area[0] + (left_button.get_width() + 5) * 2,
                           next_turn_button.get_y() - (button_height + 5)),
                          left_button.get_width(),
                          button_height,
                          (150, 150, 150),
                          "right",
                          pygame.K_RIGHT,
                          "►",
                          (0, 0, 0)
                          )

    game.add_control_object(next_turn_button)
    game.add_control_object(left_button)
    game.add_control_object(up_button)
    game.add_control_object(right_button)
    #game.add_control_object(add_ship_button)

    clock = pygame.time.Clock()

    ctrl_down = False

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode(screen_size)  # , pygame.FULLSCREEN)
    pygame.display.set_caption('Argo Battle')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                co_index = game.get_clicked(pos)
                if co_index is not None:
                    game.set_clicked(co_index)
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                co_index = game.get_clicked(pos)
                game.clear_clicks()
                if co_index is not None:
                    game.ping_co(co_index)
                    game.enact_bind(game.get_co_bind_text(co_index))
                elif game.coord_at_pos(pos) is not None:
                    game.add_ship(game.coord_at_pos(pos))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    ctrl_down = True
                elif event.key == pygame.K_z:
                    if ctrl_down:
                        game.undo()
                else:
                    co_index = game.get_co_by_key(event.key)
                    if co_index is None:
                        pass
                    else:
                        game.set_clicked(co_index)
                        game.ping_co(co_index)
                        bind_text = game.get_co_bind_text(co_index)
                        if bind_text is not None:
                            game.enact_bind(game.get_co_bind_text(co_index))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    ctrl_down = False
                else:
                    co_index = game.get_co_by_key(event.key)
                    if co_index is None:
                        pass
                    else:
                        game.set_clicked(co_index, False)

        screen.blit(background, (0, 0))
        game.draw(screen)
        pygame.display.flip()

        clock.tick(30)


main()
