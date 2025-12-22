from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import add_positions, Position2D


class CVCarrier(CGridBase):
    def __init__(self):
        super().__init__()
        self.vc_current_node = Position2D(0, 0)
        self.directions = [Position2D(0, 1), Position2D(1, 0), Position2D(0, -1), Position2D(-1, 0)]
        self.vc_dir_index = 0

    def vc_bust(self) -> bool:
        rb = False
        if self.vc_current_node in self.position_dict:
            self.vc_dir_index = (self.vc_dir_index + 1) % 4
            del self.position_dict[self.vc_current_node]
        else:
            self.vc_dir_index = (self.vc_dir_index - 1) % 4
            self.add_item(self.vc_current_node, '#')
            rb = True
        self.vc_current_node = add_positions(self.vc_current_node, self.directions[self.vc_dir_index])
        return rb

    def vc_bust2(self) -> bool:
        rb = False
        if self.vc_current_node in self.position_dict:
            if self.position_dict[self.vc_current_node] == 'W':
                self.position_dict[self.vc_current_node] = '#'
                rb = True
            elif self.position_dict[self.vc_current_node] == '#':
                self.vc_dir_index = (self.vc_dir_index + 1) % 4
                self.position_dict[self.vc_current_node] = 'F'
            else:
                self.vc_dir_index = (self.vc_dir_index + 2) % 4
                del self.position_dict[self.vc_current_node]
        else:
            self.vc_dir_index = (self.vc_dir_index - 1) % 4
            self.add_item(self.vc_current_node, 'W')
        self.vc_current_node = add_positions(self.vc_current_node, self.directions[self.vc_dir_index])
        return rb


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    answer1 = answer2 = 0
    vc = CVCarrier()
    vc2 = CVCarrier()

    for inp_row in list(yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True)):
        vc.add_row(inp_row, p_chars_to_skip='.', p_item_type=str)
        vc2.add_row(inp_row, p_chars_to_skip='.', p_item_type=str)
    vc.vc_current_node = Position2D(vc.max_x // 2, vc.max_y // 2)
    vc2.vc_current_node = Position2D(vc2.max_x // 2, vc2.max_y // 2)

    for _ in range(10001):
        if vc.vc_bust():
            answer1 += 1

    for _ in range(10000001):
        if vc2.vc_bust2():
            answer2 += 1

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 22, solve_puzzle)


if __name__ == '__main__':
    main()
