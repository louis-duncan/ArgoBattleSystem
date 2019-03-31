class SpaceObject:
    def __init__(self, description, direction, location):
        self._description = description
        self._direction = direction
        self._location = list(location)

    def get_pos(self):
        return self._location

    def get_x(self):
        return self._location[0]

    def get_y(self):
        return self._location[1]

    def get_direction(self):
        return self._direction

    def get_desc(self):
        return self._description


class TravelTrail(SpaceObject):
    pass


class Ship(SpaceObject):
    def move(self, distance=1):
        if "N" in self._direction:
            self._location[1] -= distance
        if "E" in self._direction:
            self._location[0] += distance
        if "S" in self._direction:
            self._location[1] += distance
        if "W" in self._direction:
            self._location[0] -= distance

class Decoy(SpaceObject):
    pass
