import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from enum import Enum, auto


class ReadState(Enum):
    SIMPLE = auto()
    SUB_DATA = auto()
    COMP_LENGTH = auto()
    COMP_MULTIPLIER = auto()


def get_decompressed_length(p_str: str, p_compress_sub_data: bool = False) -> int:
    rv = 0
    act_state = ReadState.SIMPLE
    compression_length = compression_multiplier = 0
    sub_data = ''
    for act_data in p_str:
        if act_state == ReadState.SIMPLE:
            if act_data == "(":
                act_state = ReadState.COMP_LENGTH
            else:
                rv += 1
            continue
        if act_state == ReadState.COMP_LENGTH:
            if act_data == "x":
                act_state = ReadState.COMP_MULTIPLIER
            else:
                compression_length = compression_length * 10 + int(act_data)
            continue
        if act_state == ReadState.COMP_MULTIPLIER:
            if act_data == ")":
                act_state = ReadState.SUB_DATA
            else:
                compression_multiplier = compression_multiplier * 10 + int(act_data)
            continue
        if act_state == ReadState.SUB_DATA:
            sub_data += act_data
            if len(sub_data) == compression_length:
                if p_compress_sub_data:
                    rv += get_decompressed_length(sub_data, True) * compression_multiplier
                else:
                    rv += len(sub_data) * compression_multiplier
                compression_length = compression_multiplier = 0
                sub_data = ''
                act_state = ReadState.SIMPLE
    return rv


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    base_str = next(yield_input_data(p_input_file_path, p_whole_row=True), None)
    answer1 = get_decompressed_length(base_str)
    answer2 = get_decompressed_length(base_str, True)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 9, solve_puzzle)


if __name__ == '__main__':
    main()
