from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import CVector2D


class CGrid(CGridBase):
    def __init__(self):
        super().__init__()

    @property
    def starting_position(self) -> CVector2D:
        return [sp for sp in self.position_dict if sp.y == self.max_y][0]

    @property
    def route_information(self) -> tuple[str, int]:
        poss_dirs = {CVector2D(1, 0): [CVector2D(1, 0), CVector2D(0, 1), CVector2D(0, -1)],
                     CVector2D(-1, 0): [CVector2D(-1, 0), CVector2D(0, 1), CVector2D(0, -1)],
                     CVector2D(0, 1): [CVector2D(0, 1), CVector2D(1, 0), CVector2D(-1, 0)],
                     CVector2D(0, -1): [CVector2D(0, -1), CVector2D(1, 0), CVector2D(-1, 0)]}
        rv = ''
        step_counter = 1
        act_direction = CVector2D(-1, 0)
        act_position = self.starting_position
        while True:
            for next_dir in poss_dirs[act_direction]:
                if (next_position := act_position + next_dir) in self.position_dict:
                    if self.position_dict[next_position] in 'ABDEFGHIJKLMNOPQRSTUVWXYZ':
                        rv += self.position_dict[next_position]
                    act_position = next_position
                    act_direction = next_dir
                    step_counter += 1
                    break
            else:
                return rv, step_counter


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    g = CGrid()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True):
        g.add_row(inp_row, p_chars_to_skip=' ', p_item_type=str, p_position_type=CVector2D)

    answer1, answer2 = g.route_information

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 19, solve_puzzle)


if __name__ == '__main__':
    main()
