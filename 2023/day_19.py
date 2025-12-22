import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from collections import deque
from math import prod
from operator import lt, eq, gt
from copy import deepcopy


def present_dict(p_present_raw: str) -> dict[str, int]:
    rd = {}
    p_presents = p_present_raw.replace('{', '').replace('}', '')
    for act_val in p_presents.split(','):
        rd[act_val[0]] = int(act_val[2:])
    return rd


class CRule:
    def __init__(self, p_id):
        self.id = p_id
        self.rule_condition = []


class CWorkflow:
    presents_set = {'x', 'm', 'a', 's'}
    func_dict = {'=': eq, '<': lt, '>': gt}

    def __init__(self):
        self.rules: dict[CRule] = {}

    @property
    def starting_rule(self) -> CRule:
        return self.get_rule('in')

    def get_rule(self, p_rule_id) -> CRule:
        if p_rule_id not in self.rules:
            self.rules[p_rule_id] = CRule(p_rule_id)
        return self.rules[p_rule_id]

    def add_rule(self, p_rules: str):
        act_rule = self.get_rule(p_rules[:p_rules.find('{')])
        act_conditions_raw = p_rules[len(act_rule.id)+1:-1]
        for act_condition in act_conditions_raw.split(','):
            if set(act_condition) & {'<', '>', '='}:
                rule_cond, target_rule_str = act_condition.split(':')
                cond_variable, cond_func, cond_value = rule_cond[0], self.func_dict[rule_cond[1]], int(rule_cond[2:])
                act_rule.rule_condition.append(((cond_variable, cond_func, cond_value), self.get_rule(target_rule_str)))
                continue
            act_rule.rule_condition.append((None, self.get_rule(act_condition)))

    def check_presents(self, p_present_dict: dict[str, int]) -> bool:
        act_rule = self.starting_rule
        while True:
            for act_condition, next_rule in act_rule.rule_condition:
                if act_condition is None:
                    act_rule = next_rule
                    break
                cond_variable, cond_func, cond_value = act_condition
                if cond_func(p_present_dict[cond_variable], cond_value):
                    act_rule = next_rule
                    break
            if act_rule.id == 'A':
                return True
            if act_rule.id == 'R':
                return False

    def accepted_presents_count(self, p_from_range: int, p_end_range: int):
        ranges_dict = {act_variable: [p_from_range, p_end_range] for act_variable in self.presents_set}
        to_be_processed = deque([[self.starting_rule, ranges_dict]])
        rv = 0
        while to_be_processed:
            act_rule, act_ranges_dict = to_be_processed.popleft()
            if act_rule.id == 'R':
                continue
            if act_rule.id == 'A':
                rv += prod(re - rs + 1 for rs, re in act_ranges_dict.values())
                continue
            for act_condition, next_rule in act_rule.rule_condition:
                if act_condition is None:
                    to_be_processed.append([next_rule, act_ranges_dict])
                    break
                cond_variable, cond_func, cond_value = act_condition
                str_state = cond_func(act_ranges_dict[cond_variable][0], cond_value)
                mid_state = cond_func(cond_value, cond_value)
                end_state = cond_func(act_ranges_dict[cond_variable][1], cond_value)
                if not(str_state or mid_state or end_state):
                    continue
                if str_state and mid_state and end_state \
                        or str_state and end_state \
                        and (cond_value < act_ranges_dict[cond_variable][0]
                             or cond_value > act_ranges_dict[cond_variable][1]):
                    to_be_processed.append([next_rule, act_ranges_dict])
                    break
                str_range_dict = deepcopy(act_ranges_dict)
                str_range_dict[cond_variable][1] = cond_value - (0 if str_state == mid_state else 1)
                to_be_processed.append([next_rule if str_state else act_rule, str_range_dict])
                if mid_state != end_state and mid_state != str_state:
                    mid_range_dict = deepcopy(act_ranges_dict)
                    mid_range_dict[cond_variable] = [cond_value, cond_value]
                    to_be_processed.append([next_rule if mid_state else act_rule, mid_range_dict])
                end_range_dict = deepcopy(act_ranges_dict)
                end_range_dict[cond_variable][0] = cond_value + (0 if end_state == mid_state else 1)
                to_be_processed.append([next_rule if end_state else act_rule, end_range_dict])
                break
        return rv


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = 0
    rh = CWorkflow()
    separator_found = False
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        if inp_row == '':
            separator_found = True
            continue
        if not separator_found:
            rh.add_rule(inp_row)
            continue
        act_presents_dict = present_dict(inp_row)
        if rh.check_presents(act_presents_dict):
            answer1 += sum(act_presents_dict.values())
    answer2 = rh.accepted_presents_count(1, 4000)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 19, solve_puzzle)


if __name__ == '__main__':
    main()
