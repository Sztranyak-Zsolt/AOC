import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from functools import cached_property


class CShape:
    def __init__(self):
        self.grid = []

    @cached_property
    def count_tiles(self) -> int:
        rv = 0
        for act_row in self.grid:
            rv += act_row.count('#')
        return rv

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        return self is other


class CRegion:
    def __init__(self, p_height: int, p_width: int):
        self.height = p_height
        self.width = p_width
        self.present_dict: dict[CShape, int] = {}

    @cached_property
    def present_tiles_count(self):
        return sum(iter(pc * p.count_tiles for p, pc in self.present_dict.items()), start=0)

    @property
    def region_area(self):
        return self.height * self.width

    @property
    def min_3x3_area(self) -> int:
        return (self.height // 3) * (self.width // 3)

    def check_can_fit(self) -> bool | None:
        # edge cases
        if self.min_3x3_area >= sum(self.present_dict.values()):
            return True
        if self.present_tiles_count > self.region_area:
            return False
        # non-edge cases - to be implemented
        raise NotImplementedError


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = 0
    shape_list = []
    region_list = []
    act_shape = CShape()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space=':x'):
        if not inp_row:
            continue
        if len(inp_row) == 1:
            if isinstance(inp_row[0], int):
                act_shape = CShape()
                shape_list.append(act_shape)
            else:
                act_shape.grid.append(inp_row[0])
            continue
        region_x, region_y, *shape_count = inp_row
        act_region = CRegion(region_x, region_y)
        region_list.append(act_region)
        for sh, sh_count in zip(shape_list, shape_count):
            act_region.present_dict[sh] = int(sh_count)
    for region in region_list:
        if region.check_can_fit():
            answer1 += 1
    return answer1, None


def main():
    aoc_solve_puzzle(2025, 12, solve_puzzle)


if __name__ == '__main__':
    main()
