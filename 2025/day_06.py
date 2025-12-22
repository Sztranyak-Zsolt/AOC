import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from math import prod
from collections import defaultdict

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    op_dict = {'+': sum, '*': prod}
    answer1 = answer2 = 0
    num_list = []
    op_list = []
    op_list_raw = ''
    digit_raw_index_nums = defaultdict(list)
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        if '+' in inp_row:
            op_list_raw = inp_row
            op_list.extend(inp_row.split())
        else:
            num_list.append(list(map(int, inp_row.split())))
            for di, act_digit in enumerate(inp_row):
                if act_digit != ' ':
                    digit_raw_index_nums[di].append(act_digit)

    for i, nums in enumerate(zip(*num_list)):
        answer1 += op_dict[op_list[i]](nums)
    for op_index, act_op in enumerate(op_list_raw):
        if act_op == ' ':
            continue
        vertical_num_list = []
        digit_index = op_index
        while (raw_digits := digit_raw_index_nums.get(digit_index)) is not None:
            vertical_num_list.append(int(''.join(raw_digits)))
            digit_index += 1
        answer2 += op_dict[act_op](vertical_num_list)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2025, 6, solve_puzzle)


if __name__ == '__main__':
    main()
