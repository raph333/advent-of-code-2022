from utils import get_file_path


def get_calories_per_elf(lines: list[str]) -> list[int]:
    efl_calories_count = 0
    elf_calories = []

    for line in lines:
        if line.strip().isnumeric():
            efl_calories_count += int(line.strip())
        elif line == '\n':
            elf_calories.append(efl_calories_count)
            efl_calories_count = 0
        else:
            print(f'WARNING: unknown calorie-entry:{line}')

    return elf_calories


def get_most_calories_per_elf(calories_per_elf: list[int]) -> int:
    most_calories = 0

    for cal in calories_per_elf:
        most_calories = max(most_calories, cal)

    return most_calories


def get_calories_of_top3_elfs(calories_per_elf: list[int]) -> int:
    # avoid having to sort the whole list => O(n)
    top3 = [0, 0, 0]
    top3_smallest = min(top3)

    for cal in calories_per_elf:
        if cal > top3_smallest:
            top3.remove(top3_smallest)
            top3.append(cal)
            top3_smallest = min(top3)

    return sum(top3)


if __name__ == '__main__':
    with open(get_file_path(1, 'calories.csv')) as infile:
        calories = get_calories_per_elf(infile.readlines())

    max_cal = get_most_calories_per_elf(calories)
    max3_cal = get_calories_of_top3_elfs(calories)
    assert max3_cal <= max_cal * 3

    print(f'Most calories carried by one elf: {max_cal}')
    print(f'Calories carried by the 3 elf that carry the most: {max3_cal}')
