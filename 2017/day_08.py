from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from collections import defaultdict


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    answer2 = 0
    reg_handler = defaultdict(lambda: 0)

    for reg_to_change, func, to_change_value, _, cond_register, cond_dir, cond_value in yield_input_data(p_input_file_path):
        if func == 'inc':
            mp = 1
        else:
            mp = -1
        if eval(f'{reg_handler[cond_register]} {cond_dir} {cond_value}'):
            reg_handler[reg_to_change] += mp * to_change_value
            answer2 = max(answer2, reg_handler[reg_to_change])

    answer1 = max(reg_handler.values())

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 8, solve_puzzle)


if __name__ == '__main__':
    main()
