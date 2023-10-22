from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from typing import Callable
from functools import cached_property


def addr(p_act_register: dict[int, int], input_a: int, input_b: int, output_c: int) -> int:
    p_act_register[output_c] = p_act_register.get(input_a, 0) + p_act_register.get(input_b, 0)
    return 1


def addi(p_act_register: dict[int, int], input_a: int, input_b: int, output_c: int) -> int:
    p_act_register[output_c] = p_act_register.get(input_a, 0) + input_b
    return 1


def mulr(p_act_register: dict[int, int], input_a: int, input_b: int, output_c: int) -> int:
    p_act_register[output_c] = p_act_register.get(input_a, 0) * p_act_register.get(input_b, 0)
    return 1


def muli(p_act_register: dict[int, int], input_a: int, input_b: int, output_c: int) -> int:
    p_act_register[output_c] = p_act_register.get(input_a, 0) * input_b
    return 1


def banr(p_act_register: dict[int, int], input_a: int, input_b: int, output_c: int) -> int:
    p_act_register[output_c] = p_act_register.get(input_a, 0) & p_act_register.get(input_b, 0)
    return 1


def bani(p_act_register: dict[int, int], input_a: int, input_b: int, output_c: int) -> int:
    p_act_register[output_c] = p_act_register.get(input_a, 0) & input_b
    return 1


def borr(p_act_register: dict[int, int], input_a: int, input_b: int, output_c: int) -> int:
    p_act_register[output_c] = p_act_register.get(input_a, 0) | p_act_register.get(input_b, 0)
    return 1


def bori(p_act_register: dict[int, int], input_a: int, input_b: int, output_c: int) -> int:
    p_act_register[output_c] = p_act_register.get(input_a, 0) | input_b
    return 1


def setr(p_act_register: dict[int, int], input_a: int, input_b: int, output_c: int) -> int:
    p_act_register[output_c] = p_act_register.get(input_a, 0)
    return 1


def seti(p_act_register: dict[int, int], input_a: int, input_b: int, output_c: int) -> int:
    p_act_register[output_c] = input_a
    return 1


def gtir(p_act_register: dict[int, int], input_a: int, input_b: int, output_c: int) -> int:
    p_act_register[output_c] = 1 if input_a > p_act_register.get(input_b, 0) else 0
    return 1


def gtri(p_act_register: dict[int, int], input_a: int, input_b: int, output_c: int) -> int:
    p_act_register[output_c] = 1 if p_act_register.get(input_a, 0) > input_b else 0
    return 1


def gtrr(p_act_register: dict[int, int], input_a: int, input_b: int, output_c: int) -> int:
    p_act_register[output_c] = 1 if p_act_register.get(input_a, 0) > p_act_register.get(input_b, 0) else 0
    return 1


def eqir(p_act_register: dict[int, int], input_a: int, input_b: int, output_c: int) -> int:
    p_act_register[output_c] = 1 if input_a == p_act_register.get(input_b, 0) else 0
    return 1


def eqri(p_act_register: dict[int, int], input_a: int, input_b: int, output_c: int) -> int:
    p_act_register[output_c] = 1 if p_act_register.get(input_a, 0) == input_b else 0
    return 1


def eqrr(p_act_register: dict[int, int], input_a: int, input_b: int, output_c: int) -> int:
    p_act_register[output_c] = 1 if p_act_register.get(input_a, 0) == p_act_register.get(input_b, 0) else 0
    return 1


operation_dict = {'addr': addr, 'addi': addi, 'mulr': mulr, 'muli': muli, 'banr': banr, 'bani': bani, 'borr': borr,
                      'bori': bori, 'setr': setr, 'seti': seti, 'gtir': gtir, 'gtri': gtri, 'gtrr': gtrr, 'eqir': eqir,
                      'eqri': eqri, 'eqrr': eqrr}


class CTest:
    def __init__(self, p_reg_before: dict[int, int], p_operation_list: list, p_reg_after: dict[int, int]):
        self.act_code, self.input_a, self.input_b, self.output_c = p_operation_list
        self.reg_before = p_reg_before
        self.reg_after = p_reg_after

    def get_possible_operations(self, p_operation_set: set[Callable]) -> set[Callable]:
        rs = set()
        for act_operation in p_operation_set:
            operation_register = self.reg_before.copy()
            act_operation(operation_register, self.input_a, self.input_b, self.output_c)
            if operation_register == self.reg_after:
                rs.add(act_operation)
        return rs


class CTestHandler:
    def __init__(self, p_operation_set: set[Callable]):
        self.test_list: list[CTest] = []
        self.operation_set = p_operation_set
        self.operation_codes: dict[int, set[Callable]] = dict()
        self.operation_decodes: dict[Callable, set[int]] = dict()
        for op in p_operation_set:
            self.operation_decodes[op] = set()

    def add_test_case(self, p_test_case: CTest):
        poss_operations = p_test_case.get_possible_operations(self.operation_set)
        self.test_list.append(p_test_case)
        if p_test_case.act_code not in self.operation_codes:
            self.operation_codes[p_test_case.act_code] = poss_operations
            for act_operation in poss_operations:
                self.operation_decodes[act_operation].add(p_test_case.act_code)
        else:
            op_to_remove = self.operation_codes[p_test_case.act_code] - poss_operations
            self.operation_codes[p_test_case.act_code] &= poss_operations
            for act_operation in op_to_remove:
                self.operation_decodes[act_operation].remove(p_test_case.act_code)

    def reduce_operation_codes(self):
        operation_found = set()
        for act_op_coded, act_operation_decoded_set in self.operation_codes.items():
            if len(act_operation_decoded_set) == 1 \
                    and len(self.operation_decodes[list(act_operation_decoded_set)[0]]) != 1:
                act_op_decoded = list(act_operation_decoded_set)[0]
                self.operation_codes[act_op_coded] = {act_op_decoded}
                self.operation_decodes[act_op_decoded] = {act_op_coded}
                operation_found.add(act_op_decoded)
        for op_to_adjust in operation_found:
            for act_op_coded, act_operation_decoded_set in self.operation_codes.items():
                if act_op_coded not in self.operation_decodes[op_to_adjust] \
                        and op_to_adjust in act_operation_decoded_set:
                    self.operation_codes[act_op_coded].remove(op_to_adjust)
        return len(operation_found) != 0

    def reduce_operation_decodes(self):
        operation_found = set()
        for act_op_decoded, act_operation_coded_set in self.operation_decodes.items():
            if len(act_operation_coded_set) == 1 \
                    and len(self.operation_codes[list(act_operation_coded_set)[0]]) != 1:
                act_op_coded = list(act_operation_coded_set)[0]
                self.operation_decodes[act_op_decoded] = {act_op_coded}
                self.operation_codes[act_op_coded] = {act_op_decoded}
                operation_found.add(act_op_coded)
        for op_to_adjust in operation_found:
            for act_op_decoded, act_operation_coded_set in self.operation_decodes.items():
                if act_op_decoded not in self.operation_codes[op_to_adjust] \
                        and op_to_adjust in act_operation_coded_set:
                    self.operation_decodes[act_op_decoded].remove(op_to_adjust)
        return len(operation_found) != 0

    @cached_property
    def get_mapping(self) -> dict[int, Callable]:
        while self.reduce_operation_codes() or self.reduce_operation_decodes():
            pass
        return {k: list(v)[0] for k, v in self.operation_codes.items()}


class CProgram:
    def __init__(self):
        self.register: dict[int, int] = {}
        self.instruction_list: list[tuple[Callable, tuple[int]]] = []

    def run_instructions(self, p_index: int) -> int:
        return self.instruction_list[p_index][0](self.register, *self.instruction_list[p_index][1])

    def execute_program(self):
        act_index = 0
        while 0 <= act_index < len(self.instruction_list):
            act_index += self.run_instructions(act_index)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    th = CTestHandler(set(operation_dict.values()))
    pr = CProgram()
    for inp_row in yield_input_data(p_input_file_path, p_group_separator='\n\n', p_chars_to_space='[],'):
        if not inp_row[0]:
            continue
        if inp_row[0][0] == 'Before:':
            new_test_case = CTest({i: v for i, v in enumerate(inp_row[0][1:])}, inp_row[1],
                                  {i: v for i, v in enumerate(inp_row[2][1:])})
            th.add_test_case(new_test_case)
        else:
            for op_code, *params in inp_row:
                pr.instruction_list.append((th.get_mapping[op_code], params))

    answer1 = len([t for t in th.test_list if len(t.get_possible_operations(th.operation_set)) >= 3])
    pr.execute_program()
    answer2 = pr.register[0]

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 16, solve_puzzle)


if __name__ == '__main__':
    main()
