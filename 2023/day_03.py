from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, neighbor_positions


class CGrid(CGridBase):
    def __init__(self):
        super().__init__()
        self.nums: dict[Position2D, int] = {}
        self.symbols: dict[Position2D, str] = {}

    def calc_nums_and_symbol_positions(self):
        for y in range(self.min_y, self.max_y + 1):
            act_num = ''
            for x in range(self.min_x, self.max_x + 2):
                act_pos = Position2D(x, y)
                if act_pos in self.position_dict and self.position_dict[act_pos].isnumeric():
                    act_num += self.position_dict[act_pos]
                    continue
                if act_num != '':
                    act_num_pos = Position2D(act_pos.x - len(act_num), act_pos.y)
                    self.nums[act_num_pos] = int(act_num)
                    act_num = ''
                if act_pos in self.position_dict:
                    self.symbols[act_pos] = self.position_dict[act_pos]

    @property
    def nums_with_symbol_sum(self):
        rv = 0
        for num_pos, num in self.nums.items():
            for nl in range(len(str(num))):
                for spos in neighbor_positions(Position2D(num_pos.x + nl, num_pos.y), p_return_corner=True):
                    if spos in self.symbols:
                        rv += num
                        break
                else:
                    continue
                break
        return rv

    @property
    def gear_ratio_sum(self) -> int:
        star_dict = {}
        for num_pos, num in self.nums.items():
            symbol_pos_found = set()
            for nl in range(len(str(num))):
                for symbol_pos in neighbor_positions(Position2D(num_pos.x + nl, num_pos.y), p_return_corner=True):
                    if symbol_pos in self.symbols and self.symbols[symbol_pos] == '*' \
                            and symbol_pos not in symbol_pos_found:
                        symbol_pos_found.add(symbol_pos)
                        if symbol_pos not in star_dict:
                            star_dict[symbol_pos] = [num]
                        else:
                            star_dict[symbol_pos].append(num)
        return sum([v[0] * v[1] for p, v in star_dict.items() if len(v) == 2])


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    g = CGrid()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        g.add_row(inp_row, p_chars_to_skip='.')
    g.calc_nums_and_symbol_positions()
    answer1 = g.nums_with_symbol_sum
    answer2 = g.gear_ratio_sum

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 3, solve_puzzle)


if __name__ == '__main__':
    main()
