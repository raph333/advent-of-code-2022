from collections import namedtuple
from utils.utils import get_file_path

Point = namedtuple('Point', ['x', 'y'])

DIR2AXIS = {
    'D': 'y',
    'U': 'y',
    'R': 'x',
    'L': 'x'
}
DIR2SIGN = {
    'D': -1,
    'U': 1,
    'R': 1,
    'L': -1
}


class RopeKnot:

    def __init__(self, name: str, x: int, y: int):
        self.name = name
        self.x = x
        self.y = y
        self.route = []
        self.route.append(self.get_position())

    def __getitem__(self, axis):
        assert axis in ('x', 'y')
        return self.__getattribute__(axis)

    def __repr__(self):
        return f'{self.name}({self.x}, {self.y})'

    def get_position(self):
        return Point(self.x, self.y)

    def log_position(self):
        self.route.append(self.get_position())

    def move(self, x: int = 0, y: int = 0):
        """
        Move one field horizontally, vertically or diagonally.
        """
        assert x != 0 or y != 0
        assert -1 <= x <= 1
        assert -1 <= y <= 1
        self.x += x
        self.y += y
        self.log_position()

    def is_adjacent(self, other_end) -> bool:
        """ Return True if the two ends are on adjacent squares: either vertically, horizontally or diagonally"""
        assert isinstance(other_end, RopeKnot)
        return abs(self.x - other_end.x) <= 1 and abs(self.y - other_end.y) <= 1

    @staticmethod
    def _sign(number: int) -> int:
        return 1 if number > 0 else -1 if number < 0 else 0

    def follow(self, lead):
        """
        Follow the lead-node that just moved.
        Assumption:
        1) The two knots where adjacent before the lead knot moved
        2) The lead knot can holy have moved one filed
        These assumptions are ensured by:
        * The method "move" only allowing a knot to move one field at a time.
        * Each time, knot k moves, the knot k + 1 executes this method
        * If the distance is larger than expected, this method throws an assertion-error
        """
        assert isinstance(lead, RopeKnot)

        if self.is_adjacent(lead):
            return

        x_diff = lead.x - self.x
        y_diff = lead.y - self.y
        x_direction = self._sign(x_diff)
        y_direction = self._sign(y_diff)
        axis_distances = {abs(x_diff), abs(y_diff)}

        if axis_distances == {1, 2} or axis_distances == {2}:
            self.move(x=x_direction, y=y_direction)
            return

        if axis_distances == {0, 2}:
            self.move(x=x_direction, y=y_direction)
            return

        raise AssertionError(f'Unexpected difference to lead: {lead} - {self}')


def get_num_unique_visited_locations(instructions: list[str], rope_length: int) -> int:
    knots = []
    for n in range(0, rope_length):
        knots.append(RopeKnot(f'Knot_{n}', 0, 0))

    for instruction in instructions:
        direction, steps = instruction.strip().split(' ')
        steps = int(steps)
        moving_axis = DIR2AXIS[direction]
        sign = DIR2SIGN[direction]

        for _ in range(steps):
            knots[0].move(**{moving_axis: sign})

            for n in range(1, rope_length):
                knots[n].follow(knots[n - 1])

    return len(set(knots[-1].route))


if __name__ == '__main__':
    with open(get_file_path(9, 'rope.text')) as infile:
        lines = infile.readlines()

    for length in (2, 10):
        print(f'Number of unique locations visited with rope-length {length}: '
              f'{get_num_unique_visited_locations(lines, length)}')
