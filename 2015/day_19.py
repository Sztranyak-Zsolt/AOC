import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from re import finditer
import heapq


def convert_molecule(p_molecule: str, p_conversion_from: str, p_conversion_to: str):
    for match in finditer(p_conversion_from, p_molecule):
        yield p_molecule[:match.start()] + p_conversion_to + p_molecule[match.end():]


def calc_next_stage_set_counter(p_orig_molecule: str, p_conversion_list: list[str, str]) -> int:
    next_stage_set = set()
    for conv_from, conv_to in p_conversion_list:
        for next_molecule in convert_molecule(p_orig_molecule, conv_from, conv_to):
            next_stage_set.add(next_molecule)
    return len(next_stage_set)


def reduce_molecule(p_molecule: str, p_conversion_list: list[str, str]):
    for conv_to, conv_from in p_conversion_list:
        for prev_molecule in convert_molecule(p_molecule, conv_from, conv_to):
            yield prev_molecule


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer2 = None
    conversion_list = dict()
    target_molecule = ''
    for gi, inp_group in enumerate(yield_input_data(p_input_file_path, p_group_separator='\n\n')):
        if gi == 0:
            conversion_list = [(x[0], x[2]) for x in inp_group]
        else:
            target_molecule = inp_group[0][0]

    answer1 = calc_next_stage_set_counter(target_molecule, conversion_list)

    pq = [[len(target_molecule), target_molecule, 0]]
    heapq.heapify(pq)
    found = set()
    while heapq:
        _, act_mol, act_conv_count = heapq.heappop(pq)
        for next_mol in reduce_molecule(act_mol, conversion_list):
            if next_mol in found:
                continue
            found.add(next_mol)
            if next_mol == 'e':
                answer2 = act_conv_count + 1
                break
            heapq.heappush(pq, [len(next_mol), next_mol, act_conv_count + 1])
        else:
            continue
        break

    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 19, solve_puzzle)


if __name__ == '__main__':
    main()
