from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from itertools import permutations
from Intcode import CIntCode, InputError


class CAmplifierController:
    def __init__(self, p_int_code_list: list[CIntCode] | None = None):
        if p_int_code_list is None:
            self.int_code_list: list[CIntCode] = []
        else:
            self.int_code_list = p_int_code_list

    @property
    def max_output_basic_mode(self):
        rv = 0
        int_codes_permutation: tuple[CIntCode]
        for int_codes_permutation in permutations(self.int_code_list):
            prev_int_code = int_codes_permutation[0]
            prev_int_code.reset_program()
            prev_int_code.input_list += [0]
            for act_int_code in int_codes_permutation[1:]:
                act_int_code.reset_program()
                prev_int_code.output_list = act_int_code.input_list
                prev_int_code = act_int_code
            for act_int_code in int_codes_permutation:
                act_int_code.run_program()
            if int_codes_permutation[-1].output_list:
                rv = max(rv, int_codes_permutation[-1].output_list[-1])
        return rv

    @property
    def max_output_feedback_mode(self):
        rv = 0
        int_codes_permutation: tuple[CIntCode]
        for int_codes_permutation in permutations(self.int_code_list):
            prev_int_code = int_codes_permutation[0]
            prev_int_code.reset_program()
            prev_int_code.input_list += [0]
            for act_int_code in int_codes_permutation[1:]:
                act_int_code.reset_program()
                prev_int_code.output_list = act_int_code.input_list
                prev_int_code = act_int_code
            int_codes_permutation[-1].output_list = int_codes_permutation[0].input_list

            act_pointer_list = [-1] * len(int_codes_permutation)
            while act_pointer_list != [ic.instruction_pointer for ic in int_codes_permutation]:
                act_pointer_list = [ic.instruction_pointer for ic in int_codes_permutation]
                for act_int_code in int_codes_permutation:
                    try:
                        act_int_code.run_program()
                    except InputError:
                        pass

            if int_codes_permutation[-1].output_list:
                rv = max(rv, int_codes_permutation[-1].output_list[-1])
        return rv


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    num_list = next(yield_input_data(p_input_file_path, p_chars_to_space=','), None)

    ac = CAmplifierController()
    for i in range(5):
        ac.int_code_list.append(CIntCode(num_list, [i]))
    answer1 = ac.max_output_basic_mode

    ac = CAmplifierController()
    for i in range(5, 10):
        ac.int_code_list.append(CIntCode(num_list, [i]))
    answer2 = ac.max_output_feedback_mode

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 7, solve_puzzle)


if __name__ == '__main__':
    main()
