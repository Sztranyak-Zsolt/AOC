import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    crane_list1 = [[] for _ in range(9)]
    crane_list2 = [[] for _ in range(9)]
    input_iterator = iter(yield_input_data(p_input_file_path, p_whole_row=True, p_group_separator='\n\n'))
    for crane_info in next(input_iterator):
        for i, act_item in enumerate(crane_info[1::4]):
            if act_item == '1':
                break
            if act_item != ' ':
                crane_list2[i].insert(0, act_item)
                crane_list1[i].insert(0, act_item)

    for move_row in next(input_iterator):
        _, box_amount, _, s_from, _, s_to = move_row.split()
        i_from = int(s_from) - 1
        i_to = int(s_to) - 1
        crane_list2[i_to] += crane_list2[i_from][-int(box_amount):]
        for _ in range(int(box_amount)):
            crane_list1[i_to].append(crane_list1[i_from].pop())
            crane_list2[i_from].pop()

    answer1 = ''.join([c[-1] for c in crane_list1])
    answer2 = ''.join([c[-1] for c in crane_list2])
    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 5, solve_puzzle)


if __name__ == '__main__':
    main()

