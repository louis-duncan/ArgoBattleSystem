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
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)


class SpaceObject:
    def __init__(self, description, direction, location, colour):
        assert colour in COLOURS
        self._description = description
        self._direction = direction
        self._location = list(location)
        self._ttl = -1
        self._colour = colour
        self._sprite_name = os.path.join(SPRITE_FOLDER, "plane-{}.png".format(self._colour))
        self._sprite = pygame.image.load(self._sprite_name)

    def as_dict(self):
        return {"description": self._description,
                "direction": self._direction,
                "location": self._location,
                "ttl": self._ttl,
                "colour": self._colour,
                "sprite": self._sprite_name}

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
    def __init__(self, description, direction, location, colour, ttl=4):
        super().__init__(description, direction, location, colour)
        self._sprite = pygame.image.load(os.path.join(SPRITE_FOLDER, "trail-{}.png".format(self._colour)))
        self._ttl = ttl


class Ship(SpaceObject):
    def __init__(self, description, direction, location, colour):
        super().__init__(description, direction, location, colour)
        self._sprite = pygame.image.load(os.path.join(SPRITE_FOLDER, "plane-{}.png".format(self._colour)))
        self._turn_history = []


class Station(SpaceObject):
    pass


class PingBox:
    def __init__(self, start_pos, end_pos, colour, creator, detailed=True, ttl=1):
        self._start_pos = start_pos
        self._end_pos = end_pos
        self._colour = colour
        self._ttl = ttl
        self._creator = creator
        self._detailed = detailed

    def get_ttl(self):
        return self._ttl

    def decrement_ttl(self):
        if self._ttl > 0:
            self._ttl -= 1

    def get_start_pos(self):
        return self._start_pos

    def get_end_pos(self):
        return self._end_pos

    def get_colour(self):
        return self._colour

    def get_ship_desc(self):
        return self._creator

    def get_detailed(self):
        return self._detailed
