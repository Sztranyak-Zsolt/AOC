from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, Position2D


def calc_pos(p_pos: Position2D, p_dir: str) -> Position2D:
    if p_dir == 'D':
        return Position2D(p_pos.x, p_pos.y - 1)
    elif p_dir == 'L':
        return Position2D(p_pos.x - 1, p_pos.y)
    elif p_dir == 'R':
        return Position2D(p_pos.x + 1, p_pos.y)


class CGridX(CGridBase):

    def __init__(self):
        super().__init__()
        self.starting_position = Position2D(500, 0)
        self.floating_water: list[Position2D] = []
        self.over_floating_water_set: set[Position2D] = set()
        self.solid_water_set: set[Position2D] = set()

    def add_water_drop(self):
        act_float = self.floating_water[-1]
        for next_dir in ['D', 'L', 'R']:
            next_float = calc_pos(act_float, next_dir)
            if next_float in self.position_dict:
                continue
            if next_float in self.over_floating_water_set or next_float[1] == self.min_y - 1:
                self.over_floating_water_set.add(self.floating_water.pop(-1))
                if next_dir == 'L' and calc_pos(act_float, 'R') not in self.position_dict \
                        and calc_pos(act_float, 'R') not in self.solid_water_set \
                        and calc_pos(act_float, 'R') not in self.floating_water:
                    self.floating_water.append(calc_pos(act_float, 'R'))
                return
            elif next_float not in self.position_dict \
                    and next_float not in self.solid_water_set \
                    and next_float not in self.floating_water:
                self.floating_water.append(next_float)
                return
        self.solid_water_set.add(self.floating_water.pop(-1))

    def open_tap(self):
        self.floating_water.append(self.starting_position)
        while self.floating_water:
            self.add_water_drop()
        change_list = []
        for act_pos in self.over_floating_water_set:
            check_pos = calc_pos(act_pos, 'L')
            while check_pos in self.solid_water_set:
                change_list.append(check_pos)
                check_pos = calc_pos(check_pos, 'L')
        for ch_pos in change_list:
            self.solid_water_set.remove(ch_pos)
            self.over_floating_water_set.add(ch_pos)

    def __str__(self):
        ret_lst = list()
        for y in range(self.max_y, self.min_y - 1, -1):
            act_row = ''
            for x in range(self.min_x - 1, self.max_x + 2):
                if (x, y) in self.position_dict:
                    act_row += "#"
                elif (x, y) in self.solid_water_set:
                    act_row += "~"
                elif (x, y) in self.over_floating_water_set:
                    act_row += "-"
                elif (x, y) == self.starting_position:
                    act_row += "+"
                elif (x, y) in self.floating_water:
                    act_row += "."
                else:
                    act_row += ' '
            ret_lst.append(act_row)
        return '\n'.join(ret_lst)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    g = CGridX()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space=',.='):
        for p2 in range(min(inp_row[3:5]), max(inp_row[3:5]) + 1):
            if inp_row[0] == 'x':
                g.add_item(Position2D(inp_row[1], -p2), '#')
            else:
                g.add_item(Position2D(p2, -inp_row[1]), '#')
    g.min_x = min([p.x for p in g.position_dict]) - 1
    g.max_x += 1
    g.open_tap()

    answer1 = len(g.over_floating_water_set | g.solid_water_set) + max([p.y for p in g.position_dict])
    answer2 = len(g.solid_water_set)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 17, solve_puzzle)


if __name__ == '__main__':
    main()
