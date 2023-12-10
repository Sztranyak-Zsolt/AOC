from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def find_next_num(p_nums: list[int], p_to_end: True) -> int:
    if len(set(p_nums)) == 1:
        return p_nums[0]
    new_list = []
    for n1, n2 in zip(p_nums, p_nums[1:]):
        new_list.append(n2 - n1)
    new_list_num = find_next_num(new_list, p_to_end)
    if p_to_end:
        return p_nums[-1] + new_list_num
    return p_nums[0] - new_list_num


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    for inp_row in yield_input_data(p_input_file_path):
        answer1 += find_next_num(inp_row, True)
        answer2 += find_next_num(inp_row, False)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 9, solve_puzzle)


if __name__ == '__main__':
    main()
