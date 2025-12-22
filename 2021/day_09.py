import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, Position2D, neighbor_positions
from collections import deque
from math import prod


class CBasin(CGridBase):
    @property
    def basins_count(self) -> int:
        rv = 0
        for act_pos, act_val in self.position_dict.items():
            for nb in neighbor_positions(act_pos):
                if act_val >= self.position_dict.get(nb, 9):
                    break
            else:
                rv += act_val + 1
        return rv

    @property
    def regions_sizes(self) -> list[int]:
        known_positions = set()
        rv = []
        for act_position in self.position_dict:
            if act_position in known_positions:
                continue
            known_positions.add(act_position)
            counter = 0
            dq = deque([act_position])
            while dq:
                ap = dq.popleft()
                counter += 1
                for next_position in neighbor_positions(ap):
                    if next_position in known_positions or next_position not in self.position_dict:
                        continue
                    known_positions.add(next_position)
                    dq.append(next_position)
            rv.append(counter)
        return rv


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    g = CBasin()
    for y, inp_row in enumerate(yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False)):
        for x, h in enumerate(inp_row):
            if h != '9':
                g.add_item(Position2D(x, y), int(h))
    answer1 = g.basins_count
    answer2 = prod(sorted(g.regions_sizes)[-3:])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 9, solve_puzzle)


if __name__ == '__main__':
    main()
