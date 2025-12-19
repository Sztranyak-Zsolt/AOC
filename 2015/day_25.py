import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


class CCodeGenerator:
    def __init__(self, p_iteration_counter: int):
        self.starting_number = 20151125
        self.multiplier = 252533
        self.divide_by = 33554393
        self.iteration_counter = p_iteration_counter

    def __iter__(self):
        self.n = 0
        self.act_number = self.starting_number
        return self

    def __next__(self):
        if self.n <= self.iteration_counter:
            result = self.act_number
            self.act_number = self.act_number * self.multiplier % self.divide_by
            self.n += 1
            return result
        else:
            raise StopIteration


def calc_rank(p_x: int, p_y: int) -> int:
    diagonal = p_x + p_y - 1
    diagonal_start = sum(range(diagonal))
    return diagonal_start + p_y - 1


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    *_, manual_row, _, manual_column = next(yield_input_data(p_input_file_path, p_chars_to_space='.,'), None)
    answer1 = list(CCodeGenerator(calc_rank(manual_row, manual_column)))[-1]
    return answer1, None


def main():
    aoc_solve_puzzle(2015, 25, solve_puzzle)


if __name__ == '__main__':
    main()
