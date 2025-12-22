from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, neighbor_positions, Position2D


class CGridX(CGridBase):
    def __init__(self):
        super().__init__()

    def gen_next_stage(self) -> CGridX:
        next_grid = CGridX()
        for d_y in range(self.min_y, self.max_y + 1):
            for d_x in range(self.min_x, self.max_x + 1):
                n_counter = {'|': 0, '#': 0, '.': 0}
                for n_pos in neighbor_positions(Position2D(d_x, d_y), p_return_corner=True):
                    if n_pos in self.position_dict:
                        n_counter[self.position_dict[n_pos]] += 1
                act_item = self.position_dict[(d_x, d_y)]
                if act_item == '.' and n_counter['|'] >= 3:
                    new_item = '|'
                elif act_item == '|' and n_counter['#'] >= 3:
                    new_item = '#'
                elif act_item == '#' and (n_counter['#'] == 0 or n_counter['|'] == 0):
                    new_item = '.'
                else:
                    new_item = act_item
                next_grid.add_item(Position2D(d_x, d_y), new_item)
        return next_grid

    def item_counter(self) -> dict[str, int]:
        r_counter = {'|': 0, '#': 0, '.': 0}
        for d_i in self.position_dict.values():
            r_counter[d_i] += 1
        return r_counter


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = None
    g = CGridX()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        g.add_row(inp_row)

    g_str_list = []
    act_grid_id = str(g)
    while act_grid_id not in g_str_list or answer1 is None:
        g_str_list.append(act_grid_id)
        g = g.gen_next_stage()
        act_grid_id = str(g)
        if len(g_str_list) == 10:
            answer1 = g.item_counter()['|'] * g.item_counter()['#']
    base = g_str_list.index(act_grid_id)
    period = len(g_str_list) - base

    target_id = (1000000000 - base) % period + base
    answer2 = g_str_list[target_id].count('|') * g_str_list[target_id].count('#')

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 18, solve_puzzle)


if __name__ == '__main__':
    main()
