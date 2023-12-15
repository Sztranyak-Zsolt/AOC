from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from functools import cache


@cache
def calc_ways(p_spring: str, p_scan: tuple[int], p_fold_num: int = 1):
    if len(p_scan) == 0:
        return 0 if p_spring.count('#') else 1
    if p_fold_num != 1:
        p_spring = (p_spring + '?') * (p_fold_num - 1) + p_spring
        p_scan = p_scan * p_fold_num
    if p_spring and p_spring[-1] != '.':
        p_spring += '.'
    rv = 0
    act_scan = p_scan[0]
    for i in range(len(p_spring)):
        if i != 0 and p_spring[i-1] == '#':
            continue
        if p_spring[i:i+act_scan].count('.') == 0 and p_spring[i+act_scan] != '#':
            rv += calc_ways(p_spring[i+act_scan+1:], tuple(p_scan[1:]))
        if p_spring[i] == '#':
            break
    return rv


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    for spring, *scan in yield_input_data(p_input_file_path, p_chars_to_space=','):
        answer1 += calc_ways(spring, tuple(scan))
        answer2 += calc_ways(spring, tuple(scan), 5)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 12, solve_puzzle)


if __name__ == '__main__':
    main()
