from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from copy import copy
from typing import Generator

class CBurrowSystem:
    def __init__(self):
        self.move_cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
        self.tunnel: list[str] = list('..a.b.c.d..')
        self.burrow: dict[str, list[str]] = {'A': [], 'B': [], 'C': [], 'D': []}

    def __copy__(self) -> CBurrowSystem:
        new_bs = CBurrowSystem()
        new_bs.tunnel = self.tunnel.copy()
        for k, v in self.burrow.items():
            new_bs.burrow[k] = v.copy()
        return new_bs

    @property
    def finished_burrow_list(self) -> list[str]:
        return [k for k, v in self.burrow.items() if len(v) == v.count('.') + v.count(k)]

    @property
    def tunnel_is_empty(self) -> bool:
        for b in self.burrow.keys():
            if b in self.tunnel:
                return False
        return True

    @property
    def finish_state(self) -> bool:
        return self.tunnel_is_empty and len(self.finished_burrow_list) == len(self.burrow)

    def tunnel_blocked(self, i1: int, i2: int) -> bool:
        i1c, i2c = sorted([i1, i2])
        for t in self.tunnel[i1c+1:i2c]:
            if t in self.burrow.keys():
                return True
        return False

    def yield_next_state_form_tunnel(self) -> Generator[tuple[CBurrowSystem, int]]:
        for i, act_tunnel_tile in enumerate(self.tunnel):
            if act_tunnel_tile not in self.burrow or act_tunnel_tile not in self.finished_burrow_list:
                continue
            move_from, move_to = sorted([i, self.tunnel.index(act_tunnel_tile.lower())])
            if self.tunnel_blocked(move_from, move_to):
                continue
            burrow_empty_index = self.burrow[act_tunnel_tile].count('.') - 1
            new_bs = copy(self)
            new_bs.tunnel[i] = '.'
            new_bs.burrow[act_tunnel_tile][burrow_empty_index] = act_tunnel_tile
            path_cost = (move_to - move_from + burrow_empty_index
                         + 1) * self.move_cost[act_tunnel_tile]
            yield new_bs, path_cost

    def yield_next_state_form_burrow(self) -> Generator[tuple[CBurrowSystem, int]]:
        for act_burrow_code, act_burrow_values in self.burrow.items():
            if act_burrow_code in self.finished_burrow_list:
                continue
            if (burrow_non_empty_index := act_burrow_values.count('.')) == len(act_burrow_values):
                continue
            act_amp = act_burrow_values[burrow_non_empty_index]
            for i, act_tunnel_tile in enumerate(self.tunnel):
                if act_tunnel_tile != '.':
                    continue
                move_from, move_to = sorted([i, self.tunnel.index(act_burrow_code.lower())])
                if self.tunnel_blocked(move_from, move_to):
                    continue
                new_bs = copy(self)
                new_bs.tunnel[i] = act_amp
                new_bs.burrow[act_burrow_code][burrow_non_empty_index] = '.'
                path_cost = (move_to - move_from + burrow_non_empty_index
                             + 1) * self.move_cost[act_amp]
                yield new_bs, path_cost

    def yield_next_states(self):
        for ns, npc in self.yield_next_state_form_burrow():
            yield ns, npc
        for ns, npc in self.yield_next_state_form_tunnel():
            yield ns, npc

    def __str__(self):
        r_str = ['#############',
                 "#" + ''.join(self.tunnel) + "#"]
        for i in zip(*self.burrow.values()):
            r_str.append(f'  #{i[0]}#{i[1]}#{i[2]}#{i[3]}#  ')
        r_str[2] = "##" + r_str[2][2:11] + "##"
        r_str.append('  #########  ')
        return '\n'.join(r_str)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return hash(self) == hash(other)


class CBurrowHandler:
    def __init__(self, p_burrow: CBurrowSystem):
        self.init_burrow = p_burrow
        self.cache = dict()

    def extend_burrows(self):
        self.init_burrow.burrow['A'] = [self.init_burrow.burrow['A'][0], 'D', 'D', self.init_burrow.burrow['A'][-1]]
        self.init_burrow.burrow['B'] = [self.init_burrow.burrow['B'][0], 'B', 'C', self.init_burrow.burrow['B'][-1]]
        self.init_burrow.burrow['C'] = [self.init_burrow.burrow['C'][0], 'A', 'B', self.init_burrow.burrow['C'][-1]]
        self.init_burrow.burrow['D'] = [self.init_burrow.burrow['D'][0], 'C', 'A', self.init_burrow.burrow['D'][-1]]

    @property
    def organize_cost(self):
        act_dict = {0: [self.init_burrow]}
        known_burrows = {self.init_burrow: 0}
        while act_dict:
            act_cost = min(act_dict.keys())
            act_burrows = act_dict.pop(act_cost)
            for act_burrow in act_burrows:
                if act_burrow.finish_state:
                    return act_cost
                if known_burrows.get(act_burrow, act_cost) < act_cost:
                    continue
                for nb, extra_cost in act_burrow.yield_next_states():
                    new_cost = act_cost + extra_cost
                    if nb in known_burrows and known_burrows[nb] <= new_cost:
                        continue
                    known_burrows[nb] = new_cost
                    if new_cost not in act_dict:
                        act_dict[new_cost] = []
                    act_dict[new_cost].append(nb)


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    bs = CBurrowSystem()

    for inp_row in list(yield_input_data(p_input_file_path, p_chars_to_space='#.'))[2:4]:
        for i, a in enumerate(inp_row):
            bs.burrow['ABCD'[i]] += [a]

    bh = CBurrowHandler(bs)
    answer1 = bh.organize_cost
    bh.extend_burrows()
    answer2 = bh.organize_cost

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 23, solve_puzzle)


if __name__ == '__main__':
    main()
