from utils import get_file_path, Int_Convertible
from copy import deepcopy


class Instruction:

    def __init__(self,
                 quantity: Int_Convertible,
                 source_stack_number: Int_Convertible,
                 target_stack_number: Int_Convertible):
        self.quantity = int(quantity)
        self.source = int(source_stack_number)
        self.target = int(target_stack_number)

    def __repr__(self):
        return f'{self.quantity} x ({self.source} -> {self.target})'

    @classmethod
    def from_verbose(cls, verbose_instruction: str):
        _, quantity, _, source, _, target = verbose_instruction.strip().split(' ')
        return cls(quantity, source, target)

    def execute_one_by_one(self, stacks: list[list[str]]):
        source = stacks[self.source - 1]
        target = stacks[self.target - 1]
        for _ in range(self.quantity):
            target.append(source.pop())

    def execute_all_at_once(self, stacks: list[list[str]]):
        source = stacks[self.source - 1]
        target = stacks[self.target - 1]

        split = len(source) - self.quantity
        crates_to_move = source[split:]
        del source[split:]
        target.extend(crates_to_move)


def separate_lines(lines: list[str]) -> tuple[list[str], str, list[str]]:
    stacks = []
    stack_numbers = ''
    instructions = []

    for line in lines:
        if line.isspace():
            continue
        if line.strip().startswith('['):
            stacks.append(line)
        elif line.strip()[0].isnumeric():
            stack_numbers = line
        elif line.startswith('move'):
            instructions.append(line)
        else:
            raise Exception(f'Unexpected line {line}')

    return stacks, stack_numbers, instructions


def parse_stacks(stack_lines, numbers_line) -> list[list[str]]:
    num_stacks = int(numbers_line.strip()[-1])
    stacks = [[] for _ in range(num_stacks)]
    stack_indices = [int(c) if c.isnumeric() else None for c in numbers_line]

    for line in stack_lines[::-1]:  # orders stacks: bottom at index 0
        for i, c in enumerate(line.strip()):
            if c.isalpha() and c.isupper() and stack_indices[i] is not None:
                stacks[stack_indices[i] - 1].append(c)

    return stacks


def get_top_crates(stacks: list[list[str]]) -> str:
    return ''.join(s[-1] for s in stacks)


if __name__ == '__main__':
    with open(get_file_path(5, 'crates.text')) as infile:
        raw_lines = infile.readlines()

    raw_stacks, raw_stack_numbers, raw_instructions = separate_lines(raw_lines)
    part1_stack_list = parse_stacks(raw_stacks, raw_stack_numbers)
    part2_stack_list = deepcopy(part1_stack_list)

    for raw_instruction in raw_instructions:
        instruction = Instruction.from_verbose(raw_instruction)
        instruction.execute_one_by_one(part1_stack_list)
        instruction.execute_all_at_once(part2_stack_list)

    print(f'Top stacks after moving crates one by one: {get_top_crates(part1_stack_list)}')
    print(f'Top stacks after moving crates in bulk: {get_top_crates(part2_stack_list)}')
