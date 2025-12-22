import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, neighbor_positions
from collections import deque
from functools import cache, cached_property


class CGrid(CGridBase):

    @cached_property
    def starting_pos(self) -> Position2D:
        rp = [k for k, v in self.position_dict.items() if v == 'S'][0]
        del self.position_dict[rp]
        return rp

    @cached_property
    def clean_tiles(self) -> int:
        return sum(1 for p in self.yield_all_position() if p not in self.position_dict)

    @cached_property
    def step_to_check(self) -> int:
        return (self.max_x - self.min_x + 1) + (self.max_y - self.min_y + 1)

    @cache
    def can_reach_dict(self, p_starting_position: Position2D) -> dict[int, int]:
        target_num = self.step_to_check + 2
        act_pos = set()
        act_pos.add(p_starting_position)
        rd = {0: 1}
        for i in range(1, target_num + 1):
            next_pos = set()
            while act_pos:
                ap = act_pos.pop()
                for np in neighbor_positions(ap):
                    if np not in self.position_dict and self.is_position_on_grid(np):
                        next_pos.add(np)
            act_pos = next_pos
            rd[i] = len(act_pos)
        return rd

    def step(self, p_step_to_take: int):
        dq = deque()
        dq.append([Position2D(0, 0), self.starting_pos, p_step_to_take])
        rv = 0
        while dq:
            act_garden, act_position, act_step_remaining = dq.popleft()
            if act_garden.y <= 0 <= act_step_remaining - (act_position.y - self.min_y + 1):
                dq.append([Position2D(act_garden.x, act_garden.y - 1),
                           Position2D(act_position.x, self.max_y),
                           act_step_remaining - (act_position.y - self.min_y + 1)])
            if act_garden.y >= 0 and act_step_remaining - (self.max_y - act_position.y + 1) >= 0:
                dq.append([Position2D(act_garden.x, act_garden.y + 1),
                           Position2D(act_position.x, self.min_y),
                           act_step_remaining - (self.max_y - act_position.y + 1)])

            if act_step_remaining >= self.step_to_check:
                corr_step_remaining = self.step_to_check + act_step_remaining % 2
            else:
                corr_step_remaining = act_step_remaining
            rv += self.can_reach_dict(act_position)[corr_step_remaining]
            new_remaining = act_step_remaining - 66
            if new_remaining < 0:
                continue

            full_tile, new_remaining = divmod(new_remaining, self.step_to_check)
            if full_tile:
                full_tile -= 1
                new_remaining += self.step_to_check
            rv += 2 * full_tile * (self.can_reach_dict(Position2D(self.min_x, act_position.y))[263] +
                                   self.can_reach_dict(Position2D(self.min_x, act_position.y))[262])

            while new_remaining >= 0:
                if new_remaining >= self.step_to_check:
                    corr_step_remaining = self.step_to_check + new_remaining % 2
                else:
                    corr_step_remaining = new_remaining
                rv += self.can_reach_dict(Position2D(self.min_x, act_position.y))[corr_step_remaining]
                rv += self.can_reach_dict(Position2D(self.max_x, act_position.y))[corr_step_remaining]
                new_remaining -= 131

        return rv


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    g = CGrid()
    for y, inp_row in enumerate(yield_input_data(p_input_file_path, p_whole_row=True)):
        g.add_row(inp_row, p_chars_to_skip='.')

    answer1 = g.step(64)

    # info for PART2:
    #  - no # tiles on the border squares
    #  - no # tiles in the starting row and column
    #  - weight / height of the grid are 131; target number = 101150 * 2 * 131 + 65
    answer2 = g.step(26501365)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 21, solve_puzzle)


if __name__ == '__main__':
    main()
