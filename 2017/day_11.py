from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_vector import CVector2D


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    hex_directions = {'ne': CVector2D(1, 1), 'se': CVector2D(1, -1), 's': CVector2D(0, -2),
                      'sw': CVector2D(-1, -1), 'nw': CVector2D(-1, 1), 'n': CVector2D(0, 2)}

    directions = next(yield_input_data(p_input_file_path, p_chars_to_space=','), None)

    act_position = CVector2D(0, 0)
    answer2 = 0

    for act_step in directions:
        act_position = act_position + hex_directions[act_step]
        answer2 = max(answer2, abs(act_position.x) + (abs(act_position.y) - abs(act_position.x)) // 2)

    answer1 = abs(act_position.x) + (abs(act_position.y) - abs(act_position.x)) // 2

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 11, solve_puzzle)


if __name__ == '__main__':
    main()
