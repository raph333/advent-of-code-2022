from utils import get_file_path

UPPER_CASE_LETTER_ASCII_START = 65
UPPER_CASE_LETTER_PRIORITY_START = 27

LOWER_CASE_LETTER_ASCII_START = 97
LOWER_CASE_LETTER_PRIORITY_START = 1


def get_common_item_between_compartments(items: str) -> str:
    items = items.strip()
    boundary = len(items) // 2

    first_comp = set(items[:boundary])
    second_comp = set(items[boundary:])

    return first_comp.intersection(second_comp).pop()


def get_priority(item: str) -> int:
    if item.islower():
        return ord(item) - LOWER_CASE_ASCII_SUBTRACT

    return ord(item) - UPPER_CASE_ASCII_SUBTRACT


def sum_priorities_of_common_items_between_compartments(rucksacks: list[str]) -> int:
    return sum(get_priority(get_common_item_between_compartments(x)) for x in rucksacks)


def get_common_item_between_rucksacks(a: str, b: str, c: str) -> str:
    return set(a.strip()).intersection(b.strip()).intersection(c.strip()).pop()


def sum_priorities_of_common_items_between_rucksacks(rucksacks: list[str]) -> int:
    return sum(get_priority(get_common_item_between_rucksacks(*rucksacks[i: i + 3]))
               for i in range(0, len(rucksacks) - 2, 3))


if __name__ == '__main__':
    LOWER_CASE_ASCII_SUBTRACT = LOWER_CASE_LETTER_ASCII_START - LOWER_CASE_LETTER_PRIORITY_START
    UPPER_CASE_ASCII_SUBTRACT = UPPER_CASE_LETTER_ASCII_START - UPPER_CASE_LETTER_PRIORITY_START

    with open(get_file_path(3, 'rucksack.text')) as infile:
        lines = infile.readlines()

    print(f'The cumulative priority of all items common between compartments is '
          f'{sum_priorities_of_common_items_between_compartments(lines)}')
    print(f'The cumulative priority of all items common between a groups rucksacks is '
          f' {sum_priorities_of_common_items_between_rucksacks(lines)}')
