from __future__ import annotations
from typing import Self, Iterable, TypeVar
from math import gcd
from itertools import zip_longest, product, permutations
from collections import namedtuple
from functools import cached_property, cache
from collections import deque
from copy import copy


Position2D = namedtuple('Position2D', ['x', 'y'])
Position3D = namedtuple('Position3D', ['x', 'y', 'z'])


@cache
def orientation_list(p_num: int):
    if p_num == 0:
        return []
    rl = []
    act_orientation = tuple(range(1, p_num + 1))
    rl.append([act_orientation, 0, False])
    rl.append([[-x for x in act_orientation], 0, True])
    if p_num <= 1:
        return rl
    dq = deque([[act_orientation, 0]])
    known_orientations = {act_orientation}
    while dq:
        prev_orientation, prev_transformation_count = dq.popleft()
        for i1 in range(p_num):
            for i2 in range(i1 + 1, p_num):
                next_orientation = list(prev_orientation)
                next_orientation[i1], next_orientation[i2] = next_orientation[i2], -next_orientation[i1]
                next_orientation = tuple(next_orientation)
                if next_orientation in known_orientations:
                    continue
                known_orientations.add(next_orientation)
                rl.append([next_orientation, prev_transformation_count + 1, False])
                rl.append([[-x for x in next_orientation], prev_transformation_count + 1, True])
                dq.append([next_orientation, prev_transformation_count + 1])
    return rl


class CVectorBase:
    def __init__(self, *p_positions: int):
        self.position_tuple: tuple[int] = tuple(p_positions)

    def __iter__(self):
        self.index = 0
        return self

    def __reversed__(self):
        self.index = -1
        return self

    def __next__(self):
        try:
            rv = self.position_tuple[self.index]
            self.index += 1 if self.index >= 0 else -1
            return rv
        except IndexError:
            raise StopIteration

    def __bool__(self):
        return any(self.position_tuple)

    def __int__(self) -> int:
        return sum([abs(p) for p in self.position_tuple])

    def __add__(self, other: Iterable[int]) -> Self:
        return self.__class__(*[sp + op for sp, op in zip_longest(self, other[:len(self)], fillvalue=0)])

    def __sub__(self, other: Iterable[int]) -> Self:
        return self.__class__(*[sp - op for sp, op in zip_longest(self, other[:len(self)], fillvalue=0)])

    def __mul__(self, p_multiplier: int) -> Self:
        return self.__class__(*[v * p_multiplier for v in self])

    def __floordiv__(self, p_divisor: int) -> Self:
        return self.__class__(*[v // p_divisor for v in self])

    def __mod__(self, p_divisor: int) -> Self:
        return self.__class__(*[v - v // p_divisor for v in self])

    def __abs__(self):
        return self.__class__(*[abs(v) for v in self])

    @property
    def min_integer_vector(self) -> Self:
        if self:
            step = gcd(*self)
            return self.__class__(*[v // step for v in self])
        return self

    def __copy__(self):
        return self.__class__(*self.position_tuple)

    def __str__(self):
        return f'{self.__class__.__name__}{self.position_tuple}'

    def __len__(self):
        return len(self.position_tuple)

    def __getitem__(self, i):
        return self.position_tuple[i]

    def __hash__(self):
        return hash(self.position_tuple)

    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.position_tuple == other
        return self.position_tuple == other.position_tuple

    @cached_property
    def rotations_dict(self) -> dict[tuple[int, ...], Self]:
        rd = {}
        for pos_sign in product((-1, 1), repeat=len(self)):
            for used_indexes in permutations(range(len(self))):
                rl = []
                orientation = []
                for act_index in used_indexes:
                    rl.append(pos_sign[act_index] * self.position_tuple[act_index])
                    orientation.append(pos_sign[act_index] * (act_index + 1))
                rd[tuple(orientation)] = self.__class__(*rl)
        return rd


class CVector2D(CVectorBase):
    def __init__(self, p_x: int, p_y: int):
        super().__init__(p_x, p_y)

    @property
    def x(self):
        return self.position_tuple[0]

    @x.setter
    def x(self, p_x: int):
        self.position_tuple = (p_x, self.position_tuple[1])

    @property
    def y(self):
        return self.position_tuple[1]

    @y.setter
    def y(self, p_y: int):
        self.position_tuple = (self.position_tuple[0], p_y)


class CVector3D(CVectorBase):
    def __init__(self, p_x: int, p_y: int, p_z: int):
        super().__init__(p_x, p_y, p_z)

    @property
    def x(self):
        return self.position_tuple[0]

    @x.setter
    def x(self, p_x: int):
        self.position_tuple = (p_x, self.position_tuple[1], self.position_tuple[2])

    @property
    def y(self):
        return self.position_tuple[1]

    @y.setter
    def y(self, p_y: int):
        self.position_tuple = (self.position_tuple[0], p_y, self.position_tuple[2])

    @property
    def z(self):
        return self.position_tuple[2]

    @z.setter
    def z(self, p_z: int):
        self.position_tuple = (self.position_tuple[0], self.position_tuple[1], p_z)


TP2D = TypeVar('TP2D', bound=tuple[int, int] | Position2D | CVector2D)
TP3D = TypeVar('TP3D', bound=tuple[int, int, int] | Position3D | CVector3D)


def min_vector(*p_vectors: CVectorBase):
    rv = []
    for v in zip(*p_vectors):
        rv.append(min(v))
    return p_vectors[0].__class__(*rv)


def max_vector(*p_vectors: CVectorBase):
    rv = []
    for v in zip(*p_vectors):
        rv.append(max(v))
    return p_vectors[0].__class__(*rv)


def neighbor_positions(p_position: tuple[int, ...] | list[int, ...] | CVectorBase | Position2D | Position3D =
                       Position2D(0, 0),
                       p_return_near: bool = True,
                       p_return_corner: bool = False,
                       p_return_self: bool = False) -> Iterable[tuple[int, ...] | list[int, ...] | CVectorBase |
                                                                Position2D | Position3D]:

    for act_dif in product((-1, 0, 1), repeat=len(p_position)):
        count_1 = len(act_dif) - act_dif.count(0)
        if count_1 == 0 and p_return_self or count_1 == 1 and p_return_near or count_1 > 1 and p_return_corner:
            if isinstance(p_position, CVectorBase) or isinstance(p_position, Position2D) \
                    or isinstance(p_position, Position3D):
                yield p_position.__class__(*[p1 + p2 for p1, p2 in zip(p_position, act_dif)])
            elif isinstance(p_position, list) or isinstance(p_position, tuple):
                yield p_position.__class__([p1 + p2 for p1, p2 in zip(p_position, act_dif)])


def add_positions(*args: tuple[int, ...] | Position2D | Position3D):
    d_arg_item_length = max([len(ti) for ti in args])
    r_l = [0] * max([len(ti) for ti in args])
    for p_item in args:
        for d_i in range(d_arg_item_length):
            try:
                r_l[d_i] += p_item[d_i]
            except IndexError:
                pass
    if all(isinstance(x, Position2D) for x in args):
        return Position2D(r_l[0], r_l[1])
    if all(isinstance(x, Position3D) for x in args):
        return Position3D(r_l[0], r_l[1], r_l[2])
    return tuple(r_l)


def mul_position(p_position: tuple[int, ...] | Position2D | Position3D, p_multiplier: int) \
        -> tuple[int, ...] | Position2D | Position3D:
    """
    Function multiply a position with an integer.
    """
    r_l = []
    for p_pos_single in p_position:
        r_l.append(p_pos_single * p_multiplier)
    if isinstance(p_position, Position2D):
        return Position2D(r_l[0], r_l[1])
    if isinstance(p_position, Position3D):
        return Position3D(r_l[0], r_l[1], r_l[2])
    return tuple(r_l)


def mh_distance(p_position1: tuple[int, ...] | Position2D | Position3D,
                p_position2: tuple[int, ...] | Position2D | Position3D) -> int:
    """
    Return the manhattan distance of the positions.
    :param p_position1: base position
    :param p_position2: target position
    :return: manhattan distance of the two positions
    """
    rv = 0
    for i_p1, i_p2 in zip(p_position1, p_position2):
        rv += abs(i_p1 - i_p2)
    return rv


def main():
    pass


if __name__ == '__main__':
    main()
