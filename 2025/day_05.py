import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = 0
    id_range = []
    ids_to_check = []
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space='-'):
        if len(inp_row) == 2:
            id_range.append(sorted(inp_row))
        elif len(inp_row) == 1:
            ids_to_check.append(inp_row[0])
    id_range.sort()
    act_index = 0
    while act_index < len(id_range) - 1:
        if id_range[act_index][1] >= id_range[act_index+1][0] - 1:
            if id_range[act_index][1] < id_range[act_index+1][1]:
                id_range[act_index][1] = id_range[act_index+1][1]
            id_range.pop(act_index+1)
        else:
            act_index += 1
    for act_id in ids_to_check:
        for period_start, period_end in id_range:
            if act_id > period_end:
                continue
            if act_id >= period_start:
                answer1 += 1
            break
    answer2 = sum(e - s + 1 for s, e in id_range)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2025, 5, solve_puzzle)


if __name__ == '__main__':
    main()
