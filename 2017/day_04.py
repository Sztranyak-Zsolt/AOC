import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    for inp_row in yield_input_data(p_input_file_path):
        if len(inp_row) == len(set(inp_row)):
            answer1 += 1
        if len(inp_row) == len(set([str(sorted(list(x))) for x in inp_row])):
            answer2 += 1
    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 4, solve_puzzle)


if __name__ == '__main__':
    main()
