from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from Intcode import CIntCode
from GENERICS.aoc_vector import Position2D
from copy import copy
from typing import Iterator


class CTractorBeam:
    def __init__(self, p_intcode: CIntCode):
        self.tb_program = p_intcode

    def something_found_on_position(self, p_position: Position2D) -> bool:
        tb_program_copy = copy(self.tb_program)
        tb_program_copy.input_list = [p_position.x, p_position.y]
        tb_program_copy.run_until_next_outputs()
        return tb_program_copy.output_list[0] == 1

    def calc_scan_item_found(self, p_position_to: Position2D) -> int:
        rv = 0
        for act_y, act_period_from, act_period_to in self.yield_row_period():
            if act_period_from is not None:
                rv += (min(p_position_to.x, act_period_to) - min(p_position_to.x, act_period_from) + 1)
            if act_y == p_position_to.y:
                return rv

    def scan_for_solid_rectangle(self, p_width: int, p_height: int) -> Position2D:
        row_dynamic_dict = {}
        for act_y, act_period_from, act_period_to in self.yield_row_period():
            row_dynamic_dict[act_y] = (act_period_from, act_period_to)
            if act_y - p_height + 1 in row_dynamic_dict:
                prev_period_from, prev_period_to = row_dynamic_dict.pop(act_y - p_height + 1)
                if prev_period_from is None:
                    continue
                if prev_period_to - act_period_from >= p_width - 1:
                    return Position2D(act_period_from, act_y - p_height + 1)

    def yield_row_period(self) -> Iterator[tuple[int, int | None, int | None]]:
        act_x = act_y = 0
        act_period_x_start = None
        start_check_from = 0
        end_check_from = 0
        while True:
            if self.something_found_on_position(Position2D(act_x, act_y)):
                if act_period_x_start is None:
                    act_period_x_start = act_x
                    act_x = max(act_x, end_check_from - 1)
            elif act_period_x_start is not None:
                yield act_y, act_period_x_start, act_x - 1
                start_check_from = act_period_x_start
                end_check_from = act_x - 1
                act_y += 1
                act_x = start_check_from
                act_period_x_start = None
                continue
            elif act_x > end_check_from + 20:   # empty row
                yield act_y, None, None
                act_y += 1
                act_x = start_check_from
                continue
            act_x += 1


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    num_list = next(yield_input_data(p_input_file_path, p_chars_to_space=','), None)
    g = CTractorBeam(CIntCode(num_list))

    answer1 = g.calc_scan_item_found(Position2D(49, 49))

    ship_position = g.scan_for_solid_rectangle(100, 100)
    answer2 = ship_position.x * 10000 + ship_position.y

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 19, solve_puzzle)


if __name__ == '__main__':
    main()
