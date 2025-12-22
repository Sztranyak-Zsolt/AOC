from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle

PORT_CONNECTIONS: dict[str, set[str]] = {}


def get_max_nodes(p_act_nodes: set[str], p_poss_nodes: set[str]) -> list[set[str]]:
    rv = [set()]
    for next_port in p_poss_nodes:
        if next_port <= max(p_act_nodes):
            continue
        if p_act_nodes - PORT_CONNECTIONS[next_port]:
            continue
        for nn in get_max_nodes(p_act_nodes | {next_port}, p_poss_nodes & PORT_CONNECTIONS[next_port]):
            rv.append(nn | {next_port})
    return rv


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0

    for port1, port2 in yield_input_data(p_input_file_path, p_chars_to_space='-', p_whole_row=False):
        PORT_CONNECTIONS.setdefault(port1, set()).add(port2)
        PORT_CONNECTIONS.setdefault(port2, set()).add(port1)

    for act_port, connected_ports in PORT_CONNECTIONS.items():
        if act_port[0] != 't':
            continue
        for n_port1 in connected_ports:
            if n_port1[0] == 't' and n_port1 <= act_port:
                continue
            for n_port2 in PORT_CONNECTIONS[n_port1]:
                if n_port2[0] == 't' and n_port2 <= act_port or n_port1 <= n_port2 or n_port2 not in connected_ports:
                    continue
                answer1 += 1

    poss_nodes = set(PORT_CONNECTIONS)

    lan_max_ports = 0

    for n1 in sorted(poss_nodes):
        poss_nodes.remove(n1)
        for act_lan in get_max_nodes({n1}, poss_nodes):
            if len(act_lan) >= lan_max_ports:
                lan_max_ports = len(act_lan)
                answer2 = ','.join(sorted({n1} | act_lan))
    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 23, solve_puzzle)


if __name__ == '__main__':
    main()
