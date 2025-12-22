import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def get_digits(p_str: str, p_mapping: dict[str, int]) -> list[int]:
    rv = []
    for i in range(len(p_str)):
        for mapped_digit, mapped_digit_value in p_mapping.items():
            if p_str[i:i + len(mapped_digit)] == mapped_digit:
                rv.append(mapped_digit_value)
    return rv


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    mapping_dict1 = {str(d): d for d in range(0, 11)}
    mapping_dict2 = mapping_dict1 | {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
                                     'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False):
        digits1 = get_digits(inp_row, mapping_dict1)
        digits2 = get_digits(inp_row, mapping_dict2)
        answer1 += digits1[0] * 10 + digits1[-1]
        answer2 += digits2[0] * 10 + digits2[-1]

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 1, solve_puzzle)


if __name__ == '__main__':
    main()
