import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import CVector2D


class CLine:
    def __init__(self, p_point1: CVector2D, p_point2: CVector2D):
        self.point1 = p_point1
        self.point2 = p_point2

    @property
    def is_horizontal(self) -> bool:
        return self.point1.x == self.point2.x

    @property
    def is_vertical(self) -> bool:
        return self.point1.y == self.point2.y

    @property
    def is_diagonal(self) -> bool:
        return abs(self.point1.x - self.point2.x) == abs(self.point1.y - self.point2.y)

    def yield_integer_points(self):
        min_vector = (self.point2 - self.point1).min_integer_vector
        act_point = self.point1
        while act_point != self.point2:
            yield act_point
            act_point = act_point + min_vector
        yield act_point


class CGridWithLines(CGridBase):
    def __init__(self):
        super().__init__()
        self.line_list: list[CLine] = []

    @property
    def crosses_count(self):
        return len(['x' for x in self.position_dict.values() if x >= 2])

    def add_horizontal_lines(self):
        for act_line in self.line_list:
            if not act_line.is_horizontal:
                continue
            for act_line_point in act_line.yield_integer_points():
                self.position_dict[act_line_point] = self.position_dict.get(act_line_point, 0) + 1

    def add_vertical_lines(self):
        for act_line in self.line_list:
            if not act_line.is_vertical:
                continue
            for act_line_point in act_line.yield_integer_points():
                self.position_dict[act_line_point] = self.position_dict.get(act_line_point, 0) + 1

    def add_diagonal_lines(self):
        for act_line in self.line_list:
            if not act_line.is_diagonal:
                continue
            for act_line_point in act_line.yield_integer_points():
                self.position_dict[act_line_point] = self.position_dict.get(act_line_point, 0) + 1


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    gwl = CGridWithLines()
    for p1x, p1y, p2x, p2y in yield_input_data(p_input_file_path, p_chars_to_space='->,'):
        gwl.line_list.append(CLine(CVector2D(p1x, p1y), CVector2D(p2x, p2y)))
    gwl.add_horizontal_lines()
    gwl.add_vertical_lines()
    answer1 = gwl.crosses_count
    gwl.add_diagonal_lines()
    answer2 = gwl.crosses_count

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 5, solve_puzzle)


if __name__ == '__main__':
    main()
