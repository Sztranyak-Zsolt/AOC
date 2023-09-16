from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
import re


def is_nice_word_base(p_word_to_check: str):
    has_three_vowels = (len(re.findall(r'[aeiou]', p_word_to_check)) >= 3)
    has_double_letter = (re.search(r'(.)\1', p_word_to_check) is not None)
    has_restricted_string = (re.search(r'(ab|cd|pq|xy)', p_word_to_check) is not None)
    return has_three_vowels and not has_restricted_string and has_double_letter


def is_nice_word_adv(p_word_to_check: str):
    has_two_pairs = (re.search(r'(.{2}).*\1', p_word_to_check) is not None)
    has_spec_repeat = (re.search(r'(.).\1', p_word_to_check) is not None)
    return has_two_pairs and has_spec_repeat


def solve_puzzle(p_input_file_path: str) -> (int, int):
    answer1 = answer2 = 0
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False):
        answer1 += is_nice_word_base(inp_row)
        answer2 += is_nice_word_adv(inp_row)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 5, solve_puzzle)


if __name__ == '__main__':
    main()
