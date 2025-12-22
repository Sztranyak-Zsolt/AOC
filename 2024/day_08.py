import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import CVector2D


class CMap(CGridBase):
    def count_antinodes(self, p_advanced_method: bool = False) -> int:
        an_set = set()
        for k1, v1 in self.position_dict.items():
            for k2, v2 in self.position_dict.items():
                if v1 != v2 or k1 >= k2:
                    continue
                if p_advanced_method:
                    an_set.add(k1)
                    an_set.add(k2)
                dif = k2 - k1
                if1 = k1 - dif
                while self.min_x <= if1.x <= self.max_x and self.min_y <= if1.y <= self.max_y:
                    an_set.add(if1)
                    if not p_advanced_method:
                        break
                    if1 = if1 - dif
                if2 = k2 + dif
                while self.min_x <= if2.x <= self.max_x and self.min_y <= if2.y <= self.max_y:
                    an_set.add(if2)
                    if not p_advanced_method:
                        break
                    if2 = if2 + dif
        return len(an_set)


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    m = CMap()
    for inp_row in yield_input_data(p_input_file_path,
                                    p_whole_row=True,
                                    p_reversed=True
                                    ):
        m.add_row(inp_row, p_position_type=CVector2D, p_chars_to_skip='.')
    answer1 = m.count_antinodes()
    answer2 = m.count_antinodes(True)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 8, solve_puzzle)


if __name__ == '__main__':
    main()
