from utils import get_file_path, Int_Convertible


class Section:

    def __init__(self, start: Int_Convertible, end: Int_Convertible):
        self.start = int(start)
        self.end = int(end)

    def __repr__(self):
        return f'Section({self.start}, {self.end})'

    def contains(self, other_section) -> bool:
        return self.start >= other_section.start and self.end <= other_section.end

    def overlaps_with(self, other_section) -> bool:
        return not (self.end < other_section.start or self.start > other_section.end)


def read_sections(line: str) -> tuple[Section, Section]:
    a, b = line.strip().split(',')
    section_a = Section(*a.split('-'))
    section_b = Section(*b.split('-'))
    return section_a, section_b


def count_fully_contained_sections(section_pairs: list[str], only_fully_contained=False) -> int:
    count = 0

    for pair in section_pairs:
        a, b = read_sections(pair)

        if only_fully_contained:
            count += a.contains(b) or b.contains(a)
        else:
            count += a.overlaps_with(b)

    return count


if __name__ == '__main__':
    with open(get_file_path(4, 'sections.text')) as infile:
        lines = infile.readlines()

    print(f'Number of section-pairs where one contains the other: '
          f'{count_fully_contained_sections(lines, only_fully_contained=True)}')
    print(f'Number of section-pairs that overlap: '
          f'{count_fully_contained_sections(lines, only_fully_contained=False)}')
