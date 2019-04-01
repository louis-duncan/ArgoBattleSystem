DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


class SpaceObject:
    def __init__(self, description, direction, location):
        self._description = description
        self._direction = direction
        self._location = list(location)
        self._char = "X"
        self._ttl = -1

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

    def draw(self, screen, real_x, real_y):
        pass


class TravelTrail(SpaceObject):
    def __init__(self, description, direction, location):
        super().__init__(description, direction, location)
        self._char = "⁞"
        self._ttl = 5


class Ship(SpaceObject):
    def __init__(self, description, direction, location):
        super().__init__(description, direction, location)
        self._char = "▲"


class Decoy(SpaceObject):
    def __init__(self, description, direction, location):
        super().__init__(description, direction, location)
        self._char = "◘"
