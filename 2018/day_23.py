from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import mh_distance, add_positions, mul_position
from GENERICS.aoc_space import Position3D, CPlane
from functools import cached_property
from heapq import heapify, heappop, heappush


class CDiamond:
    def __init__(self):
        self.side_dict: dict[Position3D, CPlane] = {}

    def diamond_intersection(self, other: CDiamond) -> CDiamond | None:
        rd = CDiamond()
        for x in [-1, 1]:
            for y in [-1, 1]:
                side1_s = self.side_dict[Position3D(x, y, 1)]
                side1_o = other.side_dict[Position3D(x, y, 1)]
                side2_s = self.side_dict[Position3D(-x, -y, -1)]
                side2_o = other.side_dict[Position3D(-x, -y, -1)]
                side1_lower = CPlane(side1_s.a, side1_s.b, side1_s.c, min(side1_s.d, side1_o.d))
                side1_upper = CPlane(side1_s.a, side1_s.b, side1_s.c, max(side1_s.d, side1_o.d))
                side2_lower = CPlane(side2_s.a, side2_s.b, side2_s.c, min(side2_s.d, side2_o.d))
                side2_upper = CPlane(side2_s.a, side2_s.b, side2_s.c, max(side2_s.d, side2_o.d))
                if x + y == 0:
                    if side1_lower.d < side2_upper.d:
                        return None
                    rd.side_dict[Position3D(x, y, 1)] = side1_lower
                    rd.side_dict[Position3D(-x, -y, -1)] = side2_upper
                else:
                    if side2_lower.d < side1_upper.d:
                        return None
                    rd.side_dict[Position3D(-x, -y, -1)] = side2_lower
                    rd.side_dict[Position3D(x, y, 1)] = side1_upper
        return rd

    def vertexes(self) -> list[Position3D]:
        points = [self.side_dict[Position3D(1, 1, 1)] & self.side_dict[Position3D(1, -1, 1)]
                  & self.side_dict[Position3D(-1, 1, 1)],
                  self.side_dict[Position3D(1, 1, -1)] & self.side_dict[Position3D(1, -1, -1)]
                  & self.side_dict[Position3D(-1, 1, -1)],
                  self.side_dict[Position3D(1, 1, 1)] & self.side_dict[Position3D(1, -1, 1)]
                  & self.side_dict[Position3D(1, 1, -1)],
                  self.side_dict[Position3D(-1, 1, 1)] & self.side_dict[Position3D(-1, -1, 1)]
                  & self.side_dict[Position3D(-1, 1, -1)],
                  self.side_dict[Position3D(-1, 1, 1)] & self.side_dict[Position3D(-1, 1, -1)]
                  & self.side_dict[Position3D(1, 1, -1)],
                  self.side_dict[Position3D(-1, -1, 1)] & self.side_dict[Position3D(-1, -1, -1)]
                  & self.side_dict[Position3D(1, -1, -1)],
                  ]
        return points

    @property
    def distance_from_origin(self) -> int:
        rv = None
        origin_inside = True
        for side in [Position3D(1, 1, 1), Position3D(1, 1, -1), Position3D(1, -1, 1), Position3D(1, -1, -1)]:
            d1 = self.side_dict[side].d
            d2 = self.side_dict[mul_position(side, -1)].d
            if d1 < 0 and d2 < 0 or 0 < d1 and 0 < d2:
                origin_inside = False
            if rv is None:
                rv = min(abs(d1), abs(d2))
            else:
                rv = max(rv, min(abs(d1), abs(d2)))
        if origin_inside:
            return 0
        return rv


class CNanobot:
    def __init__(self, p_center: Position3D, p_range: int):
        self.center = p_center
        self.range = p_range

    @property
    def nb_diamond(self) -> CDiamond:
        rd = CDiamond()
        for x in [-1, 1]:
            for y in [-1, 1]:
                for z in [-1, 1]:
                    new_side_plane = CPlane()
                    new_side_plane.get_plane_from_3_points(add_positions(self.center, Position3D(x * self.range, 0, 0)),
                                                           add_positions(self.center, Position3D(0, y * self.range, 0)),
                                                           add_positions(self.center, Position3D(0, 0, z * self.range)))
                    rd.side_dict[Position3D(x, y, z)] = new_side_plane
        return rd


class CNanobotHandler:
    def __init__(self):
        self.nanobot_list: list[CNanobot] = []
        self.nb_has_common_points_with: dict[CNanobot, set[CNanobot]] = dict()

    def add_nanobot(self, p_nanobot: CNanobot):
        new_group_set = set()
        for nb in self.nanobot_list:
            if p_nanobot.range + nb.range >= mh_distance(p_nanobot.center, nb.center):
                new_group_set.add(nb)
                self.nb_has_common_points_with[nb].add(p_nanobot)
        self.nb_has_common_points_with[p_nanobot] = new_group_set
        self.nanobot_list.append(p_nanobot)

    def nanobot_in_range_count(self, p_position: Position3D) -> int:
        return len(['x' for nb in self.nanobot_list if mh_distance(p_position, nb.center) <= nb.range])

    @property
    def nanobots_in_larger_range(self):
        max_range = max([n.range for n in self.nanobot_list])
        nb_with_max_range = [n.center for n in self.nanobot_list if n.range == max_range][0]
        return len(['x' for ch_nb in [n.center for n in self.nanobot_list]
                    if mh_distance(nb_with_max_range, ch_nb) <= max_range])

    @cached_property
    def nb_has_common_points_with_sorted(self):
        return sorted([(k, v) for k, v in self.nb_has_common_points_with.items()], key=lambda x: len(x[1]))

    def largest_cliques(self) -> list[set[CNanobot]]:
        act_largest_clique_size = 0
        next_poss_set = None
        for k, v in self.nb_has_common_points_with_sorted[::-1]:
            if next_poss_set is None:
                next_poss_set = v.copy()
                act_largest_clique_size += 1
            elif k in next_poss_set:
                next_poss_set &= v
                act_largest_clique_size += 1
        act_rl = []
        heap = [[-len(self.nanobot_list), set(), set(self.nanobot_list)]]
        heapify(heap)
        while heap:
            act_poss_length, act_selected_nbs, act_poss_nbs = heappop(heap)
            if -act_poss_length < act_largest_clique_size:
                break
            checked_nb = set()
            for act_nb_to_check, act_nb_to_check_neighbors in \
                    [(k, v) for k, v in self.nb_has_common_points_with_sorted if k in act_poss_nbs]:
                act_nb_to_set = set()
                act_nb_to_set.add(act_nb_to_check)
                possible_neighbors = act_poss_nbs & act_nb_to_check_neighbors - checked_nb
                if possible_neighbors == set():
                    if act_largest_clique_size > len(act_selected_nbs) + 1:
                        continue
                    if act_largest_clique_size < len(act_selected_nbs) + 1:
                        act_largest_clique_size = len(act_selected_nbs) + 1
                        act_rl = []
                    act_rl.append(act_selected_nbs | act_nb_to_set)
                    continue
                new_poss_length = len(act_selected_nbs) + len(possible_neighbors) + 1
                if new_poss_length < act_largest_clique_size:
                    continue
                heappush(heap, [-new_poss_length, act_selected_nbs | act_nb_to_set, possible_neighbors])
                checked_nb.add(act_nb_to_check)
        return act_rl

    def get_closest_from_larger_groups(self) -> int:
        rv = -1
        for act_larger_group in self.largest_cliques():
            act_diamond = None
            for act_nb in act_larger_group:
                if act_diamond is None:
                    act_diamond = act_nb.nb_diamond
                else:
                    act_diamond = act_diamond.diamond_intersection(act_nb.nb_diamond)
            if rv == -1:
                rv = act_diamond.distance_from_origin
            else:
                rv = min(rv, act_diamond.distance_from_origin)
        return rv


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    nh = CNanobotHandler()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space='<>,=', p_only_nums=True):
        nh.add_nanobot(CNanobot(Position3D(*inp_row[:3]), inp_row[3]))
    answer1 = nh.nanobots_in_larger_range
    answer2 = nh.get_closest_from_larger_groups()

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 23, solve_puzzle)


if __name__ == '__main__':
    main()
