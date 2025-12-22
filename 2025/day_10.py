import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
import z3


class CLights:
    def __init__(self):
        self.target: tuple[bool] = tuple()
        self.button_presses: list[tuple[bool]] = []
        self.joltage_list: tuple[int] = tuple()

    def add_button(self, button_list: tuple[int]):
        new_press = [False] * len(self.target)
        for b_num in button_list:
            new_press[b_num] = True
        self.button_presses.append(tuple(new_press))

    def calc_min_press_need(self):
        act_lights_list = [(False, ) * len(self.target)]
        act_press = 0
        visited = set(tuple(act_lights_list[0]))
        while act_lights_list:
            act_press += 1
            next_lights_list = []
            for act_lights in act_lights_list:
                for toggle_list in self.button_presses:
                    next_lights = tuple(l ^ t for l, t in zip(act_lights, toggle_list))
                    if next_lights in visited:
                        continue
                    visited.add(next_lights)
                    if next_lights == self.target:
                        return act_press
                    next_lights_list.append(next_lights)
            act_lights_list = next_lights_list
        return -1
    
    def calc_min_press_need_with_joltage(self):
        o = z3.Optimize()
        vars = z3.Ints(f"x{i}" for i in range(len(self.button_presses)))
        for var in vars:
            o.add(var >= 0)
        for ji, joltage in enumerate(self.joltage_list):
            equation = 0
            for bi, button in enumerate(self.button_presses):
                if button[ji]:
                    equation += vars[bi]
            o.add(equation == joltage)
        o.minimize(sum(vars))
        o.check()
        return o.model().eval(sum(vars)).as_long()


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer2 = 0
    lights_list = []
    for target, *button_list, joltage in yield_input_data(p_input_file_path):
        new_light = CLights()
        new_light.target = tuple(t == '#' for t in target[1:-1])
        for act_press in button_list:
            new_light.add_button(tuple(map(int, act_press[1:-1].split(','))))
        new_light.numeric_target = tuple(map(int, joltage[1:-1].split(',')))
        new_light.joltage_list = list(map(int, joltage.replace('{', '').replace('}', '').split(',')))
        lights_list.append(new_light)
    answer1 = sum(l.calc_min_press_need() for l in lights_list)
    answer2 = sum(l.calc_min_press_need_with_joltage() for l in lights_list)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2025, 10, solve_puzzle)


if __name__ == '__main__':
    main()
