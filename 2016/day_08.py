from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, Position2D


class CScreen(CGridBase):
    def __init__(self):
        super().__init__()
        self.min_x = self.min_y = 0
        self.max_x = 49
        self.max_y = 5

    def add_rectangle(self, p_a: int, p_b: int):
        for x1 in range(min(p_a, self.max_x + 1)):
            for y1 in range(min(p_b, self.max_y + 1)):
                if (x1, y1) not in self.position_dict:
                    self.add_item(Position2D(x1, y1), '#')

    def rotate_row(self, p_a: int, p_b: int):
        act_pos_list = [p for p in self.position_dict if p[1] == p_a]
        for pos in act_pos_list:
            del self.position_dict[pos]
        for pos in act_pos_list:
            new_pos = Position2D((pos[0] + p_b) % (self.max_x + 1), p_a)
            self.add_item(new_pos, '#')

    def rotate_column(self, p_a: int, p_b: int):
        act_pos_list = [p for p in self.position_dict if p[0] == p_a]
        for pos in act_pos_list:
            del self.position_dict[pos]
        for pos in act_pos_list:
            new_pos = Position2D(p_a, (pos[1] + p_b) % (self.max_y + 1))
            self.add_item(new_pos, '#')


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    s = CScreen()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space='=x'):
        if inp_row[0] == 'rect':
            s.add_rectangle(inp_row[1], inp_row[2])
        elif inp_row[1] == 'row':
            s.rotate_row(inp_row[3], inp_row[5])
        else:
            s.rotate_column(inp_row[2], inp_row[4])

    s.double_width_on_print = True
    s.print_y_reverse = True
    answer1 = len(s.position_dict)
    answer2 = f'\n{s}\n'
    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 8, solve_puzzle)


if __name__ == '__main__':
    main()
