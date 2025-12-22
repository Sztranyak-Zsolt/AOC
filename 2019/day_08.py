import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, Position2D


class CPicture:
    def __init__(self):
        self.layer_list: list[CGridBase] = []
        self.width = 25
        self.height = 6

    def create_layers_from_raw(self, p_raw_input_str: str):
        p_raw_input_list = list(p_raw_input_str)
        while p_raw_input_list:
            new_grid = CGridBase()
            for y in range(self.height - 1, -1, -1):
                for x in range(self.width):
                    if not p_raw_input_list:
                        break
                    new_grid.add_item(Position2D(x, y), p_raw_input_list.pop(0))
            self.layer_list.append(new_grid)

    @property
    def final_picture(self) -> CGridBase:
        new_grid = CGridBase()
        for x in range(self.width):
            for y in range(self.height):
                for act_picture in self.layer_list:
                    if act_picture.position_dict[Position2D(x, y)] == '1':
                        new_grid.add_item(Position2D(x, y), '#')
                    elif act_picture.position_dict[Position2D(x, y)] == '0':
                        break
        new_grid.double_width_on_print = True
        return new_grid


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    input_single_row = next(yield_input_data(p_input_file_path, p_whole_row=True), None)
    p = CPicture()
    p.create_layers_from_raw(input_single_row)

    layer_0_min = sorted([g for g in p.layer_list],
                         key=lambda g: len([x for x in g.position_dict.values() if x == '0']))[0]
    answer1 = len([x for x in layer_0_min.position_dict.values() if x == '2']) \
              * len([x for x in layer_0_min.position_dict.values() if x == '1'])
    answer2 = f'\n{p.final_picture}'

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 8, solve_puzzle)


if __name__ == '__main__':
    main()
