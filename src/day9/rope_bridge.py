from collections import namedtuple
from utils.utils import get_file_path

Point = namedtuple('Point', ['x', 'y'])


class Knot:

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
        assert isinstance(other_end, Knot)
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
        assert isinstance(lead, Knot)

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


class MoveInstruction:
    dir2axis = {
        'D': 'y',
        'U': 'y',
        'R': 'x',
        'L': 'x'
    }
    dir2sign = {
        'D': -1,
        'U': 1,
        'R': 1,
        'L': -1
    }

    def __init__(self, line: str):
        direction, steps = line.strip().split(' ')
        self.direction = direction
        self.steps = int(steps)
        self.moving_axis = self.dir2axis[direction]
        self.sign = self.dir2sign[direction]


class Rope:

    def __init__(self, length: int):
        self.length = length
        self.knots = [Knot(f'Knot_{i}', 0, 0) for i in range(length)]

    def move(self, instruction: MoveInstruction):
        for _ in range(instruction.steps):
            self.knots[0].move(**{instruction.moving_axis: instruction.sign})

            for n in range(1, self.length):
                self.knots[n].follow(self.knots[n - 1])

    def get_num_unique_visited_locations(self, instruction_lines: list[str], knot_num: int = -1) -> int:
        for line in instruction_lines:
            instruction = MoveInstruction(line)
            self.move(instruction)

        return len(set(self.knots[knot_num].route))


if __name__ == '__main__':
    with open(get_file_path(9, 'rope.text')) as infile:
        lines = infile.readlines()

    ROPE_LENGTHS = (2, 10)  # rope-lengths for part1 and part2, respectively

    for rope_length in ROPE_LENGTHS:
        print(f'Number of unique locations visited with rope-length {rope_length}: '
              f'{Rope(rope_length).get_num_unique_visited_locations(lines)}')
