import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


class SignalError(Exception):
    pass


class CCalculation:
    def __init__(self):
        self.vars = {"a": 0, "b": 0, "c": 0, "d": 0}
        self.instr_list = list()
        self.signal = 1

    @property
    def vars_code(self):
        return ''.join([f'{k}{v}' for k, v in self.vars.items()])

    def reset_vars(self):
        self.vars = {"a": 0, "b": 0, "c": 0, "d": 0}
        self.signal = 1

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

    def out(self, p_param1: str | int) -> tuple[int, bool]:
        if isinstance(p_param1, int):
            next_signal = p_param1
        else:
            next_signal = self.vars[p_param1]
        if next_signal == self.signal:
            raise SignalError
        self.signal = next_signal
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

    def calculate(self, p_act_index: int = 0, p_step_by_step: bool = False):
        act_index = p_act_index
        while True:
            try:
                if self.instr_list[act_index][0] == self.jnz:
                    self.multiplication_before_jnz(act_index)
                if self.instr_list[act_index][0] == self.tgl:
                    act_index += self.tgl(act_index, *self.instr_list[act_index][1])
                else:
                    act_index += self.instr_list[act_index][0](*self.instr_list[act_index][1])
                if p_step_by_step:
                    return act_index
            except IndexError:
                break

    def clock_signal_valid(self, p_signal_num: int) -> bool:
        self.reset_vars()
        self.vars['a'] = p_signal_num
        known_states = set()
        act_index = 0
        while True:
            if self.instr_list[act_index][0] == self.out:
                if self.vars_code in known_states:
                    return True
                known_states.add(self.vars_code)
            try:
                act_index = self.calculate(act_index, True)
            except SignalError:
                return False


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer2 = None
    c = CCalculation()
    for inp_row in yield_input_data(p_input_file_path):
        c.add_instruction(inp_row)

    act_a = 1

    while not c.clock_signal_valid(act_a):
        act_a += 1

    answer1 = act_a

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 25, solve_puzzle)


if __name__ == '__main__':
    main()
