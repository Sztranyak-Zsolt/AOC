from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def calc_key_loop_size(p_public_key: int, p_mod_num: int, p_subject_number: int = 7) -> int:
    act_value = 1
    counter = 0
    while True:
        if p_public_key == act_value:
            return counter
        counter += 1
        act_value = (act_value * p_subject_number) % p_mod_num


def encrypt_key(p_public_key: int, p_mod_num: int, p_loop_size: int) -> int:
    rv = 1
    for _ in range(p_loop_size):
        rv = (rv * p_public_key) % p_mod_num
    return rv


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    input_iterator = iter(yield_input_data(p_input_file_path, p_whole_row=True))
    card_public_key, door_public_key = next(input_iterator), next(input_iterator)
    mod_num = 20201227
    card_loop = calc_key_loop_size(card_public_key, mod_num)
    answer1 = encrypt_key(door_public_key, mod_num, card_loop)

    return answer1, None


def main():
    aoc_solve_puzzle(2020, 25, solve_puzzle)


if __name__ == '__main__':
    main()
