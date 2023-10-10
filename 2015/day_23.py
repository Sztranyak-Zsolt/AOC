from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from typing import Callable


class CRegister:
    def __init__(self, p_value: int):
        self.value = p_value


class CMachine:
    def __init__(self):
        self.register: dict[str, CRegister] = {'a': CRegister(0), 'b': CRegister(0)}
        self.instruction_list: list[tuple[Callable, list[int | str]]] = []

    def reset_registers(self):
        for reg in self.register.values():
            reg.value = 0

    def hlf(self, p_register: str):
        self.register[p_register].value //= 2
        return 1

    def tpl(self, p_register: str):
        self.register[p_register].value *= 3
        return 1

    def inc(self, p_register: str) -> int:
        self.register[p_register].value += 1
        return 1

    def jmp(self, p_offset: int) -> int:
        return p_offset

    def jie(self, p_register: str, p_offset: int) -> int:
        if self.register[p_register].value & 1 == 0:
            return p_offset
        return 1

    def jio(self, p_register: str, p_offset: int) -> int:
        if self.register[p_register].value == 1:
            return p_offset
        return 1

    def add_instruction(self, p_instruction_list: list[str]):
        func = eval(f"self.{p_instruction_list[0]}")
        self.instruction_list.append((func, p_instruction_list[1:]))

    def run_machine(self):
        act_index = 0
        try:
            while True:
                act_index += self.instruction_list[act_index][0](*self.instruction_list[act_index][1])
        except IndexError:
            return


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    m = CMachine()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space=','):
        m.add_instruction(inp_row)

    m.run_machine()
    answer1 = m.register['b'].value

    m.reset_registers()
    m.register['a'].value = 1
    m.run_machine()
    answer2 = m.register['b'].value

    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 23, solve_puzzle)


if __name__ == '__main__':
    main()
