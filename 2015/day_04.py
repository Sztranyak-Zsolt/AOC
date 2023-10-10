from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
import hashlib


def hash_num_lookup(p_input_string: str, p_hash_start_with: str) -> int:
    act_number_to_check = 0
    hash_to_check_length = len(p_hash_start_with)
    while True:
        act_number_to_check += 1
        string_to_hash = f'{p_input_string}{act_number_to_check}'
        if hashlib.md5(string_to_hash.encode()).hexdigest()[:hash_to_check_length] == p_hash_start_with:
            return act_number_to_check


def solve_puzzle(p_input_file_path: str) -> (int, int):
    input_single_row = next(yield_input_data(p_input_file_path, p_whole_row=True), None)
    answer1 = hash_num_lookup(input_single_row, '00000')
    answer2 = hash_num_lookup(input_single_row, '000000')
    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 4, solve_puzzle)


if __name__ == '__main__':
    main()
