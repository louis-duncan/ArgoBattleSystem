import os

import pygame
pygame.init()

from assets import *


class Game:
    def __init__(self, grid_width, grid_height, board_pos, cell_size):
        self._ships = []
        self._objects = []
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._board_pos = board_pos
        self._cell_size = cell_size
        self._round = 0
        self._font = pygame.font.Font(pygame.font.match_font("arial"), 20, bold=True)
        self._history = []

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

    def add_ship(self, new_ship):
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
        trail_index = self.add_object(TravelTrail("Created By {}".format(self._ships[index].get_description()),
                                    self._ships[index].get_direction(),
                                    self._ships[index].get_pos(),
                                    self._ships[index].get_colour()))
        self._ships[index].move()
        self._add_history(("create", trail_index))
        self._add_history(("move", index))

    def turn_ship(self, index, direction, history=True):
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
            char = self._font.render(chr(x + 65), 1, (0, 0, 0,), (255, 255, 255))
            width, height = char.get_size()
            x = self._board_pos[0] + (self._cell_size * x) + (self._cell_size / 2) - (width / 2)
            y = self._board_pos[1] - (self._cell_size / 2) - (height / 2)
            screen.blit(char, (x, y))

        for y in range(self._grid_height):
            char = self._font.render(str(y + 1), 1, (0, 0, 0), (255, 255, 255))
            width, height = char.get_size()
            x = self._board_pos[0] - (self._cell_size / 2) - (width / 2)
            y = self._board_pos[1] + (y * self._cell_size) + (self._cell_size / 2) - (height / 2)
            screen.blit(char, (x, y))

    def draw_assets(self, screen):
        for o in self._objects + self._ships:
            x, y = o.get_pos()
            image =o.get_image(round(self._cell_size * 0.75))
            image_size = image.get_rect().size
            scaled_pos = (round((x * self._cell_size) + self._board_pos[0] + (self._cell_size / 2) - (image_size[0] / 2)),
                          round((y * self._cell_size) + self._board_pos[1] + (self._cell_size / 2) - (image_size[1] / 2)))
            screen.blit(image, scaled_pos)

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
            if history_item[2] == "LEFT":
                self.turn_ship(history_item[1], "RIGHT", False)
            elif history_item[2] == "RIGHT":
                self.turn_ship(history_item[1], "LEFT", False)
            else:
                pass


def is_adjacent(point1, point2):
    if type(point1) is str:
        x1, y1 = grid_to_coord(point1)
        x2, y2 = grid_to_coord(point2)
    else:
        x1, y1 = point1
        x2, y2 = point2
    return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1


def grid_to_coord(grid_ref):
    return ord(grid_ref[0].upper()) - 65, int(grid_ref[1] - 1)


def coord_to_grid(coord):
    return chr(coord[0] + 65) + str(coord[1] + 1)


def main():
    height = 20
    width = 20
    size = 40

    game = Game(width, height, (size, size), size)

    game.add_ship(Ship("Louis", 1, (3, 3), "blue"))

    clock = pygame.time.Clock()

    selected_ship = 0

    ctrl_down = False

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((1500, (height + 1) * size + 5))
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.tick()
                elif event.key == pygame.K_LCTRL:
                    ctrl_down = True
                elif event.key == pygame.K_z:
                    if ctrl_down:
                        game.undo()
                elif selected_ship >= 0:
                    if event.key == pygame.K_UP:
                        game.move_ship(selected_ship)
                    elif event.key == pygame.K_LEFT:
                        game.turn_ship(selected_ship, "LEFT")
                    elif event.key == pygame.K_RIGHT:
                        game.turn_ship(selected_ship, "RIGHT")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    ctrl_down = False

        screen.blit(background, (0, 0))
        game.draw_assets(screen)
        game.draw_board(screen)
        pygame.display.flip()

        clock.tick(30)



main()