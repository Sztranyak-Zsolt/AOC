from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, Position2D


class CCucumber:
    def __init__(self, p_position: Position2D, p_facing: str):
        self.c_position = p_position
        self.facing = p_facing


class CGrid(CGridBase):

    def move_cucumbers(self) -> bool:
        dir_change = {'>': Position2D(1, 0), 'v': Position2D(0, -1)}
        has_move = False
        for act_f in '>v':
            pos_dict_copy = self.position_dict.copy()
            for act_position, act_facing in pos_dict_copy.items():
                if act_facing == act_f:
                    new_x = (act_position.x + dir_change[act_f].x) % (self.max_x + 1)
                    new_y = (act_position.y + dir_change[act_f].y) % (self.max_y + 1)
                    if Position2D(new_x, new_y) not in pos_dict_copy:
                        del self.position_dict[act_position]
                        self.position_dict[Position2D(new_x, new_y)] = act_facing
                        has_move = True
        return has_move


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = 0
    answer2 = None
    g = CGrid()
    for inp_row in yield_input_data(p_input_file_path, p_reversed=True, p_whole_row=True):
        g.add_row(inp_row, p_chars_to_skip='.')

    while g.move_cucumbers():
        answer1 += 1
    answer1 += 1

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 25, solve_puzzle)


if __name__ == '__main__':
    main()
