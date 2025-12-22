import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, neighbor_positions, add_positions


class CGridOwn(CGridBase):
    def __init__(self):
        super().__init__()

    @property
    def occupied_seats_count(self) -> int:
        return len([x for x in self.position_dict.values() if x == '#'])

    def reset_seats(self):
        for p in self.position_dict:
            self.position_dict[p] = 'L'

    def neighbor_occupied_count(self, p_position: Position2D, p_advanced_method: bool) -> int:
        rv = 0
        if not p_advanced_method:
            for next_position_to_check in neighbor_positions(p_position, p_return_corner=True):
                if self.position_dict.get(next_position_to_check, 'L') == '#':
                    rv += 1
        else:
            for act_dir in neighbor_positions(p_return_corner=True):
                next_position_to_check = add_positions(p_position, act_dir)
                while self.min_x <= next_position_to_check.x <= self.max_x \
                        and self.min_y <= next_position_to_check.y <= self.max_y:
                    if next_position_to_check in self.position_dict:
                        if self.position_dict.get(next_position_to_check, 'L') == '#':
                            rv += 1
                        break
                    next_position_to_check = add_positions(next_position_to_check, act_dir)
        return rv

    def change_seats(self, p_advanced_method: bool):
        has_change = True
        nb_tolerance = 5 if p_advanced_method else 4
        while has_change:
            has_change = False
            new_pos_dict = {}
            for p, s in self.position_dict.items():
                new_pos_dict[p] = s
                occupied_seats_count = self.neighbor_occupied_count(p, p_advanced_method)
                if s == 'L' and occupied_seats_count == 0:
                    new_pos_dict[p] = '#'
                    has_change = True
                elif s == '#' and occupied_seats_count >= nb_tolerance:
                    new_pos_dict[p] = 'L'
                    has_change = True
            self.position_dict = new_pos_dict


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    g = CGridOwn()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True):
        g.add_row(inp_row, p_chars_to_skip='.')

    g.change_seats(False)
    answer1 = g.occupied_seats_count
    g.reset_seats()
    g.change_seats(True)
    answer2 = g.occupied_seats_count

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 11, solve_puzzle)


if __name__ == '__main__':
    main()
