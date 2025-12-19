import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
import html


def solve_puzzle(p_input_file_path: str) -> tuple[int, int]:
    answer1 = answer2 = 0
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        act_word = inp_row.replace("\n", "")
        act_word2 = '"' + act_word.replace('\\', '\\\\').replace('"', '\\"') + '"'
        length3 = len(act_word2)
        length1 = len(act_word) - 2
        length2 = len(html.escape(act_word)) - 12
        answer1 += length2 - length1
        answer2 += length3 - length1 - 2
    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 8, solve_puzzle)


if __name__ == '__main__':
    main()
