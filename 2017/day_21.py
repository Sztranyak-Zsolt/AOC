from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase


class CPicture(CGridBase):
    def __init__(self):
        super().__init__()
        self.map_list: dict[int, list[tuple[CGridBase, CGridBase]]] = {2: [], 3: []}

    def add_map(self, p_source_raw: str, p_target_raw: str):
        sg = CGridBase()
        tg = CGridBase()
        for sy, sr in enumerate(p_source_raw.split('/')[::-1]):
            sg.add_row(sr, p_row_number=sy, p_chars_to_skip='.', p_item_type=str)
        for ty, tr in enumerate(p_target_raw.split('/')[::-1]):
            tg.add_row(tr, p_row_number=ty, p_chars_to_skip='.', p_item_type=str)
        if sg.max_x == 1:
            self.map_list[2].append((sg, tg))
        else:
            self.map_list[3].append((sg, tg))

    def evolve_picture(self) -> CPicture:
        if (self.max_x - 1) % 2 == 0:
            rate = 2
        else:
            rate = 3
        rp = CPicture()
        rp.map_list = self.map_list
        for y_factor in range((self.max_y + 1) // rate):
            for x_factor in range((self.max_x + 1) // rate):
                act_part = self.get_subgrid((x_factor * rate, y_factor * rate),
                                            (x_factor * rate + rate - 1, y_factor * rate + rate - 1))
                for (source_grid, target_grid) in self.map_list[rate]:
                    for mapping in source_grid.yield_all_orientations():
                        if act_part == mapping:
                            rp.add_subgrid((x_factor * (rate + 1), y_factor * (rate + 1)), target_grid)
                            break
                    else:
                        continue
                    break
        return rp


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    answer1 = None
    mm = CPicture()

    for act_row in ['.#.', '..#', '###'][::-1]:
        mm.add_row(act_row, p_chars_to_skip='.', p_item_type=str)

    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space='=>'):
        mm.add_map(inp_row[0], inp_row[1])

    for i in range(1, 19):
        mm = mm.evolve_picture()
        if i == 5:
            answer1 = len(mm.position_dict)
    answer2 = len(mm.position_dict)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 21, solve_puzzle)


if __name__ == '__main__':
    main()
