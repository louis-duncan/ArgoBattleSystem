import os

import pygame
from assets import *


class Board:
    def __init__(self, width, height):
        self._ships = []
        self._objects = []
        self._width = width
        self._height = height

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
            if o.get_pos() == (x, y):
                found_objects.append(o)
        return found_ships, found_objects

    def add_ship(self, new_ship):
        self._ships.append(new_ship)

    def add_object(self, new_object):
        self._objects.append(new_object)


class Game:
    def __init__(self, width, height):
        self._height = height
        self._width = width
        self._board = Board(width, height)

    def display(self):
        os.system("cls")
        print("-------------------")
        for y in range(self._height):
            for x in range(self._width):
                ships, objects = self._board.get_objects_in_space(x=x, y=y)
                if len(ships) + len(objects) > 0:
                    print("X", end="")
                else:
                    print(" ", end="")
            print()
        print("-------------------")


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
    game._board.add_ship(Ship("ship", "NE", (5, 5)))
    while True:
        game.display()
        input()
        game._board._ships[0].move()

main()