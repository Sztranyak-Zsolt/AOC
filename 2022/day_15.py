import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_vector import CVector2D
from functools import cached_property, cache


def merge_periods(p_period_list: list[list[int, int]]) -> list[list[int, int]]:
    act_periods = []
    for act_start, act_end in sorted([p for p in p_period_list if p is not None]):
        if not act_periods or act_periods[-1][1] < act_start - 1:
            act_periods.append([act_start, act_end])
            continue
        act_periods[-1][1] = max(act_periods[-1][1], act_end)
    return act_periods


class CSensor:
    def __init__(self, p_sensor_position: CVector2D | None = None, p_closest_beacon: CVector2D | None = None):
        self.sensor_position = p_sensor_position
        self.closest_beacon = p_closest_beacon

    @cached_property
    def min_x_point(self) -> CVector2D:
        return self.sensor_position + CVector2D(-self.sensor_range, 0)

    @cached_property
    def max_x_point(self) -> CVector2D:
        return self.sensor_position + CVector2D(self.sensor_range, 0)

    @cached_property
    def min_y_point(self) -> CVector2D:
        return self.sensor_position + CVector2D(0, -self.sensor_range)

    @cached_property
    def max_y_point(self) -> CVector2D:
        return self.sensor_position + CVector2D(0, self.sensor_range)

    @cached_property
    def sensor_range(self) -> int:
        return int(self.sensor_position - self.closest_beacon)

    def has_point_for_y(self, p_y: int) -> bool:
        return self.point_in_sensor_range(CVector2D(self.sensor_position.x, p_y))

    @cache
    def calc_scan_range_for_y(self, p_y: int) -> None | list[int, int]:
        pos_y = CVector2D(self.sensor_position.x, p_y)
        if not self.point_in_sensor_range(pos_y):
            return None
        plus_d = self.sensor_range - int(self.sensor_position - pos_y)
        return [self.sensor_position.x - plus_d, self.sensor_position.x + plus_d]

    def calc_empty_scan_range_for_y(self, p_y: int) -> None | list[int, int]:
        act_period = self.calc_scan_range_for_y(p_y)
        if self.closest_beacon.y != p_y:
            return act_period
        if act_period[0] == act_period[1]:
            return None
        if act_period[0] == self.closest_beacon.x:
            return [act_period[0] + 1, act_period[1]]
        return [act_period[0], act_period[1] - 1]

    def point_in_sensor_range(self, p_point: CVector2D) -> bool:
        return self.point_in_sensor_range_depth(p_point) >= 0

    def point_in_sensor_range_depth(self, p_point: CVector2D) -> int:
        return self.sensor_range - int(self.sensor_position - p_point)

    def __hash__(self):
        return id(self)


class CSensorHandler:
    def __init__(self):
        self.sensor_list: list[CSensor] = []

    def sensor_scan_ranges(self, p_y: int):
        return [s.calc_scan_range_for_y(p_y) for s in self.sensor_list
                if s.calc_scan_range_for_y(p_y) is not None]

    def sensor_empty_scan_ranges(self, p_y: int):
        return [s.calc_empty_scan_range_for_y(p_y) for s in self.sensor_list
                if s.calc_empty_scan_range_for_y(p_y) is not None]

    def count_empty_positions(self, p_y: int):
        act_periods = self.sensor_empty_scan_ranges(p_y)
        if act_periods:
            return sum([p[1] - p[0] + 1 for p in merge_periods(act_periods)])
        return 0

    def first_uncovered_point(self, p_from: CVector2D, p_to: CVector2D) -> CVector2D | None:
        act_y = p_from.y
        while act_y <= p_to.y:

            act_periods = self.sensor_scan_ranges(act_y)

            act_merged_periods = merge_periods(act_periods)
            # the result will be the hole in the merged period
            if not ['x' for p in merge_periods(act_periods) if p[0] <= p_from.x and p_to.x <= p[1]]:
                rel_period_end = max([p[1] for p in act_merged_periods if p[0] <= p_from.x < p[1]] + [p_from.x - 1])
                return CVector2D(rel_period_end + 1, act_y)

            add_y = min(max([s.point_in_sensor_range_depth(CVector2D(p_from.x, act_y)) for s in self.sensor_list
                             if s.point_in_sensor_range(CVector2D(p_from.x, act_y))]),
                        max([s.point_in_sensor_range_depth(CVector2D(p_to.x, act_y)) for s in self.sensor_list
                             if s.point_in_sensor_range(CVector2D(p_to.x, act_y))]))
            act_y_sensors = [s for s in self.sensor_list if s.has_point_for_y(act_y)]
            act_end_points = {s.calc_scan_range_for_y(act_y)[0] for s in act_y_sensors
                              if p_from.x < s.calc_scan_range_for_y(act_y)[0] < p_to.x} | \
                             {s.calc_scan_range_for_y(act_y)[1] for s in act_y_sensors
                              if p_from.x < s.calc_scan_range_for_y(act_y)[1] < p_to.x}
            for aep in act_end_points:
                while add_y != 0:
                    if [s for s in act_y_sensors if s.point_in_sensor_range(CVector2D(aep, act_y)) and
                                                    s.point_in_sensor_range(CVector2D(aep, act_y + add_y))]:
                        break
                    add_y //= 2
            act_y += max(1, add_y // 2)
        return None


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    sh = CSensorHandler()
    for sx, sy, bx, by in yield_input_data(p_input_file_path, p_chars_to_space=',:=', p_only_nums=True):
        sh.sensor_list.append(CSensor(CVector2D(sx, sy), CVector2D(bx, by)))

    answer1 = sh.count_empty_positions(2000000)
    uncovered_point = sh.first_uncovered_point(CVector2D(0, 0), CVector2D(4000000, 4000000))
    answer2 = uncovered_point.x * 4000000 + uncovered_point.y
    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 15, solve_puzzle)


if __name__ == '__main__':
    main()
