import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from fractions import Fraction


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    for inp_group in yield_input_data(p_input_file_path, p_chars_to_space='=+:,', p_group_separator='\n\n'):
        # constrains: variables are positive integers
        _, _, _, a_x_plus, _, a_y_plus = inp_group[0]
        _, _, _, b_x_plus, _, b_y_plus = inp_group[1]
        _, _, prize_x, _, prize_y = inp_group[2]

        try:
            b_push = (prize_y - prize_x * Fraction(a_y_plus) / a_x_plus) / \
                     (b_y_plus - b_x_plus * Fraction(a_y_plus) / a_x_plus)
            a_push = (prize_x - b_push * b_x_plus) / a_x_plus

            if b_push >= 0 and a_push >= 0 and a_push.denominator == 1 and b_push.denominator == 1:
                answer1 += 3 * int(a_push) + int(b_push)

        except ZeroDivisionError:
            cost1 = cost2 = None
            if prize_x % a_x_plus == 0 and prize_y == prize_x // a_x_plus * a_y_plus:
                cost1 = prize_x // a_x_plus * 3
            if prize_x % b_x_plus == 0 and prize_y == prize_x // b_x_plus * b_y_plus:
                cost2 = prize_x // b_x_plus
            if cost1 is not None and cost2 is not None:
                answer1 += min(cost1, cost2)
            elif cost1 is not None:
                answer1 += cost1
            elif cost2 is not None:
                answer1 += cost2

        prize_x += 10000000000000
        prize_y += 10000000000000

        try:
            b_push = (prize_y - prize_x * Fraction(a_y_plus) / a_x_plus) / \
                     (b_y_plus - b_x_plus * Fraction(a_y_plus) / a_x_plus)
            a_push = (prize_x - b_push * b_x_plus) / a_x_plus

            if b_push >= 0 and a_push >= 0 and a_push.denominator == 1 and b_push.denominator == 1:
                answer2 += 3 * int(a_push) + int(b_push)

        except ZeroDivisionError:
            cost1 = cost2 = None
            if prize_x % a_x_plus == 0 and prize_y == prize_x // a_x_plus * a_y_plus:
                cost1 = prize_x // a_x_plus * 3
            if prize_x % b_x_plus == 0 and prize_y == prize_x // b_x_plus * b_y_plus:
                cost2 = prize_x // b_x_plus
            if cost1 is not None and cost2 is not None:
                answer2 += min(cost1, cost2)
            elif cost1 is not None:
                answer2 += cost1
            elif cost2 is not None:
                answer2 += cost2

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 13, solve_puzzle)


if __name__ == '__main__':
    main()
