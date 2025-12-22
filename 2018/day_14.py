import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = None
    input_num = next(yield_input_data(p_input_file_path, p_whole_row=True), None)
    input_list = list([int(c) for c in str(input_num)])
    recipe_list = [3, 7]
    elf1_index, elf2_index = 0, 1
    while answer1 is None or answer2 is None:
        nr = (n1 := recipe_list[elf1_index]) + (n2 := recipe_list[elf2_index])
        if nr > 9:
            recipe_list.append(1)
            if recipe_list[-6:] == input_list and answer2 is None:
                answer2 = len(recipe_list) - 6
            recipe_list.append(nr - 10)
        else:
            recipe_list.append(nr)
        if recipe_list[-6:] == input_list and answer2 is None:
            answer2 = len(recipe_list) - 6
        elf1_index = (n1 + elf1_index + 1) % len(recipe_list)
        elf2_index = (n2 + elf2_index + 1) % len(recipe_list)
        if len(recipe_list) > input_num + 10 and answer1 is None:
            answer1 = ''.join([str(x) for x in recipe_list[input_num:input_num+11]])
    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 14, solve_puzzle)


if __name__ == '__main__':
    main()
