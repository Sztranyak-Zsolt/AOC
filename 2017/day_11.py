from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import add_positions, mh_distance


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    hex_directions = {'ne': (1, 1), 'se': (1, -1), 's': (0, -2),
                      'sw': (-1, -1), 'nw': (-1, 1), 'n': (0, 2)}

    directions = next(yield_input_data(p_input_file_path, p_chars_to_space=','), None)

    act_position = (0, 0)
    answer2 = 0

    for act_step in directions:
        act_position = add_positions(act_position, hex_directions[act_step])
        answer2 = max(answer2, mh_distance((0, 0), act_position) // 2)

    answer1 = mh_distance((0, 0), act_position) // 2

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 11, solve_puzzle)


if __name__ == '__main__':
    main()
