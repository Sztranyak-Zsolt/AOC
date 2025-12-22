from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from math import lcm, prod


class CMonkey:
    def __init__(self):
        self.starting_item_list: list[int] = list()
        self.item_list: list[int] = list()
        self.valuation_function = lambda x: 0
        self.test_div_by: int = 0
        self.throw_to_monkey: dict[bool: CMonkey] = dict()
        self.inspection_counter: int = 0

    def check_items(self, p_release_function=lambda x: x // 3):
        while self.item_list:
            self.inspection_counter += 1
            act_item_value = self.item_list.pop(0)
            act_item_value = self.valuation_function(act_item_value)
            act_item_value = p_release_function(act_item_value)
            self.throw_to_monkey[act_item_value % self.test_div_by == 0].item_list.append(act_item_value)

    def reset_monkey(self):
        self.item_list = self.starting_item_list.copy()
        self.inspection_counter = 0


class CMonkeyGang:
    def __init__(self):
        self.monkey_dict: dict[int: CMonkey] = {}
        self.common_mod: int = 1

    def add_monkey(self, p_monkey_id: int, p_item_list: list[int], p_valuation_function,
                   p_test_div_by: int, p_monkey_true_id: int, p_monkey_false_id: int):
        if p_monkey_id not in self.monkey_dict:
            self.monkey_dict[p_monkey_id] = CMonkey()
        self.monkey_dict[p_monkey_id].starting_item_list = p_item_list
        self.monkey_dict[p_monkey_id].item_list = p_item_list.copy()
        self.monkey_dict[p_monkey_id].valuation_function = p_valuation_function
        self.monkey_dict[p_monkey_id].test_div_by = p_test_div_by
        if p_monkey_true_id not in self.monkey_dict:
            self.monkey_dict[p_monkey_true_id] = CMonkey()
        self.monkey_dict[p_monkey_id].throw_to_monkey[True] = self.monkey_dict[p_monkey_true_id]
        if p_monkey_false_id not in self.monkey_dict:
            self.monkey_dict[p_monkey_false_id] = CMonkey()
        self.monkey_dict[p_monkey_id].throw_to_monkey[False] = self.monkey_dict[p_monkey_false_id]
        self.common_mod = lcm(self.common_mod, p_test_div_by)

    def reset_gang(self):
        for m in self.monkey_dict.values():
            m.reset_monkey()

    def check_items_base(self):
        for k, m in sorted(self.monkey_dict.items()):
            m.check_items()

    def check_items_adv(self):
        for k, m in sorted(self.monkey_dict.items()):
            m.check_items(lambda x: x % self.common_mod)


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    mg = CMonkeyGang()
    for act_monkey in yield_input_data(p_input_file_path, p_group_separator='\n\n', p_chars_to_space=':,'):
        mg.add_monkey(act_monkey[0][-1], act_monkey[1][2:],
                      eval("lambda old: " + ' '.join([str(x) for x in act_monkey[2][-3:]])),
                      act_monkey[3][-1], act_monkey[4][-1], act_monkey[5][-1])
    for i in range(20):
        mg.check_items_base()

    answer1 = prod(sorted([x.inspection_counter for x in mg.monkey_dict.values()])[-2:])

    mg.reset_gang()
    for i in range(10000):
        mg.check_items_adv()

    answer2 = prod(sorted([x.inspection_counter for x in mg.monkey_dict.values()])[-2:])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 11, solve_puzzle)


if __name__ == '__main__':
    main()
