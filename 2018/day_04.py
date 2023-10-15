from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from datetime import datetime, timedelta
from collections import Counter


class CShift:
    def __init__(self, p_start_date: datetime):
        self.start_date: datetime = p_start_date
        self.end_date: datetime | None = None
        self.sleep_list: list[list[datetime, datetime | None]] = list()

    @property
    def all_sleep_time_in_minutes(self) -> int:
        act_delta = 0
        for st_t, end_t in self.sleep_list:
            act_delta += int((end_t - st_t).total_seconds()) // 60
        return act_delta

    @property
    def sleep_minutes_list(self) -> list[int]:
        rd = []
        for act_sleep in self.sleep_list:
            act_min = 0
            while act_sleep[0] + timedelta(minutes=act_min) < act_sleep[1]:
                rd.append(int((act_sleep[0] + timedelta(minutes=act_min)).strftime('%M')))
                act_min += 1
        return rd


class CGuard:
    def __init__(self, p_id: int):
        self.id = p_id
        self.shift_list: list[CShift] = list()

    @property
    def all_sleep_time_in_minutes(self) -> int:
        sum_sleep = 0
        for shift in self.shift_list:
            sum_sleep += shift.all_sleep_time_in_minutes
        return sum([s.all_sleep_time_in_minutes for s in self.shift_list])

    @property
    def most_frequent_sleep_minute(self) -> int:
        return self.sleep_minutes_counter.most_common(1)[0][0]

    @property
    def most_frequent_sleep_minute_frequency(self) -> int:
        return self.sleep_minutes_counter.most_common(1)[0][1]

    @property
    def sleep_minutes_counter(self) -> Counter:
        s_c = Counter()
        for d_act_shift in self.shift_list:
            s_c.update(d_act_shift.sleep_minutes_list)
        return s_c

    def __gt__(self, other: CGuard):
        return other.all_sleep_time_in_minutes < self.all_sleep_time_in_minutes


class CGuardHandler:
    def __init__(self):
        self.guard_dict: dict[int, CGuard] = {}

    def get_guard(self, p_guard_id: int) -> CGuard:
        if p_guard_id not in self.guard_dict:
            self.guard_dict[p_guard_id] = CGuard(p_guard_id)
        return self.guard_dict[p_guard_id]


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = None
    act_guard: CGuard | None = None
    gh = CGuardHandler()

    for shift_date, shift_time, *info_list in sorted(yield_input_data(p_input_file_path, p_chars_to_space="#[]")):
        act_time = datetime.strptime(shift_date + " " + shift_time, '%Y-%m-%d %H:%M')
        if info_list[0] == 'Guard':
            if act_guard is not None:
                act_guard.shift_list[-1].end_date = act_time
            act_guard = gh.get_guard(info_list[1])
            gh.get_guard(info_list[1]).shift_list.append(CShift(act_time))
        elif info_list[0] == 'falls':
            act_guard.shift_list[-1].sleep_list.append([act_time, None])
        elif info_list[0] == 'wakes':
            act_guard.shift_list[-1].sleep_list[-1][1] = act_time

    longest_sleep = 0
    most_frequent_sleep = 0
    for act_guard in gh.guard_dict.values():
        if act_guard.all_sleep_time_in_minutes > longest_sleep:
            answer1 = act_guard.id * act_guard.most_frequent_sleep_minute
            longest_sleep = act_guard.all_sleep_time_in_minutes

        if act_guard.sleep_minutes_counter \
                and act_guard.most_frequent_sleep_minute_frequency > most_frequent_sleep:
            answer2 = act_guard.id * act_guard.most_frequent_sleep_minute
            most_frequent_sleep = act_guard.most_frequent_sleep_minute_frequency
    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 4, solve_puzzle)


if __name__ == '__main__':
    main()
