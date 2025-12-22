import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from collections import deque
from collections.abc import Callable


class CCalculator:
    def __init__(self):
        self.op_code: list[Callable[[int, int], int]] = [self.adv, self.bxl, self.bst, self.jnz,
                                                         self.bxc, self.out, self.bdv, self.cdv]
        self.register = {'A': 0, 'B': 0, 'C': 0}
        self.instruction_list: list[int] = []
        self.output_list: list[int] = []

    def calc_val(self, p_op: int) -> int:
        if p_op <= 3:
            return p_op
        if p_op == 4:
            return self.register['A']
        if p_op == 5:
            return self.register['B']
        if p_op == 6:
            return self.register['C']
        return -1

    def adv(self, p_op: int, p_step: int) -> int:
        self.register['A'] >>= self.calc_val(p_op)
        return p_step + 2

    def bxl(self, p_op: int, p_step: int) -> int:
        self.register['B'] ^= p_op
        return p_step + 2

    def bst(self, p_op: int, p_step: int) -> int:
        self.register['B'] = self.calc_val(p_op) & 7
        return p_step + 2

    def jnz(self, p_op: int, p_step: int) -> int:
        if self.register['A']:
            return p_op
        return p_step + 2

    def bxc(self, p_op: int, p_step: int) -> int:
        self.register['B'] ^= self.register['C']
        return p_step + 2

    def out(self, p_op: int, p_step: int) -> int:
        self.output_list.append(self.calc_val(p_op) & 7)
        return p_step + 2

    def bdv(self, p_op: int, p_step: int) -> int:
        self.register['B'] = self.register['A'] >> self.calc_val(p_op)
        return p_step + 2

    def cdv(self, p_op: int, p_step: int) -> int:
        self.register['C'] = self.register['A'] >> self.calc_val(p_op)
        return p_step + 2

    def calculate(self) -> None:
        act_pointer = 0
        self.output_list.clear()
        while 0 <= act_pointer < len(self.instruction_list) - 1:
            act_op = self.op_code[self.instruction_list[act_pointer]]
            act_combo = self.instruction_list[act_pointer + 1]
            act_pointer = act_op(act_combo, act_pointer)

    def first_num_return_instruction(self) -> int:
        act_dq = deque([[0, 1, 0]])
        while act_dq:
            base_num, act_part, act_target_instr = act_dq.pop()
            for i in range(act_part, 8):
                self.register['A'] = base_num + i
                self.calculate()
                if self.output_list == self.instruction_list[-1-act_target_instr:]:
                    if self.output_list == self.instruction_list:
                        return base_num + i
                    act_dq.append([base_num, i + 1, act_target_instr])
                    act_dq.append([(base_num + i) * 8, 0, act_target_instr+1])
                    break
        return -1


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    calc = CCalculator()
    for inp_row in yield_input_data(p_input_file_path,
                                    p_whole_row=False,
                                    p_chars_to_space=':,'
                                    ):
        if not inp_row:
            continue
        elif len(inp_row) == 3:
            calc.register[inp_row[1]] = inp_row[2]
        else:
            calc.instruction_list = inp_row[1:]

    calc.calculate()
    answer1 = ','.join(str(n) for n in calc.output_list)
    answer2 = calc.first_num_return_instruction()

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 17, solve_puzzle)


if __name__ == '__main__':
    main()
