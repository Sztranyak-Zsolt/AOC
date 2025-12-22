import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, add_positions


class CTetris(CGridBase):
    dir_dict = {'<': Position2D(-1, 0), '>': Position2D(1, 0), 'v': Position2D(0, -1)}

    def __init__(self, p_instr: str):
        super().__init__()
        self.shape_list: list[list[Position2D]] = []
        self.play_instruction: str = p_instr
        self.act_shape: list[Position2D] = []
        self.max_x = 6
        self.bottom_full_line = -1

    def reset_game(self):
        self.position_dict.clear()
        self.act_shape.clear()
        self.max_y = 0
        self.bottom_full_line = 0

    @property
    def act_position_code(self) -> int:
        rv = 0
        for y in range(self.max_y, self.bottom_full_line, -1):
            for x in range(self.min_x, self.max_x + 1):
                rv <<= 1
                if Position2D(x, y) in self.position_dict:
                    rv += 1
        return rv

    def add_shape(self, p_shape_index: int):
        add_y = self.max_y + 4
        self.act_shape = [add_positions(s, Position2D(2, add_y)) for s in self.shape_list[p_shape_index]]

    def push_shape(self, p_direction_str: str) -> bool:
        p_direction = self.dir_dict[p_direction_str]
        pushed_shape = []
        for act_position in self.act_shape:
            pushed_position = add_positions(act_position, p_direction)
            if pushed_position.x < self.min_x or self.max_x < pushed_position.x \
                    or pushed_position.y <= self.bottom_full_line or pushed_position in self.position_dict:
                return False
            pushed_shape.append(pushed_position)
        self.act_shape.clear()
        self.act_shape.extend(pushed_shape)
        return True

    def check_bottom_line(self):
        for y in range(self.max_y, self.bottom_full_line, -1):
            for x in range(self.min_x, self.max_x + 1):
                if Position2D(x, y) not in self.position_dict:
                    break
            else:
                self.bottom_full_line = y
                for p in [p for p in self.position_dict if p.y <= y]:
                    del self.position_dict[p]
                return

    def play_next_shape(self, p_parameters: list[int, int]):
        act_shape_index, act_instruction_index = p_parameters
        self.add_shape(act_shape_index)
        act_shape_index = (act_shape_index + 1) % len(self.shape_list)
        self.push_shape(self.play_instruction[act_instruction_index])
        act_instruction_index = (act_instruction_index + 1) % len(self.play_instruction)
        while self.push_shape('v'):
            self.push_shape(self.play_instruction[act_instruction_index])
            act_instruction_index = (act_instruction_index + 1) % len(self.play_instruction)
        for shape_position in self.act_shape:
            self.add_item(shape_position, '#')
        self.act_shape.clear()
        self.check_bottom_line()
        p_parameters[0] = act_shape_index
        p_parameters[1] = act_instruction_index

    def play_game(self, p_counter: int):
        self.reset_game()
        act_parameters = [0, 0]
        save_dict = {}
        for act_turn in range(1, p_counter + 1):
            self.play_next_shape(act_parameters)
            if self.max_y - self.bottom_full_line < 10:
                act_pos_code = self.act_position_code
                if (act_parameters[0], act_parameters[1], act_pos_code) in save_dict:
                    prev_turn, prev_height = save_dict[(act_parameters[0], act_parameters[1], act_pos_code)]
                    period_length = act_turn - prev_turn
                    period_height = self.max_y - prev_height
                    pre_period_height = self.play_game(p_counter % period_length)
                    period_count = p_counter // period_length
                    return pre_period_height + period_height * period_count
                save_dict[(act_parameters[0], act_parameters[1], act_pos_code)] = (act_turn, self.max_y)
        return self.max_y

    def __str__(self):
        r_str = list()
        for y in range(self.max_y, self.bottom_full_line, -1):
            ss = '|'
            for x in range(self.min_x, self.max_x + 1):
                if Position2D(x, y) in self.position_dict:
                    ss += '#'
                elif Position2D(x, y) in self.act_shape:
                    ss += '@'
                else:
                    ss += ' '
            r_str.append(f'{ss}|  y = {y}')
        r_str.append('-' * (self.max_x - self.min_x + 3))
        return '\n'.join(r_str) + "\n"


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    starting_shapes = [[Position2D(0, 0), Position2D(1, 0), Position2D(2, 0), Position2D(3, 0)],
                       [Position2D(0, 1), Position2D(1, 0), Position2D(1, 1), Position2D(2, 1), Position2D(1, 2)],
                       [Position2D(0, 0), Position2D(1, 0), Position2D(2, 0), Position2D(2, 1), Position2D(2, 2)],
                       [Position2D(0, 0), Position2D(0, 1), Position2D(0, 2), Position2D(0, 3)],
                       [Position2D(0, 0), Position2D(1, 0), Position2D(0, 1), Position2D(1, 1)]]
    input_iterator = iter(yield_input_data(p_input_file_path, p_whole_row=True))
    tx = CTetris(next(input_iterator))
    tx.shape_list = starting_shapes
    answer1 = tx.play_game(2022)
    answer2 = tx.play_game(1000000000000)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 17, solve_puzzle)


if __name__ == '__main__':
    main()
