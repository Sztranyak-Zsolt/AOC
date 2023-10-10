from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from typing import Iterator


def generate_number(p_starting_value: int, p_factor: int, p_dividend: int, p_div_filter: int = 1) -> Iterator[int]:
    act_value = p_starting_value
    while True:
        act_value = act_value * p_factor % p_dividend
        if p_div_filter == 1 or act_value % p_div_filter == 0:
            yield act_value


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    bit_mask = 2 ** 16 - 1

    input_iter = iter(yield_input_data(p_input_file_path))
    input_num1, input_num2 = next(input_iter)[-1], next(input_iter)[-1]

    gen1_iter = generate_number(input_num1, 16807, 2147483647)
    gen2_iter = generate_number(input_num2, 48271, 2147483647)

    for _ in range(40000000):
        if next(gen1_iter) & bit_mask == next(gen2_iter) & bit_mask:
            answer1 += 1

    gen1_iter = generate_number(input_num1, 16807, 2147483647, 4)
    gen2_iter = generate_number(input_num2, 48271, 2147483647, 8)

    for _ in range(5000000):
        if next(gen1_iter) & bit_mask == next(gen2_iter) & bit_mask:
            answer2 += 1

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 15, solve_puzzle)


if __name__ == '__main__':
    main()
