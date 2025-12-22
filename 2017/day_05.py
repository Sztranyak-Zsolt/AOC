import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    inp_nums = [inp_row for inp_row in yield_input_data(p_input_file_path, p_whole_row=True)]
    inp_nums_copy = inp_nums.copy()
    act_index = 0
    while 0 <= act_index < len(inp_nums_copy):
        next_index = act_index + inp_nums_copy[act_index]
        inp_nums_copy[act_index] += 1
        act_index = next_index
        answer1 += 1

    act_index = 0
    while 0 <= act_index < len(inp_nums):
        next_index = act_index + inp_nums[act_index]
        if inp_nums[act_index] < 3:
            inp_nums[act_index] += 1
        else:
            inp_nums[act_index] -= 1
        act_index = next_index
        answer2 += 1

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 5, solve_puzzle)


if __name__ == '__main__':
    main()
