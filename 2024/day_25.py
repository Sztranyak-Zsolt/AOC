import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = 0
    answer2 = None

    locks = []
    keys = []
    for act_pins in yield_input_data(p_input_file_path, p_whole_row=True, p_group_separator='\n\n'):
        act_arr = keys if act_pins[0][0] == '#' else locks
        act_arr.append([-1] * 5)
        for act_row in act_pins:
            for i, act_pin in enumerate(act_row):
                if act_pin == '#':
                    act_arr[-1][i] += 1

    for act_key in keys:
        for act_lock in locks:
            for key_pin, lock_pin in zip(act_key, act_lock):
                if key_pin + lock_pin > 5:
                    break
            else:
                answer1 += 1

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 25, solve_puzzle)


if __name__ == '__main__':
    main()
