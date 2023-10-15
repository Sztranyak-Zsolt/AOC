from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from collections import Counter


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    answer2 = None
    rows_with_2 = rows_with_3 = 0
    word_set = set()

    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        char_counter = Counter(inp_row)
        if 2 in char_counter.values():
            rows_with_2 += 1
        if 3 in char_counter.values():
            rows_with_3 += 1
        if answer2 is None:
            for i in range(len(inp_row)):
                new_word = inp_row[:i + 1] + "_" + inp_row[i + 2:]
                if new_word in word_set:
                    answer2 = inp_row[:i + 1] + inp_row[i + 2:]
                    break
                word_set.add(new_word)
    answer1 = rows_with_2 * rows_with_3

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 2, solve_puzzle)


if __name__ == '__main__':
    main()
