from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, Position2D


class CGrid(CGridBase):
    def __init__(self, p_advanced_grid: bool = False):
        super().__init__()
        self.advanced_grid = p_advanced_grid

    def switch_on(self, p_position: Position2D):
        if not self.advanced_grid:
            self.position_dict[p_position] = 1
            return
        self.position_dict[p_position] = self.position_dict.get(p_position, 0) + 1

    def switch_off(self, p_position: Position2D):
        if not self.advanced_grid:
            self.position_dict[p_position] = 0
            return
        self.position_dict[p_position] = max(0, self.position_dict.get(p_position, 0) - 1)

    def switch_toggle(self, p_position: Position2D):
        if not self.advanced_grid:
            self.position_dict[p_position] = 1 - self.position_dict.get(p_position, 0)
            return
        self.position_dict[p_position] = self.position_dict.get(p_position, 0) + 2

    def switch_rectangle(self, p_position1: Position2D, p_position2: Position2D, p_change_type: str):
        act_function = {"on": self.switch_on,
                        "off": self.switch_off,
                        "toggle": self.switch_toggle}[p_change_type]
        for d_x in range(min(p_position1.x, p_position2.x), max(p_position1.x, p_position2.x) + 1):
            for d_y in range(min(p_position1.y, p_position2.y), max(p_position1.y, p_position2.y) + 1):
                act_function(Position2D(d_x, d_y))

    @property
    def brightness(self):
        return sum(self.position_dict.values())


def solve_puzzle(p_input_file_path: str) -> (int, int):
    grid1 = CGrid()
    grid2 = CGrid(True)
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space=','):
        *_, change_type, rect_1_x, rect_1_y, _, rect_2_x, rect_2_y = inp_row
        grid1.switch_rectangle(Position2D(rect_1_x, rect_1_y), Position2D(rect_2_x, rect_2_y), change_type)
        grid2.switch_rectangle(Position2D(rect_1_x, rect_1_y), Position2D(rect_2_x, rect_2_y), change_type)
    answer1 = grid1.brightness
    answer2 = grid2.brightness
    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 6, solve_puzzle)


if __name__ == '__main__':
    main()
