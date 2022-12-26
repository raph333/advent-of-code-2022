from utils import get_file_path

CODE2NUM = {'A': 0, 'B': 1, 'C': 2,
            'X': 0, 'Y': 1, 'Z': 2}

W = 6  # win points
D = 3  # draw points
L = 0  # loose points

#                  I play
#                   0 1 2
#                 0 d w l
# opponent plays  1 l d w
#                 2 w l d
OUTCOME_POINTS = [[D, W, L],
                  [L, D, W],
                  [W, L, D]]

#                  outcome should be
#                   L D W
#                 0 3 0 1
# opponent plays  1 0 1 2
#                 2 1 2 0
RESPONSE = [[2, 0, 1],
            [0, 1, 2],
            [1, 2, 0]]


def get_total_score(matches: list[str], match_to_numbers_converter) -> int:
    total_score = 0

    for match in matches:
        play, response = match_to_numbers_converter(*match.strip().split(' '))
        total_score += get_match_score(play, response)

    return total_score


def get_match_score(play: int, response: int) -> int:
    outcome_points = OUTCOME_POINTS[play][response]
    return outcome_points + response + 1


def match_to_numeric_part1(play_code: str, response_code: str) -> tuple[int, int]:
    return CODE2NUM[play_code], CODE2NUM[response_code]


def match_to_numeric_part2(play_code: str, outcome_code) -> tuple[int, int]:
    play = CODE2NUM[play_code]
    outcome = CODE2NUM[outcome_code]
    response = RESPONSE[play][outcome]
    return play, response


if __name__ == '__main__':
    with open(get_file_path(2, 'strategy.text')) as infile:
        lines = infile.readlines()

    print(f'Part 1 total score: {get_total_score(lines, match_to_numeric_part1)}')
    print(f'Part 2 total score: {get_total_score(lines, match_to_numeric_part2)}')
