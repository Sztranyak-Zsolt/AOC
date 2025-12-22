import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, Position2D
from math import prod


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    g = CGridBase()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        g.add_row(inp_row, p_chars_to_skip='.')

    slope = {Position2D(1, 1): 0, Position2D(3, 1): 0, Position2D(5, 1): 0, Position2D(7, 1): 0, Position2D(1, 2): 0}
    for r in range(g.max_y + 1):
        for k, v in slope.items():
            if r % k.y == 0 and ((r * k.x // k.y) % (g.max_x + 1), r) in g.position_dict:
                slope[k] += 1
    answer1 = slope[Position2D(3, 1)]
    answer2 = prod(slope.values())

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 3, solve_puzzle)


if __name__ == '__main__':
    main()
