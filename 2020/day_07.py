from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CLuggage:
    def __init__(self, p_color: str):
        self.color = p_color
        self.contains: dict[CLuggage, int] = dict()

    @property
    def have_shiny_bag(self) -> bool:
        for cl in self.contains:
            if cl.color == 'shiny gold' or cl.have_shiny_bag:
                return True
        return False

    @property
    def count_all_containing_bags(self) -> int:
        rv = 0
        for b in self.contains:
            rv += self.contains[b] * (1 + b.count_all_containing_bags)
        return rv


class CLuggageHandler:
    def __init__(self):
        self.luggage_dict: dict[str, CLuggage] = {}

    def get_luggage(self, p_color: str) -> CLuggage:
        if p_color not in self.luggage_dict:
            self.luggage_dict[p_color] = CLuggage(p_color)
        return self.luggage_dict[p_color]


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    lh = CLuggageHandler()
    for act_list in yield_input_data(p_input_file_path, p_chars_to_space='.,'):
        act_luggage = lh.get_luggage(f'{act_list[0]} {act_list[1]}')
        if act_list[-3:] == ['no', 'other', 'bags']:
            continue
        for cl in range(1, len(act_list) // 4):
            containing_luggage = lh.get_luggage(f'{act_list[1 + cl * 4]} {act_list[2 + cl * 4]}')
            act_luggage.contains[containing_luggage] = act_list[0 + cl * 4]

    answer1 = len(['x' for lg in lh.luggage_dict.values() if lg.have_shiny_bag])
    answer2 = lh.luggage_dict['shiny gold'].count_all_containing_bags

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 7, solve_puzzle)


if __name__ == '__main__':
    main()
