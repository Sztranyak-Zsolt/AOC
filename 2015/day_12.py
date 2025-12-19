import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
import json


def calc_child_number_sum(p_input_dict: dict | list) -> int:
    act_sum = 0
    list_to_check = list()
    if isinstance(p_input_dict, list):
        list_to_check = p_input_dict
    elif isinstance(p_input_dict, dict):
        list_to_check = p_input_dict.values()
    for v in list_to_check:
        if isinstance(v, dict) or isinstance(v, list):
            act_sum += calc_child_number_sum(v)
        elif isinstance(v, int):
            act_sum += v
    return act_sum


def calc_child_number_sum2(p_input_dict: dict | list) -> int:
    act_sum = 0
    list_to_check = list()
    if isinstance(p_input_dict, list):
        list_to_check = p_input_dict
    elif isinstance(p_input_dict, dict):
        list_to_check = p_input_dict.values()
    for v in list_to_check:
        if isinstance(v, str) and isinstance(p_input_dict, dict):
            if v == "red":
                return 0
        elif isinstance(v, dict) or isinstance(v, list):
            act_sum += calc_child_number_sum2(v)
        elif isinstance(v, int):
            act_sum += v
    return act_sum


def solve_puzzle(p_input_file_path: str) -> tuple[int, int]:
    input_single_row = next(yield_input_data(p_input_file_path, p_whole_row=True), None)
    input_dict = json.loads(input_single_row)
    answer1 = calc_child_number_sum(input_dict)
    answer2 = calc_child_number_sum2(input_dict)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 12, solve_puzzle)


if __name__ == '__main__':
    main()
