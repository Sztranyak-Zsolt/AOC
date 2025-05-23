from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, neighbor_positions, Position2D


class CGrid(CGridBase):
    def __init__(self):
        super().__init__()

    def set_corners_on(self):
        for corner in [Position2D(0, 0), Position2D(0, 99), Position2D(99, 0), Position2D(99, 99)]:
            if corner not in self.position_dict:
                self.add_item(corner, '#')

    def count_lights_on(self):
        return len(self.position_dict)

    def calc_neighbor_on(self, p_position: Position2D) -> int:
        lights_on_counter = 0
        for neighbor_position in neighbor_positions(p_position, True, True):
            if neighbor_position in self.position_dict:
                lights_on_counter += 1
        return lights_on_counter

    def gen_next_grid(self) -> CGrid:
        new_grid = CGrid()
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                neighbor_count = self.calc_neighbor_on(Position2D(x, y))
                if (x, y) in self.position_dict and neighbor_count in [2, 3]:
                    new_grid.add_item(Position2D(x, y), "#")
                    continue
                if (x, y) not in self.position_dict and neighbor_count == 3:
                    new_grid.add_item(Position2D(x, y), "#")
                    continue
        new_grid.min_x = new_grid.min_y = 0
        new_grid.max_x = new_grid.max_y = 99
        return new_grid


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    act_grid = CGrid()
    act_grid2 = CGrid()
    for inp_row in list(yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True)):
        act_grid.add_row(p_row=inp_row, p_chars_to_skip='.', p_item_type=str)
        act_grid2.add_row(p_row=inp_row, p_chars_to_skip='.', p_item_type=str)

    act_grid2.set_corners_on()
    for _ in range(100):
        act_grid = act_grid.gen_next_grid()
        act_grid2 = act_grid2.gen_next_grid()
        act_grid2.set_corners_on()

    answer1 = act_grid.count_lights_on()
    answer2 = act_grid2.count_lights_on()
    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 18, solve_puzzle)


if __name__ == '__main__':
    main()
