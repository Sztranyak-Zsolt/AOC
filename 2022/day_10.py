import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


class CSignal:
    def __init__(self):
        self.x = 1
        self.cycle = 0
        self.value = 0
        self.scr_string = ''

    def nood(self):
        self.cycle += 1
        self.check_cycle()
        self.print()

    def addx(self, p_value: int):
        self.nood()
        self.nood()
        self.x += p_value

    def check_cycle(self):
        if (self.cycle + 20) % 40 == 0:
            self.value += self.cycle * self.x

    def print(self):
        if self.x <= (self.cycle - 1) % 40 + 1 <= self.x + 2:
            self.scr_string += "#"
        else:
            self.scr_string += " "

    def __str__(self):
        r_lst = list()
        for c in range(len(self.scr_string) // 40):
            r_lst.append(self.scr_string[0 + c * 40: (c + 1) * 40])
        return '\n'.join(r_lst)


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    s = CSignal()
    for inp_row in yield_input_data(p_input_file_path):
        if inp_row[0] == "noop":
            s.nood()
        else:
            s.addx(inp_row[1])
    answer1 = s.value
    answer2 = '\n' + str(s).replace('#', '##').replace(' ', '  ')
    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 10, solve_puzzle)


if __name__ == '__main__':
    main()
