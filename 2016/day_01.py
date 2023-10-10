from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import add_positions


directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer2 = None
    act_direction = (0, 1)
    act_position = (0, 0)
    known_positions = set()
    for inp_row in next(yield_input_data(p_input_file_path, p_chars_to_space=','), None):
        act_direction = directions[(directions.index(act_direction) + {'R': 1, 'L': -1}[inp_row[0]]) % 4]
        step_count = int(inp_row[1:])
        if answer2 is None:
            for _ in range(step_count):
                act_position = add_positions(act_position, act_direction)
                if answer2 is None and act_position in known_positions:
                    answer2 = abs(act_position[0]) + abs(act_position[1])
                known_positions.add(act_position)
        else:
            new_pos = (act_direction[0] * step_count, act_direction[1] * step_count)
            act_position = add_positions(act_position, new_pos)
    answer1 = abs(act_position[0]) + abs(act_position[1])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 1, solve_puzzle)


if __name__ == '__main__':
    main()
