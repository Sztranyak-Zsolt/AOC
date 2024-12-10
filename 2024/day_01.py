from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    left_side, right_side = zip(*list(yield_input_data(p_input_file_path, p_chars_to_space=' ')))

    left_side = sorted(left_side)
    right_side = sorted(right_side)

    answer1 = sum(abs(n1 - n2) for n1, n2 in zip(left_side, right_side))
    answer2 = sum(n1 * right_side.count(n1) for n1 in left_side)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 1, solve_puzzle)


if __name__ == '__main__':
    main()
