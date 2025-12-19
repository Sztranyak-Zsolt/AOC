from __future__ import annotations
from collections import deque
from typing import Self, Iterable
from .aoc_vector import neighbor_positions, TP2D, Position2D
from functools import cache


class CGridBase:
    def __init__(self):
        self.position_dict: dict[TP2D, str | bool | int | object] = {}
        self.position_type: type[TP2D] = Position2D
        self.min_x = self.min_y = self.max_x = self.max_y = 0
        self.double_width_on_print = False
        self.print_y_reverse = False
        self.y_mirrored_grid: Self | None = None
        self.x_mirrored_grid: Self | None = None
        self.left_rotated_grid: Self | None = None

    @property
    def normalized_grid(self):
        if self.min_x == self.min_y == 0 or not self.position_dict:
            return self
        return self.offset_grid(self.position_type(-self.min_x, -self.min_y))

    def add_item(self, p_position: TP2D, p_item: str | int | bool | object,
                 set_border_on_init: bool = False):
        self.position_dict[p_position] = p_item
        if not self.position_dict:
            self.position_type = type(p_position)
        if len(self.position_dict) != 1 or not set_border_on_init:
            self.min_x = min(self.min_x, p_position.x)
            self.max_x = max(self.max_x, p_position.x)
            self.min_y = min(self.min_y, p_position.y)
            self.max_y = max(self.max_y, p_position.y)
        else:
            self.min_x = self.max_x = p_position.x
            self.min_y = self.max_y = p_position.y

    def add_row(self, p_row: str, p_row_number: int | None = None, p_chars_to_skip: str = '',
                p_item_type: type[str] | type[int] | object = str, p_position_type: type[TP2D] = Position2D):
        if p_row_number is None:
            if len(self.position_dict) == 0 and self.min_x == self.max_x:
                p_row_number = 0
            else:
                p_row_number = self.max_y + 1
        for x, p_item_value in enumerate(p_row):
            if p_item_value not in p_chars_to_skip:
                if type(p_item_type) == str:
                    self.add_item(p_position_type(x, p_row_number), p_item_value)
                else:
                    self.add_item(p_position_type(x, p_row_number), p_item_type(p_item_value))
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
        mg.y_mirrored_grid = self
        mg.min_x, mg.max_x, mg.min_y, mg.max_y = self.min_x, self.max_x, self.min_y, self.max_y
        for p_position, pv in self.position_dict.items():
            mg.add_item(self.position_type(self.min_x + self.max_x - p_position.x, p_position.y), pv)
        return self.y_mirrored_grid

    def create_or_refresh_mirror_x(self):
        self.x_mirrored_grid = mg = self.__class__()
        mg.min_x, mg.max_x, mg.min_y, mg.max_y = self.min_x, self.max_x, self.min_y, self.max_y
        for p_position, pv in self.position_dict.items():
            mg.add_item(self.position_type(p_position.x, self.min_y + self.max_y - p_position.y), pv)
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
            mg.add_item(self.position_type(self.min_x + (p_position.y - self.min_y),
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

    def offset_grid(self, p_vector: TP2D) -> CGridBase:
        new_offset_grid = self.__class__()
        new_offset_grid.position_type = self.position_type
        new_offset_grid.min_x = self.min_x + p_vector.x
        new_offset_grid.max_x = self.max_x + p_vector.x
        new_offset_grid.min_y = self.min_y + p_vector.y
        new_offset_grid.max_y = self.max_y + p_vector.y
        for act_position, act_value in self.position_dict.items():
            new_offset_grid.add_item(self.position_type(act_position.x + p_vector.x, act_position.y + p_vector.y),
                                     act_value)
        return new_offset_grid

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

    def get_subgrid(self, p_pos1: TP2D, p_pos2: TP2D, p_keep_min_positions: bool = False) -> Self:
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
                    part_grid.add_item(self.position_type(part_grid.min_x + pos_x - min_x,
                                                          part_grid.min_y + pos_y - min_y),
                                       self.position_dict[(pos_x, pos_y)])
        return part_grid

    def add_subgrid(self, p_add_position_bottom_left: TP2D, p_subgrid: Self):
        x_length = p_subgrid.max_x - p_subgrid.min_x
        y_length = p_subgrid.max_y - p_subgrid.min_y

        for sg_pos_y in range(p_subgrid.min_y, p_subgrid.max_y + 1):
            for sg_pos_x in range(p_subgrid.min_x, p_subgrid.max_x + 1):
                if (sg_pos_x, sg_pos_y) in p_subgrid.position_dict:
                    self.position_dict[self.position_type(p_add_position_bottom_left.x + sg_pos_x,
                                                          p_add_position_bottom_left.y + sg_pos_y)] = \
                        p_subgrid.position_dict[self.position_type(sg_pos_x, sg_pos_y)]
                elif (p_add_position_bottom_left.x + sg_pos_x,
                      p_add_position_bottom_left.y + sg_pos_y) in self.position_dict:
                    del self.position_dict[self.position_type(p_add_position_bottom_left.x + sg_pos_x,
                                                              p_add_position_bottom_left.y + sg_pos_y)]
        self.min_x = min(self.min_x, p_add_position_bottom_left.x)
        self.min_y = min(self.min_y, p_add_position_bottom_left.y)
        self.max_x = max(self.max_x, p_add_position_bottom_left.x + x_length)
        self.max_y = max(self.max_y, p_add_position_bottom_left.y + y_length)

    def is_edge(self, p_position: Position2D) -> bool:
        return p_position.x in [self.min_x, self.max_x] or p_position.y in [self.min_y, self.max_y]

    def is_corner(self, p_position: Position2D) -> bool:
        return p_position.x in [self.min_x, self.max_x] and p_position.y in [self.min_y, self.max_y]

    def get_column(self, p_column: int) -> Self:
        return self.get_subgrid(self.position_type(p_column, self.min_y), self.position_type(p_column, self.max_y))

    def get_row(self, p_row: int) -> Self:
        return self.get_subgrid(self.position_type(self.min_x, p_row), self.position_type(self.max_x, p_row))

    @cache
    def get_edge(self, p_direction: TP2D) -> Self:
        if p_direction == self.position_type(0, 1):
            return self.get_row(self.max_x)
        elif p_direction == self.position_type(0, -1):
            return self.get_row(self.min_x)
        if p_direction == self.position_type(1, 0):
            return self.get_column(self.max_y)
        elif p_direction == self.position_type(-1, 0):
            return self.get_column(self.min_y)

    def yield_all_position(self, p_as_tuple: bool = False) -> Iterable[TP2D]:
        for act_x in range(self.min_x, self.max_x + 1):
            for act_y in range(self.min_y, self.max_y + 1):
                if p_as_tuple:
                    yield act_x, act_y
                else:
                    yield self.position_type(act_x, act_y)

    def count_all_cover(self, pict_to_cover: CGridBase) -> int:
        rv = 0
        dif_p = []
        pic_1st_point = list(pict_to_cover.position_dict)[0]
        for next_p in pict_to_cover.position_dict:
            dif_p.append(self.position_type(next_p.x - pic_1st_point.x, next_p.y - pic_1st_point.y))
        for act_grid_point in self.position_dict:
            for points_to_check in dif_p:
                if self.position_type(act_grid_point.x + points_to_check.x, act_grid_point.y + points_to_check.y) \
                        not in self.position_dict:
                    break
            else:
                rv += 1
        return rv

    def is_position_on_grid(self, p_position: Position2D) -> bool:
        return self.min_x <= p_position.x <= self.max_x and self.min_y <= p_position.y <= self.max_y

    def __str__(self):
        ret_lst = list()
        c_length = 2 if self.double_width_on_print else 1
        yr = slice(None) if not self.print_y_reverse else slice(None, None, -1)
        for y in range(self.max_y, self.min_y - 1, -1)[yr]:
            act_row = ''
            for x in range(self.min_x, self.max_x + 1):
                if self.position_type(x, y) in self.position_dict:
                    act_row += f"{self.position_dict[(x, y)]}@"[0] * c_length
                else:
                    act_row += ' ' * c_length
            ret_lst.append(act_row)
        return '\n'.join(ret_lst)

    def __hash__(self):
        return id(self)

    def __copy__(self):
        new_instance = self.__class__()
        new_instance.position_dict = self.position_dict.copy()
        new_instance.min_x = self.min_x
        new_instance.max_x = self.max_x
        new_instance.min_y = self.min_y
        new_instance.max_y = self.max_y
        new_instance.double_width_on_print = self.double_width_on_print
        new_instance.print_y_reverse = self.print_y_reverse


def main():
    pass


if __name__ == '__main__':
    main()
