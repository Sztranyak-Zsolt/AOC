from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CElement:
    def __init__(self, p_name: str):
        self.name = p_name
        self.input_list: list[tuple[int, CElement]] = list()
        self.output_quantity: int = 1

    def calc_ore_need(self, p_element_need: int = 1,
                      p_input_remainders: dict[CElement, int] | None = None) -> int:
        if p_input_remainders is None:
            p_input_remainders = {}
        conversion_needed, element_reminder = divmod(p_element_need, self.output_quantity)
        if element_reminder != 0:
            conversion_needed += 1
            p_input_remainders[self] = p_input_remainders.get(self, 0) + self.output_quantity - element_reminder

        rv_ore_need = 0
        for i_quality, i_element in self.input_list:
            if i_element.name == 'ORE':
                rv_ore_need += i_quality * conversion_needed
            else:
                if i_quality * conversion_needed <= p_input_remainders.get(i_element, 0):
                    p_input_remainders[i_element] = p_input_remainders.get(i_element, 0) - i_quality * conversion_needed
                else:
                    remainder_usage = p_input_remainders.get(i_element, 0)
                    p_input_remainders[i_element] = 0
                    act_need = i_quality * conversion_needed - remainder_usage
                    rv_ore_need += i_element.calc_ore_need(act_need, p_input_remainders)
        return rv_ore_need


class CElementHandler:
    def __init__(self):
        self.element_dict: dict[str, CElement] = {}

    def get_element(self, p_element_key: str) -> CElement:
        if p_element_key not in self.element_dict:
            self.element_dict[p_element_key] = CElement(p_element_key)
        return self.element_dict[p_element_key]


def calc_max_element_from_ore(p_ore_supply: int, p_target_element: CElement) -> int:

    low_range, low_ore_requirement = 1, p_target_element.calc_ore_need(1)
    if low_ore_requirement > p_ore_supply:
        return 0
    high_range, high_ore_requirement = 2, p_target_element.calc_ore_need(2)

    while not (low_ore_requirement <= p_ore_supply < high_ore_requirement and low_range + 1 == high_range):
        if high_ore_requirement <= p_ore_supply:
            low_range, low_ore_requirement = high_range, high_ore_requirement
            high_range, high_ore_requirement = low_range * 2, p_target_element.calc_ore_need(low_range * 2)
        else:
            avg_range = (low_range + high_range) // 2
            avg_ore_requirement = p_target_element.calc_ore_need(avg_range)
            if avg_ore_requirement <= p_ore_supply:
                low_range, low_ore_requirement = avg_range, avg_ore_requirement
            else:
                high_range, high_ore_requirement = avg_range, avg_ore_requirement
    return low_range


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    eh = CElementHandler()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space=',=>'):
        eh.get_element(inp_row[-1]).output_quantity = inp_row[-2]
        for input_quantity, input_element in zip(inp_row[:-2:2], inp_row[1:-2:2]):
            eh.get_element(inp_row[-1]).input_list.append((input_quantity, eh.get_element(input_element)))
    answer1 = eh.element_dict['FUEL'].calc_ore_need()
    answer2 = calc_max_element_from_ore(1000000000000, eh.element_dict['FUEL'])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 14, solve_puzzle)


if __name__ == '__main__':
    main()
