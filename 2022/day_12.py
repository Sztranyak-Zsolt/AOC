from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, neighbor_positions
from string import ascii_lowercase


class CGrid(CGridBase):
    def __init__(self):
        super().__init__()
        self.starting_square: Position2D | None = None
        self.target_square: Position2D | None = None

    def find_shortest_route(self, p_starting_square_list: list[Position2D] | None = None) -> int:
        step_counter = 0
        if p_starting_square_list is None:
            visited_squares_set = {self.starting_square}
            act_squares_set = {self.starting_square}
        else:
            visited_squares_set = set(p_starting_square_list)
            act_squares_set = set(p_starting_square_list)
        while act_squares_set:
            step_counter += 1
            next_places = set()
            for act_square in act_squares_set:
                act_height = self.position_dict[act_square]
                for next_square in neighbor_positions(act_square):
                    if next_square in visited_squares_set or next_square not in self.position_dict \
                            or self.position_dict[next_square] - act_height > 1:
                        continue
                    if next_square == self.target_square:
                        return step_counter
                    visited_squares_set.add(next_square)
                    next_places.add(next_square)
            act_squares_set = next_places
        return -1


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    g = CGrid()
    for y, act_row in enumerate(yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True)):
        for x, act_tile in enumerate(act_row):
            if act_tile == 'S':
                act_value = 0
                g.starting_square = Position2D(x, y)
            elif act_tile == 'E':
                act_value = 25
                g.target_square = Position2D(x, y)
            else:
                act_value = ascii_lowercase.find(act_tile)
            g.add_item(Position2D(x, y), act_value)

    answer1 = g.find_shortest_route()
    answer2 = g.find_shortest_route([p for p, v in g.position_dict.items() if v == 0])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 12, solve_puzzle)


if __name__ == '__main__':
    main()
