import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from functools import cache


@cache
def word_chain3() -> set[str]:
    p_restricted_letters = 'ilo'
    letters = 'abcdefghijklmnopqrstuvwxyzab'
    rs = set()
    for i in range(len(letters) - 2):
        act_chain = letters[i:i+3]
        if set(act_chain) & set(p_restricted_letters):
            continue
        rs.add(act_chain)
    return rs


@cache
def next_char_dict() -> dict[str, str]:
    p_restricted_letters = 'ilo'
    rd = dict()
    letters = 'abcdefghijklmnopqrstuvwxyz'
    for act_letter in letters:
        act_index = letters.index(act_letter) + 1
        while (letters * 2)[act_index] in p_restricted_letters:
            act_index += 1
        rd[act_letter] = (letters * 2)[act_index]
    return rd


def calc_next_word(p_word: str) -> str:
    p_word_list_rev = list(p_word)[::-1]
    for i in range(len(p_word_list_rev)):
        act_char = p_word_list_rev[i]
        next_char = next_char_dict()[p_word_list_rev[i]]
        p_word_list_rev[i] = next_char
        if act_char < next_char:
            return ''.join(p_word_list_rev[::-1])
    return next_char_dict()['z'] * len(p_word)


def is_valid_word(p_word: str) -> bool:
    double_counter = 0
    has_inc3_letter = False
    prev_letter = ''
    act_chain = '__'
    for act_letter in p_word:
        if act_letter == prev_letter:
            double_counter += 1
            prev_letter = ''
        else:
            prev_letter = act_letter
        if act_chain + act_letter in word_chain3():
            w = act_chain + act_letter
            if list(w) == sorted(list(w)):
                has_inc3_letter = True
        act_chain = act_chain[1:] + act_letter
    return has_inc3_letter and double_counter >= 2


def calc_next_valid_word(p_word: str) -> str:
    act_word = p_word
    while True:
        act_word = calc_next_word(act_word)
        if is_valid_word(act_word):
            return act_word


def solve_puzzle(p_input_file_path: str) -> tuple[int, int]:
    act_input = next(yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False), None)
    answer1 = calc_next_valid_word(act_input)
    answer2 = calc_next_valid_word(answer1)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 11, solve_puzzle)


if __name__ == '__main__':
    main()
