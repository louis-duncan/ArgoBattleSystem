import os

import pygame
from assets import *


class Game:
    def __init__(self, grid_width, grid_height, board_pos, board_width, board_height):
        self._ships = []
        self._objects = []
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._board_pos = board_pos
        self._board_width = board_width
        self._board_height = board_height

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

    def add_object(self, new_object):
        self._objects.append(new_object)

    def remove_ship(self, index):
        p = self._ships.pop(index)

    def remove_object(self, index):
        p = self._objects.pop(index)

    def move_ship(self, index):
        self.add_object(TravelTrail("Created By {}".format(self._ships[index].get_description()),
                                    self._ships[index].get_direction(),
                                    self._ships[index].get_pos()))
        self._ships[index].move()

    def turn_ship(self, index, direction):
        self._ships[index].turn(direction)

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

    def tick(self):
        self._decrement_ttls()
        self._purge_objects()
        
    def draw_board(self):


    def draw_assets(self, screen):
        real_x = real_y = 0 # TODO: Add code to get proper positions.

        for o in self._objects:
            o.draw(screen, real_x, real_y)

        for s in self._ships:
            s.draw(screen, real_x, real_y)


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

    game = Game(24, 24)
    game.add_ship(Ship("Louis", DIRECTIONS.index("E"), (3, 12)))




main()