from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    period_list = []
    for v1, v2 in yield_input_data(p_input_file_path, p_chars_to_space='-'):
        if v1 < v2:
            period_list.append([v1, v2])
        else:
            period_list.append([v2, v1])

    if any(['x' for p1, p2 in period_list if p1 <= 4294967295 <= p2]):
        answer1 = -1
    else:
        answer1 = 4294967295

    act_interval_max = -1
    answer2 = 0
    for iv in sorted(period_list):
        if iv[0] > act_interval_max + 1:
            if answer1 == -1:
                answer1 = act_interval_max + 1
            answer2 += iv[0] - act_interval_max - 1
        act_interval_max = max(act_interval_max, iv[1])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 20, solve_puzzle)


if __name__ == '__main__':
    main()
