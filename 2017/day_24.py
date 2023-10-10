from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from collections import defaultdict, deque
from typing import Iterable


class CBridgeHandler:
    def __init__(self):
        self.port_dict: defaultdict[int, set[int]] = defaultdict(lambda: set())

    def yield_bridges(self) -> Iterable[list[int]]:
        dq = deque([[[0], set()]])
        while dq:
            port_bridge, act_used_bridges = dq.popleft()
            act_port = port_bridge[-1]
            new_port_found = False
            for next_port in self.port_dict[act_port]:
                if (act_port, next_port) in act_used_bridges or (next_port, act_port) in act_used_bridges:
                    continue
                new_port_found = True
                dq.append([port_bridge + [next_port], act_used_bridges | {tuple([act_port, next_port])}])
            if not new_port_found:
                yield port_bridge


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    answer1 = answer2 = 0
    bh = CBridgeHandler()

    for port1, port2 in yield_input_data(p_input_file_path, p_chars_to_space='/'):
        bh.port_dict[port1].add(port2)
        bh.port_dict[port2].add(port1)

    max_length = 0
    for act_bridge in bh.yield_bridges():
        bridge_strength = sum(act_bridge) * 2 - act_bridge[-1]
        if len(act_bridge) == max_length:
            answer2 = max(answer2, bridge_strength)
        if len(act_bridge) > max_length:
            answer2 = bridge_strength
        answer1 = max(answer1, bridge_strength)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 24, solve_puzzle)


if __name__ == '__main__':
    main()
