import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    for act_group in yield_input_data(p_input_file_path, p_whole_row=True, p_group_separator='\n\n'):
        y_set = set(act_group[0])
        y_set2 = set(act_group[0])
        for a in act_group[1:]:
            y_set |= set(a)
            y_set2 &= set(a)
        answer1 += len(y_set)
        answer2 += len(y_set2)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 6, solve_puzzle)


if __name__ == '__main__':
    main()
