import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def yield_container_combinations(p_containers: list[int], p_target: int):
    if p_containers == [] or p_target > sum(p_containers):
        return
    for i, cont in enumerate(p_containers):
        if cont == p_target:
            yield [cont]
        if cont > p_target:
            return
        for next_cont in yield_container_combinations(p_containers[i+1:], p_target - cont):
            yield [cont] + next_cont


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    target_l = 150
    containers = sorted([x for x in yield_input_data(p_input_file_path, p_whole_row=True)])

    min_cont_poss = target_l
    for c in yield_container_combinations(containers, target_l):
        answer1 += 1
        if len(c) == min_cont_poss:
            answer2 += 1
        elif len(c) < min_cont_poss:
            answer2 = 1
            min_cont_poss = len(c)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 17, solve_puzzle)


if __name__ == '__main__':
    main()
