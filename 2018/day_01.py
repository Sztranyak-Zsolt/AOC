from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    signal_list = []
    for inp_num in yield_input_data(p_input_file_path, p_whole_row=True):
        signal_list.append(inp_num)
    answer1 = sum(signal_list)

    act_frequency = act_index = 0
    signal_set = set()

    while act_frequency not in signal_set:
        signal_set.add(act_frequency)
        act_frequency += signal_list[act_index]
        act_index = (act_index + 1) % len(signal_list)

    answer2 = act_frequency
    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 1, solve_puzzle)


if __name__ == '__main__':
    main()
