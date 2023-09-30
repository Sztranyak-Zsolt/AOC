from __future__ import annotations
from GENERICS.aoc2 import aoc_solve_puzzle
from itertools import combinations
from collections import deque
from copy import copy
from functools import cached_property


class CFloors:
    def __init__(self):
        self.elevator_floor = 0
        self.max_floor = 3
        self.items: dict[tuple[str, str], int] = {('Pm', 'G'): 0, ('Pm', 'M'): 0, ('Co', 'G'): 1,
                                                  ('Cm', 'G'): 1, ('Ru', 'G'): 1, ('Pu', 'G'): 1,
                                                  ('Co', 'M'): 2, ('Cm', 'M'): 2, ('Ru', 'M'): 2,
                                                  ('Pu', 'M'): 2}

    @property
    def is_final_state(self):
        return min(self.items.values()) == self.max_floor

    @cached_property
    def state_code(self) -> str:
        return str(self.elevator_floor) + '|' + '|'.join([f'{k[0] + k[1]}:{v}' for k, v in self.items.items()])

    @property
    def invalid_state(self) -> bool:
        for chip_type, chip_floor in [(ck[0], cf) for ck, cf in self.items.items() if ck[1] == "M"]:
            if self.items[(chip_type, "G")] == chip_floor:
                continue
            if ['x' for gk, gf in self.items.items() if gf == chip_floor and gk[1] == "G"]:
                return True
        return False

    def elevator_grab_items(self):
        el_floor_items = [k for k, v in self.items.items() if v == self.elevator_floor]
        for act_item in el_floor_items:
            yield [act_item]
        if len(el_floor_items) >= 2:
            for act_items in combinations(el_floor_items, 2):
                yield [act_items[0], act_items[1]]

    def yield_next_valid_states(self):
        for grabbed_items in self.elevator_grab_items():
            for direction in [-1, 1]:
                if self.max_floor < self.elevator_floor + direction or self.elevator_floor + direction < 0:
                    continue
                new_floor = copy(self)
                new_floor.elevator_floor += direction
                new_floor.items[grabbed_items[0]] += direction
                if len(grabbed_items) == 2:
                    new_floor.items[grabbed_items[1]] += direction
                if not new_floor.invalid_state:
                    yield new_floor

    def __copy__(self) -> CFloors:
        copy_instance = CFloors()
        copy_instance.elevator_floor = self.elevator_floor
        copy_instance.items = self.items.copy()
        return copy_instance

    def __str__(self):
        return_lst = []
        for f in range(3, -1, -1):
            s = str(f) + '. '
            if self.elevator_floor == f:
                s += 'E - '
            else:
                s += '    '
            s += ' / '.join([k[0] + ' ' + k[1] for k, v in sorted(self.items.items()) if v == f])
            return_lst.append(s)
        return '\n'.join(return_lst)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = None
    # input is hardcoded into CFloor.items
    f = CFloors()
    tf = copy(f)
    tf.elevator_floor = 3
    for item in tf.items:
        tf.items[item] = 3
    act_floor_states = deque([[f, 0, False], [tf, 0, True]])
    known_floor_states = {(f.state_code, False): 0, (tf.state_code, True): 0}
    while act_floor_states:
        act_floor_state, act_step, reverse_dir = act_floor_states.popleft()
        for next_floor_state in act_floor_state.yield_next_valid_states():
            if (next_floor_state.state_code, reverse_dir) in known_floor_states:
                continue
            if (next_floor_state.state_code, not reverse_dir) in known_floor_states:
                answer1 = act_step + known_floor_states[(next_floor_state.state_code, not reverse_dir)] + 1
                break
            known_floor_states[(next_floor_state.state_code, reverse_dir)] = act_step + 1
            act_floor_states.append([next_floor_state, act_step + 1, reverse_dir])
        else:
            del act_floor_state
            continue
        break

    f = CFloors()
    f.items[('El', 'G')] = 0
    f.items[('El', 'M')] = 0
    f.items[('Di', 'G')] = 0
    f.items[('Di', 'M')] = 0
    tf = copy(f)
    tf.elevator_floor = 3
    for item in tf.items:
        tf.items[item] = 3
    act_floor_states = deque([[f, 0, False], [tf, 0, True]])
    known_floor_states = {(f.state_code, False): 0, (tf.state_code, True): 0}
    while act_floor_states:
        act_floor_state, act_step, reverse_dir = act_floor_states.popleft()
        for next_floor_state in act_floor_state.yield_next_valid_states():
            if (next_floor_state.state_code, reverse_dir) in known_floor_states:
                continue
            if (next_floor_state.state_code, not reverse_dir) in known_floor_states:
                answer2 = act_step + known_floor_states[(next_floor_state.state_code, not reverse_dir)] + 1
                break
            known_floor_states[(next_floor_state.state_code, reverse_dir)] = act_step + 1
            act_floor_states.append([next_floor_state, act_step + 1, reverse_dir])
        else:
            del act_floor_state
            continue
        break

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 11, solve_puzzle)


if __name__ == '__main__':
    main()
