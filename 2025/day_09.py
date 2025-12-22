import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from functools import cached_property, cache
from GENERICS.aoc_vector import Position2D


def calc_rect_area(p1: Position2D, p2: Position2D) -> int:
    return (abs(p1.x - p2.x) + 1) * (abs(p1.y - p2.y) + 1)


class CShape:
    def __init__(self):
        self.point_list: list[Position2D] = []

    @property
    def max_rectangle_area(self):
        rv = 0
        for i1, p1 in enumerate(self.point_list):
            for p2 in self.point_list[i1+1:]:
                act_rect_area = calc_rect_area(p1, p2)
                if rv < act_rect_area:
                    rv = act_rect_area
        return rv

    @cache
    def left_wall_counter(self, p_point: Position2D) -> int:
        left_wall_counter = 0
        prev_point_pos = ''
        for wall_point1, wall_point2 in self.vertical_walls:
            if wall_point1.x > p_point.x:
                break
            if p_point.y < wall_point1.y or wall_point2.y < p_point.y:
                continue
            if wall_point1.x == p_point.x:
                if left_wall_counter % 2 == 0:
                    left_wall_counter += 1
                break
            if wall_point1.y == p_point.y:
                if prev_point_pos == '':
                    if left_wall_counter % 2 == 0:
                        left_wall_counter += 1
                        prev_point_pos = 'L'
                    else:
                        prev_point_pos = 'R'
                    continue
                elif prev_point_pos == 'L':
                    left_wall_counter += 1
                prev_point_pos = ''
                continue
            elif wall_point2.y == p_point.y:
                if prev_point_pos == '':
                    if left_wall_counter % 2 == 0:
                        left_wall_counter += 1
                        prev_point_pos = 'R'
                    else:
                        prev_point_pos = 'L'
                    continue
                elif prev_point_pos == 'R':
                    left_wall_counter += 1
                prev_point_pos = ''
                continue
            left_wall_counter += 1
        return left_wall_counter

    @cache
    def lower_wall_counter(self, p_point: Position2D) -> int:
        lower_wall_counter = 0
        prev_point_pos = ''
        for wall_point1, wall_point2 in self.horizontal_walls:
            if wall_point1.y > p_point.y:
                break
            if p_point.x < wall_point1.x or wall_point2.x < p_point.x:
                continue
            if wall_point1.y == p_point.y:
                if lower_wall_counter % 2 == 0:
                    lower_wall_counter += 1
                break
            if wall_point1.x == p_point.x:
                if prev_point_pos == '':
                    if lower_wall_counter % 2 == 0:
                        lower_wall_counter += 1
                        prev_point_pos = 'L'
                    else:
                        prev_point_pos = 'R'
                    continue
                elif prev_point_pos == 'L':
                    lower_wall_counter += 1
                prev_point_pos = ''
                continue
            elif wall_point2.x == p_point.x:
                if prev_point_pos == '':
                    if lower_wall_counter % 2 == 0:
                        lower_wall_counter += 1
                        prev_point_pos = 'R'
                    else:
                        prev_point_pos = 'L'
                    continue
                elif prev_point_pos == 'R':
                    lower_wall_counter += 1
                prev_point_pos = ''
                continue
            lower_wall_counter += 1
        return lower_wall_counter

    @property
    def max_rectangle_area_inside(self):
        rv = 0
        for i1, p1 in enumerate(self.point_list):
            for p2 in self.point_list[i1 + 1:]:
                if (act_rect_area := calc_rect_area(p1, p2)) <= rv:
                    continue
                min_x = p1.x if p1.x <= p2.x else p2.x
                max_x = p1.x if p1.x >= p2.x else p2.x
                min_y = p1.y if p1.y <= p2.y else p2.y
                max_y = p1.y if p1.y >= p2.y else p2.y
                if self.left_wall_counter(Position2D(min_x, min_y)) != self.left_wall_counter(Position2D(max_x, min_y)):
                    continue
                if self.left_wall_counter(Position2D(min_x, max_y)) != self.left_wall_counter(Position2D(max_x, max_y)):
                    continue
                if self.lower_wall_counter(Position2D(min_x, min_y)) != self.lower_wall_counter(Position2D(min_x, max_y)):
                    continue
                if self.lower_wall_counter(Position2D(max_x, min_y)) != self.lower_wall_counter(Position2D(max_x, max_y)):
                    continue
                rv = act_rect_area
        return rv

    @cached_property
    def vertical_walls(self):
        wall_list = []
        for p1, p2 in zip(self.point_list, self.point_list[1:] + [self.point_list[0]]):
            if p1.x == p2.x:
                if p1.y < p2.y:
                    wall_list.append((p1, p2))
                else:
                    wall_list.append((p2, p1))
        wall_list.sort()
        return wall_list

    @cached_property
    def horizontal_walls(self):
        wall_list = []
        for p1, p2 in zip(self.point_list, self.point_list[1:] + [self.point_list[0]]):
            if p1.y == p2.y:
                if p1.x < p2.x:
                    wall_list.append((p1, p2))
                else:
                    wall_list.append((p2, p1))
        wall_list.sort(key=lambda x: (x[0][1], x[0][0]))
        return wall_list


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    shape = CShape()
    for x, y in yield_input_data(p_input_file_path, p_chars_to_space=','):
        shape.point_list.append(Position2D(x, y))
    answer1 = shape.max_rectangle_area
    answer2 = shape.max_rectangle_area_inside
    return answer1, answer2


def main():
    aoc_solve_puzzle(2025, 9, solve_puzzle)


if __name__ == '__main__':
    main()
