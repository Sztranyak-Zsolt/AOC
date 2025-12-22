import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def horizontal_count(p_crossword: list[str], p_target: str) -> int:
    return sum(r.count(p_target) + r.count(p_target[::-1]) for r in p_crossword)


def vertical_count(p_crossword: list[str], p_target: str) -> int:
    rv = 0
    for r in zip(*p_crossword):
        r2 = ''.join(r)
        rv += r2.count(p_target) + r2.count(p_target[::-1])
    return rv


def diagonal_count(p_crossword: list[str], p_target: str) -> int:
    rv = 0
    for y in range(len(p_crossword) - len(p_target) + 1):
        for x in range(len(p_crossword[0]) - len(p_target) + 1):
            w1 = w2 = ''
            for i3 in range(len(p_target)):
                w1 += p_crossword[x + i3][y + i3]
                w2 += p_crossword[x + len(p_target) - 1 - i3][y + i3]
            if w1 in (p_target, p_target[::-1]):
                rv += 1
            if w2 in (p_target, p_target[::-1]):
                rv += 1
    return rv


def diagonal_x_count(p_crossword: list[str], p_target: str) -> int:
    rv = 0
    for y in range(len(p_crossword) - len(p_target) + 1):
        for x in range(len(p_crossword[0]) - len(p_target) + 1):
            w1 = w2 = ''
            for i3 in range(len(p_target)):
                w1 += p_crossword[x + i3][y + i3]
                w2 += p_crossword[x + len(p_target) - 1 - i3][y + i3]
            if w1 in (p_target, p_target[::-1]) and w2 in (p_target, p_target[::-1]):
                rv += 1
    return rv


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    crossword = []
    target_word = 'XMAS'
    for inp_row in yield_input_data(p_input_file_path,
                                    p_whole_row=True,
                                    p_chars_to_space=''
                                    ):
        crossword.append(inp_row)

    answer1 = horizontal_count(crossword, target_word) + vertical_count(crossword, target_word) \
        + diagonal_count(crossword, target_word)
    answer2 = diagonal_x_count(crossword, target_word[1:])
    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 4, solve_puzzle)


if __name__ == '__main__':
    main()
