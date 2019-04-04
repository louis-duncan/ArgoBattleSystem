import os

import pygame

pygame.font.init()
DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
COLOURS = ["black", "white", "yellow", "green", "blue", "red"]
SPRITE_FOLDER = "sprites"
COLOUR_SQUARE_PATHS = [os.path.join(SPRITE_FOLDER, "square-{}.png".format(c)) for c in COLOURS]
directions = [["SW", "S", "SE"],
              ["W", "random", "E"],
              ["NW", "N", "NE"]]
DIRECTION_SQUARE_PATHS = [[os.path.join(SPRITE_FOLDER, "arrow-{}.png".format(d)) for d in d_row] for d_row in directions]
DIRECTION_SQUARE_PATHS_IN_ORDER = [os.path.join(SPRITE_FOLDER, "arrow-{}.png".format(d)) for d in DIRECTIONS]


class SpaceObject:
    def __init__(self, description, direction, location, colour):
        assert colour in COLOURS
        self._description = description
        self._direction = direction
        self._location = list(location)
        self._ttl = -1
        self._colour = colour
        self._sprite = pygame.image.load(os.path.join(SPRITE_FOLDER, "plane-{}.png".format(self._colour)))

    def get_pos(self):
        return self._location

    def get_x(self):
        return self._location[0]

    def get_y(self):
        return self._location[1]

    def get_direction(self):
        return self._direction

    def get_description(self):
        return self._description

    def get_colour(self):
        return self._colour

    def move(self, distance=1):
        direction = DIRECTIONS[self._direction]
        if "N" in direction:
            self._location[1] -= distance
        if "E" in direction:
            self._location[0] += distance
        if "S" in direction:
            self._location[1] += distance
        if "W" in direction:
            self._location[0] -= distance

    def turn(self, direction):
        if direction == "left":
            self._direction -= 1
        elif direction == "right":
            self._direction += 1
        else:
            print("Invalid direction:", direction)
        self._direction = self._direction % len(DIRECTIONS)

    def get_ttl(self):
        return self._ttl

    def decrement_ttl(self):
        if self._ttl > 0:
            self._ttl -= 1

    def get_sprite(self, cell_size):
        image = pygame.transform.scale(self._sprite, (cell_size, cell_size))
        image = pygame.transform.rotate(image, self._direction * -45)
        return image


class TravelTrail(SpaceObject):
    def __init__(self, description, direction, location, colour):
        super().__init__(description, direction, location, colour)
        self._sprite = pygame.image.load(os.path.join(SPRITE_FOLDER, "trail-{}.png".format(self._colour)))
        self._ttl = 4


class Ship(SpaceObject):
    def __init__(self, description, direction, location, colour):
        super().__init__(description, direction, location, colour)
        self._sprite = pygame.image.load(os.path.join(SPRITE_FOLDER, "plane-{}.png".format(self._colour)))
        self._turn_history = []


class Decoy(SpaceObject):
    pass


class Sweep():
    def __init__(self, start_pos, end_pos, colour, ttl):
        super().__init__(description, direction, location, colour)
        self._width = width

    def draw(self):
        pass

    def get_ttl(self):
        return self._ttl

    def decrement_ttl(self):
        if self._ttl > 0:
            self._ttl -= 1