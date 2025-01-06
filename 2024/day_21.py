from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from functools import cache
from GENERICS.aoc_vector import Position2D

NUM_KEYPAD = (('7', '8', '9'), ('4', '5', '6'), ('1', '2', '3'), (None, '0', 'A'))
ARROW_KEYPAD = ((None, '^', 'A'), ('<', 'v', '>'))


@cache
def get_path_from_keyboard(p_keypad: tuple[tuple[str | None]], p_from: str, p_to: str) -> str:
    if p_from == p_to:
        return 'A'
    from_position: Position2D | None = None
    to_position: Position2D | None = None
    for y, act_row in enumerate(p_keypad):
        for x, act_s in enumerate(act_row):
            if act_s == p_from:
                from_position = Position2D(x, y)
                break
    for y, act_row in enumerate(p_keypad):
        for x, act_s in enumerate(act_row):
            if act_s == p_to:
                to_position = Position2D(x, y)
                break
    if from_position is None or to_position is None:
        raise ValueError
    rs = ''
    x_dif = to_position.x - from_position.x
    y_dif = to_position.y - from_position.y
    if x_dif < 0 and p_keypad[from_position.y][to_position.x] is not None:
        rs += '<' * (-x_dif)
    if y_dif > 0 and p_keypad[to_position.y][from_position.x] is not None:
        rs += 'v' * y_dif
    if y_dif < 0 and p_keypad[to_position.y][from_position.x] is not None:
        rs += '^' * (-y_dif)
    if x_dif > 0:
        rs += '>' * x_dif
    if x_dif < 0 and p_keypad[from_position.y][to_position.x] is None:
        rs += '<' * (-x_dif)
    if y_dif > 0 and p_keypad[to_position.y][from_position.x] is None:
        rs += 'v' * y_dif
    if y_dif < 0 and p_keypad[to_position.y][from_position.x] is None:
        rs += '^' * (-y_dif)
    return rs + 'A'


def decode(p_str: str) -> str:
    act_str = 'A'
    rv = ''
    for c in p_str:
        rv += get_path_from_keyboard(NUM_KEYPAD, act_str, c)
        act_str = c
    return rv


@cache
def change_dict():
    rd = {}
    for c1 in '<>^vA':
        for c2 in '<>^vA':
            rd[c1 + c2] = {}
            pc = 'A'
            for q in get_path_from_keyboard(ARROW_KEYPAD, c1, c2):
                if pc + q not in rd[c1 + c2]:
                    rd[c1 + c2][pc + q] = 1
                else:
                    rd[c1 + c2][pc + q] += 1
                pc = q
    return rd


def evolve_dict(p_dict):
    rd = {}
    for c, v in p_dict.items():
        for c2, v2 in change_dict()[c].items():
            if c2 not in rd:
                rd[c2] = v * v2
            else:
                rd[c2] += v * v2
    return rd


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):

        act_dict = {}
        prev_c = 'A'

        for c in decode(inp_row):
            if prev_c + c in act_dict:
                act_dict[prev_c + c] += 1
            else:
                act_dict[prev_c + c] = 1
            prev_c = c

        for i in range(25):
            act_dict = evolve_dict(act_dict)
            if i == 1:
                answer1 += sum(act_dict.values()) * int(inp_row[:3])
        answer2 += sum(act_dict.values()) * int(inp_row[:3])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 21, solve_puzzle)


if __name__ == '__main__':
    main()
