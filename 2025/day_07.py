
import os
import sys
from collections import defaultdict
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = 0
    grid = []
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        grid.append(inp_row)
    act_beam_pos = defaultdict(int)
    act_beam_pos[grid[0].find('S')] = 1
    for act_row in grid[1:]:
        next_beam_pos = defaultdict(int)
        for act_beam, act_beam_count in act_beam_pos.items():
            if act_row[act_beam] == '^':
                next_beam_pos[act_beam - 1] += act_beam_count
                next_beam_pos[act_beam + 1] += act_beam_count
                answer1 += 1
            else:
                next_beam_pos[act_beam] += act_beam_count
        act_beam_pos = next_beam_pos
    answer2 = sum(act_beam_pos.values())
    return answer1, answer2


def main():
    aoc_solve_puzzle(2025, 7, solve_puzzle)


if __name__ == '__main__':
    main()
