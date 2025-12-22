import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def get_breakpoint(p_race_time: int, p_act_record: int) -> int | None:
    act_start = 0
    act_end = p_race_time // 2
    if act_end * (p_race_time - act_end) <= p_act_record:
        return None
    while act_start + 1 != act_end:
        act_mid = (act_start + act_end) // 2
        act_distance = act_mid * (p_race_time - act_mid)
        if act_distance > p_act_record:
            act_end = act_mid
            continue
        act_start = act_mid
    return act_end


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = 1

    input_iterator = iter(yield_input_data(p_input_file_path))
    race_time_list = next(input_iterator)[1:]
    race_record_list = next(input_iterator)[1:]

    for act_race_time, act_race_record in zip(race_time_list, race_record_list):
        if get_breakpoint(act_race_time, act_race_record):
            answer1 *= act_race_time - 2 * get_breakpoint(act_race_time, act_race_record) + 1

    input_iterator = iter(yield_input_data(p_input_file_path, p_whole_row=True))
    race_time_total = int(next(input_iterator).split(':')[1].replace(' ', ''))
    race_record_total = int(next(input_iterator).split(':')[1].replace(' ', ''))

    answer2 = race_time_total - get_breakpoint(race_time_total, race_record_total) * 2 + 1

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 6, solve_puzzle)


if __name__ == '__main__':
    main()
