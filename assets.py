import os

import pygame

pygame.font.init()
DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
COLOURS = ["black", "white", "yellow", "green", "blue", "red"]
SPRITE_FOLDER = "sprites"


class SpaceObject:
    def __init__(self, description, direction, location, colour):
        assert colour in COLOURS
        self._description = description
        self._direction = direction
        self._location = list(location)
        self._ttl = -1
        self._colour = colour
        self._image = pygame.image.load(os.path.join(SPRITE_FOLDER, "plane-{}.png".format(self._colour)))

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
        direction = direction.upper()
        if direction == "LEFT":
            self._direction -= 1
        elif direction == "RIGHT":
            self._direction += 1
        else:
            pass
        self._direction = self._direction % len(DIRECTIONS)

    def get_ttl(self):
        return self._ttl

    def decrement_ttl(self):
        if self._ttl > 0:
            self._ttl -= 1

    def get_image(self, cell_size):
        image = pygame.transform.scale(self._image, (cell_size, cell_size))
        image = pygame.transform.rotate(image, self._direction * -45)
        return image


class TravelTrail(SpaceObject):
    def __init__(self, description, direction, location, colour):
        super().__init__(description, direction, location, colour)
        self._image = pygame.image.load(os.path.join(SPRITE_FOLDER, "trail-{}.png".format(self._colour)))
        self._ttl = 4


class Ship(SpaceObject):
    def __init__(self, description, direction, location, colour):
        super().__init__(description, direction, location, colour)
        self._image = pygame.image.load(os.path.join(SPRITE_FOLDER, "plane-{}.png".format(self._colour)))


class Decoy(SpaceObject):
    pass
