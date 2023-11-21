from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from functools import cached_property, cache


def yield_bitmap(act_bitmap: int, p_part_count: int = 1):
    act_cache = set()
    if p_part_count == 1:
        yield [act_bitmap]
        return
    if act_bitmap == 0:
        yield [0] * p_part_count
        return
    for mask in range((1 << act_bitmap.bit_length() - 1)):
        mask2 = (1 << act_bitmap.bit_length() - 1) | mask
        if (next_bm := act_bitmap & mask2) in act_cache:
            continue
        if next_bm == 0 and act_bitmap != 0:
            continue
        act_cache.add(next_bm)
        for next_part_bm in yield_bitmap(act_bitmap ^ next_bm, p_part_count - 1):
            yield [next_bm] + next_part_bm


class CValve:
    def __init__(self, p_code: str):
        self.code = p_code
        self.flow_rate = 0
        self.linked_valves: set[CValve] = set()

    def __str__(self):
        return self.code

    def __lt__(self, other):
        return self.code < other.code


class CValveHandle:
    def __init__(self):
        self.valve_dict: dict[str, CValve] = {}

    @cached_property
    def valves_with_value(self) -> list[CValve]:
        return [v for v in self.valve_dict.values() if v.flow_rate != 0]

    @cached_property
    def valve_route(self) -> dict[(CValve, CValve), int]:
        rd = {}
        for from_valve in self.valve_dict.values():
            for to_valve in self.valve_dict.values():
                if from_valve == to_valve:
                    rd[(from_valve, to_valve)] = 0
                    continue
                act_linked = {1: from_valve.linked_valves}
                act_step = 1
                while act_linked:
                    next_valves = act_linked.pop(act_step)
                    if to_valve in next_valves:
                        rd[(from_valve, to_valve)] = act_step
                        break
                    act_step += 1
                    act_linked[act_step] = set()
                    for nv in next_valves:
                        act_linked[act_step] |= nv.linked_valves
                else:
                    rd[(from_valve, to_valve)] = None
        return rd

    def get_valve(self, p_key: str) -> CValve:
        if p_key not in self.valve_dict:
            self.valve_dict[p_key] = CValve(p_key)
        return self.valve_dict[p_key]

    @cache
    def calc_release_valve_by_bitmap(self, p_act_valve: CValve, p_valves_to_open_index_bitmap: int, p_time: int) -> int:
        if p_time <= 0:
            return 0
        rv = 0
        for i, next_valve in enumerate(self.valves_with_value):
            act_bit = (1 << i)
            if p_valves_to_open_index_bitmap & act_bit:
                next_time = p_time - self.valve_route[(p_act_valve, next_valve)] - 1
                if next_time > 0:
                    rv = max(rv, next_valve.flow_rate * next_time +
                             self.calc_release_valve_by_bitmap(next_valve, p_valves_to_open_index_bitmap ^ act_bit,
                                                               next_time))
        return rv

    def calc_release_valve_value(self, p_starting_valve_list: list[CValve], p_time: int) -> int:
        rv = 0
        for bitmaps in yield_bitmap((1 << len(self.valves_with_value)) - 1, len(p_starting_valve_list)):
            rv = max(rv, sum([self.calc_release_valve_by_bitmap(v, bm, p_time) for v, bm
                              in zip(p_starting_valve_list, bitmaps)]))
        return rv

    def __hash__(self):
        return id(self)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    vh = CValveHandle()
    for _, base_tunnel, _, _, _, flow_rate, _, _, _, _, *linked_tunnels \
            in yield_input_data(p_input_file_path, p_chars_to_space='=;,'):
        vh.get_valve(base_tunnel).flow_rate = flow_rate
        vh.get_valve(base_tunnel).linked_valves = {vh.get_valve(lt) for lt in linked_tunnels}
    answer1 = vh.calc_release_valve_value([vh.get_valve('AA')], 30)
    answer2 = vh.calc_release_valve_value([vh.get_valve('AA'), vh.get_valve('AA')], 26)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 16, solve_puzzle)


if __name__ == '__main__':
    main()
