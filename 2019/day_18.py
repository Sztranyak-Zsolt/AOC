from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, Position2D, neighbor_positions
from functools import cached_property, cache
from collections import deque


class CGridX(CGridBase):
    def __init__(self):
        super().__init__()
        self.starting_positions: dict[str, Position2D] = {}
        self.object_position_dict: dict[str, Position2D] = {}

    def add_item(self, p_position: Position2D, p_item: str,
                 set_border_on_init: bool = False):
        super().add_item(p_position, p_item, set_border_on_init)
        if p_item == '@':
            self.starting_positions[p_item] = p_position
        elif p_item.isalpha():
            self.object_position_dict[p_item] = p_position

    def change_starting_location(self):
        for sp in neighbor_positions(self.starting_positions['@'], p_return_near=True, p_return_self=True):
            self.add_item(sp, '#')
            self.wall_set.add(sp)
        for i, sp in enumerate(neighbor_positions(self.starting_positions['@'], p_return_near=False,
                                                  p_return_corner=True)):
            self.add_item(sp, str(i))
            self.starting_positions[str(i)] = sp
        del self.starting_positions['@']

    @cached_property
    def wall_set(self) -> set[Position2D]:
        return {p for p, v in self.position_dict.items() if v == '#'}

    @cache
    def reachable_objects(self, p_item: str) -> dict[str, int]:
        if p_item in self.object_position_dict:
            p_position = self.object_position_dict[p_item]
        elif p_item in self.starting_positions:
            p_position = self.starting_positions[p_item]
        else:
            return {}
        dq = deque([(p_position, 0)])
        known_positions = set(p_position)
        rd = {}
        while dq:
            act_pos, act_step = dq.popleft()
            for next_pos in neighbor_positions(act_pos):
                if next_pos in self.wall_set or next_pos in known_positions:
                    continue
                known_positions.add(next_pos)
                if next_pos not in self.position_dict or not self.position_dict[next_pos].isalpha():
                    dq.append((next_pos, act_step + 1))
                else:
                    rd[self.position_dict[next_pos]] = act_step + 1
        return rd

    @cached_property
    def key_pair_path(self) -> dict[(str, str), (int, set[str])]:
        rd = {}
        for act_item in list(self.starting_positions) + [v for v, p in self.object_position_dict.items()
                                                         if v.islower()]:
            dq = deque([[act_item, 0, set()]])
            known_items = {act_item}
            while dq:
                act_object, act_path_length, act_keys_needed = dq.popleft()
                for next_object, next_object_path_cost in self.reachable_objects(act_object).items():
                    if next_object in known_items:
                        continue
                    known_items.add(next_object)
                    next_keys_needed = act_keys_needed.copy()
                    if next_object.islower():
                        rd[(act_item, next_object)] = (act_path_length + next_object_path_cost, act_keys_needed)
                    else:
                        next_keys_needed.add(next_object.lower())
                    dq.append([next_object, act_path_length + next_object_path_cost, next_keys_needed])
        return rd

    @property
    def step_needed_to_collect_all_keys(self) -> int:
        all_keys = {k for k in self.object_position_dict if k.islower()}
        step_dict = {0: [(all_keys, set(self.starting_positions), set())]}
        known_positions = set()
        while step_dict:
            act_step_counter = min(step_dict)
            act_step_possibilities = step_dict.pop(act_step_counter)
            while act_step_possibilities:
                act_keys_needed, act_reached_objects, act_keys_owned = act_step_possibilities.pop(0)
                if act_keys_needed == set():
                    return act_step_counter
                if (''.join(sorted(act_reached_objects)), ''.join(sorted(act_keys_owned))) in known_positions:
                    continue
                known_positions.add((''.join(sorted(act_reached_objects)), ''.join(sorted(act_keys_owned))))
                for act_reached_object in act_reached_objects:
                    for next_key in act_keys_needed:
                        if (act_reached_object, next_key) not in self.key_pair_path:
                            continue
                        next_cost, next_keys_needed = self.key_pair_path[(act_reached_object, next_key)]
                        if next_keys_needed - act_keys_owned != set():
                            continue
                        next_path_cost = act_step_counter + next_cost
                        if next_path_cost not in step_dict:
                            step_dict[next_path_cost] = []
                        step_dict[next_path_cost].append((act_keys_needed - {next_key},
                                                          act_reached_objects - {act_reached_object} | {next_key},
                                                          act_keys_owned | {next_key}))


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    g = CGridX()
    g2 = CGridX()
    for inp_row in yield_input_data(p_input_file_path, p_reversed=True, p_whole_row=True):
        g.add_row(inp_row, p_chars_to_skip='.')
        g2.add_row(inp_row, p_chars_to_skip='.')

    answer1 = g.step_needed_to_collect_all_keys

    g2.change_starting_location()
    answer2 = g2.step_needed_to_collect_all_keys

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 18, solve_puzzle)


if __name__ == '__main__':
    main()
