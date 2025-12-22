from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_vector import CVector3D
from itertools import combinations
from heapq import heappush, heappop
from math import prod



class Point3D(CVector3D):
    def __init__(self, p_x: int, p_y: int, p_z: int):
        super().__init__(p_x, p_y, p_z)
        self.connection: Connection | None = None

    @property
    def root_connection(self) -> Connection:
        if self.connection is None:
            self.connection = Connection(self)
            return self.connection
        return self.connection.root_connection

    def __lshift__(self, other: Point3D):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2

    def __rshift__(self, other: Point3D):
        return self << other


class Connection:
    def __init__(self, p_conn_point: Point3D | None = None):
        self.connected_point = p_conn_point
        self.parent_connection: Connection | None = None
        self.children_connections: set[Connection] = set()

    @property
    def root_connection(self) -> Connection:
        if self.parent_connection is None:
            return self
        return self.parent_connection.root_connection

    @property
    def get_all_points(self) -> set[Point3D]:
        if self.connected_point:
            return {self.connected_point}
        rs = set()
        for act_child in self.children_connections:
            rs |= act_child.get_all_points
        return rs

    @property
    def get_all_points_count(self) -> int:
        if self.connected_point:
            return 1
        rs = 0
        for act_child in self.children_connections:
            rs += act_child.get_all_points_count
        return rs

    def __add__(self, other: Connection) -> Connection:
        c1 = self.root_connection
        c2 = other.root_connection
        if c1 is c2:
            return c1
        new_parent = Connection()
        c1.parent_connection = new_parent
        c2.parent_connection = new_parent
        new_parent.children_connections.add(c1)
        new_parent.children_connections.add(c2)
        return new_parent

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        return self is other


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    point_list = []
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space=','):
        point_list.append(Point3D(*inp_row))
    
    dist_heap = []
    for p1, p2 in combinations(point_list, 2):
        heappush(dist_heap, (p1 >> p2, (p1, p2)))

    iter_count = 0
    conn_list_count = len(point_list)
    while dist_heap:
        iter_count += 1
        _, (p1, p2) = heappop(dist_heap)
        if (rc1 := p1.root_connection) is not p2.root_connection:
            rc1 += p2.root_connection
            conn_list_count -= 1
            if conn_list_count == 1:
                answer2 = p1.x * p2.x
                break
        if iter_count == 1000:
            fin_conns = sorted(set(p.root_connection for p in point_list),
                               key=lambda x: x.get_all_points_count,
                               reverse=True)
            answer1 = prod(c.get_all_points_count for c in fin_conns[:3])
    return answer1, answer2


def main():
    aoc_solve_puzzle(2025, 8, solve_puzzle)


if __name__ == '__main__':
    main()
