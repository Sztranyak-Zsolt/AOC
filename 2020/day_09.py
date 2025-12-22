import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from itertools import combinations


def check_preamble_sum(p_num: int, p_num_list: list[int]) -> bool:
    if len(p_num_list) < 25:
        return True
    for a, b in combinations(p_num_list[-25:], 2):
        if a + b == p_num:
            return True
    return False


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = None
    num_list = []
    for inp_num in yield_input_data(p_input_file_path, p_whole_row=True):
        if not check_preamble_sum(inp_num, num_list):
            answer1 = inp_num
        num_list.append(inp_num)

    for i1, num1 in enumerate(num_list):
        act_sum = num1
        for i2, act_num2 in enumerate(num_list[i1+1:], start=i1+1):
            act_sum += act_num2
            if act_sum == answer1:
                answer2 = min(num_list[i1:i2+1]) + max(num_list[i1:i2+1])
                break
            if act_sum > answer1:
                break
        if answer2 is not None:
            break

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 9, solve_puzzle)


if __name__ == '__main__':
    main()
