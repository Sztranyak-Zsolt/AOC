from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from typing import Callable


def calc_eq(p_item_list: list[int]) -> int:
    return p_item_list[0]


def calc_and(p_item_list: list[int]) -> int:
    rv = p_item_list[0]
    for d_act_item in p_item_list[1:]:
        rv &= d_act_item
    return rv


def calc_or(p_item_list: list[int]) -> int:
    rv = p_item_list[0]
    for d_act_item in p_item_list[1:]:
        rv |= d_act_item
    return rv


def calc_not(p_item_list: list[int]) -> int:
    return 65535 - p_item_list[0]


def calc_rshift(p_item_list: list[int, int]) -> int:
    return (p_item_list[0] >> p_item_list[1]) & 65535


def calc_lshift(p_item_list: list[int, int]) -> int:
    return (p_item_list[0] << p_item_list[1]) & 65535


FORMULA_DICT = {'AND': calc_and,
                'OR': calc_or,
                'NOT': calc_not,
                'LSHIFT': calc_lshift,
                'RSHIFT': calc_rshift,
                'EQ': calc_eq}


class CTreeItem:
    def __init__(self):
        self.value: int | None = None
        self.inputs: list[int | CTreeItem] = []
        self.formula: Callable[[list[int]], int] | None = None

    @property
    def inputs_available(self) -> bool:
        for input_params in self.inputs:
            if isinstance(input_params, CTreeItem):
                if input_params.value is None:
                    return False
        return True

    def calculate_value(self):
        if self.inputs_available:
            self.value = self.formula([int(x) for x in self.inputs])

    def __int__(self):
        return self.value


class CTree:
    def __init__(self):
        self.tree_item_dict: dict[str, CTreeItem] = {}

    def return_formula_item(self, p_formula_name: str) -> int | CTreeItem:
        try:
            return int(p_formula_name)
        except ValueError:
            if p_formula_name not in self.tree_item_dict:
                self.tree_item_dict[p_formula_name] = CTreeItem()
            return self.tree_item_dict[p_formula_name]

    def add_formula(self, *args):
        if len(args) == 2:
            self.return_formula_item(args[1]).inputs.append(self.return_formula_item(args[0]))
            self.tree_item_dict[args[1]].formula = FORMULA_DICT['EQ']
            return
        if len(args) == 3:
            self.return_formula_item(args[2]).inputs.append(self.return_formula_item(args[1]))
            self.tree_item_dict[args[2]].formula = FORMULA_DICT['NOT']
            return
        self.return_formula_item(args[3]).inputs.append(self.return_formula_item(args[0]))
        self.return_formula_item(args[3]).inputs.append(self.return_formula_item(args[2]))
        self.tree_item_dict[args[3]].formula = FORMULA_DICT[args[1]]

    def calc_items(self):
        has_new_calculation = True
        while has_new_calculation:
            has_new_calculation = False
            for act_formula in [x for x in self.tree_item_dict.values() if x.inputs_available and x.value is None]:
                act_formula.calculate_value()
                has_new_calculation = True


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    formula_tree = CTree()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space='->'):
        formula_tree.add_formula(*inp_row)
    formula_tree.calc_items()
    answer1 = formula_tree.tree_item_dict['a'].value

    formula_tree2 = CTree()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space='->'):
        formula_tree2.add_formula(*inp_row)
    formula_tree2.tree_item_dict['b'].value = answer1
    formula_tree2.calc_items()
    answer2 = formula_tree2.tree_item_dict['a'].value

    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 7, solve_puzzle)


if __name__ == '__main__':
    main()
