from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from collections import defaultdict
from typing import Iterator


def evolve_num(p_num: int) -> Iterator[int]:
    if p_num == 0:
        yield 1
        return
    vs = str(p_num)
    if len(vs) % 2 == 0:
        yield int(vs[:len(vs)//2])
        yield int(vs[len(vs)//2:])
        return
    yield p_num * 2024


def evolve_counter(p_counter_dict: dict[int, int]) -> dict[int, int]:
    new_dict = defaultdict(lambda: 0)
    for k, v in p_counter_dict.items():
        for next_num in evolve_num(k):
            new_dict[next_num] += v
    return new_dict


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = 0
    input_iterator = iter(yield_input_data(p_input_file_path, p_whole_row=False))
    input_single_row = next(input_iterator)

    stone_dict = defaultdict(lambda: 0)
    for n in input_single_row:
        stone_dict[n] += 1

    for i in range(75):
        stone_dict = evolve_counter(stone_dict)
        if i == 24:
            answer1 = sum(stone_dict.values())
    answer2 = sum(stone_dict.values())

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 11, solve_puzzle)


if __name__ == '__main__':
    main()
