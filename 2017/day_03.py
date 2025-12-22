import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import neighbor_positions, CVector2D


class CSpiral(CGridBase):
    directions = [CVector2D(0, 1), CVector2D(1, 0), CVector2D(0, -1), CVector2D(-1, 0)]

    def __init__(self, p_advanced_spiral: bool = False):
        super().__init__()
        self.act_dir_index = 0
        self.last_position: CVector2D | None = None
        self.advanced_spiral = p_advanced_spiral

    def add_spiral_item(self) -> int:
        if self.last_position is None:
            self.position_dict[CVector2D(0, 0)] = 1
            self.last_position = CVector2D(0, 0)
            return 1
        next_dir_index = (self.act_dir_index + 1) % 4
        if self.last_position + self.directions[next_dir_index] not in self.position_dict:
            self.act_dir_index = next_dir_index
        next_position = self.last_position + self.directions[self.act_dir_index]
        if not self.advanced_spiral:
            act_item_value = self.position_dict[self.last_position]
            self.last_position = next_position
            self.position_dict[next_position] = act_item_value + 1
            return act_item_value + 1
        next_item_value = 0
        for np in neighbor_positions(next_position, True, True):
            if np in self.position_dict:
                next_item_value += self.position_dict[np]
        self.last_position = next_position
        self.position_dict[next_position] = next_item_value
        return next_item_value


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    input_num = next(yield_input_data(p_input_file_path, p_whole_row=True), None)
    s1 = CSpiral()
    while s1.add_spiral_item() <= input_num:
        pass
    answer1 = int(s1.last_position) - 1

    s2 = CSpiral(True)
    while (answer2 := s2.add_spiral_item()) <= input_num:
        pass

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 3, solve_puzzle)


if __name__ == '__main__':
    main()
