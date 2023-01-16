from utils.utils import get_file_path

DELAY = 1
INITIAL_VALUE = 1
MEASURE_CYCLES = range(20, 221, 40)


def get_cycles(cycle_lines: list[str]) -> list[int]:
    cycle_additions = []

    for i, line in enumerate(cycle_lines):
        if line.strip() == 'noop':
            cycle_additions.append(0)

        if line.startswith('addx'):
            _, v = line.strip().split(' ')
            v = int(v)
            cycle_additions.append(0)  # addx takes two cycles to complete => log 0 to keep the index equal to the cycle
            cycle_additions.append(v)

    cycle_additions.extend([0, 0])  # add two extra cycles to allow all additions to complete

    return cycle_additions


def get_signal_strength(cycle_addictions: list[int], cycle: int):
    return (INITIAL_VALUE + sum(cycle_addictions[:cycle - DELAY])) * cycle


if __name__ == '__main__':
    with open(get_file_path(10, 'circuit.text')) as infile:
        lines = infile.readlines()

    cycles = get_cycles(lines)

    print(f'Sum of signal strengths at {list(MEASURE_CYCLES)}: '
          f'{sum(get_signal_strength(cycles, i) for i in MEASURE_CYCLES)}')
