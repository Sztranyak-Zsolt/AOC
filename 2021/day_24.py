from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from typing import Callable


def add(p_register: dict[str, int], p_key: str, p_value: int | str):
    if isinstance(p_value, str):
        p_value = p_register[p_value]
    p_register[p_key] += p_value


def mul(p_register: dict[str, int], p_key: str, p_value: int | str):
    if isinstance(p_value, str):
        p_value = p_register[p_value]
    p_register[p_key] *= p_value


def div(p_register: dict[str, int], p_key: str, p_value: int | str):
    if isinstance(p_value, str):
        p_value = p_register[p_value]
    p_register[p_key] //= p_value


def mod(p_register: dict[str, int], p_key: str, p_value: int | str):
    if isinstance(p_value, str):
        p_value = p_register[p_value]
    p_register[p_key] %= p_value


def eql(p_register: dict[str, int], p_key: str, p_value: int | str):
    if isinstance(p_value, str):
        p_value = p_register[p_value]
    p_register[p_key] = 1 if p_register[p_key] == p_value else 0


def inp(p_register: dict[str, int], p_key: str, p_value: int):
    p_register[p_key] = p_value


class CALU:
    """
    External program add number in 26 number system and check it in another phase
    e.g.: the first number + 3 are added and this is checked against the last phase number (+7)
          -> first number = last number + 4
    """
    def __init__(self):
        self.vars = {"w": 0, "x": 0, "y": 0, "z": 0}
        self.instr_list: list[tuple[Callable, str, int | str | None]] = list()

    @property
    def phase_links(self) -> dict[tuple[int, int], int]:
        rd = {}
        check_index: list[tuple[int, int]] = []
        for i, (instr1, instr2, instr3) in enumerate(zip(self.instr_list[4::18], self.instr_list[5::18],
                                                         self.instr_list[15::18])):
            if instr1[2] == 1:  # adding number to check list
                check_index.append((i, instr3[-1]))
            else:  # number validation
                last_index, last_addition = check_index.pop()
                rd[(last_index, i)] = last_addition + instr2[-1]
        return rd

    def calculate(self, p_input_num: list[int]):
        for act_function, func_param1, func_param2 in self.instr_list:
            if act_function == inp:
                try:
                    func_param2 = p_input_num.pop(0)
                except IndexError:
                    return
            act_function(self.vars, func_param1, func_param2)

    def reset_variables(self):
        self.vars = {"w": 0, "x": 0, "y": 0, "z": 0}

    def check_number_is_valid(self, p_num_str: str) -> bool:
        if str(p_num_str).count('0') != 0:
            return False
        self.reset_variables()
        self.calculate([int(x) for x in p_num_str])
        return self.vars["z"] == 0

    @property
    def min_accepted(self) -> str:
        rn = [0] * 14
        for (n1, n2), dif in self.phase_links.items():
            if dif >= 0:
                rn[n1] = 1 + dif
                rn[n2] = 1
            else:
                rn[n2] = 1
                rn[n1] = 1 - dif
        return ''.join([str(v) for v in rn])

    @property
    def max_accepted(self) -> str:
        rn = [0] * 14
        for (n1, n2), dif in self.phase_links.items():
            if dif >= 0:
                rn[n1] = 9 - dif
                rn[n2] = 9
            else:
                rn[n2] = 9 + dif
                rn[n1] = 9
        return ''.join([str(v) for v in rn])


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    func_dict = {'inp': inp, 'add': add, 'mul': mul, 'div': div, 'mod': mod, 'eql': eql}
    alu = CALU()
    for inp_row in yield_input_data(p_input_file_path):
        if len(inp_row) == 2:
            alu.instr_list.append((func_dict[inp_row[0]], inp_row[1], None))
        else:
            alu.instr_list.append((func_dict[inp_row[0]], inp_row[1], inp_row[2]))
    answer1 = alu.min_accepted
    answer2 = alu.max_accepted

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 24, solve_puzzle)


if __name__ == '__main__':
    main()
