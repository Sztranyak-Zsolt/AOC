from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from functools import cache

PATTERNS: list[str] = []


@cache
def calculate_possibilities(p_text_to_find: str) -> int:
    if p_text_to_find == '':
        return 1
    rv = 0
    for act_p in PATTERNS:
        if act_p == p_text_to_find[:len(act_p)]:
            rv += calculate_possibilities(p_text_to_find[len(act_p):])
    return rv


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space=','):
        if len(inp_row) > 1:
            PATTERNS.extend(inp_row)
        elif not inp_row:
            continue
        if act_possibilities := calculate_possibilities(inp_row[0]):
            answer1 += 1
            answer2 += act_possibilities
    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 19, solve_puzzle)


if __name__ == '__main__':
    main()
