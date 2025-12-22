import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, Position2D


class CGridFold(CGridBase):

    def fold_self_vertical(self, x_axis: int):
        folded_positions = [p for p in self.position_dict if p.x > x_axis]
        for act_position in folded_positions:
            del self.position_dict[act_position]
            self.add_item(Position2D(x_axis - (act_position.x - x_axis), act_position.y), '#')
        self.max_x = x_axis

    def fold_self_horizontal(self, y_axis: int):
        folded_positions = [p for p in self.position_dict if p.y > y_axis]
        for act_position in folded_positions:
            del self.position_dict[act_position]
            self.add_item(Position2D(act_position.x, y_axis - (act_position.y - y_axis)), '#')
        self.max_y = y_axis


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = None
    g = CGridFold()
    g.double_width_on_print = True
    g.print_y_reverse = True
    input_group_iter = iter(yield_input_data(p_input_file_path, p_group_separator='\n\n', p_chars_to_space=',='))
    for act_x, act_y in next(input_group_iter):
        g.add_item(Position2D(act_x, act_y), '#')
    for *_, act_axis, act_value in next(input_group_iter):
        if act_axis == 'x':
            g.fold_self_vertical(act_value)
        else:
            g.fold_self_horizontal(act_value)
        if answer1 is None:
            answer1 = len(g.position_dict)
    answer2 = f'\n{g}'

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 13, solve_puzzle)


if __name__ == '__main__':
    main()
