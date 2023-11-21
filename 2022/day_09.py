from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_vector import CVector2D


class CRope:
    def __init__(self, p_tail_length: int = 1):
        self.head_p: CVector2D = CVector2D(0, 0)
        self.tail_p_list: list[CVector2D] = []
        self.tail_length = p_tail_length
        for _ in range(p_tail_length):
            self.tail_p_list.append(CVector2D(0, 0))
        self.first_tail_path: set[CVector2D] = {CVector2D(0, 0)}
        self.last_tail_path: set[CVector2D] = {CVector2D(0, 0)}

    def move_head(self, p_direction: CVector2D, p_step: int):
        for _ in range(p_step):
            self.head_p += p_direction
            self.tail_follow(self.head_p, 0)

    def tail_follow(self, follow_position: CVector2D, knot_num: int):
        if abs(follow_position.x - self.tail_p_list[knot_num].x) >= 2 \
                or abs(follow_position.y - self.tail_p_list[knot_num].y) >= 2:
            if follow_position.x > self.tail_p_list[knot_num].x:
                self.tail_p_list[knot_num] += CVector2D(1, 0)
            elif follow_position.x < self.tail_p_list[knot_num].x:
                self.tail_p_list[knot_num] += CVector2D(-1, 0)
            if follow_position.y > self.tail_p_list[knot_num].y:
                self.tail_p_list[knot_num] += CVector2D(0, 1)
            elif follow_position.y < self.tail_p_list[knot_num].y:
                self.tail_p_list[knot_num] += CVector2D(0, -1)
            if knot_num == 0:
                self.first_tail_path.add(self.tail_p_list[knot_num])
            if knot_num != self.tail_length - 1:
                self.tail_follow(self.tail_p_list[knot_num], knot_num + 1)
            else:
                self.last_tail_path.add(self.tail_p_list[knot_num])


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    direction_dir = {"R": CVector2D(0, 1), "L": CVector2D(0, -1), "U": CVector2D(-1, 0), "D": CVector2D(1, 0)}
    rope = CRope(p_tail_length=9)

    for step_dir, step_count in yield_input_data(p_input_file_path):
        rope.move_head(direction_dir[step_dir], step_count)
    answer1 = len(rope.first_tail_path)
    answer2 = len(rope.last_tail_path)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 9, solve_puzzle)


if __name__ == '__main__':
    main()
