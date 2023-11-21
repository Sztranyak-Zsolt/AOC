from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = None
    input_iterator = iter(yield_input_data(p_input_file_path, p_whole_row=True))
    input_single_row = next(input_iterator)

    for l_start in range(len(input_single_row)):
        if len(set(input_single_row[l_start:l_start+4])) == 4 and answer1 is None:
            answer1 = l_start + 4
        if len(set(input_single_row[l_start:l_start+14])) == 14:
            answer2 = l_start + 14
            break

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 6, solve_puzzle)


if __name__ == '__main__':
    main()
