import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    rotation_list = []
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        rotation_list.append((inp_row[0], int(inp_row[1:])))
    act_num = 50
    for rot_direction, rot_number in rotation_list:
        if act_num != 0 and rot_direction == 'L':
            act_num = 100 - act_num
        act_num = act_num + rot_number
        full_turn, act_num = divmod(act_num, 100)
        if act_num != 0 and rot_direction == 'L':
            act_num = 100 - act_num
        if act_num == 0:
            answer1 += 1
        answer2 += full_turn
    return answer1, answer2


def main():
    aoc_solve_puzzle(2025, 1, solve_puzzle)


if __name__ == '__main__':
    main()
