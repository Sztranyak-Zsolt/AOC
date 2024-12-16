from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, add_positions, neighbor_positions
from collections import deque
from typing import NamedTuple

NTGarden = NamedTuple('NTGarden', [('garden_char', str), ('garden_start_position', str), ('garden_size', int),
                                   ('neighbor_count', int), ('fence_count', int)])


class CGarden(CGridBase):
    def __init__(self):
        super().__init__()
        self.garden_group: list[NTGarden] = []

    def set_garden(self) -> None:
        processed_tiles = set()
        for act_tile, act_garden_type in self.position_dict.items():
            if act_tile in processed_tiles:
                continue
            processed_tiles.add(act_tile)
            size = 1
            neigh_count = 0
            fence_count = 0
            tiles_dq = deque([act_tile])
            known_fences = set()
            while tiles_dq:
                tile_to_check = tiles_dq.popleft()
                for next_dir in neighbor_positions(p_return_corner=False):
                    next_tile = add_positions(tile_to_check, next_dir)
                    if self.position_dict.get(next_tile, '') != act_garden_type:
                        neigh_count += 1
                        if (tile_to_check, next_dir) in known_fences:
                            continue
                        known_fences.add((tile_to_check, next_dir))
                        fence_count += 1
                        for fence_dir in (Position2D(next_dir.y, next_dir.x), Position2D(-next_dir.y, -next_dir.x)):
                            fence_tile = add_positions(tile_to_check, fence_dir)
                            while self.position_dict.get(fence_tile, '') == act_garden_type \
                                    and self.position_dict.get(add_positions(fence_tile, next_dir), '') \
                                    != act_garden_type:
                                known_fences.add((fence_tile, next_dir))
                                fence_tile = add_positions(fence_tile, fence_dir)
                        continue
                    if next_tile in processed_tiles:
                        continue
                    processed_tiles.add(next_tile)
                    size += 1
                    tiles_dq.append(next_tile)
            self.garden_group.append(NTGarden(act_garden_type, act_tile, size, neigh_count, fence_count))


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    g = CGarden()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True):
        g.add_row(inp_row)
    g.set_garden()
    answer1 = sum(gg.garden_size * gg.neighbor_count for gg in g.garden_group)
    answer2 = sum(gg.garden_size * gg.fence_count for gg in g.garden_group)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 12, solve_puzzle)


if __name__ == '__main__':
    main()
