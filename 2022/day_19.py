from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from functools import cached_property, cache


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

    @cache
    def max_geode_production(self, p_counter: int, p_act_stock: tuple[int] | None = None,
                             p_act_robots: tuple[int] | None = None, p_next_robot_index: int = None) -> int:
        if p_act_stock is None:
            p_act_stock = (0, 0, 0, 0)
        if p_act_robots is None:
            p_act_robots = (1, 0, 0, 0)
        next_stock_base_list = [s + r for s, r in zip(p_act_stock, p_act_robots)]
        if p_counter == 1:
            return next_stock_base_list[3]
        if p_next_robot_index is not None:
            for i in range(3):
                if p_act_stock[i] < self.robot_cost[p_next_robot_index][i]:
                    next_stock = []
                    for ni, ns in enumerate(next_stock_base_list):
                        if p_act_robots[ni] < self.max_robot_needed[ni] or ni == 3:
                            next_stock.append(next_stock_base_list[ni])
                        else:
                            next_stock.append(self.max_robot_needed[ni])
                    return self.max_geode_production(p_counter - 1, tuple(next_stock), p_act_robots,
                                                     p_next_robot_index)
        rv = 0
        next_robot_list = list(p_act_robots)
        if p_next_robot_index is not None:
            next_robot_list[p_next_robot_index] += 1
            act_robot_cost = self.robot_cost[p_next_robot_index]

            next_stock = []
            for ni, ns in enumerate(next_stock_base_list):
                if ni == 3:
                    next_stock.append(next_stock_base_list[ni])
                elif p_act_robots[ni] < self.max_robot_needed[ni]:
                    next_stock.append(next_stock_base_list[ni] - act_robot_cost[ni])
                else:
                    next_stock.append(self.max_robot_needed[ni])
        else:
            next_stock = next_stock_base_list
        for next_robot_index_to_built in range(4):
            if next_robot_index_to_built != 3 \
                    and (p_act_robots[next_robot_index_to_built] >= self.max_robot_needed[next_robot_index_to_built]
                         or p_counter == 2):
                continue
            if next_robot_index_to_built != 0 and p_act_robots[next_robot_index_to_built - 1] == 0:
                break
            rv = max(rv, self.max_geode_production(p_counter - 1, tuple(next_stock), tuple(next_robot_list),
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
        nbp.max_geode_production.cache_clear()
        answer1 += gp * nbp.id
    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 19, solve_puzzle)


if __name__ == '__main__':
    main()
