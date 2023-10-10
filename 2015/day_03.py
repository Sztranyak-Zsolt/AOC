from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, add_positions, DIRS


class CGrid(CGridBase):
    directions = {"v": DIRS.DOWN,
                  "^": DIRS.UP,
                  ">": DIRS.RIGHT,
                  "<": DIRS.LEFT}

    def __init__(self):
        super().__init__()
        self.santa_position = (0, 0)
        self.robot_position = (0, 0)
        self.present_set = {(0, 0)}

    def move_santa(self, p_direction: str):
        self.santa_position = add_positions(self.santa_position, self.directions[p_direction].value)
        self.present_set.add(self.santa_position)

    def move_robot(self, p_direction: str):
        self.robot_position = add_positions(self.robot_position, self.directions[p_direction].value)
        self.present_set.add(self.robot_position)

    def count_house_with_present(self) -> int:
        return len(self.present_set)


def solve_puzzle(p_input_file_path: str) -> (int, int):
    g1 = CGrid()
    g2 = CGrid()
    input_single_row = next(yield_input_data(p_input_file_path, p_whole_row=True), None)
    for i, act_direction in enumerate(input_single_row):
        g1.move_santa(act_direction)
        if i % 2 == 0:
            g2.move_santa(act_direction)
        else:
            g2.move_robot(act_direction)
    answer1 = g1.count_house_with_present()
    answer2 = g2.count_house_with_present()
    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 3, solve_puzzle)


if __name__ == '__main__':
    main()
