import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int, int]:
    ans1 = ans2 = 0
    direction_dict = {'(': 1, ')': -1}
    input_row = next(yield_input_data(p_input_file_path, p_whole_row=True), None)
    for i, d in enumerate(input_row, start=1):
        ans1 += direction_dict[d]
        if ans2 == 0 and ans1 == -1:
            ans2 = i
    return ans1, ans2


def main():
    aoc_solve_puzzle(2015, 1, solve_puzzle)


if __name__ == '__main__':
    main()
