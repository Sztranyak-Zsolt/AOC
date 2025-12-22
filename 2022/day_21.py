from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from typing import Callable
from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def add(n1: int, n2: int) -> int:
    return n1 + n2


def sub(n1: int, n2: int) -> int:
    return n1 - n2


def mul(n1: int, n2: int) -> int:
    return n1 * n2


def div(n1: int, n2: int) -> int:
    return n1 // n2


class CYell:
    def __init__(self, p_id):
        self.id = p_id
        self.value = 0
        self.formula: Callable[[int, int], int] | None = None
        self.n1: CYell | None = None
        self.n2: CYell | None = None

    @property
    def is_calculated(self):
        return self.formula is not None

    def calc_value(self):
        if not self.is_calculated:
            return self.value
        return self.formula(self.n1.calc_value(), self.n2.calc_value())


class CYellHandler:
    def __init__(self):
        self.yell_dict: dict[str, CYell] = {}

    def get_yell(self, p_key) -> CYell:
        if p_key not in self.yell_dict:
            self.yell_dict[p_key] = CYell(p_key)
        return self.yell_dict[p_key]

    def get_root_difi_for_humn(self, p_to_yell: int) -> int:
        self.yell_dict['humn'].value = p_to_yell
        return self.yell_dict['root'].n1.calc_value() - self.yell_dict['root'].n2.calc_value()

    @property
    def humn_to_yell(self):
        target_difi = 0
        prev_nums = [1, self.get_root_difi_for_humn(1)]
        next_nums = [2, self.get_root_difi_for_humn(2)]
        while target_difi < next_nums[1]:
            prev_nums = next_nums
            next_num = next_nums[0] * 2
            next_nums = [next_num, self.get_root_difi_for_humn(next_num)]
        while prev_nums[0] + 1 != next_nums[0]:
            avg_num = (prev_nums[0] + next_nums[0]) // 2
            avg_num_difi = self.get_root_difi_for_humn(avg_num)
            if avg_num_difi <= target_difi:
                next_nums = [avg_num, avg_num_difi]
            else:
                prev_nums = [avg_num, avg_num_difi]
        return next_nums[0]


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    func_dict = {'+': add, '-': sub, '*': mul, '/': div}
    yh = CYellHandler()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space=':'):
        if len(inp_row) == 2:
            yh.get_yell(inp_row[0]).value = inp_row[1]
            continue
        yh.get_yell(inp_row[0]).n1 = yh.get_yell(inp_row[1])
        yh.get_yell(inp_row[0]).n2 = yh.get_yell(inp_row[3])
        yh.get_yell(inp_row[0]).formula = func_dict[inp_row[2]]
    answer1 = yh.get_yell('root').calc_value()
    answer2 = yh.humn_to_yell

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 21, solve_puzzle)


if __name__ == '__main__':
    main()
