from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, add_positions, neighbor_positions
from collections import deque
from functools import cached_property, cache


class CGrid(CGridBase):
    def __init__(self):
        super().__init__()

    @cached_property
    def starting_tile(self) -> Position2D:
        return Position2D(1, self.max_y)

    @cached_property
    def target_tile(self) -> Position2D:
        return Position2D(self.max_x - 1, 0)

    @cached_property
    def path_crosses(self) -> set[Position2D]:
        rs = set()
        for p in self.yield_all_position():
            if p in self.position_dict:
                continue
            if len([np for np in neighbor_positions(p) if np in self.position_dict]) == 4:
                rs.add(p)
        return rs

    @cached_property
    def crosses_connections(self) -> dict[Position2D, set[tuple[Position2D, int, bool]]]:
        rd = {cr: set() for cr in self.path_crosses | {self.starting_tile, self.target_tile}}
        dir_dict = {'>': Position2D(1, 0), '<': Position2D(-1, 0), 'v': Position2D(0, -1), '^': Position2D(0, 1)}
        dq = deque()
        for tile in rd:
            dq.append([tile, 0, {tile}, tile, False])
        while dq:
            act_pos, step_taken, visited, starting_cross, reverse_slope = dq.popleft()
            for np in neighbor_positions(act_pos):
                if np in self.position_dict and self.position_dict[np] == '#':
                    continue
                if np in visited or not (self.is_position_on_grid(np)):
                    continue
                next_reverse_slope = reverse_slope
                if np in self.position_dict and add_positions(act_pos, dir_dict[self.position_dict[np]]) != np:
                    next_reverse_slope = True
                if np in rd:
                    rd[starting_cross].add((np, step_taken + 1, next_reverse_slope))
                else:
                    dq.append([np, step_taken + 1, visited | {np}, starting_cross, next_reverse_slope])
        return rd

    @cache
    def max_steps_to_target(self,
                            p_cross: Position2D | None = None,
                            p_visited_crosses: tuple[Position2D] | None = None,
                            p_use_reverse_slope: bool = False):
        rv = -1
        if p_cross is None:
            p_cross = self.starting_tile
        if p_visited_crosses is None:
            p_visited_crosses = (self.starting_tile,)
        for next_cross, add_step, reverse_slope in self.crosses_connections[p_cross]:
            if reverse_slope and not p_use_reverse_slope or next_cross in p_visited_crosses:
                continue
            if next_cross == self.target_tile:
                rv = max(rv, add_step)
                continue
            next_steps_to_target = self.max_steps_to_target(next_cross,
                                                            tuple(sorted(list(p_visited_crosses) + [next_cross])),
                                                            p_use_reverse_slope)
            if next_steps_to_target != -1:
                rv = max(rv, add_step + next_steps_to_target)
        return rv


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    g = CGrid()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True):
        g.add_row(inp_row, p_chars_to_skip='.')

    answer1 = g.max_steps_to_target()
    g.max_steps_to_target.cache_clear()
    answer2 = g.max_steps_to_target(p_use_reverse_slope=True)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 23, solve_puzzle)


if __name__ == '__main__':
    main()
