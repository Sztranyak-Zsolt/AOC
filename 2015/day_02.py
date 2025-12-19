import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from collections import namedtuple


TPackage = namedtuple('CPackage', ['length', 'width', 'height'])


def calc_paper_need(p_package: TPackage) -> int:
    return 2 * (p_package.length * p_package.width + p_package.length * p_package.height
                + p_package.width * p_package.height) \
        + p_package.length * p_package.width * p_package.height // \
        max(p_package.length, p_package.width, p_package.height)


def calc_ribbon_need(p_package: TPackage) -> int:
    return 2 * (p_package.length + p_package.height + p_package.width
                - max(p_package.length, p_package.width, p_package.height)) \
        + p_package.length * p_package.width * p_package.height


def solve_puzzle(p_input_file_path: str) -> tuple[int, int]:

    paper_need, ribbon_need = 0, 0
    for inp_row_length, inp_row_weight, inp_row_height in yield_input_data(p_input_file_path, p_chars_to_space='x'):
        package = TPackage(inp_row_length, inp_row_weight, inp_row_height)
        paper_need += calc_paper_need(package)
        ribbon_need += calc_ribbon_need(package)

    return paper_need, ribbon_need


def main():
    aoc_solve_puzzle(2015, 2, solve_puzzle)


if __name__ == '__main__':
    main()
