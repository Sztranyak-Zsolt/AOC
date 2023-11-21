from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    for e1s, e1e, e2s, e2e in yield_input_data(p_input_file_path, p_chars_to_space='-,'):
        if e1s <= e2s and e1e >= e2e or e1s >= e2s and e1e <= e2e:
            answer1 += 1
        if e1s <= e2s <= e2e or e2s <= e1s <= e2e:
            answer2 += 1

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 4, solve_puzzle)


if __name__ == '__main__':
    main()
