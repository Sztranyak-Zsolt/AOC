import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from hashlib import md5
from re import search, findall
from functools import lru_cache


@lru_cache(maxsize=1001)
def get_hash(p_str_to_hash: str, p_stretch: bool = False) -> str:
    for _ in range(1 if not p_stretch else 2017):
        p_str_to_hash = md5(p_str_to_hash.encode()).hexdigest()
    return p_str_to_hash


def check_num(p_input_string: str, p_num: int, p_stretch: bool = False) -> bool:
    try:
        triple_chars = search(r"(.)\1{2}", get_hash(f"{p_input_string}{p_num}", p_stretch)).group()
        target_chars = triple_chars[0]
    except AttributeError:
        return False
    for next_num in range(1000):
        if target_chars in findall(r"(.)\1{4}", get_hash(f"{p_input_string}{p_num + next_num + 1}", p_stretch)):
            return True
    return False


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = -1
    input_str = next(yield_input_data(p_input_file_path, p_whole_row=True), None)

    find_counter = 0
    while find_counter < 64:
        answer1 += 1
        if check_num(input_str, answer1):
            find_counter += 1

    find_counter = 0
    while find_counter < 64:
        answer2 += 1
        if check_num(input_str, answer2, True):
            find_counter += 1

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 14, solve_puzzle)


if __name__ == '__main__':
    main()
