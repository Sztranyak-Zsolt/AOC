from __future__ import annotations
from GENERICS.aoc_item import CBaseItem
from enum import Enum
from collections import deque, namedtuple
from typing import Self, Iterable
from GENERICS.aoc_space import Position3D


Position2D = namedtuple('Position2D', ['x', 'y'])


class DIRS(Enum):
    UP = Position2D(0, 1)
    LEFT = Position2D(-1, 0)
    DOWN = Position2D(0, -1)
    RIGHT = Position2D(1, 0)


def add_positions(*args: tuple[int, ...] | Position2D | Position3D):
    """
    Function summarize each dimensions of the given positions and return the result as tuple.
    :param args: position list to be added
    :return: aggregated position, length is equal to the longest parameter length
    """
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


def neighbor_positions(p_position: tuple[int, int] | tuple[int, int, int] | Position2D | Position3D = (0, 0),
                       p_return_near: bool = True,
                       p_return_corner: bool = False,
                       p_return_self: bool = False) \
        -> Iterable[tuple[int, int] | tuple[int, int, int] | Position2D | Position3D]:
    def np_inner():
        for x in [1, 0, -1]:
            for y in [1, 0, -1]:
                if len(p_position) == 2:
                    if (p_return_self and x == y == 0
                            or p_return_near and x + y in [1, -1]
                            or p_return_corner and x != 0 and y != 0):
                        yield p_position[0] + x, p_position[1] + y
                    continue
                for z in [1, 0, -1]:
                    if x == y == z == 0 and p_return_self \
                            or [x, y, z].count(0) == 2 and p_return_corner \
                            or [x, y, z].count(0) in [0, 1] and p_return_near:
                        yield p_position[0] + x, p_position[1] + y, p_position[2] + z
    for np in np_inner():
        if isinstance(p_position, Position2D):
            yield Position2D(np[0], np[1])
        elif isinstance(p_position, Position3D):
            yield Position3D(np[0], np[1], np[2])
        else:
            yield np


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


class CGridBase:
    def __init__(self):
        self.position_dict: dict[Position2D, CBaseItem | str | bool | int] = {}
        self.min_x = self.min_y = self.max_x = self.max_y = 0
        self.double_width_on_print = False
        self.print_y_reverse = False
        self.y_mirrored_grid: Self | None = None
        self.x_mirrored_grid: Self | None = None
        self.left_rotated_grid: Self | None = None

    def add_item(self, p_position: Position2D, p_item: CBaseItem | str | int | bool,
                 set_border_on_init: bool = False):
        self.position_dict[p_position] = p_item
        if len(self.position_dict) != 1 or not set_border_on_init:
            self.min_x = min(self.min_x, p_position.x)
            self.max_x = max(self.max_x, p_position.x)
            self.min_y = min(self.min_y, p_position.y)
            self.max_y = max(self.max_y, p_position.y)
        else:
            self.min_x = self.max_x = p_position.x
            self.min_y = self.max_y = p_position.y

    def add_row(self, p_row: str, p_row_number: int | None = None, p_chars_to_skip: str = '',
                p_item_type: type[CBaseItem] | type[str] | type[int] = str):
        if p_row_number is None:
            if len(self.position_dict) == 0:
                p_row_number = 0
            else:
                p_row_number = self.max_y + 1
        for x, p_item_value in enumerate(p_row):
            if p_item_value not in p_chars_to_skip:
                if type(p_item_type) == str:
                    self.add_item(Position2D(x, p_row_number), p_item_value)
                else:
                    self.add_item(Position2D(x, p_row_number), p_item_type(p_item_value))
        self.min_y = min(self.min_y, p_row_number)
        self.max_y = max(self.max_y, p_row_number)
        self.max_x = max(self.max_x, len(p_row) - 1)

    @property
    def regions_count(self) -> int:
        known_positions = set()
        rv = 0
        for act_position in self.position_dict:
            if act_position in known_positions:
                continue
            known_positions.add(act_position)
            rv += 1
            dq = deque([act_position])
            while dq:
                ap = dq.popleft()
                for next_position in neighbor_positions(ap):
                    if next_position in known_positions or next_position not in self.position_dict:
                        continue
                    known_positions.add(next_position)
                    dq.append(next_position)
        return rv

    def get_y_mirrored_grid(self):
        if self.y_mirrored_grid is None:
            return self.create_or_refresh_mirror_y()
        return self.y_mirrored_grid

    def get_x_mirrored_grid(self):
        if self.x_mirrored_grid is None:
            return self.create_or_refresh_mirror_x()
        return self.x_mirrored_grid

    def create_or_refresh_mirror_y(self):
        self.y_mirrored_grid = mg = self.__class__()
        mg.min_x, mg.max_x, mg.min_y, mg.max_y = self.min_x, self.max_x, self.min_y, self.max_y
        for p_position, pv in self.position_dict.items():
            mg.add_item(Position2D(self.min_x + self.max_x - p_position.x, p_position.y), pv)
        self.y_mirrored_grid.y_mirrored_grid = self
        return self.y_mirrored_grid

    def create_or_refresh_mirror_x(self):
        self.x_mirrored_grid = mg = self.__class__()
        mg.min_x, mg.max_x, mg.min_y, mg.max_y = self.min_x, self.max_x, self.min_y, self.max_y
        for p_position, pv in self.position_dict.items():
            mg.add_item(Position2D(p_position.x, self.min_y + self.max_y - p_position.y), pv)
        self.x_mirrored_grid.x_mirrored_grid = self
        return self.x_mirrored_grid

    def get_rotated_grid(self):
        if self.left_rotated_grid is None:
            return self.set_rotations()
        return self.left_rotated_grid

    def create_next_rotation(self):
        self.left_rotated_grid = mg = self.__class__()
        mg.min_x, mg.max_x = self.min_x, self.min_x + self.max_y - self.min_y
        mg.min_y, mg.max_y = self.min_y, self.min_y + self.max_x - self.min_x
        for p_position, pv in self.position_dict.items():
            mg.add_item(Position2D(self.min_x + (p_position.y - self.min_y),
                                   self.min_y + (self.max_x - p_position.x)), pv)
        return self.left_rotated_grid

    def set_rotations(self):
        act_grid = self
        for _ in range(3):
            act_grid = act_grid.create_next_rotation()
        act_grid.left_rotated_grid = self
        return self.left_rotated_grid

    def set_all_orientations(self):
        self.set_rotations()
        ymg = self.y_mirrored_grid = self.create_or_refresh_mirror_y()
        ymg.set_rotations()
        ag = self
        xmg = ag.x_mirrored_grid = ag.y_mirrored_grid.left_rotated_grid.left_rotated_grid
        xmg.x_mirrored_grid = ag
        for _ in range(3):
            ag = ag.left_rotated_grid
            ymg = ymg.left_rotated_grid
            ag.y_mirrored_grid = ymg
            ymg.y_mirrored_grid = ag
            xmg = ag.x_mirrored_grid = ag.y_mirrored_grid.left_rotated_grid.left_rotated_grid
            xmg.x_mirrored_grid = ag

    def yield_all_orientations(self) -> Iterable[Self]:
        if self.left_rotated_grid is None or self.x_mirrored_grid is None or self.y_mirrored_grid is None:
            self.set_all_orientations()
        ag = self
        for _ in range(4):
            yield ag
            yield ag.y_mirrored_grid
            ag = ag.left_rotated_grid

    def __eq__(self, other: Self):
        if self is other:
            return True
        if self.min_x != other.min_x or self.max_x != other.max_x \
                or self.min_y != other.min_y or self.max_y != other.max_y:
            return False
        for s_position, sv in self.position_dict.items():
            if s_position not in other.position_dict or other.position_dict[s_position] != sv:
                return False
        if ['x' for k in other.position_dict if k not in self.position_dict]:
            return False
        return True

    def get_subgrid(self, p_pos1: Position2D, p_pos2: Position2D, p_keep_min_positions: bool = False) -> Self:
        part_grid = self.__class__()
        min_x, max_x = min(p_pos1.x, p_pos2.x), max(p_pos1.x, p_pos2.x)
        min_y, max_y = min(p_pos1.y, p_pos2.y), max(p_pos1.y, p_pos2.y)
        if p_keep_min_positions:
            part_grid.min_x = min_x
            part_grid.min_y = min_y
        part_grid.max_x = part_grid.min_x + max_x - min_x
        part_grid.max_y = part_grid.min_y + max_y - min_y
        for pos_y in range(min_y, max_y + 1):
            for pos_x in range(min_x, max_x + 1):
                if (pos_x, pos_y) in self.position_dict:
                    part_grid.add_item(Position2D(part_grid.min_x + pos_x - min_x, part_grid.min_y + pos_y - min_y),
                                       self.position_dict[(pos_x, pos_y)])
        return part_grid

    def add_subgrid(self, p_add_position_bottom_left: Position2D, p_subgrid: Self):
        x_length = p_subgrid.max_x - p_subgrid.min_x
        y_length = p_subgrid.max_y - p_subgrid.min_y

        for sg_pos_y in range(p_subgrid.min_y, p_subgrid.max_y + 1):
            for sg_pos_x in range(p_subgrid.min_x, p_subgrid.max_x + 1):
                if (sg_pos_x, sg_pos_y) in p_subgrid.position_dict:
                    self.position_dict[Position2D(p_add_position_bottom_left.x + sg_pos_x,
                                                  p_add_position_bottom_left.y + sg_pos_y)] = \
                        p_subgrid.position_dict[Position2D(sg_pos_x, sg_pos_y)]
                elif (p_add_position_bottom_left.x + sg_pos_x,
                      p_add_position_bottom_left.y + sg_pos_y) in self.position_dict:
                    del self.position_dict[Position2D(p_add_position_bottom_left.x + sg_pos_x,
                                                      p_add_position_bottom_left.y + sg_pos_y)]
        self.max_x = max(self.max_x, p_add_position_bottom_left.x + x_length)
        self.max_y = max(self.max_y, p_add_position_bottom_left.y + y_length)

    def is_edge(self, p_position: Position2D) -> bool:
        return p_position.x in [self.min_x, self.max_x] or p_position.y in [self.min_y, self.max_y]

    def is_corner(self, p_position: Position2D) -> bool:
        return p_position.x in [self.min_x, self.max_x] and p_position.y in [self.min_y, self.max_y]

    def yield_all_position(self) -> Iterable[Position2D]:
        for act_x in range(self.min_x, self.max_x + 1):
            for act_y in range(self.min_y, self.max_y + 1):
                yield Position2D(act_x, act_y)

    def __str__(self):
        ret_lst = list()
        c_length = 2 if self.double_width_on_print else 1
        yr = slice(None) if not self.print_y_reverse else slice(None, None, -1)
        for y in range(self.max_y, self.min_y - 1, -1)[yr]:
            act_row = ''
            for x in range(self.min_x, self.max_x + 1):
                if (x, y) in self.position_dict:
                    act_row += f"{self.position_dict[(x, y)]}@"[0] * c_length
                else:
                    act_row += ' ' * c_length
            ret_lst.append(act_row)
        return '\n'.join(ret_lst)


def main():
    pass


if __name__ == '__main__':
    main()
