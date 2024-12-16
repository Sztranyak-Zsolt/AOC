from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, neighbor_positions
from functools import reduce

MAX_X = 101
MAX_Y = 103
PRINT_PICTURE = False


class CRobot:
    def __init__(self, px: int, py: int, vx: int, vy: int):
        self.orig_pos = Position2D(px, py)
        self.velocity = Position2D(vx, vy)

    def position_after_steps(self, step: int):
        x = self.orig_pos.x + self.velocity.x * step
        y = self.orig_pos.y + self.velocity.y * step
        x %= MAX_X
        y %= MAX_Y
        return Position2D(x, y)

    def quadrant_after_step(self, p_step: int) -> int:
        step_pos = self.position_after_steps(p_step)
        if step_pos.x == MAX_X // 2 or step_pos.y == MAX_Y // 2:
            return 0
        rv = 1
        if step_pos.x > MAX_X // 2:
            rv = 2
        if step_pos.y > MAX_Y // 2:
            rv += 2
        return rv


def neighbors_count_after_step(p_robot_list: list[CRobot], p_step: int) -> int:
    pos_set = set()
    for act_robot in p_robot_list:
        pos_set.add(act_robot.position_after_steps(p_step))
    rv = 0
    for p in pos_set:
        for np in neighbor_positions(p, p_return_corner=False):
            if np in pos_set:
                rv += 1
    return rv // 2


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    q = [0] * 5
    r_list: list[CRobot] = []
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space='=,pv'):
        r = CRobot(*inp_row)
        r_list.append(r)
        q[r.quadrant_after_step(100)] += 1

    answer1 = reduce(lambda x, y: x * y,  q[1:], 1)

    act_step = 1
    answer2 = None

    while act_step < 100000:
        if neighbors_count_after_step(r_list, act_step) > 300:
            answer2 = act_step
            if PRINT_PICTURE:
                p = CGridBase()
                p.print_y_reverse = True
                for act_r in r_list:
                    act_r.position_after_steps(act_step)
                    p.add_item(act_r.position_after_steps(act_step), '#')
                print(p)
            break
        act_step += 1

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 14, solve_puzzle)


if __name__ == '__main__':
    main()
