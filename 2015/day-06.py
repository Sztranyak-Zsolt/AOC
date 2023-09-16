from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CGridItem:
    def __init__(self, p_value: bool | int):
        self.value = p_value


class CGrid:
    def __init__(self, p_advanced_grid: bool = False):
        self.advanced_grid = p_advanced_grid
        self.position_dict: dict[tuple[int, int], bool | int] = {}

    def switch_on(self, p_position):
        if not self.advanced_grid:
            self.position_dict[p_position] = 1
            return
        self.position_dict[p_position] = self.position_dict.get(p_position, 0) + 1

    def switch_off(self, p_position):
        if not self.advanced_grid:
            self.position_dict[p_position] = 0
            return
        self.position_dict[p_position] = max(0, self.position_dict.get(p_position, 0) - 1)

    def switch_toggle(self, p_position):
        if not self.advanced_grid:
            self.position_dict[p_position] = 1 - self.position_dict.get(p_position, 0)
            return
        self.position_dict[p_position] = self.position_dict.get(p_position, 0) + 2

    def switch_rectangle(self, p_position1: tuple[int, int], p_position2: tuple[int, int], p_change_type: str):
        act_function = {"on": self.switch_on,
                        "off": self.switch_off,
                        "toggle": self.switch_toggle}[p_change_type]
        for d_x in range(min(p_position1[0], p_position2[0]), max(p_position1[0], p_position2[0]) + 1):
            for d_y in range(min(p_position1[1], p_position2[1]), max(p_position1[1], p_position2[1]) + 1):
                act_function((d_x, d_y))

    @property
    def brightness(self):
        return sum(self.position_dict.values())


def solve_puzzle(p_input_file_path: str) -> (int, int):
    grid1 = CGrid()
    grid2 = CGrid(True)
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space=','):
        *_, change_type, rect_1_x, rect_1_y, _, rect_2_x, rect_2_y = inp_row
        grid1.switch_rectangle((rect_1_x, rect_1_y), (rect_2_x, rect_2_y), change_type)
        grid2.switch_rectangle((rect_1_x, rect_1_y), (rect_2_x, rect_2_y), change_type)
    answer1 = grid1.brightness
    answer2 = grid2.brightness
    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 6, solve_puzzle)


if __name__ == '__main__':
    main()
