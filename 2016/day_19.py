from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from math import log


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    input_num = next(yield_input_data(p_input_file_path, p_whole_row=True), None)

    answer1 = (input_num - 2 ** int(log(input_num, 2))) * 2 + 1

    l3 = int(log(input_num, 3))
    if 3 ** l3 == input_num:
        answer2 = input_num
    else:
        in2 = input_num - 3 ** l3
        if in2 <= 3 ** l3:
            answer2 = in2
        else:
            answer2 = 3 ** l3 + (in2 - 3 ** l3) * 2

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 19, solve_puzzle)


if __name__ == '__main__':
    main()
