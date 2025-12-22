from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


class CPotHandler:
    def __init__(self, p_state: str, p_mapping: dict[str, str], p_index: int = 0):
        self.mapping = p_mapping
        if '#' in p_state:
            self.index = p_index + p_state.index('#')
            self.state = p_state[p_state.index('#'):p_state.rindex('#')+1]
        else:
            self.state = p_state
            self.index = p_index

    @property
    def pot_value(self) -> int:
        return sum([i for i, c in enumerate(self.state, start=self.index) if c == '#'])

    @property
    def next_state(self) -> CPotHandler:
        next_state = ''
        prev_str = '....'
        for act_char in self.state + '....':
            next_state += self.mapping[prev_str + act_char]
            prev_str = prev_str[1:] + act_char
        return CPotHandler(next_state, self.mapping, self.index - 2)


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = None

    period = 50000000000
    mapping: dict[str, str] = {}
    init_state = ''

    for i, inp_row in enumerate(yield_input_data(p_input_file_path, p_group_separator='\n\n', p_chars_to_space='=>')):
        if i == 0:
            init_state = inp_row[0][-1]
            continue
        for m1, m2 in inp_row:
            mapping[m1] = m2
    ph = CPotHandler(init_state, mapping)

    generation = 1
    nph = ph.next_state
    while nph.state != ph.state:
        ph = nph
        nph = ph.next_state
        generation += 1
        if generation == 20:
            answer1 = nph.pot_value
    answer2 = ph.pot_value + (period - generation + 1) * (nph.pot_value - ph.pot_value)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 12, solve_puzzle)


if __name__ == '__main__':
    main()
