from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from Intcode import CIntCode
from GENERICS.aoc_grid import CGridBase, Position2D, add_positions
from copy import copy
from collections import deque


class CGrid(CGridBase):
    def __init__(self, p_intcode_input: CIntCode):
        super().__init__()
        self.dir_dict = {1: Position2D(0, 1), 2: Position2D(0, -1), 3: Position2D(-1, 0), 4: Position2D(1, 0)}
        self.robot_position_init = Position2D(0, 0)
        self.oxygen_position: Position2D | None = None
        self.init_program = p_intcode_input
        self.add_item(self.robot_position_init, ' ')

    def map_grid_for_oxygen(self) -> int:
        dq = deque([[self.robot_position_init, self.init_program, 0]])
        steps_needed = -1
        while dq:
            act_position, act_program_instance, act_step = dq.popleft()
            for dir_code, dir_pos in self.dir_dict.items():
                if (new_pos := add_positions(act_position, dir_pos)) in self.position_dict:
                    continue
                new_program_instance = copy(act_program_instance)
                new_program_instance.input_list = [dir_code]
                new_program_instance.run_until_next_outputs()
                new_output = new_program_instance.output_list.pop(0)
                if new_output == 0:
                    self.add_item(new_pos, '#')
                    continue
                elif new_output == 1:
                    self.add_item(new_pos, ' ')
                elif new_output == 2:
                    self.add_item(new_pos, 'O')
                    self.oxygen_position = new_pos
                    steps_needed = act_step + 1
                dq.append([new_pos, new_program_instance, act_step + 1])
        return steps_needed

    @property
    def time_to_fill_map(self) -> int:
        act_step = -1
        dq = deque([[self.oxygen_position, 0]])
        visited_positions = set()
        while dq:
            act_position, act_step = dq.popleft()
            for next_dir in self.dir_dict.values():
                if (next_pos := add_positions(act_position, next_dir)) in visited_positions \
                        or self.position_dict[add_positions(act_position, next_dir)] == '#':
                    continue
                visited_positions.add(next_pos)
                dq.append([next_pos, act_step + 1])
        return act_step


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    num_list = next(yield_input_data(p_input_file_path, p_chars_to_space=','), None)
    g = CGrid(CIntCode(num_list))
    answer1 = g.map_grid_for_oxygen()
    answer2 = g.time_to_fill_map

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 15, solve_puzzle)


if __name__ == '__main__':
    main()
