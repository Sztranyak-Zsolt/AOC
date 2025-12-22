from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from day_16 import operation_dict
from day_19 import CProgram
from functools import cached_property


def program_rewritten():
    reg_list = list()

    reg4 = 0  # 05 seti 0 5 4
    while True:
        reg5 = reg4 | 65536  # 06 bori 4 65536 5
        reg4 = 1765573  # 07 seti 1765573 9 4
        while True:
            # 08 bani 5 255 1, 09 addr 4 1 4, 10 bani 4 16777215 4, 11 muli 4 65899 4, 12 bani 4 16777215 4
            reg4 = ((reg4 + reg5 % 256) % 16777216) * 65899 % 16777216

            # 13 gtir 256 5 1, 14 addr 1 2 2, 15 addi 2 1 2, 16 seti 27 0 2
            if 256 > reg5:
                break

            # 17 seti 0 8 1, 18 addi 1 1 3, 19 muli 3 256 3, 20 gtrr 3 5 3, 21 addr 3 2 2
            # 22 addi 2 1 2, 23 seti 25 1 2, 24 addi 1 1 1, 25 seti 17 7 2, 26 setr 1 4 5
            reg5 = reg5 // 256

            # 27 seti 7 6 2
            continue

        # 28 eqrr 4 0 1 -> program stops when register[0] == register[4]
        # break
        # instead of condition and stopping the program, save the results and check for the loop
        if reg4 in reg_list:
            break
        reg_list.append(reg4)
    return reg_list


class CProgramInfLoop(CProgram):

    @cached_property
    def execute_program_check_0_output(self) -> list[int]:
        # Raw program makes some transformation in register 4 and compare the result with register 0,
        # if they are equal, output the result. These outputs are cyclical.
        # This function collects these outputs in a list.

        output_list = []
        while 0 <= self.register[self.instruction_pointer] < len(self.instruction_list):
            instruction_index = self.register[self.instruction_pointer]
            if instruction_index == 28 or self.instruction_list[instruction_index][0] == eqrr \
                    and self.instruction_list[instruction_index][1][1] == 0:
                check_output0_val = self.register[self.instruction_list[instruction_index][1][0]]
                if check_output0_val in output_list:
                    return output_list
                output_list.append(check_output0_val)
            plus_step = self.run_instructions(self.register[self.instruction_pointer])
            self.register[self.instruction_pointer] += plus_step
        return []


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    p = CProgramInfLoop(0)
    for inp_row in yield_input_data(p_input_file_path):
        if inp_row[0] == '#ip':
            p.set_pointer(inp_row[1])
        else:
            p.instruction_list.append((operation_dict[inp_row[0]], tuple(inp_row[1:])))

    # output_list = p.execute_program_check_0_output -> program gives the same result but the runtime is ~47 minutes
    output_list = program_rewritten()

    answer1 = output_list[0]
    answer2 = output_list[-1]

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 21, solve_puzzle)


if __name__ == '__main__':
    main()
