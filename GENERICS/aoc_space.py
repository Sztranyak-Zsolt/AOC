from __future__ import annotations
from math import gcd
from typing import Self
from GENERICS.aoc_vector import CVector3D, Position3D, TP3D
from copy import copy
from fractions import Fraction


class CSpaceBase:
    def __init__(self):
        self.position_dict: dict[TP3D, str | bool | int] = {}
        self.act_orientation: Position3D = Position3D(1, 2, 3)
        self.other_orientations: dict[Position3D, Self] = {}
        self.position_type: type[TP3D] = Position3D
        self.min_vector = CVector3D(0, 0, 0)
        self.max_vector = CVector3D(0, 0, 0)

    @property
    def min_x(self):
        return self.min_vector.x

    @min_x.setter
    def min_x(self, p_min_x: int):
        self.min_vector = CVector3D(p_min_x, self.min_vector.y, self.min_vector.z)

    @property
    def min_y(self):
        return self.min_vector.y

    @min_y.setter
    def min_y(self, p_min_y: int):
        self.min_vector = CVector3D(self.min_vector.x, p_min_y, self.min_vector.z)

    @property
    def min_z(self):
        return self.min_vector.z

    @min_z.setter
    def min_z(self, p_min_z: int):
        self.min_vector = CVector3D(self.min_vector.x, self.min_vector.y, p_min_z)

    @property
    def max_x(self):
        return self.max_vector.x

    @max_x.setter
    def max_x(self, p_max_x: int):
        self.max_vector = CVector3D(p_max_x, self.max_vector.y, self.max_vector.z)

    @property
    def max_y(self):
        return self.max_vector.y

    @max_y.setter
    def max_y(self, p_max_y: int):
        self.max_vector = CVector3D(self.max_vector.x, p_max_y, self.max_vector.z)

    @property
    def max_z(self):
        return self.max_vector.z

    @max_z.setter
    def max_z(self, p_max_z: int):
        self.max_vector = CVector3D(self.max_vector.x, self.max_vector.y, p_max_z)

    @property
    def normalized_space(self):
        if all([p == 0 for p in self.min_vector]) or not self.position_dict:
            return self
        return self.offset_space(self.position_type(-self.min_x, -self.min_y, -self.min_z))

    def offset_space(self, p_vector: TP3D) -> Self:
        new_offset_space = self.__class__()
        new_offset_space.position_type = self.position_type
        new_offset_space.min_vector = self.min_vector + CVector3D(*p_vector)
        new_offset_space.max_vector = self.max_vector + CVector3D(*p_vector)
        for act_position, act_value in self.position_dict.items():
            new_offset_space.add_item(self.position_type(act_position.x + p_vector.x, act_position.y + p_vector.y,
                                                         act_position.z + p_vector.z), act_value)
        return new_offset_space

    def set_other_orientations(self):
        if self.position_type != CVector3D:
            raise NotImplementedError('Function is used only with CVector3D position_type!')
        self.other_orientations[self.act_orientation] = self
        min_vector = CVector3D(self.min_x, self.min_y, self.min_z)
        for min_vector_orientation, new_min_vector in min_vector.rotations_dict.items():
            if min_vector_orientation == self.act_orientation:
                continue
            new_space = self.other_orientations[Position3D(*min_vector_orientation)] = self.__class__()
            new_space.position_type = self.position_type
            new_space.act_orientation = Position3D(*min_vector_orientation)
            new_space.other_orientations = self.other_orientations
            new_space.min_vector = new_space.max_vector = new_min_vector
        max_vector = CVector3D(self.max_x, self.max_y, self.max_z)
        for max_vector_orientation, new_max_vector in max_vector.rotations_dict.items():
            if max_vector_orientation == self.act_orientation:
                continue
            new_space = self.other_orientations[Position3D(*max_vector_orientation)]
            new_space.min_vector = CVector3D(min(new_space.min_x, new_max_vector.x),
                                             min(new_space.min_y, new_max_vector.y),
                                             min(new_space.min_z, new_max_vector.z))
            new_space.max_vector = CVector3D(max(new_space.min_x, new_max_vector.x),
                                             max(new_space.min_y, new_max_vector.y),
                                             max(new_space.min_z, new_max_vector.z))
        for act_vector, act_value in self.position_dict.items():
            for vector_orientation, new_vector in act_vector.rotations_dict.items():
                if vector_orientation == self.act_orientation:
                    continue
                self.other_orientations[Position3D(*vector_orientation)].add_item(new_vector, act_value)

    def add_item(self, p_position: TP3D, p_item: str | int | bool,
                 set_border_on_init: bool = False):
        if not self.position_dict:
            self.position_type = type(p_position)
        self.position_dict[p_position] = p_item
        if len(self.position_dict) != 1 or not set_border_on_init:
            self.min_vector = CVector3D(min(self.min_x, p_position.x), min(self.min_y, p_position.y),
                                        min(self.min_z, p_position.z))
            self.max_vector = CVector3D(max(self.max_x, p_position.x), max(self.max_y, p_position.y),
                                        max(self.max_z, p_position.z))
        else:
            self.min_vector = CVector3D(p_position.x, p_position.y, p_position.z)
            self.max_vector = CVector3D(p_position.x, p_position.y, p_position.z)

    def __copy__(self) -> Self:
        new_instance = self.__class__()
        new_instance.min_vector = copy(self.min_vector)
        new_instance.max_vector = copy(self.max_vector)
        new_instance.position_type = self.position_type
        new_instance.act_orientation = self.act_orientation
        new_instance.position_dict = copy(self.position_dict)
        return new_instance


def line_from_two_points(p_p: Position3D | CVector3D, p_q: Position3D | CVector3D, p_t_p: int = 0, p_t_q: int = 1):
    if p_t_p == p_t_q:
        raise ValueError('Line cannot be calculated for the same time parameter.')
    if p_p == p_q:
        raise ValueError('Line cannot be calculated for the same points.')
    a = Fraction(p_q.x - p_p.x, p_t_q - p_t_p)
    if a.denominator == 1:
        a = int(a)
    b = Fraction(p_q.y - p_p.y, p_t_q - p_t_p)
    if b.denominator == 1:
        b = int(b)
    c = Fraction(p_q.z - p_p.z, p_t_q - p_t_p)
    if c.denominator == 1:
        c = int(c)
    point0 = p_p - CVector3D(a, b, c) * p_t_p
    return CPlaneLine(point0, a, b, c)


def plane_from_three_points(p_p: Position3D | CVector3D,
                            p_q: Position3D | CVector3D,
                            p_r: Position3D | CVector3D):
    rp = CPlane()
    v_pq = (p_q.x - p_p.x, p_q.y - p_p.y, p_q.z - p_p.z)
    v_pr = (p_r.x - p_p.x, p_r.y - p_p.y, p_r.z - p_p.z)
    v_pq_x_pr = (v_pq[1] * v_pr[2] - v_pq[2] * v_pr[1],
                 v_pq[2] * v_pr[0] - v_pq[0] * v_pr[2],
                 v_pq[0] * v_pr[1] - v_pq[1] * v_pr[0])

    rp.a, rp.b, rp.c = v_pq_x_pr
    rp.d = -(p_p[0] * rp.a + p_p[1] * rp.b + p_p[2] * rp.c)
    if isinstance(rp.a, Fraction) and rp.a.denominator == 1:
        rp.a = int(rp.a)
    if isinstance(rp.b, Fraction) and rp.b.denominator == 1:
        rp.b = int(rp.b)
    if isinstance(rp.c, Fraction) and rp.c.denominator == 1:
        rp.c = int(rp.c)
    if isinstance(rp.d, Fraction) and rp.d.denominator == 1:
        rp.d = int(rp.d)
    if isinstance(rp.a, int) and isinstance(rp.b, int) and isinstance(rp.c, int) and isinstance(rp.d, int):
        simpl = gcd(rp.a, rp.b, rp.c, rp.d)
        rp.a //= simpl
        rp.b //= simpl
        rp.c //= simpl
        rp.d //= simpl
    return rp


def planes_intersection(p_plane1: CPlane, p_plane2: CPlane) -> CPlaneLine:
    rpl = CPlaneLine()
    rpl.a = p_plane1.b * p_plane2.c - p_plane1.c * p_plane2.b
    rpl.b = p_plane1.c * p_plane2.a - p_plane1.a * p_plane2.c
    rpl.c = p_plane1.a * p_plane2.b - p_plane1.b * p_plane2.a
    if rpl.c != 0:
        x = Fraction(p_plane2.d * p_plane1.b - p_plane1.d * p_plane2.b, rpl.c)
        if x.denominator == 1:
            x = int(x)
        y = Fraction(p_plane1.d * p_plane2.a - p_plane2.d * p_plane1.a, rpl.c)
        if y.denominator == 1:
            y = int(y)
        rpl.point0 = Position3D(x, y, 0)
    elif rpl.b != 0:
        x = Fraction(p_plane1.d * p_plane2.c - p_plane2.d * p_plane1.c, rpl.b)
        if x.denominator == 1:
            x = int(x)
        z = Fraction(p_plane2.d * p_plane1.a - p_plane1.d * p_plane2.a, rpl.b)
        if z.denominator == 1:
            z = int(z)
        rpl.point0 = Position3D(x, 0, z)
    elif rpl.a != 0:
        y = Fraction(p_plane2.d * p_plane1.c - p_plane1.d * p_plane2.c, rpl.a)
        if y.denominator == 1:
            y = int(y)
        z = Fraction(p_plane1.d * p_plane2.b - p_plane2.d * p_plane1.b, rpl.a)
        if z.denominator == 1:
            z = int(z)
        rpl.point0 = Position3D(0, y, z)
    return rpl


def lines_intersection(p_line1: CPlaneLine, p_line2: CPlaneLine) -> CVector3D | None:
    if p_line1.point0 == p_line2.point0:
        return copy(p_line1.point0)
    for v1, v2, v3 in [(0, 1, 2), (0, 2, 1), (1, 2, 0)]:
        if p_line1.vector[v1] != 0:
            if p_line2.vector[v2] - p_line1.vector[v2] * Fraction(p_line2.vector[v1], p_line1.vector[v1]) != 0:
                t2 = Fraction(p_line1.point0[v2] - p_line2.point0[v2] + p_line1.vector[v2]
                              * Fraction(p_line2.point0[v1] - p_line1.point0[v1], p_line1.vector[v1]),
                              p_line2.vector[v2] - p_line1.vector[v2]
                              * Fraction(p_line2.vector[v1], p_line1.vector[v1]))
                t1 = Fraction(p_line2.point0[v1] - p_line1.point0[v1] + p_line2.vector[v1] * t2, p_line1.vector[v1])
                if p_line1.point0[v3] + p_line1.vector[v3] * t1 != p_line2.point0[v3] + p_line2.vector[v3] * t2:
                    return None
                return p_line1.point0 + p_line1.vector * t1


def plane_line_intersection(p_plane: CPlane, p_plane_line: CPlaneLine) -> Position3D | CVector3D:
    # plane_a * (x0 + t * line_a) + plane_b * (y0 + t * line_b) + plane_c * (z0 + t * line_c) + plane_d = 0
    # t = -(plane_a * x0 + plane_b * y0 + plane_c * z0 + plane_d)
    #         / (plane_a * line_a + plane_b * line_b + plane_c * line_c)
    t0 = p_plane.a * p_plane_line.a + p_plane.b * p_plane_line.b + p_plane.c * p_plane_line.c
    t1 = -(p_plane.a * p_plane_line.point0.x + p_plane.b * p_plane_line.point0.y
           + p_plane.c * p_plane_line.point0.z + p_plane.d)
    t = Fraction(t1, t0)
    if t.denominator == 1:
        t = int(t)
    if isinstance(p_plane_line.point0, CVector3D):
        return CVector3D(p_plane_line.point0.x + t * p_plane_line.a,
                         p_plane_line.point0.y + t * p_plane_line.b,
                         p_plane_line.point0.z + t * p_plane_line.c)
    return Position3D(p_plane_line.point0.x + t * p_plane_line.a,
                      p_plane_line.point0.y + t * p_plane_line.b,
                      p_plane_line.point0.z + t * p_plane_line.c)


class CPlane:
    def __init__(self, p_a: int = 0, p_b: int = 0, p_c: int = 0, p_d: int = 0):
        # plane equation: a * x + b * y + c * z + d = 0
        self.a = p_a
        self.b = p_b
        self.c = p_c
        self.d = p_d

    def __and__(self, other: CPlane | CPlaneLine) -> CPlaneLine | Position3D | CVector3D:
        if isinstance(other, CPlane):
            return planes_intersection(self, other)
        if isinstance(other, CPlaneLine):
            return plane_line_intersection(self, other)

    def __str__(self):
        return f'{self.a} * x + {self.b} * y + {self.c} * z + {self.d} = 0'


class CPlaneLine:
    def __init__(self,
                 p_point0: Position3D | CVector3D = Position3D(0, 0, 0),
                 p_a: int | Fraction = 0,
                 p_b: int | Fraction = 0,
                 p_c: int | Fraction = 0):
        # x = x0 + a * t; y = y0 + b * t ; z = z0 + c * t
        # X = u1 * λ + x0 ; Y = u2 * λ + y0 ; Z = u3 * λ + z0
        self.point0 = p_point0
        self.vector = CVector3D(p_a, p_b, p_c)

    @property
    def a(self) -> int | Fraction:
        return self.vector[0]

    @a.setter
    def a(self, p_a):
        self.vector[0] = p_a

    @property
    def b(self) -> int | Fraction:
        return self.vector[1]

    @b.setter
    def b(self, p_b):
        self.vector[1] = p_b

    @property
    def c(self) -> int | Fraction:
        return self.vector[2]

    @c.setter
    def c(self, p_c):
        self.vector[2] = p_c

    def eliminate_dimension(self, p_dimension: int):
        self.point0 = self.point0.__class__(*[v if i != p_dimension else 0 for i, v in enumerate(self.point0)])
        self.vector[p_dimension] = 0

    def adjust_point0_with_t(self, p_t: int | Fraction):
        self.point0 += self.vector * p_t
        if isinstance(self.a, Fraction) and self.a.denominator == 1:
            self.a = int(self.a)
        if isinstance(self.b, Fraction) and self.b.denominator == 1:
            self.b = int(self.b)
        if isinstance(self.c, Fraction) and self.c.denominator == 1:
            self.c = int(self.c)

    def point_by_t(self, p_t: int | Fraction):
        act_point = copy(self.point0)
        act_point += self.vector * p_t
        if isinstance(self.a, Fraction) and self.a.denominator == 1:
            self.a = int(self.a)
        if isinstance(self.b, Fraction) and self.b.denominator == 1:
            self.b = int(self.b)
        if isinstance(self.c, Fraction) and self.c.denominator == 1:
            self.c = int(self.c)
        return act_point

    def calc_t(self, p_position: CVector3D) -> int | Fraction | None:
        if self.point0 == p_position:
            return 0
        if self.a == 0 and self.point0.x != p_position.x \
                or self.b == 0 and self.point0.y != p_position.y \
                or self.c == 0 and self.point0.z != p_position.z:
            return None
        for v in range(3):
            if p_position[v] != self.point0[v]:
                t = Fraction(p_position[v] - self.point0[v], self.vector[v])
                if isinstance(t, Fraction) and t.denominator == 1:
                    t = int(t)
                if self.point0 + self.vector * t == p_position:
                    return t
                return None

    def __and__(self, other: CPlane | CPlaneLine) -> Position3D | CVector3D:
        if isinstance(other, CPlane):
            return plane_line_intersection(other, self)
        if isinstance(other, CPlaneLine):
            return lines_intersection(self, other)

    def __str__(self):
        return f'x = {self.point0.x} + {self.a} * t ; ' \
               f'y = {self.point0.y} + {self.b} * t ; ' \
               f'z = {self.point0.z} + {self.c} * t'

    def __copy__(self):
        new_instance = self.__class__()
        new_instance.point0 = copy(self.point0)
        new_instance.a = self.a
        new_instance.b = self.b
        new_instance.c = self.c
        return new_instance

    def __hash__(self):
        return hash(tuple(self.point0.position_list + self.vector.position_list))

    def __eq__(self, other):
        return self.point0 == other.point0 and self.vector == other.vector


def main():
    pass


if __name__ == '__main__':
    main()
