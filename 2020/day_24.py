from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import Position2D, CGridBase, add_positions
from functools import cache


class CTileHandler(CGridBase):
    hex_direction = {'e': Position2D(2, 0), 'w': Position2D(-2, 0),
                     'ne': Position2D(1, 1), 'nw': Position2D(-1, 1),
                     'se': Position2D(1, -1), 'sw': Position2D(-1, -1)}

    @cache
    def hex_neighbor(self, p_position: Position2D, p_return_center: bool = False) -> list[Position2D]:
        rl = []
        if p_return_center:
            rl.append(p_position)
        for act_dir in self.hex_direction.values():
            rl.append(add_positions(p_position, act_dir))
        return rl

    def flip_tile(self, p_direction_line: str):
        dir_prefix = ''
        act_position = Position2D(0, 0)
        for act_dir in p_direction_line:
            if act_dir in ('e', 'w'):
                act_position = add_positions(act_position, self.hex_direction[dir_prefix + act_dir])
                dir_prefix = ''
            else:
                dir_prefix = act_dir
        if act_position in self.position_dict:
            del self.position_dict[act_position]
        else:
            self.position_dict[act_position] = '#'

    def day_end_flip(self):
        checked_tiles = set()
        new_position_dict = {}
        for flipped_tile in self.position_dict:
            for act_tile in self.hex_neighbor(flipped_tile, True):
                if act_tile in checked_tiles:
                    continue
                checked_tiles.add(act_tile)
                nc = len(['x' for p in self.hex_neighbor(act_tile) if p in self.position_dict])
                if self.position_dict and nc == 2 or act_tile in self.position_dict and nc == 1:
                    new_position_dict[act_tile] = '#'
        self.position_dict = new_position_dict

    def __hash__(self):
        return id(self)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    th = CTileHandler()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        th.flip_tile(inp_row)
    answer1 = len(th.position_dict)

    for i in range(100):
        th.day_end_flip()
    answer2 = len(th.position_dict)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 24, solve_puzzle)


if __name__ == '__main__':
    main()
