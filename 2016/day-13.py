from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from collections import deque
from functools import cache
from GENERICS.aoc_grid import neighbor_positions


@cache
def check_coordinate(p_position: tuple[int, int], p_secret_number: int) -> bool:
    check_num = p_position[0] ** 2 + 3 * p_position[0] + 2 * p_position[0] * p_position[1] \
                + p_position[1] + p_position[1] ** 2 + p_secret_number
    return str(bin(check_num)).count('1') % 2 == 0


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = None
    secret_number = next(yield_input_data(p_input_file_path, p_whole_row=True), None)
    starting_position = (1, 1)
    target_position = (31, 39)
    reachable_positions = {starting_position: 0}
    dq = deque([[starting_position, 0]])

    while answer1 is None or answer2 is None:
        act_position, act_step = dq.popleft()
        if answer2 is None and act_step == 51:
            answer2 = len(reachable_positions) - 1
        for next_position in neighbor_positions(act_position):
            if check_coordinate(next_position, secret_number) and next_position not in reachable_positions \
                    and -1 not in next_position:
                if next_position == target_position:
                    answer1 = act_step + 1
                reachable_positions[next_position] = act_step + 1
                dq.append([next_position, act_step + 1])
    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 13, solve_puzzle)


if __name__ == '__main__':
    main()
