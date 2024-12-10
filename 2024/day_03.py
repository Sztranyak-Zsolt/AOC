from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
import re


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    mem = ''
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        mem += inp_row
    do_index_list = [-1] + [do_match.start() for do_match in re.finditer(r'do\(\)', mem)]
    dont_index_list = [-2] + [do_match.start() for do_match in re.finditer(r"don't\(\)", mem)]
    for mul_match in re.finditer(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)', mem):
        mul_result = int(mul_match.group(1)) * int(mul_match.group(2))
        answer1 += mul_result
        if max(di for di in do_index_list if di <= mul_match.start()) > \
                max(di for di in dont_index_list if di <= mul_match.start()):
            answer2 += mul_result
    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 3, solve_puzzle)


if __name__ == '__main__':
    main()
