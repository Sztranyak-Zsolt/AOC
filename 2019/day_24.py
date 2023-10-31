from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import Position2D, CGridBase, neighbor_positions
from functools import cache


@cache
def level_link():
    rl = []
    for i in range(5):
        rl.append((Position2D(1, 2), Position2D(0, i)))
        rl.append((Position2D(3, 2), Position2D(4, i)))
        rl.append((Position2D(2, 1), Position2D(i, 0)))
        rl.append((Position2D(2, 3), Position2D(i, 4)))
    return rl


class CGridX(CGridBase):
    def __init__(self):
        super().__init__()
        self.bug_positions: set[Position2D] = set()
        self.max_x = self.max_y = 4
        self.lower_grid: CGridX | None = None
        self.upper_grid: CGridX | None = None
        self.level = 0

    @property
    def biodiversity_rating(self) -> int:
        rv = 0
        for act_pos in self.bug_positions:
            rv += 2 ** (act_pos.x + (4 - act_pos.y) * 5)
        return rv

    @property
    def lowest_grid(self) -> CGridX:
        if self.lower_grid is None:
            return self
        return self.lower_grid.lowest_grid

    @property
    def highest_grid(self) -> CGridX:
        if self.upper_grid is None:
            return self
        return self.upper_grid.highest_grid

    @property
    def bugs_count(self) -> int:
        rv = 0
        d_act_grid = self.highest_grid
        while d_act_grid:
            rv += len(d_act_grid.bug_positions)
            d_act_grid = d_act_grid.lower_grid
        return rv

    def count_neighbor_bugs(self, p_position: Position2D, p_recourse: bool = False) -> int:
        neighbors_count = len([np for np in neighbor_positions(p_position) if np in self.bug_positions])
        if not p_recourse:
            return neighbors_count
        if p_position == Position2D(2, 2):
            return 0
        if self.upper_grid is not None:
            neighbors_count += len([ul for ul, ll in level_link() if ll == p_position
                                    and ul in self.upper_grid.bug_positions])
        if self.lower_grid is not None:
            neighbors_count += len([ul for ul, ll in level_link() if ul == p_position
                                    and ll in self.lower_grid.bug_positions])
        return neighbors_count

    @property
    def possible_parent(self) -> bool:
        return len([b for b in self.bug_positions if b.x == 0]) in [1, 2] \
               or len([b for b in self.bug_positions if b.x == 4]) in [1, 2] \
               or len([b for b in self.bug_positions if b.y == 0]) in [1, 2] \
               or len([b for b in self.bug_positions if b.y == 4]) in [1, 2]

    def evolve_bugs_base(self) -> CGridX:
        new_grid = CGridX()
        for act_position in self.yield_all_position():
            nb_counter = self.count_neighbor_bugs(act_position)
            if nb_counter == 1 or act_position not in self.bug_positions and nb_counter == 2:
                new_grid.bug_positions.add(act_position)
        return new_grid

    def evolve_bugs_recurse(self) -> CGridX:
        if self.lowest_grid is not self:
            return self.lowest_grid.evolve_bugs_recurse()
        if self.bug_positions & {Position2D(1, 2), Position2D(2, 1), Position2D(3, 2), Position2D(2, 3)}:
            self.lower_grid = CGridX()
            self.lower_grid.level = self.level + 1
            self.lower_grid.upper_grid = self
            return self.lower_grid.evolve_bugs_recurse()
        act_grid = self
        evolved_grid = CGridX()
        evolved_grid.level = act_grid.level
        while act_grid:
            for act_position in act_grid.yield_all_position():
                if act_position == Position2D(2, 2):
                    continue
                nb_counter = act_grid.count_neighbor_bugs(act_position, True)
                if nb_counter == 1 or act_position not in act_grid.bug_positions and nb_counter == 2:
                    evolved_grid.bug_positions.add(act_position)
            if act_grid.upper_grid is None and act_grid.possible_parent:
                act_grid.upper_grid = CGridX()
                act_grid.upper_grid.level = act_grid.level - 1
                act_grid.upper_grid.lower_grid = act_grid
            if act_grid.upper_grid:
                evolved_grid.upper_grid = CGridX()
                evolved_grid.upper_grid.level = evolved_grid.level - 1
                evolved_grid.upper_grid.lower_grid = evolved_grid
                evolved_grid = evolved_grid.upper_grid
            act_grid = act_grid.upper_grid
        return evolved_grid

    def __str__(self):
        rl = [f'level {self.level}']
        for d_y in range(4, -1, -1):
            rs = ''
            for d_x in range(5):
                if (d_x, d_y) == (2, 2):
                    rs += '?'
                elif (d_x, d_y) in self.bug_positions:
                    rs += '#'
                else:
                    rs += ' '
            rl.append(rs)
        if self.lower_grid:
            return '\n'.join(rl) + '\n\n' + str(self.lower_grid)
        return '\n'.join(rl)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    g = CGridX()
    g2 = CGridX()

    for y, inp_row in enumerate(yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True)):
        g.add_row(inp_row, p_chars_to_skip='.', p_row_number=y)
        g2.add_row(inp_row, p_chars_to_skip='.', p_row_number=y)
    g.bug_positions = set(g.position_dict)
    g2.bug_positions = set(g2.position_dict)
    bd_list = []
    while g.biodiversity_rating not in bd_list:
        bd_list.append(g.biodiversity_rating)
        g = g.evolve_bugs_base()
    answer1 = g.biodiversity_rating

    for i in range(200):
        g2 = g2.evolve_bugs_recurse()
    answer2 = g2.bugs_count
    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 24, solve_puzzle)


if __name__ == '__main__':
    main()
