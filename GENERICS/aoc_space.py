from __future__ import annotations
from math import gcd
from typing import Self
from GENERICS.aoc_vector import CVector3D, Position3D, TP3D
from copy import copy


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
            self.max_vector = CVector3D(min(self.max_x, p_position.x), min(self.max_y, p_position.y),
                                        min(self.max_z, p_position.z))
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


def plane_intersection(p_plane1: CPlane, p_plane2: CPlane) -> CPlaneLine:
    rpl = CPlaneLine()
    rpl.a = p_plane1.b * p_plane2.c - p_plane1.c * p_plane2.b
    rpl.b = p_plane1.c * p_plane2.a - p_plane1.a * p_plane2.c
    rpl.c = p_plane1.a * p_plane2.b - p_plane1.b * p_plane2.a
    if rpl.c != 0:  # z0 = 0
        x0 = (p_plane2.d * p_plane1.b - p_plane1.d * p_plane2.b)
        x = x0 // rpl.c if x0 % rpl.c == 0 else x0 / rpl.c
        y0 = (p_plane1.d * p_plane2.a - p_plane2.d * p_plane1.a)
        y = y0 // rpl.c if y0 % rpl.c == 0 else y0 / rpl.c
        rpl.point0 = Position3D(x, y, 0)
    elif rpl.b != 0:  # y0 = 0
        x0 = (p_plane1.d * p_plane2.c - p_plane2.d * p_plane1.c)
        x = x0 // rpl.b if x0 % rpl.b == 0 else x0 / rpl.b
        z0 = (p_plane2.d * p_plane1.a - p_plane1.d * p_plane2.a)
        z = z0 // rpl.b if z0 % rpl.b == 0 else z0 / rpl.b
        rpl.point0 = Position3D(x, 0, z)
    elif rpl.a != 0:  # x0 = 0
        y0 = (p_plane2.d * p_plane1.c - p_plane1.d * p_plane2.c)
        y = y0 // rpl.a if y0 % rpl.a == 0 else y0 / rpl.a
        z0 = (p_plane1.d * p_plane2.b - p_plane2.d * p_plane1.b)
        z = z0 // rpl.b if z0 % rpl.b == 0 else z0 / rpl.b
        rpl.point0 = Position3D(0, y, z)
    return rpl


def plane_line_intersection(p_plane: CPlane, p_plane_line: CPlaneLine) -> Position3D | CVector3D:
    # plane_a * (x0 + t * line_a) + plane_b * (y0 + t * line_b) + plane_c * (z0 + t * line_c) + plane_d = 0
    # t = -(plane_a * x0 + plane_b * y0 + plane_c * z0 + plane_d)
    #         / (plane_a * line_a + plane_b * line_b + plane_c * line_c)
    t0 = p_plane.a * p_plane_line.a + p_plane.b * p_plane_line.b + p_plane.c * p_plane_line.c
    t1 = -(p_plane.a * p_plane_line.point0.x + p_plane.b * p_plane_line.point0.y
           + p_plane.c * p_plane_line.point0.z + p_plane.d)
    if t1 % t0 == 0:
        t = t1 // t0
    else:
        t = t1 / t0
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

    def get_plane_from_3_points(self, p_p: Position3D | CVector3D, p_q: Position3D | CVector3D,
                                p_r: Position3D | CVector3D):
        v_pq = (p_q.x - p_p.x, p_q.y - p_p.y, p_q.z - p_p.z)
        v_pr = (p_r.x - p_p.x, p_r.y - p_p.y, p_r.z - p_p.z)
        v_pq_x_pr = (v_pq[1] * v_pr[2] - v_pq[2] * v_pr[1],
                     v_pq[2] * v_pr[0] - v_pq[0] * v_pr[2],
                     v_pq[0] * v_pr[1] - v_pq[1] * v_pr[0])
        self.a, self.b, self.c = v_pq_x_pr
        self.d = -(p_p[0] * self.a + p_p[1] * self.b + p_p[2] * self.c)
        simpl = gcd(self.a, self.b, self.c, self.d)
        self.a //= simpl
        self.b //= simpl
        self.c //= simpl
        self.d //= simpl

    def __and__(self, other: CPlane | CPlaneLine) -> CPlaneLine | Position3D | CVector3D:
        if isinstance(other, CPlane):
            return plane_intersection(self, other)
        if isinstance(other, CPlaneLine):
            return plane_line_intersection(self, other)

    def __str__(self):
        return f'{self.a} * x + {self.b} * y + {self.c} * z + {self.d} = 0'


class CPlaneLine:
    def __init__(self):
        # x = x0 + a * t; y = y0 + b * t ; z = z0 + c * t
        # X = u1 * λ + x0 ; Y = u2 * λ + y0 ; Z = u3 * λ + z0
        self.point0: Position3D | CVector3D = Position3D(0, 0, 0)  # x0, y0, z0
        self.a = self.b = self.c = 0

    def get_line_from_2_points(self, p_p: Position3D | CVector3D, p_q: Position3D | CVector3D):
        a = p_q.x - p_p.x
        b = p_q.y - p_p.y
        c = p_q.z - p_p.z
        simpl = gcd(a, b, c)
        self.point0 = p_p
        self.a = a // simpl
        self.b = b // simpl
        self.c = c // simpl

    def __and__(self, other: CPlane) -> Position3D | CVector3D:
        return plane_line_intersection(other, self)

    def __str__(self):
        return f'x = {self.point0.x} + {self.a} * t ; ' \
               f'y = {self.point0.y} + {self.b} * t ; ' \
               f'z = {self.point0.z} + {self.c} * t'


def main():
    pass


if __name__ == '__main__':
    main()
