from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_space import Position3D
from GENERICS.aoc_grid import neighbor_positions
from collections import namedtuple
from typing import Iterator


Position4D = namedtuple('Position4D', ['x', 'y', 'z', 'w'])


def neighbor_positions_4d(p_position: Position3D | Position4D) -> Iterator[Position3D | Position4D]:
    if isinstance(p_position, Position3D):
        for np in neighbor_positions(p_position, p_return_corner=True, p_return_self=True):
            yield np
    else:
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    for w in [-1, 0, 1]:
                        yield Position4D(p_position.x + x, p_position.y + y, p_position.z + z, p_position.w + w)


class CSpace:
    def __init__(self):
        self.cube_positions: set[Position3D | Position4D] = set()

    def gen_next_stage(self):
        checked_position = set()
        new_positions = set()
        for i in self.cube_positions:
            for pos_to_check in neighbor_positions_4d(i):
                if pos_to_check in checked_position:
                    continue
                checked_position.add(pos_to_check)
                neighbor_count = 0
                for pos_neighbor in neighbor_positions_4d(pos_to_check):
                    if pos_neighbor == pos_to_check:
                        continue
                    if pos_neighbor in self.cube_positions:
                        neighbor_count += 1
                if neighbor_count == 3 or neighbor_count == 2 and pos_to_check in self.cube_positions:
                    new_positions.add(pos_to_check)
        self.cube_positions = new_positions


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    s = CSpace()
    s4 = CSpace()

    for y, inp_row in enumerate(yield_input_data(p_input_file_path, p_whole_row=True)):
        for x, act_c in enumerate(inp_row):
            if act_c == '#':
                s.cube_positions.add(Position3D(x, y, 0))
                s4.cube_positions.add(Position4D(x, y, 0, 0))

    for _ in range(6):
        s.gen_next_stage()
        s4.gen_next_stage()

    answer1 = len(s.cube_positions)
    answer2 = len(s4.cube_positions)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 17, solve_puzzle)


if __name__ == '__main__':
    main()
