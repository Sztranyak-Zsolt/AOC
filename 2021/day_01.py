from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    prev_depths = []
    for act_depth in yield_input_data(p_input_file_path, p_whole_row=True):
        if prev_depths != [] and prev_depths[-1] < act_depth:
            answer1 += 1
        if len(prev_depths) == 3:
            prev_depth2 = prev_depths.pop(0)
            if act_depth > prev_depth2:
                answer2 += 1
        prev_depths.append(act_depth)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 1, solve_puzzle)


if __name__ == '__main__':
    main()
