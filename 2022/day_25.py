import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


class CSnafu:
    def __init__(self, p_value: str = '0'):
        self.value = p_value

    @property
    def value(self):
        p_dec = self.value_int
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

    @value.setter
    def value(self, p_value):
        self.value_int = 0
        for d in p_value:
            self.value_int = self.value_int * 5 + '=-012'.index(d) - 2

    def __add__(self, other):
        rs = CSnafu('0')
        rs.value_int = self.value_int + other.value_int
        return rs


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    answer2 = None
    act_num = CSnafu()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False):
        act_num += CSnafu(inp_row)
    answer1 = act_num.value

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 25, solve_puzzle)


if __name__ == '__main__':
    main()
