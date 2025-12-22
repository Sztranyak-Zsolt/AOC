import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_link_decoder import CCodeDecode


class CAllergyManager:
    def __init__(self):
        self.food_list: list[list[tuple[str], tuple[str]]] = []
        self.ingredient_dict: dict[str, set[str]] = {}
        self.allergy_dict: dict[str, set[str]] = {}
        self.decoder = CCodeDecode()

    def add_food(self, p_food_list_raw: list[str]):
        ingredient_list: list[str] = []
        allergy_list: list[str] = []
        act_list = ingredient_list
        for act_item in p_food_list_raw:
            if act_item == 'contains':
                act_list = allergy_list
                continue
            act_list.append(act_item)
        self.food_list.append([tuple(ingredient_list), tuple(allergy_list)])
        for act_all in allergy_list:
            self.decoder.add_code_link(act_all, ingredient_list)

    @property
    def count_non_allergic_ingredients(self) -> int:
        rv = 0
        non_allergic_ingredient_set = {k for k, v in self.decoder.get_decode_mapping.items() if v is None}
        for act_ingredients, act_allergies in self.food_list:
            rv += len(['x' for act_ing in act_ingredients if act_ing in non_allergic_ingredient_set])
        return rv

    @property
    def canonical_dangerous_ingredient(self) -> str:
        rl = []
        for act_ing, act_allergy in sorted([(ing, allergy) for ing, allergy in self.decoder.get_decode_mapping.items()
                                            if allergy is not None], key=lambda x: x[1]):
            rl.append(act_ing)
        return ','.join(rl)


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    am = CAllergyManager()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space='(),'):
        am.add_food(inp_row)

    answer1 = am.count_non_allergic_ingredients
    answer2 = am.canonical_dangerous_ingredient
    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 21, solve_puzzle)


if __name__ == '__main__':
    main()
