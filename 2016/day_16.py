import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def calc_new_num(p_act_num: str):
    return p_act_num + '0' + p_act_num[::-1].replace('0', '_').replace('1', '0').replace('_', '1')


def decode_str(p_act_num: str):
    rs = ''
    for s1, s2 in zip(p_act_num[::2], p_act_num[1::2]):
        rs += '1' if s1 == s2 else '0'
    return rs


def calc_cm(p_str: str, p_length: int):
    while len(p_str) < p_length:
        p_str = calc_new_num(p_str)

    while len(p_str[:p_length]) % 2 == 0:
        p_str = decode_str(p_str[:p_length])
    return p_str


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    input_single_row = next(yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False), None)

    answer1 = calc_cm(input_single_row, 272)
    answer2 = calc_cm(input_single_row, 35651584)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 16, solve_puzzle)


if __name__ == '__main__':
    main()
