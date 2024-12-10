from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    input_iterator = iter(yield_input_data(p_input_file_path, p_chars_to_space='|,', p_group_separator='\n\n'))
    reqs = set(tuple(r) for r in next(input_iterator))

    for act_book in next(input_iterator):

        for prev_page, act_page in zip(act_book, act_book[1:]):
            if (act_page, prev_page) in reqs:
                break
        else:
            answer1 += act_book[len(act_book) // 2]
            continue

        for i in range(1, len(act_book)):
            for i2 in range(i, 0, -1):
                act_page = act_book[i2]
                prev_page = act_book[i2 - 1]
                if (act_page, prev_page) not in reqs:
                    break
                act_book[i2] = prev_page
                act_book[i2 - 1] = act_page
        answer2 += act_book[len(act_book) // 2]

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 5, solve_puzzle)


if __name__ == '__main__':
    main()
