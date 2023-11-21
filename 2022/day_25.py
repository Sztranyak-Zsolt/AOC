from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def snafu_to_dec(p_snafu: str) -> int:
    return_int = 0
    for d in p_snafu:
        return_int = return_int * 5 + '=-012'.index(d) - 2
    return return_int


def dec_to_snafu(p_dec: int) -> str:
    new_add = 0
    return_str = ''
    while p_dec != 0:
        new_digit_div = p_dec % 5
        p_dec = p_dec // 5
        return_str = '012=-0'[new_digit_div + new_add] + return_str
        if new_digit_div + new_add in [0, 1, 2]:
            new_add = 0
        else:
            new_add = 1
    if new_add in [1, 2]:
        return_str = str(new_add) + return_str
    return return_str


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    answer2 = None
    act_num = 0
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False):
        act_num += snafu_to_dec(inp_row)
    answer1 = dec_to_snafu(act_num)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 25, solve_puzzle)


if __name__ == '__main__':
    main()
