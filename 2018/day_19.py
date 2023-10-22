from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from day_16 import operation_dict
from typing import Callable


def get_divs(n):
    factors = {1}
    max_p = int(n ** 0.5)
    p, inc = 2, 1
    while p <= max_p:
        while n % p == 0:
            factors.update([f*p for f in factors])
            n //= p
            max_p = int(n ** 0.5)
        p, inc = p + inc, 2
    if n > 1:
        factors.update([f * n for f in factors])
    return sorted(factors)


class CProgram:
    def __init__(self, p_instruction_pointer: int):
        self.instruction_pointer = p_instruction_pointer
        self.register: dict[int, int] = {p_instruction_pointer: 0}
        self.instruction_list: list[tuple[Callable, tuple[int]]] = []

    def set_pointer(self, p_instruction_pointer: int):
        self.instruction_pointer = p_instruction_pointer
        if p_instruction_pointer not in self.register:
            self.register[p_instruction_pointer] = 0

    def reset_register(self):
        self.register = {self.instruction_pointer: 0}

    def run_instructions(self, p_index: int) -> int:
        return self.instruction_list[p_index][0](self.register, *self.instruction_list[p_index][1])

    def execute_program(self):
        while 0 <= self.register[self.instruction_pointer] < len(self.instruction_list):
            plus_step = self.run_instructions(self.register[self.instruction_pointer])
            self.register[self.instruction_pointer] += plus_step


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    p = CProgram(0)
    for inp_row in yield_input_data(p_input_file_path):
        if inp_row[0] == '#ip':
            p.set_pointer(inp_row[1])
        else:
            p.instruction_list.append((operation_dict[inp_row[0]], tuple(inp_row[1:])))
    p.execute_program()
    answer1 = p.register[0]

    p.reset_register()
    p.register[0] = 1
    # program summarize of all divisors of reg5 after initialization

    while p.register[p.instruction_pointer] != 1:
        plus_step = p.run_instructions(p.register[p.instruction_pointer])
        p.register[p.instruction_pointer] += plus_step

    answer2 = sum(get_divs(p.register[5]))

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 19, solve_puzzle)


if __name__ == '__main__':
    main()
