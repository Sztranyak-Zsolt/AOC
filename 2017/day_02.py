import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    for inp_row in yield_input_data(p_input_file_path):
        answer1 += max(inp_row) - min(inp_row)
        for n1 in inp_row:
            for n2 in inp_row:
                if n1 >= n2:
                    continue
                if n2 % n1 == 0:
                    answer2 += n2 // n1
                    break
    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 2, solve_puzzle)


if __name__ == '__main__':
    main()
