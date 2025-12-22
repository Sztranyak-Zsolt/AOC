import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, add_positions, neighbor_positions


class CTileManager:
    def __init__(self):
        self.tile_dict: dict[int, CGridBase] = {}
        self.full_picture_tiles: dict[Position2D, CGridBase] = {}
        self.full_picture_ids: dict[Position2D, int] = {}
        self.picture_grid: CGridBase = CGridBase()

    @property
    def tile_min_x(self) -> int | None:
        if self.full_picture_tiles == {}:
            return None
        return min([p.x for p in self.full_picture_tiles])

    @property
    def tile_max_x(self) -> int | None:
        if self.full_picture_tiles == {}:
            return None
        return max([p.x for p in self.full_picture_tiles])

    @property
    def tile_min_y(self) -> int | None:
        if self.full_picture_tiles == {}:
            return None
        return min([p.y for p in self.full_picture_tiles])

    @property
    def tile_max_y(self) -> int | None:
        if self.full_picture_tiles == {}:
            return None
        return max([p.y for p in self.full_picture_tiles])

    def gen_full_picture(self):
        first_tile_id = min(self.tile_dict)
        self.full_picture_tiles[Position2D(0, 0)] = self.tile_dict[first_tile_id]
        self.full_picture_ids[Position2D(0, 0)] = first_tile_id
        used_tiles_id = {first_tile_id}
        next_tile_position = next_tile_dir = Position2D(-1, 0)

        while True:
            for n_id, next_tile_to_check in self.tile_dict.items():
                if n_id in used_tiles_id:
                    continue
                for next_orientation in next_tile_to_check.yield_all_orientations():
                    for act_dir in neighbor_positions():
                        if (picture_part := add_positions(next_tile_position, act_dir)) in self.full_picture_tiles:
                            if self.full_picture_tiles[picture_part].get_edge(Position2D(-act_dir.x, -act_dir.y)) \
                                    != next_orientation.get_edge(act_dir):
                                break
                    else:
                        used_tiles_id.add(n_id)
                        self.tile_dict[n_id] = next_orientation
                        self.full_picture_tiles[next_tile_position] = next_orientation
                        self.full_picture_ids[next_tile_position] = n_id
                        next_tile_position = add_positions(next_tile_position, next_tile_dir)
                        break
                else:
                    continue
                break
            else:
                if len(used_tiles_id) == 144:
                    self.concat_tiles()
                    return
                if next_tile_position.y == 0 and next_tile_dir == Position2D(-1, 0):
                    next_tile_position = next_tile_dir = Position2D(1, 0)
                    continue
                if next_tile_position.y == min([p.y for p in self.full_picture_tiles]):
                    next_tile_position = Position2D(min([p.x for p in self.full_picture_tiles]),
                                                    next_tile_position.y - 1)
                    continue
                next_tile_position = Position2D(min([p.x for p in self.full_picture_tiles]),
                                                max([p.y for p in self.full_picture_tiles]) + 1)

    def concat_tiles(self):
        for pos, act_tile in self.full_picture_tiles.items():
            self.picture_grid.add_subgrid(Position2D(pos.x * 8, pos.y * 8),
                                          act_tile.get_subgrid(Position2D(1, 1), Position2D(8, 8)))


def monster_picture() -> CGridBase:
    rg = CGridBase()
    for monster_point in [Position2D(0, 1), Position2D(1, 0), Position2D(4, 0), Position2D(5, 1), Position2D(6, 1),
                          Position2D(7, 0), Position2D(10, 0), Position2D(11, 1), Position2D(12, 1), Position2D(13, 0),
                          Position2D(16, 0), Position2D(17, 1), Position2D(18, 1), Position2D(18, 2),
                          Position2D(19, 1)]:
        rg.add_item(monster_point, '#')
    return rg


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer2 = None
    tm = CTileManager()
    for inp_group in yield_input_data(p_input_file_path, p_group_separator='\n\n', p_chars_to_space=':'):
        tile_grid = CGridBase()
        tm.tile_dict[inp_group[0][-1]] = tile_grid
        for tile_row in inp_group[:0:-1]:
            tile_grid.add_row(tile_row[0], p_chars_to_skip='.')
    tm.gen_full_picture()

    answer1 = tm.full_picture_ids[Position2D(tm.tile_min_x, tm.tile_min_y)] \
              * tm.full_picture_ids[Position2D(tm.tile_min_x, tm.tile_max_y)] \
              * tm.full_picture_ids[Position2D(tm.tile_max_x, tm.tile_min_y)] \
              * tm.full_picture_ids[Position2D(tm.tile_max_x, tm.tile_max_y)]

    mg = monster_picture()

    for mg_o in mg.yield_all_orientations():
        if (monster_found := tm.picture_grid.count_all_cover(mg_o)) != 0:
            answer2 = len(tm.picture_grid.position_dict) - monster_found * len(mg.position_dict)
            break

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 20, solve_puzzle)


if __name__ == '__main__':
    main()
