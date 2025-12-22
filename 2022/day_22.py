import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, add_positions


class CMap(CGridBase):
    facing_dir = [Position2D(1, 0), Position2D(0, 1), Position2D(-1, 0), Position2D(0, -1)]

    def __init__(self):
        super().__init__()
        self.map_row: list[str] = list()
        # self.x = 0
        # self.y = 0
        self.facing = 0
        self.inst: list[str | int] = []

    @property
    def starting_position(self):
        return Position2D(min([p.x for p in self.position_dict if p.y == self.min_y]), self.min_y)

    def make_instruction_list(self, p_inst_str: str):
        prev_step = 0
        for c in p_inst_str:
            if c in ['R', 'L']:
                if prev_step != 0:
                    self.inst.append(prev_step)
                self.inst.append(c)
                prev_step = 0
                continue
            prev_step = prev_step * 10 + int(c)
        if prev_step != 0:
            self.inst.append(prev_step)

    def make_step_base(self, p_facing: int, p_position: Position2D, p_step: int) -> Position2D:
        for s in range(p_step):
            next_position = add_positions(p_position, self.facing_dir[p_facing])
            if next_position not in self.position_dict:
                if p_facing == 0:
                    next_position = Position2D(min([p.x for p in self.position_dict
                                                    if p.y == p_position.y]), p_position.y)
                elif p_facing == 1:
                    next_position = Position2D(p_position.x, min([p.y for p in self.position_dict
                                                                  if p.x == p_position.x]))
                elif p_facing == 2:
                    next_position = Position2D(max([p.x for p in self.position_dict
                                                    if p.y == p_position.y]), p_position.y)
                elif p_facing == 3:
                    next_position = Position2D(p_position.x, max([p.y for p in self.position_dict
                                                                  if p.x == p_position.x]))
            if self.position_dict[next_position] == '#':
                return p_position, p_facing
            p_position = next_position
        return p_position, p_facing

    def make_step_advanced(self, p_facing: int, p_position: Position2D, p_step: int) -> (Position2D, int):
        for s in range(p_step):
            next_position = add_positions(p_position, self.facing_dir[p_facing])
            next_facing = p_facing
            if next_position not in self.position_dict:
                if p_facing == 3 and next_position.y < 0 and 50 <= next_position.x < 100:
                    next_position = Position2D(0, 150 + next_position.x - 50)
                    next_facing = 0
                if p_facing == 2 and next_position.x < 0 and 150 <= next_position.y < 200:
                    next_position = Position2D(50 + next_position.y - 150, 0)
                    next_facing = 1
                if p_facing == 3 and next_position.y < 0 and 100 <= next_position.x < 150:
                    next_position = Position2D(next_position.x - 100, 199)
                    next_facing = 3
                if p_facing == 1 and next_position.y >= 200 and 0 <= next_position.x < 50:
                    next_position = Position2D(100 + next_position.x, 0)
                    next_facing = 1
                if p_facing == 2 and next_position.x < 50 and 0 <= next_position.y < 50:
                    next_position = Position2D(0, 150 - next_position.y - 1)
                    next_facing = 0
                if p_facing == 2 and next_position.x < 0 and 100 <= next_position.y < 150:
                    next_position = Position2D(50, 150 - next_position.y - 1)
                    next_facing = 0
                if p_facing == 2 and 0 <= next_position.x < 50 and 50 <= next_position.y < 100:
                    next_position = Position2D(next_position.y - 50, 100)
                    next_facing = 1
                if p_facing == 3 and 0 <= next_position.x < 50 and 50 <= next_position.y < 100:
                    next_position = Position2D(50, 50 + next_position.x)
                    next_facing = 0
                if p_facing == 0 and 150 <= next_position.x and 0 <= next_position.y < 50:
                    next_position = Position2D(99, 150 - next_position.y - 1)
                    next_facing = 2
                if p_facing == 0 and 100 <= next_position.x and 100 <= next_position.y < 150:
                    next_position = Position2D(149, 150 - next_position.y - 1)
                    next_facing = 2
                if p_facing == 1 and 100 <= next_position.x < 150 and 50 <= next_position.y < 100:
                    next_position = Position2D(99, next_position.x - 50)
                    next_facing = 2
                if p_facing == 0 and 100 <= next_position.x < 150 and 50 <= next_position.y < 100:
                    next_position = Position2D(next_position.y + 50, 49)
                    next_facing = 3
                if p_facing == 1 and 50 <= next_position.x < 100 and 150 <= next_position.y < 200:
                    next_position = Position2D(49, next_position.x + 100)
                    next_facing = 2
                if p_facing == 0 and 50 <= next_position.x < 100 and 150 <= next_position.y < 200:
                    next_position = Position2D(next_position.y - 100, 149)
                    next_facing = 3
            if self.position_dict[next_position] == '#':
                return p_position, p_facing
            p_position = next_position
            p_facing = next_facing
        return p_position, p_facing

    def move(self, p_advanced_method: bool):
        if not p_advanced_method:
            step_func = self.make_step_base
        else:
            step_func = self.make_step_advanced
        act_position = self.starting_position
        act_facing = 0
        for act_instr in self.inst:
            if isinstance(act_instr, int):
                act_position, act_facing = step_func(act_facing, act_position, act_instr)
                continue
            if act_instr == 'R':
                act_facing = (act_facing + 1) % 4
            elif act_instr == 'L':
                act_facing = (act_facing - 1) % 4
        return act_position, act_facing


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    m = CMap()
    m.print_y_reverse = True
    group_iterator = iter(yield_input_data(p_input_file_path, p_whole_row=True, p_group_separator='\n\n'))
    for map_row in next(group_iterator):
        m.add_row(map_row, p_chars_to_skip=' ')
    m.make_instruction_list(next(group_iterator)[0])
    end_pos1, end_face1 = m.move(False)
    answer1 = (end_pos1.y + 1) * 1000 + (end_pos1.x + 1) * 4 + end_face1
    end_pos2, end_face2 = m.move(True)
    answer2 = (end_pos2.y + 1) * 1000 + (end_pos2.x + 1) * 4 + end_face2
    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 22, solve_puzzle)


if __name__ == '__main__':
    main()
