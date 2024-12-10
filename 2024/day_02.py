from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def level_is_safe(p_level_nums: list[int]) -> bool:
    if p_level_nums[1] - p_level_nums[0] in (1, 2, 3):
        asc_mul = 1
    elif p_level_nums[0] - p_level_nums[1] in (1, 2, 3):
        asc_mul = -1
    else:
        return False

    prev_num = p_level_nums[1]
    for act_num in p_level_nums[2:]:
        if asc_mul * (act_num - prev_num) in (1, 2, 3):
            prev_num = act_num
            continue
        return False
    return True


def level_expect_one_is_safe(p_level_nums: list[int]) -> bool:
    for i in range(len(p_level_nums)):
        ir2 = p_level_nums[:i] + p_level_nums[i + 1:]
        if level_is_safe(ir2):
            return True
    return False


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    for inp_row in yield_input_data(p_input_file_path):
        if level_is_safe(inp_row):
            answer1 += 1
            answer2 += 1
        elif level_expect_one_is_safe(inp_row):
            answer2 += 1
    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 2, solve_puzzle)


if __name__ == '__main__':
    main()
