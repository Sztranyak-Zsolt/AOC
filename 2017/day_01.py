from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    input_single_row = next(yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False), None)
    for n1, n2 in zip(input_single_row[-1] + input_single_row, input_single_row):
        if n1 == n2:
            answer1 += int(n1)
    for n1, n2 in zip(input_single_row[:len(input_single_row)//2:], input_single_row[len(input_single_row)//2::]):
        if n1 == n2:
            answer2 += int(n1) * 2
    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 1, solve_puzzle)


if __name__ == '__main__':
    main()
