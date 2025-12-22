import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


class CCave:
    def __init__(self, p_code: str):
        self.code = p_code
        self.big_cave = p_code == p_code.upper()
        self.route_set: set[CCave] = set()


class CCaveSystem:
    def __init__(self):
        self.cave_dict: dict[str, CCave] = {}

    def add_cave_connections(self, p_cave1: str, p_cave2: str):
        if p_cave1 not in self.cave_dict.keys():
            self.cave_dict[p_cave1] = CCave(p_cave1)
        if p_cave2 not in self.cave_dict.keys():
            self.cave_dict[p_cave2] = CCave(p_cave2)
        self.cave_dict[p_cave1].route_set.add(self.cave_dict[p_cave2])
        self.cave_dict[p_cave2].route_set.add(self.cave_dict[p_cave1])

    def cave_routes(self, p_cave_list: list[CCave], allow_twice_small_visit: bool) -> 0:
        route_found = 0
        for conn_cave in p_cave_list[-1].route_set:
            if conn_cave.code == "start":
                continue
            elif conn_cave.code == "end":
                route_found += 1
            elif conn_cave.big_cave or conn_cave not in p_cave_list or allow_twice_small_visit:
                if conn_cave.big_cave or conn_cave not in p_cave_list:
                    route_found += self.cave_routes(p_cave_list + [conn_cave], allow_twice_small_visit)
                else:
                    route_found += self.cave_routes(p_cave_list + [conn_cave], False)
        return route_found

    def calc_all_route(self) -> int:
        return self.cave_routes([self.cave_dict["start"]], False)

    def calc_all_route2(self) -> int:
        return self.cave_routes([self.cave_dict["start"]], True)


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    cs = CCaveSystem()
    for cave1, cave2 in yield_input_data(p_input_file_path, p_chars_to_space='-'):
        cs.add_cave_connections(cave1, cave2)

    answer1 = cs.calc_all_route()
    answer2 = cs.calc_all_route2()

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 12, solve_puzzle)


if __name__ == '__main__':
    main()
