from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_loop import CLoopHandler


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    lh = CLoopHandler()
    for d in 'abcdefghijklmnop':
        lh.add_loop_item_to_left_by_key(d)
    instruction_list = []
    for instruction in next(yield_input_data(p_input_file_path, p_chars_to_space=','), None):
        i = instruction[0]
        parameters = instruction[1:].split('/')
        if i == 's':
            instruction_list.append([lh.move_left, [int(parameters[0])]])
        elif i == 'x':
            instruction_list.append([lh.swap_loop_item_by_index, [int(parameters[0]), int(parameters[1])]])
        elif i == 'p':
            instruction_list.append([lh.swap_loop_item_by_key, [parameters[0], parameters[1]]])
    dance_cache = []

    dance_counter = 0
    while str(lh) not in dance_cache:
        dance_cache.append(str(lh))
        dance_counter += 1
        for instruction, parameters in instruction_list:
            instruction(*parameters)

    answer1 = dance_cache[0]
    answer2 = dance_cache[1000000000 % len(dance_cache)]

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 16, solve_puzzle)


if __name__ == '__main__':
    main()
