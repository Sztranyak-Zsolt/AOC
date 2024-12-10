from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, add_positions
from functools import cached_property


class CMap(CGridBase):
    def __init__(self):
        super().__init__()

    @cached_property
    def path_endpoints(self):
        act_pos_dict = {k: [k] for k, v in self.position_dict.items() if v == 9}
        for prev_height in range(8, -1, -1):
            prev_pos_dict = {}
            for p, c in act_pos_dict.items():
                for pd in (Position2D(1, 0), Position2D(0, 1), Position2D(-1, 0), Position2D(0, -1)):
                    prev_pos = add_positions(p, pd)
                    if prev_pos.x in (-1, self.max_x + 1) or prev_pos.y in (-1, self.max_y + 1) \
                            or self.position_dict[prev_pos] != prev_height:
                        continue
                    if prev_pos not in prev_pos_dict:
                        prev_pos_dict[prev_pos] = c.copy()
                    else:
                        prev_pos_dict[prev_pos] += c
            act_pos_dict = prev_pos_dict
        return act_pos_dict


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    m = CMap()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True, p_convert_to_num=False):
        m.add_row(inp_row, p_item_type=int)
    answer1 = sum(len(set(v)) for v in m.path_endpoints.values())
    answer2 = sum(len(v) for v in m.path_endpoints.values())

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 10, solve_puzzle)


if __name__ == '__main__':
    main()
