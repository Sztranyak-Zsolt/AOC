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
        self.position_dict: dict[tuple[int, int]] = {}

    @property
    def min_x(self):
        if self.position_dict == {}:
            return 0
        return min([x for x, y in self.position_dict.keys()])

    @property
    def max_x(self):
        if self.position_dict == {}:
            return 0
        return max([x for x, y in self.position_dict.keys()])

    @property
    def min_y(self):
        if self.position_dict == {}:
            return 0
        return min([y for x, y in self.position_dict.keys()])

    @property
    def max_y(self):
        if self.position_dict == {}:
            return 0
        return max([y for x, y in self.position_dict.keys()])

    def add_item(self, p_position: tuple[int, int], p_item: CBaseItem):
        self.position_dict[p_position] = p_item

    def __str__(self):
        ret_lst = list()
        for y in range(self.max_y, self.min_y - 1, -1):
            act_row = ''
            for x in range(self.min_x, self.max_x + 1):
                if (x, y) in self.position_dict:
                    act_row += f"{self.position_dict[(x, y)]}@"[0]
                else:
                    act_row += ' '
            ret_lst.append(act_row)
        return '\n'.join(ret_lst)


def main():
    pass


if __name__ == '__main__':
    main()
