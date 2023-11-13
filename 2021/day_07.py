from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = None
    input_iterator = iter(yield_input_data(p_input_file_path, p_chars_to_space=','))
    crab_position = next(input_iterator)
    for i in range(min(crab_position), max(crab_position) + 1):
        if answer1 is None:
            answer1 = sum([abs(i - x) for x in crab_position])
        else:
            answer1 = min(answer1, sum([abs(i - x) for x in crab_position]))
        if answer2 is None:
            answer2 = sum([abs(i - x) * (abs(i - x) + 1) // 2 for x in crab_position])
        else:
            answer2 = min(answer2, sum([abs(i - x) * (abs(i - x) + 1) // 2 for x in crab_position]))

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 7, solve_puzzle)


if __name__ == '__main__':
    main()
