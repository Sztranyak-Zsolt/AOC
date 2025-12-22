from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from collections import defaultdict
from functools import cached_property


class CNode:
    def __init__(self, p_id: str):
        self.id = p_id
        self.output_link: list[CNode] = []
        self.input_link: list[CNode] = []

    def add_child(self, p_child: CNode) -> None:
        self.output_link.append(p_child)
        p_child.input_link.append(self)

    @property
    def possible_paths(self) -> int:
        return self.possible_paths_to_node('out')

    def possible_paths_to_node(self, p_target) -> int:
        if self.id == p_target:
            return 1
        return sum(iter(act_child.possible_paths_to_node(p_target) for act_child in self.output_link), start=0)

    @cached_property
    def possible_paths_fft_dac(self) -> defaultdict[tuple[bool, bool], int]:
        if self.id == 'out':
            rd = defaultdict(int)
            rd[(False, False)] = 1
            return rd
        act_poss_dict: defaultdict[tuple[bool, bool], int] = defaultdict(int)
        for act_child in self.output_link:
            for next_flags, next_poss_count in act_child.possible_paths_fft_dac.items():
                act_flag = (next_flags[0] or self.id == 'fft', next_flags[1] or self.id == 'dac')
                act_poss_dict[act_flag] += next_poss_count
        return act_poss_dict

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        return self is other


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    node_dict = {}
    for parent_str, *children_str in yield_input_data(p_input_file_path, p_chars_to_space=':'):
        act_parent_node = node_dict.setdefault(parent_str, CNode(parent_str))
        for act_child_str in children_str:
            act_child_node = node_dict.setdefault(act_child_str, CNode(act_child_str))
            act_parent_node.add_child(act_child_node)
    answer1 = node_dict['you'].possible_paths
    answer2 = node_dict['svr'].possible_paths_fft_dac[True, True]
    return answer1, answer2


def main():
    aoc_solve_puzzle(2025, 11, solve_puzzle)


if __name__ == '__main__':
    main()







def get_answer1() -> int:
    node_dict = {}
    with open('input1.txt', 'r') as f:
        for act_row in f.readlines():
            parent_str, *children_str = act_row.strip().replace(':', '').split()
            act_parent_node = node_dict.setdefault(parent_str, CNode(parent_str))
            for act_child_str in children_str:
                act_child_node = node_dict.setdefault(act_child_str, CNode(act_child_str))
                act_parent_node.add_child(act_child_node)
    ans1 = node_dict['you'].possible_paths
    return ans1


def get_answer2() -> int:
    node_dict = {}
    with open('input1.txt', 'r') as f:
        for act_row in f.readlines():
            parent_str, *children_str = act_row.strip().replace(':', '').split()
            act_parent_node = node_dict.setdefault(parent_str, CNode(parent_str))
            for act_child_str in children_str:
                act_child_node = node_dict.setdefault(act_child_str, CNode(act_child_str))
                act_parent_node.add_child(act_child_node)
    ans2 = node_dict['svr'].possible_paths_fft_dac[True, True]
    return ans2

