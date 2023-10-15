from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CPowerGrid:
    def __init__(self, p_serial_number: int):
        self.square_power: dict[int: dict[tuple[int, int]: int]] = {}
        self.create_power_grid(p_serial_number)
        self.gen_grid_square_power()

    def create_power_grid(self, p_serial_number: int):
        self.square_power[1] = {}
        for x in range(1, 301):
            for y in range(1, 301):
                power_level = (((x + 10) * y + p_serial_number) * (x + 10) // 100) % 10 - 5
                self.square_power[1][(x, y)] = power_level

    def gen_grid_square_power(self):
        for act_size in range(2, 301):
            self.square_power[act_size] = {}
            step_size = 1
            for step_size_ch in range(act_size // 2, 1, -1):
                if act_size % step_size_ch == 0:
                    step_size = step_size_ch
                    break
            for x in range(1, 302 - act_size):
                for y in range(1, 302 - act_size):
                    if step_size == 1:
                        act_power = self.square_power[act_size - 1][(x + 1, y + 1)]
                        for sx in range(x, x + act_size):
                            act_power += self.square_power[1][(sx, y)]
                        for sy in range(y + 1, y + act_size):
                            act_power += self.square_power[1][(x, sy)]
                    else:
                        act_power = 0
                        for sx in range(0, act_size // step_size):
                            for sy in range(0, act_size // step_size):
                                act_power += self.square_power[step_size][(x + sx * step_size, y + sy * step_size)]
                    self.square_power[act_size][(x, y)] = act_power


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = None
    serial_num = next(yield_input_data(p_input_file_path, p_whole_row=True), None)

    g = CPowerGrid(serial_num)

    act_max_value = 0
    for size, pos_dict in g.square_power.items():
        if size == 3:
            mp3 = sorted([(v, k) for k, v in g.square_power[size].items() if v > act_max_value], reverse=True)[0]
            answer1 = f'{mp3[1][0]},{mp3[1][1]}'
        try:
            act_max_value, act_position = sorted([(v, k) for k, v in g.square_power[size].items()
                                                  if v > act_max_value], reverse=True)[0]
            answer2 = f'{act_position[0]},{act_position[1]},{size}'
        except IndexError:
            continue
    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 11, solve_puzzle)


if __name__ == '__main__':
    main()
