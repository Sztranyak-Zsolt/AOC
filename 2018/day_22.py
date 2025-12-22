from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, Position2D, neighbor_positions
from functools import cached_property
from collections import defaultdict
import heapq


class CGridX(CGridBase):
    equipment_dict = {0: {'T', 'C'}, 1: {'C', 'N'}, 2: {'T', 'N'}}

    def __init__(self, p_depth: int, p_target: Position2D):
        super().__init__()
        self.starting_position = Position2D(0, 0)
        self.depth = p_depth
        self.target = p_target

    def get_position_erosion_level(self, p_position: Position2D) -> int:
        if p_position not in self.position_dict:
            if p_position in [self.starting_position, self.target]:
                geological_index = 0
            elif p_position.x == 0:
                geological_index = p_position.y * 48271
            elif p_position.y == 0:
                geological_index = p_position.x * 16807
            else:
                geological_index = self.get_position_erosion_level(Position2D(p_position.x - 1, p_position.y)) \
                                   * self.get_position_erosion_level(Position2D(p_position.x, p_position.y - 1))
            self.position_dict[p_position] = (geological_index + self.depth) % 20183
        return self.position_dict[p_position]

    def get_region_type(self, p_position: Position2D) -> int:
        return self.get_position_erosion_level(p_position) % 3

    @property
    def total_risk_level(self):
        rv = 0
        for d_y in range(self.starting_position.y, self.target.y + 1):
            for d_x in range(self.starting_position.x, self.target.x + 1):
                rv += self.get_region_type(Position2D(d_x, d_y))
        return rv

    @cached_property
    def quickest_route_pq(self) -> int:
        timer_heap = [(0, self.starting_position, 'T', [[0, self.starting_position, 'T']])]
        heapq.heapify(timer_heap)
        visited_positions = dict()
        visited_positions[(self.starting_position, 'T')] = 0
        while timer_heap:
            act_timer, act_position, act_equipment, act_chain = heapq.heappop(timer_heap)
            if act_position == self.target and act_equipment == 'T':
                return act_timer
            if visited_positions[(act_position, act_equipment)] < act_timer:
                continue
            for np in neighbor_positions(act_position):
                if -1 in np:
                    continue
                new_timer = act_timer + 1
                new_equipment = act_equipment
                if act_equipment not in self.equipment_dict[self.get_region_type(np)]:
                    new_timer += 7
                    new_equipment = list(self.equipment_dict[self.get_region_type(np)]
                                         & self.equipment_dict[self.get_region_type(act_position)])[0]
                if (np, new_equipment) not in visited_positions \
                        or visited_positions[(np, new_equipment)] > new_timer:
                    visited_positions[(np, new_equipment)] = new_timer
                else:
                    continue
                new_chain = act_chain.copy()
                new_chain.append([new_timer, np, new_equipment])
                heapq.heappush(timer_heap, (new_timer, np, new_equipment, new_chain))

    @cached_property
    def quickest_route_dp(self) -> int:
        timer_dict = defaultdict(lambda: [])
        timer_dict[0] = [[self.starting_position, 'T']]
        visited_dict = defaultdict(lambda: 9999999)
        visited_dict[(self.starting_position, 'T')] = 0
        act_timer = 0
        while True:
            if act_timer in timer_dict:
                for d_act_pos, d_eq in timer_dict[act_timer]:
                    if d_act_pos == self.target and d_eq == 'T':
                        return act_timer
                    for neighbor_pos in neighbor_positions(d_act_pos):
                        if -1 in neighbor_pos:
                            continue
                        new_timer = act_timer + 1
                        new_equipment = d_eq
                        if d_eq not in self.equipment_dict[self.get_region_type(neighbor_pos)]:
                            new_timer += 7
                            new_equipment = list(self.equipment_dict[self.get_region_type(neighbor_pos)]
                                                 & self.equipment_dict[self.get_region_type(d_act_pos)])[0]
                        if (neighbor_pos, new_equipment) not in visited_dict or \
                                visited_dict[(neighbor_pos, new_equipment)] > new_timer:
                            timer_dict[new_timer].append([neighbor_pos, new_equipment])
                            visited_dict[(neighbor_pos, new_equipment)] = new_timer
            act_timer += 1


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    depth_init = 0
    target_init = Position2D(0, 0)
    for i, inp_row in enumerate(yield_input_data(p_input_file_path, p_chars_to_space=',')):
        if i == 0:
            depth_init = inp_row[1]
        else:
            target_init = Position2D(inp_row[1], inp_row[2])
    g = CGridX(depth_init, target_init)
    answer1 = g.total_risk_level
    answer2 = g.quickest_route_dp

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 22, solve_puzzle)


if __name__ == '__main__':
    main()
