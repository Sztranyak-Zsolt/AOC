import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import CVector2D

DIR = {'<': CVector2D(-1, 0), '>': CVector2D(1, 0), 'v': CVector2D(0, 1), '^': CVector2D(0, -1)}


class CWarehouse(CGridBase):
    def __init__(self):
        super().__init__()
        self.robot_pos_orig: CVector2D | None = None
        self.robot_pos: CVector2D | None = None
        self.robot_instr: str = ''
        self.double_warehouse = False

    def set_robot_position(self):
        for k, v in self.position_dict.items():
            if v in '@':
                self.robot_pos_orig = k
                self.robot_pos = k
                break
        del self.position_dict[self.robot_pos_orig]

    def make_step_single(self, p_direction_str: str):
        act_dir = DIR[p_direction_str]
        act_pos = self.robot_pos + act_dir
        if self.position_dict.get(act_pos, '') == '':
            self.robot_pos = act_pos
            return
        while self.position_dict.get(act_pos, '') in ('O', '[', ']'):
            act_pos = act_pos + act_dir
        if self.position_dict.get(act_pos, '') == '#':
            return
        self.robot_pos += act_dir
        while act_pos != self.robot_pos:
            prev_pos = act_pos - act_dir
            self.position_dict[act_pos] = self.position_dict[prev_pos]
            act_pos = prev_pos
        del self.position_dict[act_pos]

    def make_step_double_horizontal(self, p_direction_str: str):
        act_dir = DIR[p_direction_str]
        act_pos = self.robot_pos + act_dir
        if self.position_dict.get(act_pos, '') == '':
            self.robot_pos += act_dir
            return
        if self.position_dict.get(act_pos, '') == '#':
            return

        # collected pushed boxes
        pushed_rows = [set()]
        pushed_rows[0].add(act_pos)
        if self.position_dict[act_pos] == '[':
            pushed_rows[-1].add(act_pos + CVector2D(1, 0))
        else:
            pushed_rows[-1].add(act_pos + CVector2D(-1, 0))
        while pushed_rows[-1]:
            next_push_row = set()
            for last_pushed_row in pushed_rows[-1]:
                next_pos = last_pushed_row + act_dir
                if self.position_dict.get(next_pos, '') == '#':
                    return
                if self.position_dict.get(next_pos, '') == '[':
                    next_push_row.add(next_pos)
                    next_push_row.add(next_pos + CVector2D(1, 0))
                elif self.position_dict.get(next_pos, '') == ']':
                    next_push_row.add(next_pos)
                    next_push_row.add(next_pos + CVector2D(-1, 0))
            pushed_rows.append(next_push_row)

        # setting pushed boxes coordinates
        for last_pushed_row in pushed_rows[::-1]:
            for act_box in last_pushed_row:
                self.position_dict[act_box + act_dir] = self.position_dict[act_box]
                del self.position_dict[act_box]
        self.robot_pos += act_dir

    def move_robot(self):
        for c in self.robot_instr:
            if c in ('<', '>') or not self.double_warehouse:
                self.make_step_single(c)
                continue
            self.make_step_double_horizontal(c)

    def goods_gps(self):
        return sum(k.x + k.y * 100 for k, v in self.position_dict.items() if v in ('O', '['))


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    warehouse1 = CWarehouse()
    warehouse1.print_y_reverse = True

    warehouse2 = CWarehouse()
    warehouse2.double_warehouse = True
    warehouse2.print_y_reverse = True

    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        if not inp_row:
            continue
        if inp_row[0] in '<>v^':
            warehouse1.robot_instr += inp_row
            warehouse2.robot_instr += inp_row
        else:
            warehouse1.add_row(inp_row, p_chars_to_skip='.', p_position_type=CVector2D)
            inp_row = inp_row.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')
            warehouse2.add_row(inp_row, p_chars_to_skip='.', p_position_type=CVector2D)

    warehouse1.set_robot_position()
    warehouse1.move_robot()
    answer1 = warehouse1.goods_gps()

    warehouse2.set_robot_position()
    warehouse2.move_robot()
    answer2 = warehouse2.goods_gps()

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 15, solve_puzzle)


if __name__ == '__main__':
    main()
