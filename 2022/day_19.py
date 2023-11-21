from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from functools import cached_property


class CBlueprint:
    def __init__(self, p_id: int):
        self.id: int = p_id
        self.robot_cost: list[tuple[int, ...]] = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]

    @cached_property
    def max_robot_needed(self) -> list[int, int, int, int]:
        rd = [0, 0, 0, -1]
        for act_element_index in range(3):
            for v in self.robot_cost:
                rd[act_element_index] = max(rd[act_element_index], v[act_element_index])
        return rd

    def max_geode_production(self, p_counter: int, p_act_stock: list[int] | None = None,
                             p_act_robots: list[int] | None = None, p_next_robot_index: int = None) -> int:
        if p_act_stock is None:
            p_act_stock = [0, 0, 0, 0]
        if p_act_robots is None:
            p_act_robots = [1, 0, 0, 0]
        next_stock = [p_act_stock[0] + p_act_robots[0], p_act_stock[1] + p_act_robots[1],
                      p_act_stock[2] + p_act_robots[2], p_act_stock[3] + p_act_robots[3]]
        if p_counter == 1:
            return next_stock[3]
        if p_next_robot_index is not None:
            for i in range(3):
                if p_act_stock[i] < self.robot_cost[p_next_robot_index][i]:
                    return self.max_geode_production(p_counter - 1, next_stock, p_act_robots,
                                                     p_next_robot_index)
        rv = 0
        next_robot_list = p_act_robots.copy()
        if p_next_robot_index is not None:
            next_robot_list[p_next_robot_index] += 1
            act_robot_cost = self.robot_cost[p_next_robot_index]
            next_stock = [next_stock[0] - act_robot_cost[0], next_stock[1] - act_robot_cost[1],
                          next_stock[2] - act_robot_cost[2], next_stock[3]]
        for next_robot_index_to_built in range(4):
            if next_robot_index_to_built != 3 \
                    and (p_act_robots[next_robot_index_to_built] >= self.max_robot_needed[next_robot_index_to_built]
                         or p_counter == 2):
                continue
            if next_robot_index_to_built != 0 and p_act_robots[next_robot_index_to_built - 1] == 0:
                break
            rv = max(rv, self.max_geode_production(p_counter - 1, next_stock, next_robot_list,
                                                   next_robot_index_to_built))
        return rv

    def __hash__(self):
        return id(self)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1, answer2 = 0, 1
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space=':'):
        nbp = CBlueprint(inp_row[1])
        nbp.robot_cost[0] = (inp_row[6], 0, 0)
        nbp.robot_cost[1] = (inp_row[12], 0, 0)
        nbp.robot_cost[2] = (inp_row[18], inp_row[21], 0)
        nbp.robot_cost[3] = (inp_row[27], 0, inp_row[30])
        gp = nbp.max_geode_production(24)
        if nbp.id in (1, 2, 3):
            answer2 *= nbp.max_geode_production(32)
        answer1 += gp * nbp.id

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 19, solve_puzzle)


if __name__ == '__main__':
    main()
