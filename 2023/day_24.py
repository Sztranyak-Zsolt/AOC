import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_vector import CVector3D
from GENERICS.aoc_space import CPlaneLine, lines_intersection, CPlane, line_from_two_points, plane_from_three_points,\
    plane_line_intersection
from typing import Iterator
from copy import copy
from fractions import Fraction


class CPlaneX(CPlane):
    def __init__(self):
        super().__init__()
        self.hailstone_list: list[CPlaneLine] = []

    def hailstone_crosses_xy(self) -> Iterator[tuple[CVector3D, int, int]]:
        for i1, hs1 in enumerate(self.hailstone_list):
            for hs2 in self.hailstone_list[i1+1:]:
                hs1xy, hs2xy = copy(hs1), copy(hs2)
                hs1xy.eliminate_dimension(2)
                hs2xy.eliminate_dimension(2)
                if hs_xy_cross := lines_intersection(hs1xy, hs2xy):
                    yield hs_xy_cross, hs1xy.calc_t(hs_xy_cross), hs2xy.calc_t(hs_xy_cross)

    def calc_perfect_position_pl(self):
        # Calculation first determine an adjustment vector, which can be used to adjust lines to be parallel.
        # These parallel lines determine a plane.
        # Other adjusted lines crosses that plane in the same time as the original line crosses the result line
        # -> the sought vector can be calculated by these crosses

        i1 = i2 = 0
        lines = set()
        # construction adjusted vector and plane
        while i1 != len(self.hailstone_list):
            i2 += 1
            if i2 == len(self.hailstone_list):
                i1 += 1
                i2 = i1
                continue
            hs1 = self.hailstone_list[i1]
            hs2 = self.hailstone_list[i2]
            if hs1.point0 == hs2.point0 or hs1.a == hs2.a or hs1.b == hs2.b or hs1.c == hs2.c:
                continue
            hs_parallel1, hs_parallel2 = copy(hs1), copy(hs2)
            # vectors to be adjusted in order to lines to be parallel and a plane can be determined
            vector_adjustment = CVector3D(0, 0, 0)
            for d in range(3):
                target_dim_value = Fraction(abs(hs1.vector[d] - hs2.vector[d]), 2)
                vector_adjustment[d] = max(hs1.vector[d], hs2.vector[d]) - target_dim_value
            hs_parallel1.vector -= vector_adjustment
            hs_parallel2.vector -= vector_adjustment
            adjusted_plane = plane_from_three_points(hs_parallel1.point0, hs_parallel1.point0 + hs_parallel1.vector,
                                                     hs_parallel2.point0)
            break
        else:
            return
        prev_cross = None
        for hs in self.hailstone_list:
            if hs in [hs1, hs2]:
                continue
            hs_adjusted = copy(hs)
            hs_adjusted.vector -= vector_adjustment
            cross_2d = plane_line_intersection(adjusted_plane, hs_adjusted)
            # collision time can be calculated by the cross of the adjusted line and the plane
            control_t = hs_adjusted.calc_t(cross_2d)
            # with the known t the collision point can be determined
            act_cross = (hs.point_by_t(control_t), control_t)
            if prev_cross:
                act_line = line_from_two_points(prev_cross[0], act_cross[0], prev_cross[1], act_cross[1])
                lines.add(act_line)
            prev_cross = act_cross
        if len(lines) == 1:
            return lines.pop()


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    limit1, limit2 = 200000000000000, 400000000000000
    p = CPlaneX()
    for x1, y1, z1, vx1, vy1, vz1 in yield_input_data(p_input_file_path, p_chars_to_space=',@'):
        p.hailstone_list.append(line_from_two_points(CVector3D(x1, y1, z1),
                                                     CVector3D(x1, y1, z1) + CVector3D(vx1, vy1, vz1)))
    for cross, t1, t2 in p.hailstone_crosses_xy():
        if t1 >= 0 and t2 >= 0 and limit1 <= cross.x <= limit2 and limit1 <= cross.y <= limit2:
            answer1 += 1
    base_line = p.calc_perfect_position_pl()
    if base_line:
        answer2 = sum(base_line.point0)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 24, solve_puzzle)


if __name__ == '__main__':
    main()
