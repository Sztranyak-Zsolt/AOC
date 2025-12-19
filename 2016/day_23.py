import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


class CCalculation:
    def __init__(self):
        self.vars = {"a": 0, "b": 0, "c": 0, "d": 0}
        self.instr_list = list()

    def reset_vars(self):
        self.vars = {"a": 0, "b": 0, "c": 0, "d": 0}

    def cpy(self, p_param1: str | int, p_param2: str | int) -> int:
        if isinstance(p_param2, int):
            pass
        elif isinstance(p_param1, int):
            self.vars[p_param2] = p_param1
        else:
            self.vars[p_param2] = self.vars[p_param1]
        return 1

    def inc(self, p_param1: str) -> int:
        self.vars[p_param1] += 1
        return 1

    def dec(self, p_param1: str) -> int:
        self.vars[p_param1] -= 1
        return 1

    def jnz(self, p_param1: str | int, p_param2: str | int) -> int:
        if isinstance(p_param1, int):
            if p_param1 != 0:
                if isinstance(p_param2, int):
                    return p_param2
                return self.vars[p_param2]
        else:
            if self.vars[p_param1] != 0:
                if isinstance(p_param2, int):
                    return p_param2
                return self.vars[p_param2]
        return 1

    def tgl(self, p_act_index: int, p_additional_index: int | str):
        if isinstance(p_additional_index, str):
            p_index_to_tgl = p_act_index + self.vars[p_additional_index]
        else:
            p_index_to_tgl = p_act_index + p_additional_index
        if p_index_to_tgl < 0 or p_index_to_tgl >= len(self.instr_list):
            pass
        elif self.instr_list[p_index_to_tgl][0] in [self.tgl, self.dec]:
            self.instr_list[p_index_to_tgl][0] = self.inc
        elif self.instr_list[p_index_to_tgl][0] == self.inc:
            self.instr_list[p_index_to_tgl][0] = self.dec
        elif self.instr_list[p_index_to_tgl][0] == self.cpy:
            self.instr_list[p_index_to_tgl][0] = self.jnz
        elif self.instr_list[p_index_to_tgl][0] == self.jnz:
            self.instr_list[p_index_to_tgl][0] = self.cpy
        return 1

    def add_instruction(self, p_instruction_row: list[int | str]):
        self.instr_list.append([eval(f"self.{p_instruction_row[0]}"), p_instruction_row[1:]])

    def multiplication_before_jnz(self, p_index: int):
        if p_index >= 5 and self.instr_list[p_index][1][1] == -5:
            if self.instr_list[p_index-5][0] == self.cpy \
               and self.instr_list[p_index-4][0] == self.inc \
               and self.instr_list[p_index-3][0] == self.dec \
               and self.instr_list[p_index-5][1][1] == self.instr_list[p_index-3][1][0] \
               and self.instr_list[p_index-2][0] == self.jnz and self.instr_list[p_index-2][1][1] == -2 \
               and self.instr_list[p_index-1][0] == self.dec:
                if isinstance(self.instr_list[p_index-5][1][0], int):
                    mp1 = self.instr_list[p_index-5][1][0]
                else:
                    mp1 = self.vars[self.instr_list[p_index-5][1][0]]
                mp2 = self.instr_list[p_index-1][1][0]
                t = self.instr_list[p_index-4][1][0]
                if mp1 != mp2 and mp1 != t and mp2 != t:
                    self.vars[t] += mp1 * self.vars[mp2]
                    self.vars[mp2] = 0

    def calculate(self):
        act_index = 0
        while True:
            try:
                if self.instr_list[act_index][0] == self.jnz:
                    self.multiplication_before_jnz(act_index)
                if self.instr_list[act_index][0] == self.tgl:
                    act_index += self.tgl(act_index, *self.instr_list[act_index][1])
                else:
                    act_index += self.instr_list[act_index][0](*self.instr_list[act_index][1])
            except IndexError:
                break


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    c1 = CCalculation()
    c2 = CCalculation()
    for inp_row in yield_input_data(p_input_file_path):
        c1.add_instruction(inp_row)
        c2.add_instruction(inp_row)

    c1.vars['a'] = 7
    c1.calculate()
    answer1 = c1.vars['a']

    c2.vars['a'] = 12
    c2.calculate()
    answer2 = c2.vars['a']

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 23, solve_puzzle)


if __name__ == '__main__':
    main()
