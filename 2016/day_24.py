from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, neighbor_positions, Position2D
from functools import cached_property
from collections import deque
from itertools import permutations


class CGrid(CGridBase):
    def __init__(self):
        super().__init__()
        self.distance_dict: dict[Position2D, int] = {}

    @cached_property
    def point_dict(self) -> dict[str, Position2D]:
        return {v: k for k, v in self.position_dict.items() if v != '#'}

    def calc_point_distances(self):
        for k, v in sorted(self.point_dict.items()):
            dq = deque([[v, 0]])
            known_positions = {v}
            points_to_find = {k2 for k2 in self.point_dict if k2 > k}
            while dq and points_to_find:
                act_position, act_step = dq.popleft()
                for next_position in neighbor_positions(act_position):
                    if next_position in known_positions:
                        continue
                    known_positions.add(next_position)
                    try:
                        if (next_point_id := self.position_dict[next_position]) == '#':
                            continue
                        if next_point_id in points_to_find:
                            self.distance_dict[(k, next_point_id)] = act_step + 1
                            self.distance_dict[(next_point_id, k)] = act_step + 1
                            points_to_find.remove(next_point_id)
                    except KeyError:
                        pass
                    dq.append([next_position, act_step + 1])

    @property
    def shortest_path_from_0(self) -> int:
        if not self.distance_dict:
            self.calc_point_distances()
        rv = None
        for act_path in permutations([k for k in self.point_dict if k != '0']):
            act_path_length = 0
            prev_point = '0'
            for act_point in act_path:
                act_path_length += self.distance_dict[(prev_point, act_point)]
                prev_point = act_point
            if rv is None:
                rv = act_path_length
            else:
                rv = min(rv, act_path_length)
        return rv

    @property
    def shortest_circle_from_0(self) -> int:
        if not self.distance_dict:
            self.calc_point_distances()
        rv = None
        for act_path in permutations([k for k in self.point_dict if k != '0']):
            act_path_length = self.distance_dict['0', act_path[-1]]
            prev_point = '0'
            for act_point in act_path:
                act_path_length += self.distance_dict[(prev_point, act_point)]
                prev_point = act_point
            if rv is None:
                rv = act_path_length
            else:
                rv = min(rv, act_path_length)
        return rv


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    g = CGrid()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True):
        g.add_row(inp_row, p_chars_to_skip='.', p_item_type=str)

    answer1 = g.shortest_path_from_0
    answer2 = g.shortest_circle_from_0

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 24, solve_puzzle)


if __name__ == '__main__':
    main()
