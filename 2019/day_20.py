import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, neighbor_positions, add_positions
from collections import deque
from functools import cache


class CMaze(CGridBase):
    def __init__(self):
        super().__init__()
        self.portals_decode: dict[Position2D, (str, bool)] = {}
        self.portals_code: dict[(str, bool), Position2D] = {}
        self.walls_set = set()
        self.starting_position: Position2D | None = None
        self.target_position: Position2D | None = None

    def set_portals_and_walls(self):
        for act_position, act_item in self.position_dict.items():
            if not act_item.isupper():
                continue
            for act_dir in neighbor_positions():
                if self.position_dict.get(add_positions(act_position, act_dir), '') == '.':
                    portal_position = act_position
                    prev_position = add_positions(act_position, Position2D(-act_dir.x, -act_dir.y))
                    if act_dir in [Position2D(1, 0), Position2D(0, -1)]:
                        portal_code = self.position_dict[prev_position] + self.position_dict[act_position]
                    else:
                        portal_code = self.position_dict[act_position] + self.position_dict[prev_position]
                    if portal_code == 'AA':
                        self.starting_position = portal_position
                    elif portal_code == 'ZZ':
                        self.target_position = portal_position
                    outer = portal_position.x <= 1 or portal_position.x >= self.max_x - 1 \
                        or portal_position.y <= 1 or portal_position.y >= self.max_y - 1
                    self.portals_decode[portal_position] = (portal_code, outer)
                    self.portals_code[(portal_code, outer)] = portal_position
        self.walls_set = {p for p, v in self.position_dict.items() if v == '#'}

    @cache
    def portals_neighbor_path(self, p_portal: str, p_outer_portal: bool) -> dict[(str, int), int]:
        rd = {}
        init_position = self.portals_code[(p_portal, p_outer_portal)]
        known_positions = {init_position}
        dq = deque([[init_position, 0]])
        while dq:
            act_position, act_step = dq.popleft()
            for np in neighbor_positions(act_position):
                if np in known_positions:
                    continue
                known_positions.add(np)
                if np in self.portals_decode:
                    rd[(self.portals_decode[np])] = act_step
                    continue
                if np in self.walls_set or np not in self.position_dict:
                    continue
                dq.append([np, act_step + 1])
        return rd

    def shortest_path_to_target(self, p_recursive_maze: bool):
        known_positions = {('AA', 0)}
        step_dict = {0: [(('AA', True), 0)]}
        while step_dict:
            act_step_counter = min(step_dict)
            act_step_possibilities = step_dict.pop(act_step_counter)
            while act_step_possibilities:
                act_portal, act_level = act_step_possibilities.pop(0)
                if act_portal[0] == 'ZZ' and (not p_recursive_maze or act_level == -1):
                    return act_step_counter - 1
                if act_portal[0] == 'ZZ':
                    continue
                for next_portal, next_cost in self.portals_neighbor_path(act_portal[0], act_portal[1]).items():
                    if not p_recursive_maze:
                        next_level = act_level
                    elif next_portal[1]:
                        next_level = act_level - 1
                    else:
                        next_level = act_level + 1
                    if next_portal[0] == 'AA' or next_level == -1 and next_portal[0] != 'ZZ' \
                            or (next_portal[0], min(act_level, next_level)) in known_positions:
                        continue
                    known_positions.add((next_portal[0], min(act_level, next_level)))
                    if act_step_counter + next_cost not in step_dict:
                        step_dict[act_step_counter + next_cost] = []
                    step_dict[act_step_counter + next_cost].append(((next_portal[0], not next_portal[1]), next_level))

    def __hash__(self) -> int:
        return id(self)


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    m = CMaze()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True):
        m.add_row(inp_row, p_chars_to_skip=' ')
    m.set_portals_and_walls()
    answer1 = m.shortest_path_to_target(False)
    answer2 = m.shortest_path_to_target(True)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 20, solve_puzzle)


if __name__ == '__main__':
    main()
