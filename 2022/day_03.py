import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from string import ascii_lowercase, ascii_uppercase


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    coder = ascii_lowercase + ascii_uppercase
    act_pack_list = []
    for package_str in yield_input_data(p_input_file_path, p_whole_row=True):
        common_item = list(set(package_str[:len(package_str) // 2]) & set(package_str[len(package_str) // 2:]))[0]
        answer1 += coder.find(common_item) + 1
        if len(act_pack_list) == 2:
            common_item = list(set(act_pack_list[0]) & set(act_pack_list[1]) & set(package_str))[0]
            answer2 += coder.find(common_item) + 1
            act_pack_list = []
        else:
            act_pack_list.append(package_str)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 3, solve_puzzle)


if __name__ == '__main__':
    main()
