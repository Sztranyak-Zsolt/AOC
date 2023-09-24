from __future__ import annotations
from typing import Callable
import time
import aocd  # pip install advent-of-code-data
from os import path, mkdir

solution_func = Callable[[str], tuple[int | str, int | str | None]]


def aoc_solve_puzzle(p_year: int, p_day: int, p_solution_func: solution_func):
    if not path.isdir('input'):
        mkdir('input')
    input_file_name = f'input/input_{p_year}{p_day:02}.txt'
    if not path.isfile(input_file_name):
        try:
            aocd_input = aocd.get_data(year=p_year, day=p_day)
        except:
            print(f"Can't download AOC input, you can add it manually into {input_file_name}.")
            raise
        with open(input_file_name, mode='w') as f:
            f.write(aocd_input)
    start_time = time.perf_counter()
    solution1, solution2 = p_solution_func(input_file_name)
    finish_time = time.perf_counter()
    print(f"Advent of Code {p_year} - Day {p_day}")
    print(f"https://adventofcode.com/{p_year}/day/{p_day}")
    print(f"Answer1: {solution1}")
    if solution2 is not None:
        print(f"Answer2: {solution2}")
    print(f"Execution time: {finish_time - start_time:0.4f} seconds")


def try_to_int(p_str: str) -> int | str:
    try:
        return int(p_str)
    except ValueError:
        return p_str


def yield_input_data(p_file_name: str,
                     p_whole_row: bool = False,
                     p_only_nums: bool = False,
                     p_convert_to_num: bool = True,
                     p_chars_to_space: str = '',
                     p_group_separator: str | None = None):

    def return_conv_item(p_item: str) -> int | str | None:
        if not p_convert_to_num:
            return p_item
        conv_item = try_to_int(p_item)
        if not p_only_nums or isinstance(conv_item, int):
            return conv_item

    def yield_data_inner(p_raw_data_inner: str):
        for p_raw_data_inner_line in p_raw_data_inner.split('\n'):
            if p_whole_row:
                yield return_conv_item(p_raw_data_inner_line)
            else:
                d_row_list = list()
                for p_raw_item in p_raw_data_inner_line.split():
                    d_row_list.append(return_conv_item(p_raw_item))
                yield d_row_list

    with open(p_file_name) as f:
        d_raw_data = f.read()
    for char_to_space in p_chars_to_space:
        d_raw_data = d_raw_data.replace(char_to_space, ' ')
    if p_group_separator is None:
        for inner_yield in yield_data_inner(d_raw_data):
            yield inner_yield
        return
    for d_raw_data_group in d_raw_data.split(p_group_separator):
        yield list(yield_data_inner(d_raw_data_group))


def main():
    pass


if __name__ == '__main__':
    main()
