from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import mh_distance
from collections import namedtuple


Position4D = namedtuple('Position4D', ['x', 'y', 'z', 't'])


class CSpaceTimeHandler:
    def __init__(self):
        self.space_time_group_list: list[list[Position4D]] = []

    @property
    def count_groups(self):
        return len(self.space_time_group_list)

    def add_space_time(self, p_st: Position4D):
        st_groups_to_merge = []
        for i, st_group in enumerate(self.space_time_group_list):
            for st_item in st_group:
                if mh_distance(st_item, p_st) <= 3:
                    st_groups_to_merge.append(i)
                    break
        if not st_groups_to_merge:
            new_st_group = [p_st]
            self.space_time_group_list.append(new_st_group)
        else:
            self.space_time_group_list[st_groups_to_merge[0]].append(p_st)
            for other_gr_to_join in st_groups_to_merge[:0:-1]:
                self.space_time_group_list[st_groups_to_merge[0]] += self.space_time_group_list[other_gr_to_join]
                self.space_time_group_list.pop(other_gr_to_join)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer2 = None
    st = CSpaceTimeHandler()
    for x, y, z, t in yield_input_data(p_input_file_path, p_chars_to_space=','):
        st.add_space_time(Position4D(x, y, z, t))
    answer1 = st.count_groups

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 25, solve_puzzle)


if __name__ == '__main__':
    main()
