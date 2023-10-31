from __future__ import annotations
from collections import namedtuple
from math import gcd
from typing import Self


Position3D = namedtuple('Position3D', ['x', 'y', 'z'])


class CSpaceBase:
    def __init__(self):
        self.position_dict: dict[Position3D, str | bool | int] = {}
        self.min_x = self.min_y = self.min_z = self.max_x = self.max_y = self.max_z = 0
        self.x_mirrored_space: Self | None = None
        self.y_mirrored_space: Self | None = None
        self.z_mirrored_space: Self | None = None
        # self.left_rotated_space: Self | None = None

    def add_item(self, p_position: Position3D, p_item: str | int | bool,
                 set_border_on_init: bool = False):
        self.position_dict[p_position] = p_item
        if len(self.position_dict) != 1 or not set_border_on_init:
            self.min_x = min(self.min_x, p_position.x)
            self.max_x = max(self.max_x, p_position.x)
            self.min_y = min(self.min_y, p_position.y)
            self.max_y = max(self.max_y, p_position.y)
            self.min_z = min(self.min_z, p_position.z)
            self.max_z = max(self.max_z, p_position.z)
        else:
            self.min_x = self.max_x = p_position.x
            self.min_y = self.max_y = p_position.y
            self.min_z = self.max_z = p_position.z


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


def plane_line_intersection(p_plane: CPlane, p_plane_line: CPlaneLine) -> Position3D:
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

    def get_plane_from_3_points(self, p_p: Position3D, p_q: Position3D, p_r: Position3D):
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

    def __and__(self, other: CPlane | CPlaneLine) -> CPlaneLine | Position3D:
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
        self.point0 = Position3D(0, 0, 0)  # x0, y0, z0
        self.a = self.b = self.c = 0

    def get_line_from_2_points(self, p_p: Position3D, p_q: Position3D):
        a = p_q.x - p_p.x
        b = p_q.y - p_p.y
        c = p_q.z - p_p.z
        simpl = gcd(a, b, c)
        self.point0 = p_p
        self.a = a // simpl
        self.b = b // simpl
        self.c = c // simpl

    def __and__(self, other: CPlane) -> Position3D:
        return plane_line_intersection(other, self)

    def __str__(self):
        return f'x = {self.point0.x} + {self.a} * t ; ' \
               f'y = {self.point0.y} + {self.b} * t ; ' \
               f'z = {self.point0.z} + {self.c} * t'


def main():
    pass


if __name__ == '__main__':
    main()
