from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from math import prod


def eval_list_in_order(p_calc_list: tuple) -> int:
    act_num = new_num = 0
    addition = True
    for act_item in p_calc_list:
        if isinstance(act_item, tuple):
            new_num = eval_list_in_order(act_item)
        elif isinstance(act_item, int):
            new_num = act_item
        elif act_item == "*":
            addition = False
            continue
        elif act_item == "+":
            addition = True
            continue
        if addition:
            act_num += new_num
        else:
            act_num *= new_num
    return act_num


def eval_list_in_order2(p_calc_list: tuple) -> int:
    multiplication_list = list()
    act_num = 0
    for act_item in p_calc_list:
        if isinstance(act_item, tuple):
            act_num += eval_list_in_order2(act_item)
        elif isinstance(act_item, int):
            act_num += act_item
        elif act_item == "*":
            multiplication_list.append(act_num)
            act_num = 0
    multiplication_list.append(act_num)
    return prod(multiplication_list)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    for act_line in yield_input_data(p_input_file_path, p_whole_row=True):
        act_list = eval("(" + act_line.strip().replace(" ", ",")
                        .replace("*", "'*'").replace("+", "'+'") + ")")
        answer1 += eval_list_in_order(act_list)
        answer2 += eval_list_in_order2(act_list)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 18, solve_puzzle)


if __name__ == '__main__':
    main()
