import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


class CNum:
    def __init__(self, p_value: int):
        self.value = p_value


class CWrapper:
    def __init__(self):
        self.num_list: list[CNum] = []
        self.wrapped_list: list[CNum] = []
        self.description_key = 1
        self.num_0: CNum | None = None

    def add_num(self, p_num: int):
        new_num = CNum(p_num)
        self.num_list.append(new_num)
        if p_num == 0:
            self.num_0 = new_num

    def wrap_list(self, p_counter: int = 1):
        self.wrapped_list = self.num_list.copy()
        for _ in range(p_counter):
            for n in self.num_list:
                if n.value == 0:
                    continue
                act_pos = self.wrapped_list.index(n)
                new_pos = act_pos + n.value * self.description_key
                self.wrapped_list.pop(act_pos)
                self.wrapped_list.insert(new_pos % len(self.wrapped_list), n)

    @property
    def groove_nums(self) -> list[int]:
        coord0 = self.wrapped_list.index(self.num_0)
        rv = []
        for x in [1000, 2000, 3000]:
            rv.append(self.description_key * self.wrapped_list[(coord0 + x) % len(self.wrapped_list)].value)
        return rv


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    w = CWrapper()
    for inp_num in yield_input_data(p_input_file_path, p_whole_row=True):
        w.add_num(inp_num)

    w.wrap_list()
    answer1 = sum(w.groove_nums)

    w.description_key = 811589153
    w.wrap_list(10)
    answer2 = sum(w.groove_nums)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 20, solve_puzzle)


if __name__ == '__main__':
    main()
