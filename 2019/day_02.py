from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from Intcode import CIntCode


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer2 = None
    num_list = next(yield_input_data(p_input_file_path, p_chars_to_space=','), None)
    ic = CIntCode(num_list)
    ic.program_code_dict[1] = 12
    ic.program_code_dict[2] = 2
    ic.run_program()
    answer1 = ic.program_code_dict[0]
    for noun_verb in range(10000):
        ic = CIntCode(num_list)
        ic.program_code_dict[1] = noun_verb // 100
        ic.program_code_dict[2] = noun_verb % 100
        ic.run_program()
        if ic.program_code_dict[0] == 19690720:
            answer2 = noun_verb

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 2, solve_puzzle)


if __name__ == '__main__':
    main()
