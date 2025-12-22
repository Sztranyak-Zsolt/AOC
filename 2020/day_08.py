import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


class CCalculation:
    def __init__(self):
        self.func_decode = {'nop': self.nop, 'acc': self.acc, 'jmp': self.jmp}
        self.acc_value = 0
        self.instr_list = list()
        self.program_finished = False

    def reset_vars(self):
        self.acc_value = 0
        self.program_finished = False

    def add_instruction(self, p_func_code: str, p_func_param: int):
        self.instr_list.append([self.func_decode[p_func_code], p_func_param])

    def acc(self, p_value: int) -> int:
        self.acc_value += p_value
        return 1

    def nop(self, p_value: int) -> int:
        return 1

    def jmp(self, p_value: int) -> int:
        return p_value

    def calc_first_loop(self):
        executed_instr_set = set()
        act_instr_index = 0
        while True:
            if act_instr_index in executed_instr_set:
                return
            else:
                executed_instr_set.add(act_instr_index)
            try:
                act_instr_index += self.instr_list[act_instr_index][0](self.instr_list[act_instr_index][1])
            except IndexError:
                self.program_finished = True
                return

    def repair_code_and_execute(self):
        change_dict = {self.jmp: self.nop, self.nop: self.jmp}
        self.reset_vars()
        for i in range(len(self.instr_list)):
            if self.instr_list[i][0] in change_dict:
                self.instr_list[i][0] = change_dict[self.instr_list[i][0]]
                self.calc_first_loop()
                if self.program_finished:
                    return
                self.instr_list[i][0] = change_dict[self.instr_list[i][0]]
                self.reset_vars()


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    c = CCalculation()
    for func_code, func_param in yield_input_data(p_input_file_path):
        c.add_instruction(func_code, func_param)

    c.calc_first_loop()
    answer1 = c.acc_value

    c.repair_code_and_execute()
    answer2 = c.acc_value

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 8, solve_puzzle)


if __name__ == '__main__':
    main()
