from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from day_18 import CTablet
from sympy import isprime


def prog_rewritten(p_debug_mode: bool, p_b: int):
    """
    Process counts prime numbers between 100000 + p_b * 100 and 117000 + p_b * 100 + 100000,
    checking every 17th numbers.
    """

    mul_counter = 0

    a = 0 if p_debug_mode else 1
    b = c = p_b
    h = 0

    if a != 0:
        b = 81 * 100 + 100000
        mul_counter += 1
        c = b + 17000

    mul_counter += (b - 2) ** 2

    for act_b in range(b, c + 1, 17):
        if not (isprime(act_b)):
            h += 1
    prime_counter = h

    return mul_counter, prime_counter


class CProcessor(CTablet):
    def __init__(self):
        super().__init__(0)

    def sub(self, p_param1: str, p_param2: str | int) -> int:
        self.register[p_param1] -= self.ret_val(p_param2)
        return 1

    def jnz(self, p_param1: str | int, p_param2: str | int):
        if self.ret_val(p_param1) != 0:
            return self.ret_val(p_param2)
        return 1


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    p = CProcessor()
    for inp_row in yield_input_data(p_input_file_path):
        p.add_instruction(inp_row)

    # originally 'debug' mode can return answer1 with the following way:
    # act_index = 0
    # while 0 <= act_index < len(p.instruction_list):
    #     if p.instruction_list[act_index][0] == p.mul:
    #         answer1 += 1
    #     act_index = p.operate_step(act_index)

    b = p.instruction_list[0][1][1]

    answer1, _ = prog_rewritten(p_debug_mode=True, p_b=b)
    _, answer2 = prog_rewritten(p_debug_mode=False, p_b=b)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 23, solve_puzzle)


if __name__ == '__main__':
    main()
