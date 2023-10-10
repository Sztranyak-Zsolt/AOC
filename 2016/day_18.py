from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def get_next_row(p_row: str) -> str:
    p_row = '.' + p_row + '.'
    rs = ''
    for i in range(len(p_row) - 2):
        rs += '^' if p_row[i:i+3] in ['.^^', '^^.', '^..', '..^'] else '.'
    return rs


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = None
    act_row = next(yield_input_data(p_input_file_path, p_whole_row=True), None)
    safe_counter = act_row.count('.')

    for i in range(1, 400000):
        act_row = get_next_row(act_row)
        safe_counter += act_row.count('.')
        if i == 39:
            answer1 = safe_counter
    answer2 = safe_counter
    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 18, solve_puzzle)


if __name__ == '__main__':
    main()
