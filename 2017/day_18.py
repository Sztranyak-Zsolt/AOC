from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from collections import defaultdict
from typing import Self


class ExceptionRCVFound(Exception):
    pass


class CTablet:
    def __init__(self, p_prog_id):
        self.id = p_prog_id
        self.register: defaultdict[str, int] = defaultdict(lambda: 0)
        self.register['p'] = p_prog_id
        self.instruction_list = list()
        self.snd_list = []
        self.snd_counter = 0
        self.twin_program: Self = self

    def reset_values(self):
        self.register: defaultdict[str, int] = defaultdict(lambda: 0)
        self.register['p'] = self.id
        self.snd_list = []
        self.snd_counter = 0

    def add_instruction(self, p_raw_list: list[str | int]):
        self.instruction_list.append([eval(f'self.{p_raw_list[0]}'), p_raw_list[1:]])

    def ret_val(self, p_param: str | int) -> int:
        if isinstance(p_param, int):
            return p_param
        else:
            return self.register[p_param]

    def snd(self, p_param: str) -> int:
        self.snd_list.append(self.register[p_param])
        self.snd_counter += 1
        return 1

    def set(self, p_param1: str, p_param2: str | int) -> int:
        self.register[p_param1] = self.ret_val(p_param2)
        return 1

    def add(self, p_param1: str, p_param2: str | int) -> int:
        self.register[p_param1] += self.ret_val(p_param2)
        return 1

    def mul(self, p_param1: str, p_param2: str | int) -> int:
        self.register[p_param1] *= self.ret_val(p_param2)
        return 1

    def mod(self, p_param1: str, p_param2: str | int) -> int:
        self.register[p_param1] %= self.ret_val(p_param2)
        return 1

    def rcv(self, p_param: str | int):
        if self.twin_program == self:
            if self.ret_val(p_param) != 0:
                raise ExceptionRCVFound
        else:
            if not self.twin_program.snd_list:
                return 0
            self.register[p_param] = self.twin_program.snd_list.pop(0)
        return 1

    def jgz(self, p_param1: str | int, p_param2: str | int):
        if self.ret_val(p_param1) > 0:
            return self.ret_val(p_param2)
        return 1

    def operate_step(self, p_instr_index: int = 0):
        try:
            return p_instr_index + self.instruction_list[p_instr_index][0](*self.instruction_list[p_instr_index][1])
        except IndexError:
            return p_instr_index

    def play(self):
        act_index = 0
        while True:
            try:
                act_index = self.operate_step(act_index)
            except ExceptionRCVFound:
                return


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    d1 = CTablet(0)
    d2 = CTablet(1)
    for inp_row in yield_input_data(p_input_file_path):
        d1.add_instruction(inp_row)
        d2.add_instruction(inp_row)
    d1.play()
    answer1 = d1.snd_list[-1]

    d1.reset_values()

    d1.twin_program = d2
    d2.twin_program = d1

    prev_run_index = (-1, -1)
    act_run_index = (0, 0)
    while prev_run_index != act_run_index:
        prev_run_index = act_run_index
        act_run_index = (d1.operate_step(act_run_index[0]), d2.operate_step(act_run_index[1]))
    answer2 = d2.snd_counter

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 18, solve_puzzle)


if __name__ == '__main__':
    main()
