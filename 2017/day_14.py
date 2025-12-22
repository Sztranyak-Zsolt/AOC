from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from day_10 import CKnotHash
from GENERICS.aoc_grid import CGridBase


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    inp_row = next(yield_input_data(p_input_file_path, p_whole_row=True), None)

    g = CGridBase()
    for y in range(128):
        kh = CKnotHash(256)
        kh.create_hash(inp_row + '-' + str(y))
        g.add_row(kh.dense_hash_bit, p_chars_to_skip='0', p_item_type=str)
    answer1 = len(g.position_dict)
    answer2 = g.regions_count
    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 14, solve_puzzle)


if __name__ == '__main__':
    main()
