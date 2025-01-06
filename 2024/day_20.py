from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, neighbor_positions
from functools import cached_property


class CMaze(CGridBase):
    def __init__(self):
        super().__init__()
        self.start_pos: Position2D | None = None
        self.end_pos: Position2D | None = None

    def set_start_end_pos(self):
        for k, v in self.position_dict.items():
            if v == 'E':
                self.end_pos = k
            elif v == 'S':
                self.start_pos = k
        del self.position_dict[self.start_pos]
        del self.position_dict[self.end_pos]

    @cached_property
    def path_cost_wo_cheat(self) -> int:
        return self.tile_cost_from_start[self.end_pos]

    @cached_property
    def tile_cost_from_start(self) -> dict[Position2D, int]:
        act_pos = self.start_pos
        rd = {act_pos: 0}
        act_cost = 0
        act_pos_list = [act_pos]
        visited = {act_pos}
        while act_pos_list:
            act_cost += 1
            next_pos_list = []
            for act_pos in act_pos_list:
                for next_pos in neighbor_positions(act_pos, p_return_corner=False):
                    if next_pos in self.position_dict or next_pos in visited:
                        continue
                    visited.add(next_pos)
                    rd[next_pos] = act_cost
                    next_pos_list.append(next_pos)
            act_pos_list = next_pos_list
        return rd

    @cached_property
    def tile_cost_to_end(self) -> dict[Position2D, int]:
        act_pos = self.end_pos
        rd = {act_pos: 0}
        act_cost = 0
        act_pos_list = [act_pos]
        visited = {act_pos}
        while act_pos_list:
            act_cost += 1
            next_pos_list = []
            for act_pos in act_pos_list:
                for next_pos in neighbor_positions(act_pos, p_return_corner=False):
                    if next_pos in self.position_dict or next_pos in visited:
                        continue
                    visited.add(next_pos)
                    rd[next_pos] = act_cost
                    next_pos_list.append(next_pos)
            act_pos_list = next_pos_list
        return rd

    def count_cheat(self, p_cheat_length: int, p_cheat_min_save: int) -> int:
        rv = 0
        for start_pos, start_cost in self.tile_cost_from_start.items():
            visited = {start_pos, }
            act_pos_list = [start_pos]
            for i in range(1, p_cheat_length + 1):
                next_pos_list = []
                for act_pos in act_pos_list:
                    for next_pos in neighbor_positions(act_pos, p_return_corner=False):
                        if next_pos in visited:
                            continue
                        visited.add(next_pos)
                        if start_cost + i + self.tile_cost_to_end.get(next_pos, float('inf')) <= \
                                self.path_cost_wo_cheat - p_cheat_min_save:
                            rv += 1
                        next_pos_list.append(next_pos)
                act_pos_list = next_pos_list
        return rv


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    m = CMaze()
    m.print_y_reverse = True
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        m.add_row(inp_row, p_chars_to_skip='.')
    m.set_start_end_pos()

    answer1 = m.count_cheat(p_cheat_length=2, p_cheat_min_save=100)
    answer2 = m.count_cheat(p_cheat_length=20, p_cheat_min_save=100)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 20, solve_puzzle)


if __name__ == '__main__':
    main()
