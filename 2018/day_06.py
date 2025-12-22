import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import mh_distance, Position2D


class CSpaceGrid(CGridBase):
    def __init__(self):
        super().__init__()

    def get_closest_id(self, p_position: Position2D) -> int | None:
        rv = closest_distance = None
        for k, v in self.position_dict.items():
            if closest_distance is None or (act_distance := mh_distance(k, p_position)) < closest_distance:
                closest_distance = mh_distance(k, p_position)
                rv = v
                continue
            if act_distance == closest_distance:
                rv = None
        return rv

    def get_sum_mh_distance(self, p_position: Position2D) -> int:
        return sum([mh_distance(k, p_position) for k in self.position_dict])

    def calc_safe_points(self, p_safe_distance: int) -> int:
        rv = 0
        for act_position in self.yield_all_position():
            if (act_sum_difference := self.get_sum_mh_distance(act_position)) >= p_safe_distance:
                continue
            rv += 1
            if self.is_edge(act_position):
                rv += (p_safe_distance - 1 - act_sum_difference) // len(self.position_dict)
                if self.is_corner(act_position):
                    additional_dif = (p_safe_distance - 1 - act_sum_difference - len(self.position_dict)) \
                                     // len(self.position_dict)
                    if additional_dif > 0:
                        rv += (additional_dif * (additional_dif + 1)) // 2
        return rv

    def area_count(self):
        infinitive_ids = set()
        rd: dict[int, int] = {}
        for act_position in self.yield_all_position():
            if (closest_id := self.get_closest_id(act_position)) is None:
                continue
            if act_position.x in [self.min_x, self.max_x] or act_position.y in [self.min_y, self.max_y]:
                infinitive_ids.add(closest_id)
                continue
            if closest_id not in rd:
                rd[closest_id] = 1
            else:
                rd[closest_id] += 1
        for inf_p in infinitive_ids:
            if inf_p in rd:
                del rd[inf_p]
        return rd


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    grid = CSpaceGrid()
    for i, (x, y) in enumerate(yield_input_data(p_input_file_path, p_chars_to_space=',')):
        grid.add_item(Position2D(x, y), i)

    answer1 = max(grid.area_count().values())
    answer2 = grid.calc_safe_points(10000)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 6, solve_puzzle)


if __name__ == '__main__':
    main()
