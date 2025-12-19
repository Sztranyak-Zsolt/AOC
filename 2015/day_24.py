import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from collections import namedtuple


PossibilityEnd = namedtuple('PossibilityEnd', ['greatest_weight', 'pack_count'])


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    package_list = [package_size for package_size in yield_input_data(p_input_file_path, p_whole_row=True)]
    target1 = sum(package_list) // 3
    target2 = sum(package_list) // 4
    poss_dict = {0: {PossibilityEnd(0, 0): 1}}
    for i in range(1, target1 + 1):
        poss_dict[i] = {}
        for act_pack in package_list:
            if i - act_pack in poss_dict:
                for prev_end, prev_qe in poss_dict[i - act_pack].items():
                    if prev_end.greatest_weight >= act_pack:
                        continue
                    new_end = PossibilityEnd(act_pack, prev_end.pack_count + 1)
                    if new_end not in poss_dict[i] or poss_dict[i][new_end] > prev_qe * act_pack:
                        poss_dict[i][new_end] = prev_qe * act_pack
        if i - package_list[-1] in poss_dict and i - package_list[-1] != target2:
            del poss_dict[i - package_list[-1]]

    min_pack1_size = min([k.pack_count for k in poss_dict[target1]])
    min_pack2_size = min([k.pack_count for k in poss_dict[target2]])

    answer1 = min([v for k, v in poss_dict[target1].items() if k.pack_count == min_pack1_size])
    answer2 = min([v for k, v in poss_dict[target2].items() if k.pack_count == min_pack2_size])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 24, solve_puzzle)


if __name__ == '__main__':
    main()
