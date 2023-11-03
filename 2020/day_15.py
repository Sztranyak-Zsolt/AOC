from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from typing import Iterator


def gen_nums(p_init_list: list[int]) -> Iterator[int]:
    last_turn_dict = {n: i for i, n in enumerate(p_init_list[:-1])}
    act_num = p_init_list[-1]
    act_turn = len(p_init_list) - 1
    while True:
        if act_num in last_turn_dict:
            next_num = act_turn - last_turn_dict[act_num]
        else:
            next_num = 0
        yield next_num
        last_turn_dict[act_num] = act_turn
        act_num = next_num
        act_turn += 1


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = None
    spoken_list = next(yield_input_data(p_input_file_path, p_chars_to_space=','), None)

    for i, sn in enumerate(gen_nums(spoken_list), start=1+len(spoken_list)):
        if i == 2020:
            answer1 = sn
        if i == 30000000:
            answer2 = sn
            break

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 15, solve_puzzle)


if __name__ == '__main__':
    main()
