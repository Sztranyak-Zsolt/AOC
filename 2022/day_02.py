import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    strategy_1 = {"A X": 4, "A Y": 8, "A Z": 3,
                  "B X": 1, "B Y": 5, "B Z": 9,
                  "C X": 7, "C Y": 2, "C Z": 6}
    strategy_2 = {"A X": 3, "A Y": 4, "A Z": 8,
                  "B X": 1, "B Y": 5, "B Z": 9,
                  "C X": 2, "C Y": 6, "C Z": 7}
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        answer1 += strategy_1[inp_row]
        answer2 += strategy_2[inp_row]

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 2, solve_puzzle)


if __name__ == '__main__':
    main()
