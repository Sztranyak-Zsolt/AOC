from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_vector import CVector3D, min_vector, max_vector
from GENERICS.aoc_space import CSpaceBase
from functools import cached_property


class CCube:
    def __init__(self, p_vector1: CVector3D = CVector3D(0, 0, 0), p_vector2: CVector3D = CVector3D(0, 0, 0)):
        self.min_corner = min_vector(p_vector1, p_vector2)
        self.max_corner = max_vector(p_vector1, p_vector2)
        self.cubes_below: set[CCube] = set()
        self.cubes_above: set[CCube] = set()

    @cached_property
    def all_cubes_below(self):
        rs = set(self.cubes_below)
        to_be_checked_cubes = rs.copy()
        for c in to_be_checked_cubes:
            rs |= c.all_cubes_below
        return rs

    @cached_property
    def all_cubes_above(self):
        rs = set(self.cubes_above)
        to_be_checked_cubes = rs.copy()
        for c in to_be_checked_cubes:
            rs |= c.all_cubes_above
        return rs

    def offset_cube(self, p_offset: CVector3D):
        self.min_corner += p_offset
        self.max_corner += p_offset

    def __add__(self, p_vector: CVector3D) -> CCube:
        return CCube(self.min_corner + p_vector, self.max_corner + p_vector)

    def __and__(self, p_other_cube: CCube) -> CCube | None:
        if p_other_cube.max_corner.x < self.min_corner.x \
           or self.max_corner.x < p_other_cube.min_corner.x \
           or p_other_cube.max_corner.y < self.min_corner.y \
           or self.max_corner.y < p_other_cube.min_corner.y \
           or p_other_cube.max_corner.z < self.min_corner.z \
           or self.max_corner.z < p_other_cube.min_corner.z:
            return None
        return CCube(max_vector(self.min_corner, p_other_cube.min_corner),
                     min_vector(self.max_corner, p_other_cube.max_corner))


class CSpace(CSpaceBase):
    def __init__(self):
        super().__init__()
        self.cube_list: list[CCube] = []

    def fall_cubes(self):
        fixed_cubes = [c for c in self.cube_list if c.min_corner.z == 1]
        max_z = max(c.max_corner.z for c in fixed_cubes) + 1
        cubes_to_process = sorted([c for c in self.cube_list if c.min_corner.z != 1], key=lambda c: c.min_corner.z)
        for c in cubes_to_process:
            if max_z < c.min_corner.z:
                c.offset_cube(CVector3D(0, 0, -(c.min_corner.z - max_z)))
            while c.min_corner.z != 1:
                fallen_cube = CCube(c.min_corner - CVector3D(0, 0, 1), c.max_corner - CVector3D(0, 0, 1))
                for fc in fixed_cubes:
                    if fc & fallen_cube:
                        break
                else:
                    c.offset_cube(CVector3D(0, 0, -1))
                    continue
                break
            max_z = max(max_z, c.max_corner.z + 1)
            fixed_cubes.append(c)

    def get_connections(self):
        for c1 in self.cube_list:
            for c2 in [c for c in self.cube_list if c.max_corner.z == c1.min_corner.z - 1]:
                if c2 & (c1 + CVector3D(0, 0, -1)):
                    c1.cubes_below.add(c2)
                    c2.cubes_above.add(c1)
            for c2 in [c for c in self.cube_list if c.min_corner.z - 1 == c1.max_corner.z]:
                if c1 & (c2 + CVector3D(0, 0, -1)):
                    c2.cubes_below.add(c1)
                    c1.cubes_above.add(c2)

    def cubes_disintegration(self) -> tuple[int, int]:
        self.get_connections()
        cubes_to_be_dis = set(self.cube_list)
        for c in self.cube_list:
            if len(c.cubes_below) == 1:
                cubes_to_be_dis -= c.cubes_below
        rv = 0
        for c in self.cube_list:
            if c in cubes_to_be_dis:
                continue
            for hc in c.all_cubes_above:
                if not hc.all_cubes_below - c.all_cubes_below - c.all_cubes_above - {c}:
                    rv += 1
        return len(cubes_to_be_dis), rv


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    s = CSpace()
    for x1, y1, z1, x2, y2, z2 in yield_input_data(p_input_file_path, p_chars_to_space=',~'):
        s.cube_list.append(CCube(CVector3D(x1, y1, z1), CVector3D(x2, y2, z2)))
    s.fall_cubes()
    answer1, answer2 = s.cubes_disintegration()

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 22, solve_puzzle)


if __name__ == '__main__':
    main()
