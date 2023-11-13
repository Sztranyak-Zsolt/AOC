from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D


class CImage(CGridBase):
    def __init__(self, p_decode_str: str = ''):
        super().__init__()
        self.decoder: str = p_decode_str
        self.infinite_is_on = False

    def draw_new_image(self) -> CImage:
        drawn_image = CImage(self.decoder)
        if not self.infinite_is_on:
            drawn_image.infinite_is_on = self.decoder[0] == '#'
        else:
            drawn_image.infinite_is_on = self.decoder[-1] == '#'
        for act_position_y in range(self.min_y - 1, self.max_y + 2):
            for act_position_x in range(self.min_x - 1, self.max_x + 2):
                act_decode_index = 0
                for pos_y in [1, 0, -1]:
                    for pos_x in [-1, 0, 1]:
                        check_pos = Position2D(act_position_x + pos_x, act_position_y + pos_y)
                        act_decode_index *= 2
                        if check_pos in self.position_dict:
                            act_decode_index += 1
                        elif self.infinite_is_on \
                                and (check_pos.x <= self.min_x - 1 or check_pos.x >= self.max_x + 1
                                     or check_pos.y <= self.min_x - 1 or check_pos.y >= self.max_y + 1):
                            act_decode_index += 1
                if self.decoder[act_decode_index] == '#':
                    drawn_image.add_item(Position2D(act_position_x, act_position_y), '#')
        return drawn_image

    @property
    def count_lit(self) -> int:
        return len(self.position_dict)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = None
    im = CImage()
    for i, inp_group in enumerate(yield_input_data(p_input_file_path, p_group_separator='\n\n', p_whole_row=True)):
        if i == 0:
            im = CImage(inp_group[0])
            continue
        for act_row in inp_group[::-1]:
            im.add_row(act_row, p_chars_to_skip='.')

    for i in range(1, 51):
        im = im.draw_new_image()
        if i == 2:
            answer1 = im.count_lit
        if i == 50:
            answer2 = im.count_lit

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 20, solve_puzzle)


if __name__ == '__main__':
    main()
