from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_space import CSpaceBase
from GENERICS.aoc_vector import Position3D, neighbor_positions
from collections import deque
from functools import cached_property


class CSpace(CSpaceBase):
    def __init__(self):
        super().__init__()

    @cached_property
    def outer_space_positions(self) -> set[Position3D]:
        corner1 = Position3D(self.min_x - 1, self.min_y - 1, self.min_z - 1)
        corner2 = Position3D(self.max_x + 1, self.max_y + 1, self.max_z + 1)
        dq = deque([corner1, corner2])
        outer_space_positions = {corner1, corner2}
        while dq:
            act_position = dq.popleft()
            for np in neighbor_positions(act_position):
                if self.min_x - 1 <= np.x <= self.max_x + 1 and self.min_y - 1 <= np.y <= self.max_y + 1 \
                    and self.min_z - 1 <= np.z <= self.max_z + 1 \
                        and np not in outer_space_positions and np not in self.position_dict:
                    dq.append(np)
                    outer_space_positions.add(np)
        return outer_space_positions

    @property
    def calc_outer_open_sides(self) -> int:
        return_int = 0
        for cube_position in self.position_dict:
            for np in neighbor_positions(cube_position):
                if np in self.outer_space_positions:
                    return_int += 1
        return return_int

    @property
    def calc_all_open_sides(self) -> int:
        return_int = 0
        for cube_position in self.position_dict:
            return_int += 6
            for np in neighbor_positions(cube_position):
                if np in self.position_dict:
                    return_int -= 1
        return return_int


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    sp = CSpace()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space=','):
        sp.add_item(Position3D(*inp_row), '#')

    answer1 = sp.calc_all_open_sides
    answer2 = sp.calc_outer_open_sides

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 18, solve_puzzle)


if __name__ == '__main__':
    main()
