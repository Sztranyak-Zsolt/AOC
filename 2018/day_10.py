from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, add_positions, Position2D


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    positions_list = []
    velocity_list = []
    for p1, p2, v1, v2 in yield_input_data(p_input_file_path, p_chars_to_space=',<>', p_only_nums=True):
        positions_list.append(Position2D(p1, p2))
        velocity_list.append(Position2D(v1, v2))

    min_y_velo = min([v.y for v in velocity_list])
    max_y_velo = max([v.y for v in velocity_list])
    min_height = min([p.y for p in positions_list])
    max_height = max([p.y for p in positions_list])
    timer = (max_height - min_height) // (max_y_velo - min_y_velo)

    g = CGridBase()
    g.double_width_on_print = True
    g.print_y_reverse = True
    for p, v in zip(positions_list, velocity_list):
        g.add_item(add_positions(p, Position2D(v.x * timer, v.y * timer)), 'x', True)

    answer1 = f'\n{g}'
    answer2 = timer

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 10, solve_puzzle)


if __name__ == '__main__':
    main()
