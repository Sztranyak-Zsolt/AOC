import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space=',:;'):
        g = b = r = 0
        limit_breached = False
        for v, c in zip(inp_row[2::2], inp_row[3::2]):
            if c == 'red' and v > 12 or c == 'green' and v > 13 or c == 'blue' and v > 14:
                limit_breached = True
            if c == 'red':
                r = max(r, v)
            elif c == 'green':
                g = max(g, v)
            elif c == 'blue':
                b = max(b, v)
        if not limit_breached:
            answer1 += inp_row[1]
        answer2 += b * r * g
    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 2, solve_puzzle)


if __name__ == '__main__':
    main()
