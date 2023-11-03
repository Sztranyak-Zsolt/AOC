from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = None
    # input_iterator = iter(yield_input_data(p_input_file_path, p_whole_row=True))
    # input_single_row = next(input_iterator)
    for inp_row in yield_input_data(p_input_file_path):
        pass

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 0, solve_puzzle)


if __name__ == '__main__':
    main()
