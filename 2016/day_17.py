from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from functools import cached_property
from hashlib import md5
from collections import deque
from typing import Generator


def get_possible_directions(p_act_str: str) -> Generator[str]:
    check_str = md5(p_act_str.encode()).hexdigest()
    for c, act_c in enumerate(check_str[:4]):
        if act_c in 'bcdef':
            yield 'UDLR'[c]


class CVaultState:
    dir_dict = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

    def __init__(self, p_vault_code: str):
        self.vault_code = p_vault_code
        self.max_x = self.max_y = 3

    @property
    def is_final_state(self) -> bool:
        return self.act_position == (self.max_x, self.max_y)

    @cached_property
    def act_position(self) -> tuple[int, int]:
        return (self.vault_code.count('R') - self.vault_code.count('L'),
                self.vault_code.count('D') - self.vault_code.count('U'))

    def yield_next_states(self) -> Generator[CVaultState]:
        for next_dir_str in get_possible_directions(self.vault_code):
            if self.act_position[0] + self.dir_dict[next_dir_str][0] in [-1, self.max_x + 1] \
              or self.act_position[1] + self.dir_dict[next_dir_str][1] in [-1, self.max_y + 1]:
                continue
            yield CVaultState(self.vault_code + next_dir_str)


def find_route(p_code_init: str) -> tuple[str, int]:
    dq = deque([[CVaultState(p_code_init), 0]])
    shortest_route_str = ''
    longest_path = 0
    while dq:
        act_state, act_step = dq.popleft()
        for next_state in act_state.yield_next_states():
            if next_state.is_final_state:
                longest_path = act_step + 1
                if shortest_route_str == '':
                    shortest_route_str = next_state.vault_code[len(p_code_init):]
            else:
                dq.append([next_state, act_step + 1])
    return shortest_route_str, longest_path


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    input_single_row = next(yield_input_data(p_input_file_path, p_whole_row=True), None)
    answer1, answer2 = find_route(input_single_row)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 17, solve_puzzle)


if __name__ == '__main__':
    main()
