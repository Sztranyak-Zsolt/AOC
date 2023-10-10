from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from itertools import permutations


class CCity:
    def __init__(self, p_name: str):
        self.name = p_name
        self.route_list: list[CRouteTo] = []


class CRouteTo:
    def __init__(self, p_city_to: CCity, p_distance: int):
        self.city_to = p_city_to
        self.distance = p_distance


class CRouteHandler:
    def __init__(self):
        self.city_dict: dict[str, CCity] = {}

    def city_dict_item(self, p_dict_item: str) -> CCity:
        if p_dict_item not in self.city_dict:
            self.city_dict[p_dict_item] = CCity(p_dict_item)
        return self.city_dict[p_dict_item]

    def add_route(self, p_city1: str, p_city2: str, p_distance: int):
        self.city_dict_item(p_city1).route_list.append(CRouteTo(self.city_dict_item(p_city2), p_distance))
        self.city_dict[p_city2].route_list.append(CRouteTo(self.city_dict[p_city1], p_distance))

    def calc_routes(self):
        for city_permutation in permutations(self.city_dict.values()):
            act_route = 0
            act_city = None
            for next_city in city_permutation[::]:
                if act_city is not None:
                    for route in act_city.route_list:
                        if route.city_to == next_city:
                            act_route += route.distance
                            break
                act_city = next_city
            yield act_route


def solve_puzzle(p_input_file_path: str) -> (int, int):
    answer1 = answer2 = None
    cr = CRouteHandler()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space='='):
        c1, _, c2, dist = inp_row
        cr.add_route(c1, c2, int(dist))
    for route_length in cr.calc_routes():
        if answer1 is None:
            answer1 = answer2 = route_length
            continue
        answer1 = min(answer1, route_length)
        answer2 = max(answer2, route_length)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 9, solve_puzzle)


if __name__ == '__main__':
    main()
