import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


class CSubmarine:
    def __init__(self):
        self.depth = 0
        self.x = 0
        self.aim = 0
        self.depth2 = 0

    def move(self, p_direction: str, p_length: int):
        if p_direction == "up":
            self.depth -= p_length
            self.aim -= p_length
        elif p_direction == "down":
            self.depth += p_length
            self.aim += p_length
        elif p_direction == "forward":
            self.x += p_length
            self.depth2 += self.aim * p_length

    def calc_multiplication(self):
        return self.depth * self.x

    def calc_multiplication2(self):
        return self.depth2 * self.x


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    sm = CSubmarine()
    for inp_direction, inp_step in yield_input_data(p_input_file_path):
        sm.move(inp_direction, inp_step)
    answer1 = sm.calc_multiplication()
    answer2 = sm.calc_multiplication2()

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 2, solve_puzzle)


if __name__ == '__main__':
    main()
