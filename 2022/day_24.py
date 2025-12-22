import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from math import lcm
from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from functools import cached_property
from GENERICS.aoc_vector import Position2D, neighbor_positions, add_positions
from GENERICS.aoc_grid import CGridBase


class CBlizzard:
    def __init__(self, p_facing: str):
        self.facing = p_facing

    @cached_property
    def direction(self):
        return {'^': Position2D(0, 1), '>': Position2D(1, 0),
                'v': Position2D(0, -1), '<': Position2D(-1, 0)}[self.facing]

    def __hash__(self):
        return id(self)


class CGrid(CGridBase):
    def __init__(self):
        super().__init__()
        self.blizzard_init_position_dict: dict[CBlizzard, Position2D] = {}

    @cached_property
    def blizzard_period(self) -> int:
        return lcm(self.max_x, self.max_y)

    @cached_property
    def starting_position(self) -> Position2D | None:
        for x in range(self.min_x, self.max_x + 1):
            if Position2D(x, self.max_y) not in self.position_dict:
                return Position2D(x, self.max_y)
        return None

    @cached_property
    def target_position(self) -> Position2D | None:
        for x in range(self.min_x, self.max_x + 1):
            if Position2D(x, self.min_y) not in self.position_dict:
                return Position2D(x, self.min_y)
        return None

    def add_row(self, p_row: str, p_row_number: int | None = None, p_chars_to_skip: str = '',
                p_item_type: type[str] | type[int] | object = str, p_position_type: type[Position2D] = Position2D):
        super().add_row(p_row, p_row_number, p_chars_to_skip + '<>^v', p_item_type, p_position_type)
        for x, s in enumerate(p_row):
            if s in '<>^v':
                self.blizzard_init_position_dict[CBlizzard(s)] = Position2D(x, self.max_y)

    @cached_property
    def blizzard_positions_turn_set(self) -> list[set[Position2D]]:
        rl = [set(self.blizzard_init_position_dict.values())]
        act_bl_positions = self.blizzard_init_position_dict.copy()
        for c in range(lcm(self.max_x, self.max_y)):
            new_bl_positions = {}
            for bl, act_bl_pos in act_bl_positions.items():
                new_bl_pos = add_positions(act_bl_pos, bl.direction)
                if not (self.min_x + 1 <= new_bl_pos.x <= self.max_x - 1
                        and self.min_y + 1 <= new_bl_pos.y <= self.max_y - 1):
                    if bl.facing == '<':
                        new_bl_pos = Position2D(self.max_x - 1, act_bl_pos.y)
                    elif bl.facing == '>':
                        new_bl_pos = Position2D(self.min_x + 1, act_bl_pos.y)
                    elif bl.facing == 'v':
                        new_bl_pos = Position2D(act_bl_pos.x, self.max_y - 1)
                    elif bl.facing == '^':
                        new_bl_pos = Position2D(act_bl_pos.x, self.min_y + 1)
                new_bl_positions[bl] = new_bl_pos
            rl.append(set(new_bl_positions.values()))
            act_bl_positions = new_bl_positions
        return rl

    def try_step(self, p_position: Position2D, p_counter: int):
        if p_position in self.blizzard_positions_turn_set[p_counter % (len(self.blizzard_positions_turn_set))]:
            return False
        return True

    def get_path(self, p_starting_turn: int = 0, p_reverse: bool = False) -> int:
        if p_reverse:
            from_position = self.target_position
            target_position = self.starting_position
        else:
            from_position = self.starting_position
            target_position = self.target_position
        act_positions: set[Position2D] = {from_position}
        p_act_turn = p_starting_turn
        while True:
            new_positions: set[Position2D] = set()
            new_positions.add(from_position)
            p_act_turn += 1
            for next_pos in act_positions:
                for next_step in neighbor_positions(next_pos, p_return_self=True):
                    if next_step == target_position:
                        return p_act_turn
                    if next_step in self.position_dict or next_step.y < self.min_y or self.max_y < next_step.y or \
                            not self.try_step(next_step, p_act_turn):
                        continue
                    new_positions.add(next_step)
            act_positions = new_positions.copy()

    def __hash__(self):
        return id(self)


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    g = CGrid()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True):
        g.add_row(inp_row, p_chars_to_skip='.')

    answer1 = g.get_path()
    rev_turn = g.get_path(answer1, True)
    answer2 = g.get_path(rev_turn)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 24, solve_puzzle)


if __name__ == '__main__':
    main()
