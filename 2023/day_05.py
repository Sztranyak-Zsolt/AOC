from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from collections import namedtuple


TPeriod = namedtuple('TPeriod', ['period_from', 'period_to'])


def convert_id(p_id: TPeriod | int, p_map: dict[TPeriod, int]) -> list[TPeriod] | int:
    new_ids_range = []
    if isinstance(p_id, int):
        act_id = period_to = p_id
    else:
        act_id = p_id.period_from
        period_to = p_id.period_to
    for source_period, id_change in sorted(p_map.items()):
        if act_id < source_period.period_from:
            if period_to < source_period.period_from:
                if isinstance(p_id, int):
                    return p_id
                new_ids_range.append(TPeriod(act_id, period_to))
                return new_ids_range
            new_ids_range.append(TPeriod(act_id, source_period.period_from - 1))
            act_id = source_period.period_from
        if source_period.period_from <= act_id <= source_period.period_to:
            if period_to <= source_period.period_to:
                if isinstance(p_id, int):
                    return p_id + id_change
                new_ids_range.append(TPeriod(act_id + id_change, period_to + id_change))
                return new_ids_range
            new_ids_range.append(TPeriod(act_id + id_change, source_period.period_to + id_change))
            act_id = source_period.period_to + 1
    if isinstance(p_id, int):
        return p_id
    new_ids_range.append(TPeriod(act_id, period_to))
    return new_ids_range


def merge_periods(p_period_list: list[TPeriod]) -> list[TPeriod]:
    act_periods = []
    for act_period in sorted([p for p in p_period_list if p is not None]):
        if not act_periods or act_periods[-1].period_to < act_period.period_from - 1:
            act_periods.append(TPeriod(act_period.period_from, act_period.period_to))
            continue
        act_periods[-1] = TPeriod(act_periods[-1].period_from, max(act_periods[-1].period_to, act_period.period_to))
    return act_periods


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    info_dict = {}
    for i1, act_group in enumerate(yield_input_data(p_input_file_path, p_group_separator='\n\n')):
        if i1 == 0:
            info_dict['seeds'] = act_group[0][1:]
            continue
        info_dict[act_group_id := act_group[0][0]] = {}
        for act_line in act_group[1:]:
            info_dict[act_group_id][TPeriod(act_line[1], act_line[1] + act_line[2] - 1)] = act_line[0] - act_line[1]

    act_ids = info_dict['seeds']
    act_ids_range = [TPeriod(n1, n1 + n2 - 1) for n1, n2 in zip(info_dict['seeds'][::2], info_dict['seeds'][1::2])]
    for act_converter in ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light',
                          'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']:
        act_mapping = info_dict[act_converter]
        act_ids = [convert_id(act_id, act_mapping) for act_id in act_ids]
        new_ids_range = []
        for act_id_range in act_ids_range:
            new_ids_range += convert_id(act_id_range, act_mapping)
        act_ids_range = merge_periods(new_ids_range)
    answer1 = min(act_ids)
    answer2 = min([act_id_range.period_from for act_id_range in act_ids_range])
    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 5, solve_puzzle)


if __name__ == '__main__':
    main()
