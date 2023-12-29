from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
# from GENERICS.aoc_grid import CGridBase
# from GENERICS.aoc_vector import Position2D, CVector2D, add_positions, neighbor_positions, mh_distance
# from collections import deque, Counter, defaultdict, namedtuple
# from itertools import product, permutations, combinations, combinations_with_replacement
# from functools import cache, cached_property
# from math import prod, lcm, gcd
# from heapq import heapify, heappop, heappush


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    # input_iterator = iter(yield_input_data(p_input_file_path, p_whole_row=True))
    # input_single_row = next(input_iterator)
    for inp_row in yield_input_data(p_input_file_path,
                                    p_whole_row=False,
                                    p_chars_to_space=''
                                    ):
        print(inp_row)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 0, solve_puzzle)


if __name__ == '__main__':
    main()
