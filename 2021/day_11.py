from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, Position2D, neighbor_positions


class COctGrid(CGridBase):

    def evolve(self) -> int:
        flashed_octopuses = set()
        first_round = has_flash = True
        flash_count = 0
        while has_flash:
            has_flash = False
            for act_position, act_value in self.position_dict.items():
                if act_position in flashed_octopuses:
                    continue
                if first_round:
                    self.position_dict[act_position] += 1
                    act_value += 1
                if act_value > 9:
                    has_flash = True
                    flash_count += 1
                    flashed_octopuses.add(act_position)
                    self.position_dict[act_position] = 0
                    for np in neighbor_positions(act_position, p_return_corner=True):
                        if np in self.position_dict and np not in flashed_octopuses:
                            self.position_dict[np] += 1
            first_round = False
        return flash_count


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = 0
    answer2 = None
    g = COctGrid()
    for y, inp_row in enumerate(yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False)):
        for x, h in enumerate(inp_row):
            g.add_item(Position2D(x, y), int(h))

    c = 0
    while c <= 100 or answer2 is None:
        act_flash = g.evolve()
        c += 1
        if c <= 100:
            answer1 += act_flash
        if act_flash == 100:
            answer2 = c

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 11, solve_puzzle)


if __name__ == '__main__':
    main()
