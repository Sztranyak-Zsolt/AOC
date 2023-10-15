from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from string import ascii_lowercase, ascii_uppercase


def reduce_word(p_str: str, p_remove_set: set[str]) -> str:
    act_length = 0
    while act_length != len(p_str):
        act_length = len(p_str)
        for rc in p_remove_set:
            p_str = p_str.replace(rc, '')
    return p_str


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    reduction_set = set()
    for a1, a2 in zip(ascii_lowercase, ascii_uppercase):
        reduction_set.add(a1 + a2)
        reduction_set.add(a2 + a1)

    initial_word = next(yield_input_data(p_input_file_path, p_whole_row=True), None)

    answer1 = len(reduce_word(initial_word, reduction_set))

    answer2 = len(initial_word)
    for a1, a2 in zip(ascii_lowercase, ascii_uppercase):
        answer2 = min(answer2, len(reduce_word(initial_word.replace(a1, '').replace(a2, ''), reduction_set)))

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 5, solve_puzzle)


if __name__ == '__main__':
    main()
