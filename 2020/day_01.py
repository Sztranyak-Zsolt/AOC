import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from itertools import combinations


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = None
    num_list: list[int] = []
    for num in yield_input_data(p_input_file_path, p_whole_row=True):
        num_list.append(num)
    for a1, a2 in combinations(num_list, 2):
        if a1 + a2 == 2020:
            answer1 = a1 * a2
            break
    for a1, a2, a3 in combinations(num_list, 3):
        if a1 + a2 + a3 == 2020:
            answer2 = a1 * a2 * a3
            break

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 1, solve_puzzle)


if __name__ == '__main__':
    main()
