import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from math import lcm


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    input_iter = iter(yield_input_data(p_input_file_path, p_chars_to_space=','))
    wait_until = next(input_iter)[0]
    bus_ids = next(input_iter)

    min_wait = -1
    period = 1

    for t, n in enumerate(bus_ids):
        if isinstance(n, int):
            if wait_until % n == 0:
                act_wait = 0
            else:
                act_wait = n - wait_until % n
            if min_wait == -1 or act_wait < min_wait:
                min_wait = act_wait
                answer1 = min_wait * n
            act_num = 0
            while True:
                if (answer2 + period * act_num) % n == (n - t) % n:
                    answer2 = answer2 + period * act_num
                    period = lcm(period, n)
                    break
                else:
                    act_num += 1

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 13, solve_puzzle)


if __name__ == '__main__':
    main()
