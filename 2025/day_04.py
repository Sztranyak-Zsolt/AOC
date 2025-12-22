import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_vector import Position2D, neighbor_positions


def get_accessable_rolls(p_grid: list[list[str]]) -> list[Position2D]:
    r_rolls = []
    for y, act_row in enumerate(p_grid):
        for x, act_item in enumerate(act_row):
            if act_item != '@':
                continue
            n_count = 0
            for n_roll in neighbor_positions(Position2D(x, y), p_return_corner=True):
                if n_roll.y in (-1, len(p_grid)) or n_roll.x in (-1, len(p_grid[0])):
                    continue
                if p_grid[n_roll.y][n_roll.x] == '@':
                    n_count += 1
            if n_count < 4:
                r_rolls.append(Position2D(x, y))
    return r_rolls


def remove_accessable_rolls(p_grid: list[list[str]]) -> int:
    accessable_rolls = get_accessable_rolls(p_grid)
    for ar in accessable_rolls:
        p_grid[ar.y][ar.x] = '.'
    return len(accessable_rolls)


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    grid = []
    for act_row in yield_input_data(p_input_file_path, p_whole_row=True):
        grid.append(list(act_row))
    answer1 = len(get_accessable_rolls(grid))
    while (act_turn_remove := remove_accessable_rolls(grid)):
        answer2 += act_turn_remove
    return answer1, answer2


def main():
    aoc_solve_puzzle(2025, 4, solve_puzzle)


if __name__ == '__main__':
    main()
