from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import mh_distance
from functools import cache, cached_property


class CGrid(CGridBase):
    @cached_property
    def empty_rows_set(self) -> set[int]:
        rs = set()
        for y in range(self.min_y, self.max_y + 1):
            if not [p for p in self.position_dict if p.y == y]:
                rs.add(y)
        return rs

    @cached_property
    def empty_cols_set(self) -> set[int]:
        rs = set()
        for x in range(self.min_x, self.max_x + 1):
            if not [p for p in self.position_dict if p.x == x]:
                rs.add(x)
        return rs

    @cache
    def empty_cols_count(self, p_x1: int, p_x2: int) -> int:
        return len([x for x in range(min(p_x1, p_x2), max(p_x1, p_x2) + 1) if x in self.empty_cols_set])

    @cache
    def empty_rows_count(self, p_y1: int, p_y2: int) -> int:
        return len([y for y in range(min(p_y1, p_y2), max(p_y1, p_y2) + 1) if y in self.empty_rows_set])

    def mh_sum_with_expansion(self, p_expansion_scale: int) -> int:
        rv = 0
        for p1 in self.position_dict:
            for p2 in self.position_dict:
                if p1 >= p2:
                    continue
                rv += mh_distance(p1, p2)
                rv += (p_expansion_scale - 1) * self.empty_cols_count(p1.x, p2.x)
                rv += (p_expansion_scale - 1) * self.empty_rows_count(p1.y, p2.y)
        return rv

    def __hash__(self):
        return id(self)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    g = CGrid()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True,  p_chars_to_space='', p_reversed=True):
        g.add_row(inp_row, p_chars_to_skip='.')
    answer1 = g.mh_sum_with_expansion(2)
    answer2 = g.mh_sum_with_expansion(1000000)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 11, solve_puzzle)


if __name__ == '__main__':
    main()
