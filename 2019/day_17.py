import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from Intcode import CIntCode
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import CVector2D, neighbor_positions


class CGrid(CGridBase):
    def __init__(self, p_robot_intcode: CIntCode):
        super().__init__()
        self.robot_position: CVector2D | None = None
        self.robot_program = p_robot_intcode

    def build_grid_from_output(self):
        self.robot_program.init_memory_list[0] = 1
        self.robot_program.reset_program()
        self.robot_program.run_program()
        for act_row in self.robot_program.output_text.split('\n'):
            self.add_row(act_row, p_chars_to_skip='.')
        self.robot_position = [k for k, v in self.position_dict.items() if v == '^'][0]

    @property
    def crosses_count(self):
        rv = 0
        for act_pos in self.position_dict:
            if len([x for x in neighbor_positions(act_pos) if x in self.position_dict]) == 4:
                rv += act_pos.x * act_pos.y
        return rv

    @property
    def collect_dust(self) -> int:
        self.robot_program.init_memory_list[0] = 2
        self.robot_program.reset_program()
        self.robot_program.set_input_from_text_list(['A,C,A,B,C,B,C,B,A,B',
                                                     'L,10,R,12,R,12',
                                                     'R,10,L,10,L,12,R,6',
                                                     'R,6,R,10,L,10', 'n'])
        self.robot_program.run_program()
        return self.robot_program.output_list[-1]


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    num_list = next(yield_input_data(p_input_file_path, p_chars_to_space=','), None)
    g = CGrid(CIntCode(num_list))
    g.build_grid_from_output()
    answer1 = g.crosses_count
    answer2 = g.collect_dust

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 17, solve_puzzle)


if __name__ == '__main__':
    main()
