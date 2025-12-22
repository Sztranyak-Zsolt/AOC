import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    elf_list = []
    for act_elf in yield_input_data(p_input_file_path, p_whole_row=True, p_group_separator='\n\n'):
        elf_list.append(sum(act_elf))
    elf_list.sort()
    answer1 = elf_list[-1]
    answer2 = sum(elf_list[-3:])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 1, solve_puzzle)


if __name__ == '__main__':
    main()
