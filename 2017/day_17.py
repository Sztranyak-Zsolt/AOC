import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_loop import CLoopHandler


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    lh = CLoopHandler()
    input_num = next(yield_input_data(p_input_file_path, p_whole_row=True), None)

    for i in range(2018):
        lh.move_right(input_num)
        lh.act_item = lh.add_loop_item_to_right(i)

    answer1 = lh.act_item.right_node.value

    act_index = answer2 = 0
    for i in range(1, 50000000):
        act_index = (act_index + input_num) % i + 1
        if act_index == 1:
            answer2 = i

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 17, solve_puzzle)


if __name__ == '__main__':
    main()
