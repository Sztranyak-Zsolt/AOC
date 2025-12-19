import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_vector import CVector2D


directions = [CVector2D(0, 1), CVector2D(1, 0), CVector2D(0, -1), CVector2D(-1, 0)]


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer2 = None
    act_direction = CVector2D(0, 1)
    act_position = CVector2D(0, 0)
    known_positions = set()
    for inp_row in next(yield_input_data(p_input_file_path, p_chars_to_space=','), None):
        act_direction = directions[(directions.index(act_direction) + {'R': 1, 'L': -1}[inp_row[0]]) % 4]
        step_count = int(inp_row[1:])
        if answer2 is None:
            for _ in range(step_count):
                act_position = act_position + act_direction
                if answer2 is None and act_position in known_positions:
                    answer2 = int(act_position)
                known_positions.add(act_position)
        else:
            new_pos = act_direction * step_count
            act_position = act_position + new_pos
    answer1 = int(act_position)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 1, solve_puzzle)


if __name__ == '__main__':
    main()
