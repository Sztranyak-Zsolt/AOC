from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D


class CSandGlass(CGridBase):
    def __init__(self):
        super().__init__()
        self.sand_positions: set[Position2D] = set()
        self.print_y_reverse = True
        self.sand_init_position = Position2D(500, 0)

    def draw_rocks(self, p_position_list: list[Position2D]):
        prev_position = p_position_list.pop(0)
        while p_position_list:
            act_position = p_position_list.pop(0)
            dif_p_index = 0
            if act_position.x == prev_position.x:
                dif_p_index = 1
            for ip in range(min(prev_position[dif_p_index], act_position[dif_p_index]),
                            max(prev_position[dif_p_index], act_position[dif_p_index]) + 1):
                new_pos = Position2D(ip if dif_p_index == 0 else prev_position.x,
                                     ip if dif_p_index == 1 else prev_position.y)
                self.add_item(new_pos, '#')
            prev_position = act_position

    def reset_sand(self):
        self.sand_positions = set()

    def calc_sand(self, p_has_solid_bottom: bool = True) -> int:
        self.reset_sand()
        r_int = 0
        while self.add_sand(p_has_solid_bottom):
            r_int += 1
        return r_int

    def add_sand(self, p_has_solid_bottom: bool) -> bool:
        if self.sand_init_position in self.sand_positions:
            return False
        sp_x, sp_y = self.sand_init_position
        for sp_y in range(0, self.max_y + 2):
            for x_change in [0, -1, 1]:
                new_pos = Position2D(sp_x + x_change, sp_y + 1)
                if new_pos in self.sand_positions or new_pos in self.position_dict:
                    continue
                sp_x = sp_x + x_change
                break
            else:
                self.sand_positions.add(Position2D(sp_x, sp_y))
                return True
        if not p_has_solid_bottom:
            return False
        self.sand_positions.add(Position2D(sp_x, sp_y))
        return True


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    sg = CSandGlass()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space=',->'):
        sg.draw_rocks([Position2D(x, y) for x, y in zip(inp_row[::2], inp_row[1::2])])

    answer1 = sg.calc_sand(False)
    answer2 = sg.calc_sand(True)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 14, solve_puzzle)


if __name__ == '__main__':
    main()
