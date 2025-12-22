import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from collections import defaultdict


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    cn = defaultdict(lambda: 1)
    for i, inp_row in enumerate(yield_input_data(p_input_file_path, p_whole_row=True)):
        part_1, part_2 = inp_row.split('|')
        match_count = len(set(part_1.split()[2:]) & set(part_2.split()))
        for d in range(match_count):
            cn[i+1+d] += cn[i]
        if match_count != 0:
            answer1 += 2 ** (match_count - 1)
        answer2 += cn[i]

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 4, solve_puzzle)


if __name__ == '__main__':
    main()
