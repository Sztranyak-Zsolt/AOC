from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from collections import Counter, defaultdict


def calc_fish(p_fish_init_timer: dict, p_after_day: int) -> dict:
    act_dict = p_fish_init_timer
    for e in range(p_after_day):
        new_dict = defaultdict(lambda: 0)
        for k, v in act_dict.items():
            if k == '0':
                new_dict['6'] += v
                new_dict['8'] = v
            else:
                new_dict[str(int(k) - 1)] += v
        act_dict = new_dict
    return act_dict


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    input_iterator = iter(yield_input_data(p_input_file_path, p_chars_to_space=','))
    input_single_row = next(input_iterator)
    fish_timer_counter = Counter(input_single_row)

    answer1 = sum([x for x in calc_fish(fish_timer_counter, 80).values()])
    answer2 = sum([x for x in calc_fish(fish_timer_counter, 256).values()])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 6, solve_puzzle)


if __name__ == '__main__':
    main()
