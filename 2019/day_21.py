from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from Intcode import CIntCode


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    num_list = next(yield_input_data(p_input_file_path, p_chars_to_space=','), None)
    p = CIntCode(num_list)

    p.set_input_from_text_list(['NOT A J', 'NOT J J', 'AND B J', 'AND C J', 'NOT J J', 'AND D J', 'WALK'])
    p.run_program()
    answer1 = p.output_list[-1]

    p.reset_program()
    p.set_input_from_text_list(['NOT A J', 'NOT J J', 'AND B J', 'AND C J', 'NOT J J', 'AND D J', 'NOT I T', 'NOT T T',
                                'OR F T', 'AND E T', 'OR H T', 'AND T J', 'RUN'])
    p.run_program()
    answer2 = p.output_list[-1]

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 21, solve_puzzle)


if __name__ == '__main__':
    main()
