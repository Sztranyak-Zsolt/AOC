from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, add_positions


class CGrid(CGridBase):

    def cycle_beam(self):
        for act_push in [Position2D(0, 1), Position2D(-1, 0), Position2D(0, -1), Position2D(1, 0)]:
            self.push_rocks(act_push)

    def push_rocks(self, p_direction: Position2D):
        rock_pos_list = sorted([k for k, v in self.position_dict.items() if v == 'O'],
                               key=lambda rp: (-rp.x * p_direction.x, -rp.y * p_direction.y))
        for act_rock in rock_pos_list:
            del self.position_dict[act_rock]
            while True:
                next_position = add_positions(act_rock, p_direction)
                if next_position in self.position_dict \
                        or next_position.x in [self.min_x - 1, self.max_x + 1] \
                        or next_position.y in [self.min_y - 1, self.max_y + 1]:
                    break
                act_rock = next_position
            self.position_dict[act_rock] = 'O'

    @property
    def total_load(self) -> int:
        return sum(k.y + 1 for k, v in self.position_dict.items() if v == 'O')

    @property
    def rocks_state(self):
        return tuple(sorted(k for k, v in self.position_dict.items() if v == 'O'))


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    g = CGrid()
    g2 = CGrid()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True):
        g.add_row(inp_row, p_chars_to_skip='.')
        g2.add_row(inp_row, p_chars_to_skip='.')

    g.push_rocks(Position2D(0, 1))
    answer1 = g.total_load

    period_dict = {}
    total_load_dict = {}
    cycle_length = 1000000000
    for i in range(1, cycle_length + 1):
        g2.cycle_beam()
        if (act_state := g2.rocks_state) in period_dict:
            period_start = period_dict[act_state]
            period_length = i - period_start
            act_period_item = period_start // period_length * period_length + cycle_length % period_length
            if act_period_item < period_start:
                period_start += period_length
            answer2 = total_load_dict[act_period_item]
            break
        period_dict[act_state] = i
        total_load_dict[i] = g2.total_load
    else:
        answer2 = g2.total_load

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 14, solve_puzzle)


if __name__ == '__main__':
    main()
