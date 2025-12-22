import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from functools import cache


class CRule:
    def __init__(self, p_id: int):
        self.id = p_id
        self.child_rules: str | list[list[CRule]] = list()

    @cache
    def check_rule(self, p_input_string: str) -> bool:
        if p_input_string == '':
            return False
        if isinstance(self.child_rules, str):
            return p_input_string == self.child_rules
        for act_rule in self.child_rules:
            if len(act_rule) == 1:
                if act_rule[0].check_rule(p_input_string):
                    return True
                continue
            if len(act_rule) == 2:
                for i_split in range(1, len(p_input_string)):
                    if act_rule[0].check_rule(p_input_string[:i_split]) \
                            and act_rule[1].check_rule(p_input_string[i_split:]):
                        return True
                continue
            for i_split in range(1, len(p_input_string) - 1):
                for i_split2 in range(i_split, len(p_input_string)):
                    if act_rule[0].check_rule(p_input_string[:i_split])\
                            and act_rule[1].check_rule(p_input_string[i_split:i_split2])\
                            and act_rule[2].check_rule(p_input_string[i_split2:]):
                        return True
            continue
        return False

    def __hash__(self):
        return id(self)


class CRuleHandler:
    def __init__(self):
        self.rule_dict: dict[int, CRule] = dict()
        self.str_list: list[str] = []

    def get_rule(self, p_key: int):
        if p_key not in self.rule_dict:
            self.rule_dict[p_key] = CRule(p_key)
        return self.rule_dict[p_key]

    def reset_cache(self):
        for r in self.rule_dict.values():
            r.check_rule.cache_clear()

    def add_rule(self, p_rule_id: int, p_child_rule_list: list[int | str]):
        act_rule = self.get_rule(p_rule_id)
        if p_child_rule_list[0] in ['a', 'b']:
            act_rule.child_rules = p_child_rule_list[0]
            return
        act_rule.child_rules = [[]]
        for act_ch_item in p_child_rule_list:
            if act_ch_item == '|':
                act_rule.child_rules.append([])
                continue
            act_rule.child_rules[-1].append(self.get_rule(act_ch_item))

    def valid_str_count(self, p_rule_id: int = 0) -> int:
        return len(['x' for s in self.str_list if self.rule_dict[p_rule_id].check_rule(s)])


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    rc = CRuleHandler()
    inp_iter = iter(yield_input_data(p_input_file_path, p_group_separator='\n\n', p_chars_to_space=':"'))
    for rule_key, *inp_rules in next(inp_iter):
        rc.add_rule(rule_key, inp_rules)
    for act_str in next(inp_iter):
        rc.str_list.append(act_str[0])
    answer1 = rc.valid_str_count(0)

    rc.rule_dict[8].child_rules.append([rc.rule_dict[42], rc.rule_dict[8]])
    rc.rule_dict[11].child_rules.append([rc.rule_dict[42], rc.rule_dict[11], rc.rule_dict[31]])

    rc.reset_cache()
    answer2 = rc.valid_str_count(0)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 19, solve_puzzle)


if __name__ == '__main__':
    main()
