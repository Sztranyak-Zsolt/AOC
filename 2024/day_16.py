import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, add_positions
from heapq import heappop, heappush


class CMaze(CGridBase):
    def __init__(self):
        super().__init__()
        self.start_pos: Position2D | None = None
        self.end_pos: Position2D | None = None
        self.path_cost: int | None = None
        self.path_tiles: set[Position2D] | None = None

    def set_pos(self):
        for k, v in self.position_dict.items():
            if v == 'E':
                self.end_pos = k
            elif v == 'S':
                self.start_pos = k
        del self.position_dict[self.start_pos]
        del self.position_dict[self.end_pos]

    def find_sortest_path(self) -> None:
        act_heap = [[0, self.start_pos, Position2D(1, 0)]]
        pos_path = {(self.start_pos, Position2D(1, 0)): {self.start_pos, }}
        pos_cost_dict = {(self.start_pos, Position2D(1, 0)): 0}
        while act_heap:
            act_cost = act_heap[0][0]
            if self.path_cost is not None and act_cost > self.path_cost:
                self.path_tiles = pos_path[(self.end_pos, Position2D(0, 1))]
                return
            while act_heap[0][0] == act_cost:
                _, act_pos, act_face = heappop(act_heap)
                for next_face, pos_cost in ((act_face, 1),
                                            (Position2D(act_face.y, act_face.x), 1001),
                                            (Position2D(-act_face.y, -act_face.x), 1001)):
                    next_pos = add_positions(act_pos, next_face)
                    next_cost = act_cost + pos_cost
                    if next_pos == self.end_pos and (self.path_cost is None or self.path_cost < next_cost):
                        self.path_cost = next_cost
                    if next_pos in self.position_dict \
                            or pos_cost_dict.get((next_pos, next_face), float('inf')) < next_cost:
                        continue
                    if pos_cost_dict.get((next_pos, next_face), float('inf')) > next_cost:
                        pos_cost_dict[(next_pos, next_face)] = next_cost
                        pos_path[(next_pos, next_face)] = pos_path[(act_pos, act_face)] | {next_pos, }
                    else:
                        pos_path[(next_pos, next_face)] |= pos_path[(act_pos, act_face)]
                    heappush(act_heap, [next_cost, next_pos, next_face])


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    g = CMaze()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True):
        g.add_row(inp_row, p_chars_to_skip='.')
    g.set_pos()
    g.find_sortest_path()
    answer1 = g.path_cost
    answer2 = len(g.path_tiles)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 16, solve_puzzle)


if __name__ == '__main__':
    main()
