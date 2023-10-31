from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    for inp_num in yield_input_data(p_input_file_path, p_whole_row=True):
        act_num = inp_num // 3 - 2
        answer1 += act_num
        while act_num > 0:
            answer2 += act_num
            act_num = act_num // 3 - 2
    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 1, solve_puzzle)


if __name__ == '__main__':
    main()
