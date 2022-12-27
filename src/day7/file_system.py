from utils.utils import get_file_path
from collections import defaultdict

CD_PREFIX = '$ cd'
CD_UP = '..'
ROOT = '/'
MAX_SIZE = 100000
FS_SIZE = 70000000
REQUIRED_SPACE = 30000000


def get_directory_sizes(console_lines: list[str]) -> dict:
    dir2space = defaultdict(lambda: 0)
    current_path = []

    for line in console_lines:

        if line.startswith(CD_PREFIX):
            current_dir = line.removeprefix(CD_PREFIX).strip()
            if current_dir == CD_UP:
                current_path.pop()
            else:
                current_path.append(current_dir)
            continue

        first_part = line.split(' ')[0]
        if first_part.isnumeric():
            size = int(first_part)

            dir_path = ''
            for dir_ in current_path:
                dir_path += (f'{dir_}/' if dir_ != ROOT else ROOT)
                dir2space[dir_path] += size

    return dict(dir2space)


def sum_directory_size(dirs: dict[str, int], max_size: int) -> int:
    return sum(v for v in dirs.values() if v <= max_size)


def find_smallest_directory_size(dir2size: dict[str, int], min_size: int) -> int:
    smallest = FS_SIZE

    for dir_, size in dir2size.items():
        if min_size <= size < smallest:
            smallest = size

    return smallest


if __name__ == '__main__':
    with open(get_file_path(7, 'file_system.text')) as infile:
        lines = infile.readlines()

    directory_sizes = get_directory_sizes(lines)
    print(f'The sum of total sizes of directories with max-size=100000 is '
          f'{sum_directory_size(directory_sizes, MAX_SIZE)}')

    space_left = FS_SIZE - directory_sizes[ROOT]
    space_missing = REQUIRED_SPACE - space_left
    print(f'The smallest directory that frees up enough space is '
          f'{find_smallest_directory_size(directory_sizes, space_missing)}')
