from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from Intcode import CIntCode


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    num_list = next(yield_input_data(p_input_file_path, p_chars_to_space=','), None)
    ic = CIntCode(num_list, [1])
    ic.run_program()
    answer1 = ic.output_list[-1]
    ic.init_input_list = [5]
    ic.reset_program()
    ic.run_program()
    answer2 = ic.output_list[-1]

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 5, solve_puzzle)


if __name__ == '__main__':
    main()
