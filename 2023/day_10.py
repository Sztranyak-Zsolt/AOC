import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, add_positions
from collections import deque
from functools import cached_property


def neighbor_fence_positions(p_position: Position2D, p_pipe: str):
    if p_pipe in ('|', 'S', '7', 'F'):
        yield add_positions(p_position, Position2D(0, -1))
    if p_pipe in ('|', 'S', 'J', 'L'):
        yield add_positions(p_position, Position2D(0, 1))
    if p_pipe in ('-', 'S', 'F', 'L'):
        yield add_positions(p_position, Position2D(1, 0))
    if p_pipe in ('-', 'S', '7', 'J'):
        yield add_positions(p_position, Position2D(-1, 0))


class CGrid(CGridBase):

    @cached_property
    def starting_position(self) -> Position2D:
        try:
            return [k for k, v in self.position_dict.items() if v == 'S'][0]
        except IndexError:
            return Position2D(0, 0)

    @cached_property
    def starting_fence(self) -> str:
        fence_mapping = {'1100': 'F', '1010': '-', '1001': 'L', '0110': '7', '0101': '|', '0011': 'J'}
        map_str = ''
        for neighbor_pos in [Position2D(1, 0), Position2D(0, -1), Position2D(-1, 0), Position2D(0, 1)]:
            act_neighbor = add_positions(self.starting_position, neighbor_pos)
            if Position2D(-neighbor_pos.x, -neighbor_pos.y) in \
                    neighbor_fence_positions(Position2D(0, 0), self.position_dict[act_neighbor]):
                map_str += '1'
            else:
                map_str += '0'
        return fence_mapping[map_str]

    @cached_property
    def fence_pos_dict(self) -> dict[Position2D, int]:
        rd = {self.starting_position: 0}
        dq = deque([(self.starting_position, 0)])
        while dq:
            act_pos, act_step = dq.popleft()
            for next_pos in neighbor_fence_positions(act_pos, self.position_dict[act_pos]):
                if next_pos in rd or next_pos not in self.position_dict:
                    continue
                if act_pos not in neighbor_fence_positions(next_pos, self.position_dict[next_pos]):
                    continue
                rd[next_pos] = act_step + 1
                dq.append((next_pos, act_step + 1))
        return rd

    @property
    def internal_area_count(self) -> int:
        rv = 0
        for act_y in range(self.min_y, self.max_y + 1):
            inner_area = False
            prev_fence = ''
            for act_x in range(self.min_x, self.max_x + 1):
                if (act_pos := Position2D(act_x, act_y)) not in self.fence_pos_dict:
                    if inner_area:
                        rv += 1
                    continue
                act_fence = self.position_dict[act_pos] if act_pos != self.starting_position else self.starting_fence
                if act_fence == '-':
                    continue
                if act_fence == '|' or (prev_fence, act_fence) in [('F', 'J'), ('L', '7')]:
                    inner_area = not inner_area
                    prev_fence = ''
                    continue
                if act_fence in ['F', 'L']:
                    prev_fence = act_fence
        return rv


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    g = CGrid()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True):
        g.add_row(inp_row, p_chars_to_skip='.')
    answer1 = max(g.fence_pos_dict.values())
    answer2 = g.internal_area_count
    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 10, solve_puzzle)


if __name__ == '__main__':
    main()
