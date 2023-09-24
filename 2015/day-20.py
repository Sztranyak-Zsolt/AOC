from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from collections import defaultdict


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    target = next(yield_input_data(p_input_file_path, p_whole_row=True), None)
    act_num = 1
    num_dict = defaultdict(lambda: [])
    while not answer1 or not answer2:
        num_dict[act_num].append([act_num, 1])
        if answer1 == 0 and sum([f * 10 for f, c in num_dict[act_num]]) >= target:
            answer1 = act_num
        if answer2 == 0 and sum([f * 11 for f, c in num_dict[act_num] if c <= 50]) >= target:
            answer2 = act_num
        for act_num_factor, act_num_div in num_dict[act_num]:
            num_dict[act_num + act_num_factor].append([act_num_factor, act_num_div + 1])
        del num_dict[act_num]
        act_num += 1
    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 20, solve_puzzle)


if __name__ == '__main__':
    main()
