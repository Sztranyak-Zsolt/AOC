from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, add_positions, mh_distance, neighbor_positions


class CSpiral(CGridBase):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, p_advanced_spiral: bool = False):
        super().__init__()
        self.act_dir_index = 0
        self.last_position: tuple[int, int] | None = None
        self.advanced_spiral = p_advanced_spiral

    def add_spiral_item(self) -> int:
        if self.last_position is None:
            self.position_dict[(0, 0)] = 1
            self.last_position = (0, 0)
            return 1
        next_dir_index = (self.act_dir_index + 1) % 4
        if add_positions(self.last_position, self.directions[next_dir_index]) not in self.position_dict:
            self.act_dir_index = next_dir_index
        next_position = add_positions(self.last_position, self.directions[self.act_dir_index])
        if not self.advanced_spiral:
            act_item_value = self.position_dict[self.last_position]
            self.last_position = next_position
            self.position_dict[next_position] = act_item_value + 1
            return act_item_value + 1
        next_item_value = 0
        for np_x, np_y in neighbor_positions(next_position, True, True):
            if (np_x, np_y) in self.position_dict:
                next_item_value += self.position_dict[(np_x, np_y)]
        self.last_position = next_position
        self.position_dict[next_position] = next_item_value
        return next_item_value


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    input_num = next(yield_input_data(p_input_file_path, p_whole_row=True), None)
    s1 = CSpiral()
    while s1.add_spiral_item() <= input_num:
        pass
    answer1 = mh_distance(s1.last_position, (0, 0)) - 1

    s2 = CSpiral(True)
    while (answer2 := s2.add_spiral_item()) <= input_num:
        pass

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 3, solve_puzzle)


if __name__ == '__main__':
    main()
