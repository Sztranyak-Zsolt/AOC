import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def calc_period_range_start(p_start_id: str, split_num: int) -> str:
    part_length = len(p_start_id) // split_num
    id_range_start = int(p_start_id[:part_length])
    for id_start_part in range(0, len(p_start_id), part_length):
        if p_start_id[id_start_part:id_start_part + part_length] == \
                p_start_id[id_start_part + part_length:id_start_part + 2 * part_length]:
            continue
        if p_start_id[id_start_part:id_start_part+part_length] < \
                p_start_id[id_start_part + part_length:id_start_part + 2 * part_length]:
            id_range_start += 1
        break
    return id_range_start
    

def calc_period_range_end(p_end_id: str, split_num: int) -> str:
    part_length = len(p_end_id) // split_num
    id_range_end = int(p_end_id[:part_length])
    for id_end_part in range(0, len(p_end_id) - 1, part_length):
        if p_end_id[id_end_part:id_end_part + part_length] == \
                p_end_id[id_end_part + part_length:id_end_part + 2 * part_length]:
            continue
        if p_end_id[id_end_part:id_end_part+part_length] > \
                p_end_id[id_end_part + part_length:id_end_part + 2 * part_length]:
            id_range_end -= 1
        break
    return id_range_end


def count_invalid_id_range(p_start_id: str, p_id_end: str) -> int:
    rv = 0
    for id_length in range(len(p_start_id), len(p_id_end) + 1):
        if id_length % 2:
            continue
        part_length = id_length // 2
        if id_length == len(p_start_id):
            id_range_start = calc_period_range_start(p_start_id, 2)
        else:
            id_range_start = int('1' + '0' * (part_length - 1))
        
        if id_length == len(p_id_end):
            id_range_end = calc_period_range_end(p_id_end, 2)
        else:
            id_range_end = int('9' * part_length)
        if id_range_end >= id_range_start:
            mp = int('1' + '0' * (part_length - 1) + '1')
            rv += (id_range_end + id_range_start) * (id_range_end - id_range_start + 1) // 2 * mp
    return rv


def count_invalid_id_range_all_split(p_start_id: str, p_end_id: str) -> int:
    rv = set()
    for id_length in range(len(p_start_id), len(p_end_id) + 1):
        for part_length in range(1, id_length):
            if id_length % part_length:
                continue
            split_num = id_length // part_length
            if id_length == len(p_start_id):
                id_range_start = calc_period_range_start(p_start_id, split_num)
            else:
                id_range_start = int('1' + '0' * (part_length - 1))
            if id_length == len(p_end_id):
                id_range_end = calc_period_range_end(p_end_id, split_num)
            else:
                id_range_end = int('9' * part_length)
            if id_range_end >= id_range_start:
                mp = int(('1' + '0' * (part_length - 1)) * (id_length // part_length - 1) + '1')
                rv |= {n * mp for n in range(id_range_start, id_range_end + 1)}
    return sum(rv)


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    input_iterator = yield_input_data(p_input_file_path, p_chars_to_space=',')
    id_ranges = next(input_iterator)
    for period_info in id_ranges:
        period_start, period_end = period_info.split('-')
        answer1 += count_invalid_id_range(period_start, period_end)
        answer2 += count_invalid_id_range_all_split(period_start, period_end)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2025, 2, solve_puzzle)


if __name__ == '__main__':
    main()
