from assets import *
from control_objects import *
from coms import *

import pygame
import pygame.gfxdraw
import easygui
import random


class Game:
    def __init__(self, grid_width, grid_height, board_pos, cell_size):
        self._tool_tip = ToolTip()
        self._ships = []
        self._objects = []
        self._ping_boxes = []
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._board_pos = board_pos
        self._cell_size = cell_size
        self._round = 1
        self._font = pygame.font.Font(pygame.font.match_font("arial"), 30, bold=1)
        self._history = []
        self._control_objects = []
        self._selected_ship = -1
        self._coord_pos = (self._board_pos[0], self._board_pos[1] + (self._grid_height * self._cell_size) + 5)
        self._pop_up = None
        self._controls_area = (0, 0, 100, 100)
        self._ship_selectors = []
        self._default_button_height = 60
        self._actions = {"add_ship": False,
                         "add_ping": False,
                         }
        self._messages = {"add_ship": "Click a cell to add ship...",
                          "add_ping": "Click and drag to create a ping for the current ship..."}
        self._click_started_pos = None
        self._sender = Sender()

    def get_objects_in_space(self, x=None, y=None):
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
        if len(self._ships) == 6:
            return None

        if not self._actions["add_ship"]:
            return

        name = easygui.enterbox("Adding Ship at {}\n\nEnter Ship Name:".format(coord_to_grid(location)),
                                "New Ship", "Ship " + str(len(self._ships) + 1))
        if name is None:
            return
        colour = easygui.buttonbox("Choose ship colour:", "New Ship", [], images=COLOUR_SQUARE_PATHS)
        if colour is None:
            return None
        direction = easygui.buttonbox("Choose ship direction:", "New Ship", [], images=DIRECTION_SQUARE_PATHS)
        if direction is None:
            return None
        if "random" in direction:
            direction = random.randint(0, 7)
        else:
            direction = DIRECTION_SQUARE_PATHS_IN_ORDER.index(direction)
        new_ship = Ship(name, direction, location, COLOURS[COLOUR_SQUARE_PATHS.index(colour)])

        self._ships.append(new_ship)
        self._add_ship_selector(self._ships.index(new_ship))
        self._selected_ship = len(self._ships) - 1

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
        self._add_history(("create_object", trail_index))
        self._add_history(("move", index))
        self._ship_selectors[index].add_history("Forward")

    def turn_ship(self, index, direction, history=True):
        if self._selected_ship >= len(self._ships):
            return None
        self._ships[index].turn(direction)
        if history:
            self._history.append(("turn", index, direction))
            self._ship_selectors[index].add_history(direction.capitalize())

    def _purge_objects(self):
        i = 0
        while i < len(self._objects):
            if self._objects[i].get_ttl() == 0:
                self._objects.remove(self._objects[i])
            else:
                i += 1
        i = 0
        while i < len(self._ping_boxes):
            if self._ping_boxes[i].get_ttl() == 0:
                self._ping_boxes.remove(self._ping_boxes[i])
            else:
                i += 1

    def _decrement_ttls(self):
        for o in self._objects:
            o.decrement_ttl()
        for p in self._ping_boxes:
            p.decrement_ttl()

    def get_round(self):
        return self._round

    def tick(self):
        if len(self._history) == 0:
            return
        self._decrement_ttls()
        self._purge_objects()
        self._round += 1
        self._history = []
        for s in self._ship_selectors:
            s.clear_history()
            self._sender.send(s.get_ship_desc(), "next_round")

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

        r_message = self._font.render(self.get_current_message(), 1, (0, 0, 0), (255, 255, 255))
        message_pos = [
            self._coord_pos[0] + (((self._grid_width * self._cell_size) / 2) - (r_message.get_size()[0] / 2)),
            self._coord_pos[1]]
        screen.blit(r_message, message_pos)

    def get_current_message(self):
        msg = ""
        for a in self._actions:
            if self._actions[a]:
                msg = self._messages[a]
        return msg

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

    def draw_ship_selectors(self, screen):
        margin = 5
        rolling_y = self._controls_area[1] + (self._default_button_height * .75) + margin
        for ss in self._ship_selectors:
            ss.set_pos((self._controls_area[0], rolling_y))
            ss.draw(screen)
            rolling_y += ss.get_height() + margin

    def _add_history(self, history_item):
        self._history.append(history_item)

    def undo(self):
        if len(self._history) == 0:
            return
        history_item = self._history.pop()
        if history_item[0] == "move":
            self._ships[history_item[1]].move(-1)
            self.undo()
            self._ship_selectors[history_item[1]].pop_history()
        elif history_item[0] == "create_object":
            self.remove_object(history_item[1])
        elif history_item[0] == "create_ping":
            ping_ship = self._ping_boxes[-1].get_ship_desc()
            self.remove_ping(history_item[1])
            self._sender.send(ping_ship, "clear")
        elif history_item[0] == "turn":
            if history_item[2] == "left":
                self.turn_ship(history_item[1], "right", False)
                self._ship_selectors[history_item[1]].pop_history()
            elif history_item[2] == "right":
                self.turn_ship(history_item[1], "left", False)
                self._ship_selectors[history_item[1]].pop_history()
            else:
                pass

    def draw(self, screen):
        self.update_cos()
        self.update_sss()
        self.draw_assets(screen)
        self.draw_control_objects(screen)
        self.draw_ship_selectors(screen)
        self.draw_board(screen)
        self.draw_pings(screen)
        self.draw_click_drag(screen)
        self.draw_tool_tip(screen)

    def update_cos(self):
        state = len(self._ships) > 0
        for co in self._control_objects:
            if co.get_always_active():
                pass
            else:
                co.set_enabled(state)

    def update_sss(self):
        for i in range(len(self._ship_selectors)):
            self._ship_selectors[i].set_selected(False)
        if len(self._ships) > 0:
            self._ship_selectors[self._selected_ship].set_selected(True)

    def get_clicked_co(self, pos):
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
        if bind_text is None:
            return
        elif bind_text == "next_turn":
            return self.tick()
        elif bind_text == "left":
            self.turn_ship(self._selected_ship, "left")
        elif bind_text == "right":
            self.turn_ship(self._selected_ship, "right")
        elif bind_text == "up":
            self.move_ship(self._selected_ship)
        elif bind_text.startswith("arm_"):
            try:
                self.arm_action(bind_text[4:])
            except KeyError:
                print("Invalid Bind:", bind_text[4:])
                return False
        elif bind_text.startswith("ship_"):
            self._selected_ship = int(bind_text[5:])
            self.update_cos()
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
        return self._control_objects[co_index].get_selected()

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

    def set_controls_area(self, rect):
        self._controls_area = rect

    def get_controls_area(self):
        return self._controls_area

    def _add_ship_selector(self, ship_index):
        self._ship_selectors.append(ShipSelector((0, 0),
                                                 self._controls_area[2],
                                                 100,
                                                 (255, 255, 255),
                                                 bind_text="ship_{}".format(ship_index),
                                                 bind_key=NUMBER_KEYS[ship_index],
                                                 ship=self._ships[ship_index]))

    def get_clicked_ss(self, pos):
        i = len(self._ship_selectors) - 1
        found = False
        while i >= 0 and found is False:
            if self._ship_selectors[i].pos_in_bound(pos):
                found = True
            else:
                i -= 1
        if found:
            return i
        else:
            return None

    def ping_ss(self, ss_index):
        self._ship_selectors[ss_index].ping()

    def get_ss_bind_text(self, ss_index):
        return self._ship_selectors[ss_index].get_bind_text()

    def get_ss_by_key(self, key):
        for ss in self._ship_selectors:
            if ss.get_bind_key() == key:
                return self._ship_selectors.index(ss)

    def arm_action(self, action):
        was_active = self._actions[action]
        if True in self._actions.values():
            self.disarm_actions()
        if was_active:
            return
        self._actions[action] = True

    def disarm_actions(self):
        for a in self._actions:
            self._actions[a] = False

    def submit_mb_up(self, pos):
        if pos is None:
            pass
        else:
            for a in self._actions:
                if self._actions[a]:
                    getattr(Game, a)(self, pos)
                    self._actions[a] = False

        self._click_started_pos = None

    def submit_mb_down(self, pos):
        self._click_started_pos = pos

    def get_default_button_height(self):
        return self._default_button_height

    def add_ping(self, pos, detailed=True):
        col = GREY
        if self._ships[self._selected_ship].get_colour() == "red":
            col = RED
        elif self._ships[self._selected_ship].get_colour() == "green":
            col = GREEN
        elif self._ships[self._selected_ship].get_colour() == "blue":
            col = BLUE
        elif self._ships[self._selected_ship].get_colour() == "yellow":
            col = YELLOW
        elif self._ships[self._selected_ship].get_colour() == "black":
            col = BLACK
        else:
            pass
        new_pb = PingBox(self._click_started_pos, pos, col, self._ships[self._selected_ship].get_description())
        self._ping_boxes.append(new_pb)
        self._sender.send(self._ships[self._selected_ship].get_description(),
                          self.format_for_ping(self._click_started_pos, pos, detailed)
                          )
        self._add_history(("create_ping", self._ping_boxes.index(new_pb)))

    def draw_click_drag(self, screen):
        if self._click_started_pos is not None and self._actions["add_ping"]:
            start_coord = self._click_started_pos
            end_coord = self.coord_at_pos(pygame.mouse.get_pos())
            if end_coord is None:
                return

            col = GREY
            if self._ships[self._selected_ship].get_colour() == "red":
                col = RED
            elif self._ships[self._selected_ship].get_colour() == "green":
                col = GREEN
            elif self._ships[self._selected_ship].get_colour() == "blue":
                col = BLUE
            elif self._ships[self._selected_ship].get_colour() == "yellow":
                col = YELLOW
            elif self._ships[self._selected_ship].get_colour() == "black":
                col = BLACK
            else:
                pass

            self.draw_ping(screen, start_coord, end_coord, col)

    def draw_pings(self, screen):
        for pb in self._ping_boxes:
            self.draw_ping(screen, pb.get_start_pos(), pb.get_end_pos(), pb.get_colour())

    def draw_ping(self, screen, start_coord, end_coord, colour):
        start_pos = ((start_coord[0] * self._cell_size) + self._board_pos[0],
                     (start_coord[1] * self._cell_size) + self._board_pos[1]
                     )
        end_pos = (((end_coord[0] + 1) * self._cell_size) + self._board_pos[0],
                   ((end_coord[1] + 1) * self._cell_size) + self._board_pos[1])

        pygame.gfxdraw.box(screen,
                           (start_pos[0],
                            start_pos[1],
                            end_pos[0] - start_pos[0],
                            end_pos[1] - start_pos[1]),
                           tuple(colour) + (50,))

    def remove_ping(self, index):
        p = self._ping_boxes.pop(index)

    def format_for_ping(self, start_pos, end_pos, detailed=True):
        entries = []
        for y in range((end_pos[1] - start_pos[1]) + 1):
            for x in range((end_pos[0] - start_pos[0]) + 1):
                rel_x = x + start_pos[0]
                rel_y = y + start_pos[1]
                ships, objects = self.get_objects_in_space(rel_x, rel_y)
                # [x, y, type (ship, trail), direction (0-7)]
                for o in objects:
                    if not detailed:
                        type_text = "?"
                    elif type(o) == TravelTrail:
                        type_text = "trail"
                    else:
                        type_text = "?"
                    entries.append([o.get_x(), o.get_y(), type_text, o.get_direction()])
                for s in ships:
                    if detailed:
                        type_text = "ship"
                    else:
                        type_text = "?"
                    entries.append([s.get_x(), s.get_y(), type_text, s.get_direction()])
        return entries

    def end(self):
        print("Resetting")
        self._sender.send("", "reset")
        time.sleep(0.2)


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


def coord_to_grid(pos):
    return chr(pos[1] + 65) + str((pos[0] + 1))


def main():
    board_height = 20
    board_width = 20
    cell_size = 45

    game = Game(board_width, board_height, (cell_size, cell_size), cell_size)

    game.set_controls_area(((board_width + 1) * cell_size + 5,  # x
                            5,  # y
                            600,  # width
                            ((board_height + 1) * cell_size) + 35))  # height

    screen_size = (((board_width + 1) * cell_size) + game.get_controls_area()[2] + 10,
                   max([((board_height + 1) * cell_size) + 5, game.get_controls_area()[3] + 10]))

    # Create Game Control Objects
    next_turn_button = Button(
        (game.get_controls_area()[0],
         game.get_controls_area()[1] + game.get_controls_area()[3] - game.get_default_button_height()),
        game.get_controls_area()[2],
        game.get_default_button_height(),
        (255, 0, 0),
        "next_turn",
        pygame.K_SPACE,
        "Next Turn",
        (255, 255, 255))
    left_button = Button((game.get_controls_area()[0],
                          next_turn_button.get_y() - (game.get_default_button_height() + 5)),
                         round((next_turn_button.get_width() - 10) / 3),
                         game.get_default_button_height(),
                         (150, 150, 150),
                         "left",
                         pygame.K_LEFT,
                         "◄",
                         (255, 255, 255)
                         )
    up_button = Button((game.get_controls_area()[0] + left_button.get_width() + 5,
                        next_turn_button.get_y() - (game.get_default_button_height() + 5)),
                       left_button.get_width(),
                       game.get_default_button_height(),
                       (150, 150, 150),
                       "up",
                       pygame.K_UP,
                       " ▲",
                       (255, 255, 255)
                       )
    right_button = Button((game.get_controls_area()[0] + (left_button.get_width() + 5) * 2,
                           next_turn_button.get_y() - (game.get_default_button_height() + 5)),
                          left_button.get_width(),
                          game.get_default_button_height(),
                          (150, 150, 150),
                          "right",
                          pygame.K_RIGHT,
                          " ►",
                          (255, 255, 255)
                          )
    add_ping_button = Button((game.get_controls_area()[0],
                              left_button.get_y() - (game.get_default_button_height() + 5)),
                             game.get_controls_area()[2],
                             game.get_default_button_height(),
                             (0, 0, 200),
                             "arm_add_ping",
                             pygame.K_p,
                             "Create Ping",
                             (255, 255, 255)
                             )
    add_ship_button = Button((game.get_controls_area()[0],
                              game.get_controls_area()[1]),
                             game.get_controls_area()[2],
                             game.get_default_button_height() * 0.75,
                             (0, 200, 0),
                             "arm_add_ship",
                             pygame.K_a,
                             "Add Ship",
                             (255, 255, 255)
                             )
    add_ship_button.make_always_active()

    game.add_control_object(next_turn_button)
    game.add_control_object(left_button)
    game.add_control_object(up_button)
    game.add_control_object(right_button)
    game.add_control_object(add_ship_button)
    game.add_control_object(add_ping_button)

    ctrl_down = False

    # Initialise screen
    pygame.init()
    clock = pygame.time.Clock()
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
                game.end()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                co_index = game.get_clicked_co(pos)
                if co_index is not None:
                    game.set_clicked(co_index)
                if game.coord_at_pos(pos) is not None:
                    game.submit_mb_down(game.coord_at_pos(pos))
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                co_index = game.get_clicked_co(pos)
                ss_index = game.get_clicked_ss(pos)
                game.clear_clicks()
                if co_index is not None:
                    game.ping_co(co_index)
                    game.enact_bind(game.get_co_bind_text(co_index))
                if ss_index is not None:
                    game.ping_ss(ss_index)
                    game.enact_bind(game.get_ss_bind_text(ss_index))
                game.submit_mb_up(game.coord_at_pos(pos))

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
                            game.enact_bind(bind_text)

                    ss_index = game.get_ss_by_key(event.key)
                    if ss_index is None:
                        pass
                    else:
                        game.ping_ss(ss_index)
                        bind_text = game.get_ss_bind_text(ss_index)
                        if bind_text is not None:
                            game.enact_bind(bind_text)

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
