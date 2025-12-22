import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def max_joltage(p_batteries: str, p_bank_length: int = 2) -> int:
    max_digit_list = list(p_batteries[:p_bank_length])
    for act_digit in p_batteries[p_bank_length:]:
        for di in range(p_bank_length - 1):
            if max_digit_list[di] < max_digit_list[di + 1]:
                max_digit_list.pop(di)
                max_digit_list.append(act_digit)
                break
        else:
            if act_digit > max_digit_list[-1]:
                max_digit_list[-1] = act_digit
    return int(''.join(max_digit_list))


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    num_list = list(yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False))
    answer1 = sum(max_joltage(act_num) for act_num in num_list)
    answer2 = sum(max_joltage(act_num, 12) for act_num in num_list)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2025, 3, solve_puzzle)


if __name__ == '__main__':
    main()
