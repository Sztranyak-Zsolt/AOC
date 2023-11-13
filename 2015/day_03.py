from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import CVector2D


class CGrid(CGridBase):
    directions = {"v": CVector2D(0, -1),
                  "^": CVector2D(0, 1),
                  ">": CVector2D(1, 0),
                  "<": CVector2D(-1, 0)}

    def __init__(self):
        super().__init__()
        self.santa_position = CVector2D(0, 0)
        self.robot_position = CVector2D(0, 0)
        self.present_set = {CVector2D(0, 0)}
        self.santa_position_set = set()

    def move_santa(self, p_direction: str):
        self.santa_position = self.santa_position + self.directions[p_direction]
        self.present_set.add(self.santa_position)

    def move_robot(self, p_direction: str):
        self.robot_position = self.robot_position + self.directions[p_direction]
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
