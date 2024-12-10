from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from functools import lru_cache
from operator import add, mul


@lru_cache(maxsize=1)
def get_10_pow(p_n):
    act_pow_10 = 10
    while act_pow_10 <= p_n:
        act_pow_10 *= 10
    return act_pow_10


def op_concat(p_n1, p_n2):
    return p_n1 * get_10_pow(p_n2) + p_n2


def can_eval(p_nums: list[int], p_target: int, has_concat_op: bool = False) -> bool:
    act_calc_list = [p_nums[0]]
    used_operators = [add, mul]
    if has_concat_op:
        used_operators += [op_concat]
    for act_num in p_nums[1:]:
        next_calc_list = []
        for prev_num in act_calc_list:
            for act_op in used_operators:
                next_num = act_op(prev_num, act_num)
                if next_num <= p_target:
                    next_calc_list.append(next_num)
        act_calc_list = next_calc_list
    return p_target in act_calc_list


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    for inp_row in yield_input_data(p_input_file_path,
                                    p_whole_row=False,
                                    p_chars_to_space=':'
                                    ):
        if can_eval(inp_row[1:], inp_row[0]):
            answer1 += inp_row[0]
        if can_eval(inp_row[1:], inp_row[0], True):
            answer2 += inp_row[0]

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 7, solve_puzzle)


if __name__ == '__main__':
    main()
