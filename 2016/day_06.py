import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from collections import Counter


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    sign_list = None
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        if sign_list is None:
            sign_list = [''] * len(inp_row)
        for i, letter in enumerate(inp_row):
            sign_list[i] += letter
    answer1 = ''.join([Counter(x).most_common(1)[0][0] for x in sign_list])
    answer2 = ''.join([Counter(x).most_common()[-1][0] for x in sign_list])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 6, solve_puzzle)


if __name__ == '__main__':
    main()
