from utils import get_file_path

PACKAGE_MARKER_LENGTH = 4
MESSAGE_MARKER_LENGTH = 14


def find_marker_index(message: str, n: int) -> int:
    last_n = list(message[:n])

    for i in range(n, len(message)):
        if len(set(last_n)) == n:  # set computation at each iteration is time-intensive for large n
            return i
        last_n.pop(0)
        last_n.append(message[i])


if __name__ == '__main__':
    with open(get_file_path(6, 'tuning.text')) as infile:
        line = infile.readline()

    print(f'Package marker ends at character number {find_marker_index(line, PACKAGE_MARKER_LENGTH)}')
    print(f'Message marker ends at character number {find_marker_index(line, MESSAGE_MARKER_LENGTH)}')
