from utils.utils import get_file_path
import numpy as np
from itertools import product


def get_num_hidden_trees():
    is_hidden = np.zeros((N_ROWS, N_COLS))

    for i in range(N_ROWS):
        for j in range(N_COLS):
            h = HEIGHTS[i, j]

            # skip trees on the outside
            if i == 0 or j == 0 or i == N_ROWS - 1 or j == N_COLS - 1:
                continue

            if all([
                (HEIGHTS[i, :j]).max() >= h,
                (HEIGHTS[i, j + 1:]).max() >= h,
                (HEIGHTS[0:i, j]).max() >= h,
                (HEIGHTS[i + 1:, j]).max() >= h
            ]):
                is_hidden[i, j] = 1

    print(f'Visible from the outside: {(is_hidden == 0).sum()}')


def get_scenic_score(i: int, j: int) -> int:
    height = HEIGHTS[i, j]
    right = get_direction_score(HEIGHTS[i, j + 1:], height)
    left = get_direction_score(HEIGHTS[i, :j][::-1], height)

    down = get_direction_score(HEIGHTS[i + 1:, j], height)
    up = get_direction_score(HEIGHTS[:i, j][::-1], height)

    return right * left * down * up


def get_direction_score(line_of_sight: np.ndarray, h: int):
    score = 1
    i = 0

    while i < len(line_of_sight) - 1 and line_of_sight[i] < h:
        score += 1
        i += 1

    return score


if __name__ == '__main__':
    with open(get_file_path(8, 'trees.text')) as infile:
        lines = infile.readlines()

    N_ROWS = len(lines)
    N_COLS = len(lines[0].strip())
    HEIGHTS = np.array([list(row.strip()) for row in lines]).astype(int)

    print(f'Visible from the outside: {get_num_hidden_trees()}')
    print(f'Max scenic score: {max(get_scenic_score(i, j) for i, j in product(range(N_ROWS), range(N_COLS)))}')
