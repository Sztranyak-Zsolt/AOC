from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def yield_pattern(p_depth: int, p_pattern_base: list[int] | None = None, p_range: int | None = None):
    if p_pattern_base is None:
        p_pattern_base = [0, 1, 0, -1]
    counter = 1
    counter2 = 1
    act_index = 0
    act_value = p_pattern_base[act_index]
    while p_range is None or p_range >= counter:
        if counter2 == p_depth + 1:
            act_index = (act_index + 1) % 4
            act_value = p_pattern_base[act_index]
            counter2 = 0
        yield act_value
        counter += 1
        counter2 += 1


def generate_next_num_list(p_num_list) -> list[int]:
    new_num_list = []
    for c in range(len(p_num_list)):
        next_num = get_last_digit(sum([b * a for a, b in zip(p_num_list, yield_pattern(c)) if b]))
        new_num_list.append(next_num)
    return new_num_list


def get_last_digit(p_num: int) -> int:
    if p_num >= 0:
        return p_num % 10
    else:
        return 9 - (p_num - 1) % 10


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    input_single_row = next(yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False), None)
    starting_num_list = [int(x) for x in input_single_row]

    string_repeat = 10000
    num_list = starting_num_list.copy()

    for _ in range(100):
        num_list = generate_next_num_list(num_list)

    answer1 = ''.join([str(x) for x in num_list[:8]])

    # after the half of the list the next phase element is the sum of previous phase self + following elements
    from_element_index = sum([x * 10 ** (6 - c) for c, x in enumerate(starting_num_list[:7])])
    from_element_period = from_element_index // len(num_list)
    remaining_period_count = string_repeat - from_element_period
    num_list = starting_num_list * remaining_period_count
    new_period_start = from_element_index % len(num_list)

    for _ in range(100):
        new_num_list = [sum(num_list) % 10]
        for act_num in num_list:
            new_num_list.append((new_num_list[-1] - act_num) % 10)
        new_num_list.pop(-1)
        num_list = new_num_list
    answer2 = ''.join([str(x) for x in num_list[new_period_start:new_period_start + 8]])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 16, solve_puzzle)


if __name__ == '__main__':
    main()
