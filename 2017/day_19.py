from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, add_positions, Position2D


class CGrid(CGridBase):
    def __init__(self):
        super().__init__()

    @property
    def starting_position(self) -> tuple[int, int]:
        return [sp for sp in self.position_dict if sp.y == self.max_y][0]

    @property
    def route_information(self) -> tuple[str, int]:
        poss_dirs = {Position2D(1, 0): [Position2D(1, 0), Position2D(0, 1), Position2D(0, -1)],
                     Position2D(-1, 0): [Position2D(-1, 0), Position2D(0, 1), Position2D(0, -1)],
                     Position2D(0, 1): [Position2D(0, 1), Position2D(1, 0), Position2D(-1, 0)],
                     Position2D(0, -1): [Position2D(0, -1), Position2D(1, 0), Position2D(-1, 0)]}
        rv = ''
        step_counter = 1
        act_direction = Position2D(-1, 0)
        act_position = self.starting_position
        while True:
            for next_dir in poss_dirs[act_direction]:
                if (next_position := add_positions(act_position, next_dir)) in self.position_dict:
                    if self.position_dict[next_position] in 'ABDEFGHIJKLMNOPQRSTUVWXYZ':
                        rv += self.position_dict[next_position]
                    act_position = next_position
                    act_direction = next_dir
                    step_counter += 1
                    break
            else:
                return rv, step_counter


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    g = CGrid()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True):
        g.add_row(inp_row, p_chars_to_skip=' ', p_item_type=str)

    answer1, answer2 = g.route_information

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 19, solve_puzzle)


if __name__ == '__main__':
    main()
