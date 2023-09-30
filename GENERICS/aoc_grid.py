from GENERICS.aoc_item import CBaseItem
from enum import Enum


class DIRS(Enum):
    UP = (0, 1)
    LEFT = (-1, 0)
    DOWN = (0, -1)
    RIGHT = (1, 0)


def add_positions(*args: tuple[int, ...]):
    """
    Function summarize each dimensions of the given positions and return the result as tuple.
    :param args: position list to be added
    :return: aggregated position, length is equal to the longest parameter length
    """
    d_arg_item_length = max([len(ti) for ti in args])
    r_l = [0] * d_arg_item_length
    for p_item in args:
        for d_i in range(d_arg_item_length):
            try:
                r_l[d_i] += p_item[d_i]
            except IndexError:
                pass
    return tuple(r_l)


def neighbor_positions(p_position: tuple[int, int] | tuple[int, int, int] = (0, 0),
                       p_return_near: bool = True,
                       p_return_corner: bool = False,
                       p_return_self: bool = False) -> tuple[int, int] | tuple[int, int, int]:

    for x in [1, 0, -1]:
        for y in [1, 0, -1]:
            if len(p_position) == 2:
                if x == y == 0:
                    if p_return_self:
                        yield p_position
                    continue
                if 0 in [x, y]:
                    if p_return_near:
                        yield p_position[0] + x, p_position[1] + y
                    continue
                if p_return_corner:
                    yield p_position[0] + x, p_position[1] + y
                continue
            for z in [1, 0, -1]:
                if x == y == z == 0:
                    if p_return_self:
                        yield p_position
                    continue
                if x == y == 0 or x == z == 0 or y == z == 0:
                    if p_return_corner:
                        yield p_position[0] + x, p_position[1] + y, p_position[2] + z
                    continue
                if p_return_near:
                    yield p_position[0] + x, p_position[1] + y, p_position[2] + z


def mh_distance(p_position1: tuple[int, ...],
                p_position2: tuple[int, ...]) -> int:
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
        self.position_dict: dict[tuple[int, int], CBaseItem | str | bool | int] = {}
        self.min_x = self.min_y = self.max_x = self.max_y = 0
        self.double_on_print = False
        self.print_y_reverse = False

    def add_item(self, p_position: tuple[int, int], p_item: CBaseItem | str | bool):
        self.position_dict[p_position] = p_item
        self.min_x = min(self.min_x, p_position[0])
        self.max_x = max(self.max_x, p_position[0])
        self.min_y = min(self.min_y, p_position[1])
        self.max_y = max(self.max_y, p_position[1])

    def add_row(self, p_row: str, p_row_number: int | None = None, p_chars_to_skip: str = '',
                p_item_type: type[CBaseItem] | type[str] = CBaseItem):
        if p_row_number is None:
            if len(self.position_dict) == 0:
                p_row_number = 0
            else:
                p_row_number = self.max_y + 1
        for x, p_item_value in enumerate(p_row):
            if p_item_value not in p_chars_to_skip:
                if type(p_item_type) == str:
                    self.add_item((x, p_row_number), p_item_value)
                else:
                    self.add_item((x, p_row_number), p_item_type(p_item_value))
        self.max_y = p_row_number
        self.max_x = max(self.max_x, len(p_row) - 1)

    def __str__(self):
        ret_lst = list()
        c_length = 2 if self.double_on_print else 1
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
