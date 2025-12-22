from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


class CLayer:
    def __init__(self, p_depth: int, p_range: int):
        self.depth = p_depth
        self.range = p_range
        self.circle_time = 2 * (p_range - 1)

    def get_caught(self, p_delay: int = 0) -> bool:
        return (p_delay + self.depth) % self.circle_time == 0


class CFirewall:
    def __init__(self):
        self.layer_dict: dict[int, CLayer] = dict()

    def calc_severity(self, p_delay: int = 0) -> int:
        rv = 0
        for d_layer in self.layer_dict.values():
            if d_layer.get_caught(p_delay):
                rv += d_layer.depth * d_layer.range
        return rv

    def calc_catch(self, p_delay: int = 0) -> bool:
        for d_layer in self.layer_dict.values():
            if d_layer.get_caught(p_delay):
                return True
        return False


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    f = CFirewall()
    for depth, l_range in yield_input_data(p_input_file_path, p_chars_to_space=':'):
        f.layer_dict[depth] = CLayer(depth, l_range)

    answer1 = f.calc_severity()

    answer2 = 0
    while f.calc_catch(answer2):
        answer2 += 1

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 13, solve_puzzle)


if __name__ == '__main__':
    main()
