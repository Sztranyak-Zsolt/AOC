import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer2 = None
    seat_id_list = set()
    for act_line in yield_input_data(p_input_file_path, p_whole_row=True):
        act_seat_num = int(act_line[:7].replace('F', '0').replace('B', '1'), 2) * 8 + \
                       int(act_line[7:].replace('L', '0').replace('R', '1'), 2)
        seat_id_list.add(act_seat_num)
    answer1 = max(seat_id_list)
    for c in range(min(seat_id_list), max(seat_id_list) + 1):
        if c - 1 in seat_id_list and c + 1 in seat_id_list and c not in seat_id_list:
            answer2 = c
            break
    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 5, solve_puzzle)


if __name__ == '__main__':
    main()
