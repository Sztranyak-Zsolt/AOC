import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from Intcode import CIntCode
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import CVector2D


class CGridRobot(CGridBase):
    dir_dict = {0: CVector2D(0, 1), 1: CVector2D(1, 0), 2: CVector2D(0, -1), 3: CVector2D(-1, 0)}

    def __init__(self):
        super().__init__()
        self.robot_position = CVector2D(0, 0)
        self.robot_facing = 0

    def robot_paint(self,  p_color: bool):
        painted_str = '#' if p_color else ' '
        if self.robot_position not in self.position_dict:
            self.add_item(self.robot_position, painted_str)
        else:
            self.position_dict[self.robot_position] = painted_str

    def turn_robot_and_move(self, p_direction: bool):
        if p_direction:
            self.robot_facing = (self.robot_facing + 1) % 4
        else:
            self.robot_facing = (self.robot_facing - 1) % 4
        self.robot_position = self.robot_position + self.dir_dict[self.robot_facing]


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    num_list = next(yield_input_data(p_input_file_path, p_chars_to_space=','), None)

    ic = CIntCode(num_list, [0])
    gr = CGridRobot()
    while not ic.program_finished:
        ic.execute_next_instruction()
        if len(ic.output_list) == 2:
            gr.robot_paint(ic.output_list.pop(0) == 1)
            gr.turn_robot_and_move(ic.output_list.pop(0) == 1)
            if gr.position_dict.get(gr.robot_position, ' ') == '#':
                ic.input_list.append(1)
            else:
                ic.input_list.append(0)

    answer1 = len(gr.position_dict)

    ic.reset_program()
    ic.input_list = [1]
    gr = CGridRobot()
    gr.double_width_on_print = True
    while not ic.program_finished:
        ic.execute_next_instruction()
        if len(ic.output_list) == 2:
            gr.robot_paint(ic.output_list.pop(0) == 1)
            gr.turn_robot_and_move(ic.output_list.pop(0) == 1)
            if gr.position_dict.get(gr.robot_position, ' ') == '#':
                ic.input_list.append(1)
            else:
                ic.input_list.append(0)

    answer2 = f'\n{gr}'

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 11, solve_puzzle)


if __name__ == '__main__':
    main()
