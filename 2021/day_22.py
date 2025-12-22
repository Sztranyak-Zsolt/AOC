from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_vector import CVector3D
from copy import copy


class CCube:
    def __init__(self,
                 p_min_vector: CVector3D = CVector3D(0, 0, 0),
                 p_max_vector: CVector3D = CVector3D(0, 0, 0),
                 p_is_on: bool = True):
        self.min_vector = p_min_vector
        self.max_vector = p_max_vector
        self.is_on = p_is_on

    @property
    def is_small(self):
        return -50 <= min(self.min_vector) and max(self.max_vector) <= 50

    def calc_volume(self):
        return (self.max_vector.x + 1 - self.min_vector.x) * (self.max_vector.y + 1 - self.min_vector.y) \
            * (self.max_vector.z + 1 - self.min_vector.z)

    def has_intersection(self, other: CCube) -> bool:
        for c in range(3):
            if self.max_vector[c] < other.min_vector[c] or other.max_vector[c] < self.min_vector[c]:
                return False
        return True

    def split_cube(self, p_axis_rank: int, p_axis_value: int) -> list[CCube, CCube] | None:
        if self.min_vector[p_axis_rank] < p_axis_value <= self.max_vector[p_axis_rank]:
            c1 = copy(self)
            c1.max_vector = CVector3D(*[p_axis_value - 1 if i == p_axis_rank else p
                                        for i, p in enumerate(self.max_vector)])
            c2 = copy(self)
            c2.min_vector = CVector3D(*[p_axis_value if i == p_axis_rank else p
                                        for i, p in enumerate(self.min_vector)])
            return [c1, c2]

    def __copy__(self) -> CCube:
        new_instance = CCube()
        new_instance.min_vector = copy(self.min_vector)
        new_instance.max_vector = copy(self.max_vector)
        new_instance.is_on = self.is_on
        return new_instance

    def __str__(self):
        return f'{self.__class__.__name__}: ' \
               f'{self.min_vector.x}..{self.max_vector.x}, ' \
               f'{self.min_vector.y}..{self.max_vector.y} ' \
               f'{self.min_vector.z}..{self.max_vector.z}'


class CUniverse:
    def __init__(self):
        self.cube_list: list[CCube] = list()

    def add_cube(self, p_cube: CCube):
        act_cube_list = self.cube_list.copy()
        new_cube_list = []
        for prev_cube in act_cube_list:
            if p_cube.has_intersection(prev_cube):
                for act_axis in range(3):
                    if sc_list := prev_cube.split_cube(act_axis, p_cube.min_vector[act_axis]):
                        act_cube_list.extend(sc_list)
                        break
                    if sc_list := prev_cube.split_cube(act_axis, p_cube.max_vector[act_axis] + 1):
                        act_cube_list.extend(sc_list)
                        break
            else:
                new_cube_list.append(prev_cube)
        if p_cube.is_on:
            new_cube_list.append(p_cube)
        self.cube_list = new_cube_list

    @property
    def count_lit(self):
        return sum([x.calc_volume() for x in self.cube_list])


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    u = CUniverse()
    u2 = CUniverse()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space='xyz.=,'):
        c = CCube(CVector3D(*inp_row[1::2]), CVector3D(*inp_row[2::2]), inp_row[0] == 'on')
        if c.is_small:
            u.add_cube(c)
        u2.add_cube(c)

    answer1 = u.count_lit
    answer2 = u2.count_lit

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 22, solve_puzzle)


if __name__ == '__main__':
    main()
