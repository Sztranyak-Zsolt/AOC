import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def is_triangle(p_sides: list[int]) -> bool:
    sides = sorted(p_sides)
    return sides[0] + sides[1] > sides[2]


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    t1, t2, t3 = [], [], []
    for a, b, c in yield_input_data(p_input_file_path):
        if is_triangle([a, b, c]):
            answer1 += 1
        t1.append(a)
        t2.append(b)
        t3.append(c)
        if len(t1) == 3:
            if is_triangle(t1):
                answer2 += 1
            if is_triangle(t2):
                answer2 += 1
            if is_triangle(t3):
                answer2 += 1
            t1, t2, t3 = [], [], []

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 3, solve_puzzle)


if __name__ == '__main__':
    main()
