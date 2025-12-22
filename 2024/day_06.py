import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, add_positions
from functools import cached_property


class CGuardGrid(CGridBase):
    def __init__(self):
        super().__init__()
        self.guard_pos_orig: Position2D | None = None
        self.guard_face_orig: Position2D | None = None
        self.turn_dict = {Position2D(-1, 0): Position2D(0, 1), Position2D(0, 1): Position2D(1, 0),
                          Position2D(1, 0): Position2D(0, -1), Position2D(0, -1): Position2D(-1, 0)}

    def set_guard(self):
        for k, v in self.position_dict.items():
            if v in '<>v^':
                self.guard_pos_orig = k
                self.guard_face_orig = {'^': Position2D(0, 1), 'v': Position2D(0, -1),
                                        '>': Position2D(1, 0), '<': Position2D(-1, 0)}[v]
        del self.position_dict[self.guard_pos_orig]

    def take_step(self, p_pos: Position2D, p_face: Position2D) -> tuple[Position2D, Position2D]:
        act_pos = p_pos
        act_face = p_face
        for _ in range(3):
            next_pos = add_positions(act_pos, act_face)
            if next_pos in self.position_dict:
                act_face = self.turn_dict[act_face]
                continue
            return next_pos, act_face

    @cached_property
    def guard_path(self) -> set[Position2D]:
        rs = set()
        if self.guard_pos_orig is None:
            self.set_guard()
        rs.add(self.guard_pos_orig)

        act_pos = self.guard_pos_orig
        act_face = self.guard_face_orig

        while True:
            act_pos, act_face = self.take_step(act_pos, act_face)
            if act_pos.x in (self.min_x - 1, self.max_x + 1) or act_pos.y in (self.min_y - 1, self.max_y + 1):
                break
            rs.add(act_pos)
        return rs

    def check_path_is_loop(self, p_pos, p_face) -> bool:
        act_pos = p_pos
        act_face = p_face
        known_path = set()
        known_path.add((act_pos, act_face))
        while True:
            act_pos, act_face = self.take_step(act_pos, act_face)
            if act_pos.x in (self.min_x - 1, self.max_x + 1) or act_pos.y in (self.min_y - 1, self.max_y + 1):
                return False
            if (act_pos, act_face) in known_path:
                return True
            known_path.add((act_pos, act_face))

    def count_loop_obstacle(self) -> int:
        act_pos = self.guard_pos_orig
        act_face = self.guard_face_orig
        pos_loop_ops = {(act_pos, act_face): False}
        while True:
            next_pos, next_face = self.take_step(act_pos, act_face)
            if next_pos.x in (self.min_x - 1, self.max_x + 1) or next_pos.y in (self.min_y - 1, self.max_y + 1):
                break
            if next_pos not in pos_loop_ops:
                self.position_dict[next_pos] = 'O'
                pos_loop_ops[next_pos] = self.check_path_is_loop(act_pos, act_face)
                del self.position_dict[next_pos]
            act_pos, act_face = next_pos, next_face
        return len([v for v in pos_loop_ops.values() if v])


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    g = CGuardGrid()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True):
        g.add_row(inp_row, p_chars_to_skip='.')
    answer1 = len(g.guard_path)
    answer2 = g.count_loop_obstacle()

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 6, solve_puzzle)


if __name__ == '__main__':
    main()
