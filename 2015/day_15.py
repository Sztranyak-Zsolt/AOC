import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


class CIngredient:
    def __init__(self, p_name, p_capacity, p_durability, p_flavor, p_texture, p_calories):
        self.name = p_name
        self.capacity = p_capacity
        self.durability = p_durability
        self.flavor = p_flavor
        self.texture = p_texture
        self.calories = p_calories


def calc_cauldron_score(p_cauldron: dict[CIngredient, int], p_extra_item: None | CIngredient = None) -> int:
    if p_extra_item is None:
        capacity = durability = flavor = texture = 0
    else:
        capacity = p_extra_item.capacity
        durability = p_extra_item.durability
        flavor = p_extra_item.flavor
        texture = p_extra_item.texture
    for act_ing, act_count in p_cauldron.items():
        capacity += act_ing.capacity * act_count
        durability += act_ing.durability * act_count
        flavor += act_ing.flavor * act_count
        texture += act_ing.texture * act_count
    return capacity * durability * flavor * texture


class CIngredientHandler:
    def __init__(self):
        self.ingredient_list: list[CIngredient] = list()

    def calc_optimal_score(self, p_spoon_count: int) -> int:
        act_ing_dict = {ing: 1 for ing in self.ingredient_list}
        act_score = calc_cauldron_score(act_ing_dict)
        new_ing = self.ingredient_list[0]
        for _ in range(p_spoon_count - 4):
            for act_ing in self.ingredient_list:
                new_score = calc_cauldron_score(act_ing_dict, act_ing)
                if new_score > act_score:
                    new_ing = act_ing
                    act_score = new_score
            act_ing_dict[new_ing] += 1
        return act_score

    def calc_optimal_score_cal_limit(self, p_spoon_count: int) -> int:
        max_score = 0
        for ing4 in range(1, p_spoon_count - 2):
            if self.ingredient_list[3].calories * ing4 >= 500:
                break
            for ing3 in range(1, p_spoon_count - 1 - ing4):
                if self.ingredient_list[3].calories * ing4 + self.ingredient_list[2].calories * ing3 >= 500:
                    break
                for ing1 in range(1, p_spoon_count - ing4 - ing3):
                    if self.ingredient_list[0].calories * ing1 + self.ingredient_list[3].calories * ing4 \
                            + self.ingredient_list[2].calories * ing3 >= 500:
                        break
                    ing2 = p_spoon_count - ing1 - ing3 - ing4
                    if self.ingredient_list[0].calories * ing1 + self.ingredient_list[3].calories * ing4 \
                            + self.ingredient_list[1].calories * ing2 + self.ingredient_list[2].calories * ing3 == 500:
                        act_cauldron = {self.ingredient_list[0]: ing1,
                                        self.ingredient_list[1]: ing2,
                                        self.ingredient_list[2]: ing3,
                                        self.ingredient_list[3]: ing4}
                        max_score = max(max_score, calc_cauldron_score(act_cauldron))
        return max_score


def solve_puzzle(p_input_file_path: str) -> tuple[int, int]:
    teaspoon_count = 100
    ih = CIngredientHandler()
    for ing_name, _, ing_capacity, _, ing_durability, _, ing_flavor, _, ing_texture, _, ing_cal \
            in yield_input_data(p_input_file_path, p_chars_to_space=':,'):
        ih.ingredient_list.append(CIngredient(ing_name, ing_capacity, ing_durability, ing_flavor, ing_texture, ing_cal))
    answer1 = ih.calc_optimal_score(teaspoon_count)
    answer2 = ih.calc_optimal_score_cal_limit(teaspoon_count)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 15, solve_puzzle)


if __name__ == '__main__':
    main()
