import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    for n1, n2, check_s, pw in yield_input_data(p_input_file_path, p_chars_to_space='-:'):
        ch_count = pw.count(check_s)
        if n1 <= ch_count <= n2:
            answer1 += 1
        if pw[n1 - 1] != pw[n2 - 1] and (pw[n1 - 1] == check_s or pw[n2 - 1] == check_s):
            answer2 += 1

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 2, solve_puzzle)


if __name__ == '__main__':
    main()
