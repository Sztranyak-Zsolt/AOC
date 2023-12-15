from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from collections import defaultdict


def calc_hash(p_str: str) -> int:
    rv = 0
    for s in p_str:
        rv = (rv + ord(s)) * 17 % 256
    return rv


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    input_single_row = next(yield_input_data(p_input_file_path, p_whole_row=True))
    boxes = defaultdict(lambda: {})
    for ir in input_single_row.split(','):
        answer1 += calc_hash(ir)
        if ir[-1] == '-':
            act_label = ir[:-1]
            act_box = calc_hash(act_label)
            if act_label in boxes[act_box]:
                del boxes[act_box][act_label]
        else:
            act_label, val = ir.split('=')
            act_box = calc_hash(act_label)
            boxes[act_box][act_label] = int(val)

    for box_num, present_dict in boxes.items():
        for i, present_value in enumerate(present_dict.values(), start=1):
            answer2 += (box_num + 1) * i * present_value

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 15, solve_puzzle)


if __name__ == '__main__':
    main()
