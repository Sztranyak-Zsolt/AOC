import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


class CPairHandler:
    def __init__(self, p_init_str: str):
        self.pair_counter: dict[str, int] = {}
        self.letter_counter: dict[str, int] = {}
        self.init_str = p_init_str
        self.conversion_dict: dict[str, str] = {}

    @property
    def init_str(self):
        return self._init_str

    @init_str.setter
    def init_str(self, p_init_str):
        self._init_str = p_init_str
        self.pair_counter.clear()
        self.letter_counter.clear()
        if len(p_init_str) in [0, 1]:
            return
        prev_letter = p_init_str[0]
        self.letter_counter[prev_letter] = self.letter_counter.get(prev_letter, 0) + 1
        for act_letter in p_init_str[1:]:
            self.pair_counter[prev_letter + act_letter] = self.pair_counter.get(prev_letter + act_letter, 0) + 1
            self.letter_counter[act_letter] = self.letter_counter.get(act_letter, 0) + 1
            prev_letter = act_letter

    def evolve(self):
        next_pair_counter: dict[str, int] = {}
        for act_pair, act_pair_counter in self.pair_counter.items():
            new_letter = self.conversion_dict[act_pair]
            self.letter_counter[new_letter] = self.letter_counter.get(new_letter, 0) + act_pair_counter
            next_pair_counter[act_pair[0] + new_letter] = \
                next_pair_counter.get(act_pair[0] + new_letter, 0) + act_pair_counter
            next_pair_counter[new_letter + act_pair[1]] = \
                next_pair_counter.get(new_letter + act_pair[1], 0) + act_pair_counter
        self.pair_counter = next_pair_counter

    @property
    def letter_count_range(self):
        return max(self.letter_counter.values()) - min(self.letter_counter.values())


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = None
    input_group_iter = iter(yield_input_data(p_input_file_path, p_group_separator='\n\n', p_chars_to_space='->'))
    ch = CPairHandler(next(input_group_iter)[0][0])
    for p1, p2 in next(input_group_iter):
        ch.conversion_dict[p1] = p2
    for i in range(1, 41):
        ch.evolve()
        if i == 10:
            answer1 = ch.letter_count_range
        elif i == 40:
            answer2 = ch.letter_count_range

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 14, solve_puzzle)


if __name__ == '__main__':
    main()
