class ArrowGen:
    def __init__(self):
        self._o_arrows = "↑↗→↘↓↙←↖"
        self._e_arrows = "⇧⬀⇨⬂⇩⬃⇦⬁"
        self._f_arrows = "⬆⬈⮕⬊⬇⬋⬅⬉"


class Board:
    def __init__(self, width, height):
        self._objects = []
        self._width = width
        self._height = height

    def get_objects_in_space(self, grid_ref=None, x=None, y=None):
        if grid_ref is not None:
            x, y = grid_to_coord(grid_ref)
        else:
            pass
        found = []
        for o in self._objects:
            if o.is_at():
                found.append(o)
        return found

    def add_object(self, new_object):
        self._objects = []


class SpaceObject:
    def __init__(self, description, direction, location):
        self._description = description
        self._direction = direction
        self._location = location

    def get_pos(self):
        return self._location

    def get_direction(self):
        return self._direction

    def get_desc(self):
        return self._description


class TravelTrail(SpaceObject):
    pass


class Ship(SpaceObject):
    pass


class Decoy(SpaceObject):
    pass


class Game:
    def __init__(self, width, height):
        self._board = Board(width, height)

    def move_ship(self, move_sequence):
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
    game = Game(24, 24)
