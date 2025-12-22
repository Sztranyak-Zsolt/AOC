import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from string import ascii_uppercase
from heapq import heapify, heappop, heappush
from itertools import combinations


class CStep:
    def __init__(self, p_id: str):
        self.id = p_id
        self.prev_steps: set[CStep] = set()
        self.cost = 60 + ascii_uppercase.find(p_id) + 1

    def __lt__(self, other):
        return self.id < other.id

    def __str__(self):
        return self.id


def gen_cache_code(p_time: int, p_used_step: set[CStep], p_current_step: list[tuple[CStep, int]]):
    return f'{p_time}{"".join(sorted([s.id for s in p_used_step]))}' \
           f'{"".join(sorted([cs[0].id + str(cs[1]) for cs in p_current_step]))}'


class CStepManager:
    def __init__(self):
        self.step_dict: dict[str, CStep] = dict()

    def get_step(self, p_step_key) -> CStep:
        if p_step_key not in self.step_dict:
            self.step_dict[p_step_key] = CStep(p_step_key)
        return self.step_dict[p_step_key]

    def next_steps_list(self, p_finished_steps: set[CStep], p_used_steps: set[CStep]) -> list[CStep]:
        rl = []
        for ns in self.step_dict.values():
            if ns in p_used_steps:
                continue
            if not ns.prev_steps - p_finished_steps:
                rl.append(ns)
        return rl

    @property
    def step_order1(self) -> str:
        rv = ''
        unused_steps = set(self.step_dict.values())
        used_steps = set()
        while unused_steps:
            next_step = min(self.next_steps_list(used_steps, used_steps))
            rv += next_step.id
            unused_steps.remove(next_step)
            used_steps.add(next_step)
        return rv

    def step_order2(self, p_worker_count: int) -> int:

        step_heap = [[0, set(), []]]
        heapify(step_heap)
        all_steps = set(self.step_dict.values())
        known_step_cache = set()

        while True:
            act_time, used_steps, current_step_list = heappop(step_heap)
            if all_steps - used_steps == set() and current_step_list == []:
                return act_time

            next_steps_list = self.next_steps_list(used_steps - set([v[0] for v in current_step_list]), used_steps)

            # case 1 - no current step and all next steps can be taken at once
            if not current_step_list and len(next_steps_list) <= p_worker_count:
                new_steps = {min(next_steps_list)}
                next_time = min(next_steps_list).cost
                for ns in sorted(next_steps_list):
                    new_steps = new_steps | {ns}
                    new_cur_step_list = [(s, s.cost - next_time) for s in new_steps if s.cost != next_time]
                    if (ch_c := gen_cache_code(act_time + next_time, used_steps | new_steps, new_cur_step_list)) \
                            in known_step_cache:
                        continue
                    known_step_cache.add(ch_c)
                    heappush(step_heap, [act_time + next_time, used_steps | new_steps, new_cur_step_list])
                continue

            # case 2 - there are some current steps, and we will wait for the finish of the next one
            if current_step_list:
                next_time = min([v[1] for v in current_step_list])
                next_cur_step_list = [(v[0], v[1] - next_time) for v in current_step_list if v[1] != next_time]

                if (ch_c := gen_cache_code(act_time + next_time, used_steps, next_cur_step_list)) in known_step_cache:
                    continue
                known_step_cache.add(ch_c)
                heappush(step_heap, [act_time + next_time, used_steps, next_cur_step_list])

            # case 3 - otherwise choose a next steps to be taken
            for next_steps_to_take in combinations(next_steps_list +
                                                   [None] * (p_worker_count - len(current_step_list)),
                                                   p_worker_count - len(current_step_list)):
                if not (new_steps := [v for v in next_steps_to_take if v]):
                    continue
                if not current_step_list:
                    next_step_list_act = [(v, v.cost) for v in new_steps]
                else:
                    next_step_list_act = current_step_list + [(v, v.cost) for v in new_steps]
                next_time = min([v[1] for v in next_step_list_act])
                next_cur_step_list = [(v[0], v[1] - next_time) for v in next_step_list_act if v[1] != next_time]
                next_used_steps = used_steps | set(new_steps)

                if (ch_c := gen_cache_code(act_time + next_time, next_used_steps, next_cur_step_list)) \
                        in known_step_cache:
                    continue
                known_step_cache.add(ch_c)

                heappush(step_heap, [act_time + next_time, next_used_steps, next_cur_step_list])


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    sm = CStepManager()

    for _, step1, *_, step2, _, _ in yield_input_data(p_input_file_path):
        sm.get_step(step2).prev_steps.add(sm.get_step(step1))

    answer1 = sm.step_order1
    answer2 = sm.step_order2(5)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 7, solve_puzzle)


if __name__ == '__main__':
    main()
