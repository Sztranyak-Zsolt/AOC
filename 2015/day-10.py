from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def gen_look_and_say(p_word: str) -> str:
    word_counter = 1
    act_letter = p_word[0]
    new_word = ''
    for new_letter in p_word[1:]:
        if new_letter != act_letter:
            new_word += f"{word_counter}{act_letter}"
            word_counter = 1
        else:
            word_counter += 1
        act_letter = new_letter
    new_word += f"{word_counter}{act_letter}"
    return new_word


def solve_puzzle(p_input_file_path: str) -> (int, int):
    answer1 = None
    act_input = next(yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False), None)
    for i in range(50):
        act_input = gen_look_and_say(act_input)
        if i == 39:
            answer1 = len(act_input)
    answer2 = len(act_input)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 10, solve_puzzle)


if __name__ == '__main__':
    main()
