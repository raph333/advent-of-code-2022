from utils.utils import get_file_path

from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

DIR2AXIS = {
    'D': 'y',
    'U': 'y',
    'R': 'x',
    'L': 'x'
}


class RopeEnd:

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

    def get_num_visited_locations(self) -> int:
        return len(set(self.route))

    def move_axis(self, axis: str, n: int, direction: int):
        if axis == 'x':
            self.move_x(n, direction)
        else:
            self.move_y(n, direction)

    def move_x(self, n: int, sign):
        for _ in range(n):
            self.x += sign
            self.log_position()

    def move_y(self, n, sign):
        for _ in range(n):
            self.y += sign
            self.log_position()

    def move_diagonal(self, axis2step: dict[str, int]):
        assert set(axis2step.keys()) == {'x', 'y'}
        assert set(axis2step.values()).issubset({-1, 1})
        self.x += axis2step['x']
        self.y += axis2step['y']
        self.log_position()

    def is_adjacent(self, other_end) -> bool:
        """ Return True if the two ends are on adjacent squares: either vertically, horizontally or diagonally"""
        assert isinstance(other_end, RopeEnd)
        return abs(self.x - other_end.x) <= 1 and abs(self.y - other_end.y) <= 1

    def axis_diff(self, other_end, axis: str):
        assert isinstance(other_end, RopeEnd)
        return self[axis] - other_end[axis]


def move(instruction: str, head: RopeEnd, tail: RopeEnd, verbose=False):
    direction, steps = instruction.strip().split(' ')
    steps = int(steps)
    sign = 1 if direction in ('R', 'U') else - 1

    moving_axis = DIR2AXIS[direction]
    static_axis = 'x' if moving_axis == 'y' else 'y'

    head.move_axis(moving_axis, steps, direction=sign)

    if not tail.is_adjacent(head):

        # diagonal jump needs to happen first
        static_axis_diff = head.axis_diff(tail, static_axis)
        if static_axis_diff != 0:
            tail.move_diagonal({static_axis: static_axis_diff, moving_axis: sign})

        # move along the direction that the head moved
        tail_axis_target = head[moving_axis] - sign
        tail_steps = abs(tail_axis_target - tail[moving_axis])

        tail.move_axis(moving_axis, tail_steps, direction=sign)

        print(f'{instruction}\n{head}\n{tail}\n')


if __name__ == '__main__':
    with open(get_file_path(9, 'rope.text')) as infile:
        lines = infile.readlines()

    head_end = RopeEnd('Head', 0, 0)
    tail_end = RopeEnd('Tail', 0, 0)

    for line in lines:
        move(line, head_end, tail_end, verbose=True)

    print(f'Number of unique locations visited: {tail_end.get_num_visited_locations()}')
