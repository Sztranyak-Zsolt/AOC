import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D


class CMirror(CGridBase):

    def vertical_mirror(self, p_smudge_count: int = 0) -> int:
        for x in range(self.min_x, self.max_x):
            difi = 0
            for p in self.position_dict:
                x_mirror = 2 * x - p.x + 1
                if x_mirror < self.min_x or x_mirror > self.max_x:
                    continue
                if Position2D(x_mirror, p.y) not in self.position_dict:
                    difi += 1
            if difi == p_smudge_count:
                return x + 1
        return 0

    def horizontal_mirror(self, p_smudge_count: int = 0) -> int:
        for y in range(self.min_y, self.max_y):
            difi = 0
            for p in self.position_dict:
                y_mirror = 2 * y - p.y + 1
                if y_mirror < self.min_y or y_mirror > self.max_y:
                    continue
                if Position2D(p.x, y_mirror) not in self.position_dict:
                    difi += 1
            if difi == p_smudge_count:
                return y + 1
        return 0


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    for inp_group in yield_input_data(p_input_file_path, p_whole_row=True, p_group_separator='\n\n'):
        nm = CMirror()
        for inp_row in inp_group:
            nm.add_row(inp_row, p_chars_to_skip='.')
        answer1 += nm.vertical_mirror() + nm.horizontal_mirror() * 100
        answer2 += nm.vertical_mirror(1) + nm.horizontal_mirror(1) * 100

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 13, solve_puzzle)


if __name__ == '__main__':
    main()
