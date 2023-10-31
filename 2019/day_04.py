from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from collections import defaultdict


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    pwd_from, pwd_to = next(yield_input_data(p_input_file_path, p_chars_to_space='-'), None)

    for act_pwd in range(pwd_from, pwd_to + 1):
        next_num = 9
        digit_counter = defaultdict(lambda: 0)
        while act_pwd:
            act_pwd, act_num = divmod(act_pwd, 10)
            if act_num > next_num:
                break
            next_num = act_num
            digit_counter[act_num] += 1
        else:
            if max(digit_counter.values()) >= 2:
                answer1 += 1
            if 2 in digit_counter.values():
                answer2 += 1
    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 4, solve_puzzle)


if __name__ == '__main__':
    main()
