from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, Position2D
from math import gcd
from collections import defaultdict
from functools import cached_property


class CGridx(CGridBase):

    @property
    def base(self) -> Position2D:
        return sorted(self.visible_asteroids_dict.items(), key=lambda k: k[1], reverse=True)[0][0]

    @property
    def base_visible_count(self) -> int:
        return sorted(self.visible_asteroids_dict.items(), key=lambda k: k[1], reverse=True)[0][1]

    def block_count(self, p_pos1: Position2D, p_pos2: Position2D) -> int:
        int_steps = gcd(abs(p_pos1.x - p_pos2.x), abs(p_pos1.y - p_pos2.y))
        rv_block_count = 0
        for act_step in range(1, int_steps):
            if Position2D(p_pos1.x + (p_pos2.x - p_pos1.x) // int_steps * act_step,
                          p_pos1.y + (p_pos2.y - p_pos1.y) // int_steps * act_step) in self.position_dict:
                rv_block_count += 1
        return rv_block_count

    @cached_property
    def visible_asteroids_dict(self):
        vis_dict: defaultdict[Position2D, int] = defaultdict(lambda: 0)
        processed_positions = set()
        for act_ast in self.position_dict:
            processed_positions.add(act_ast)
            for next_ast in self.position_dict:
                if next_ast in processed_positions:
                    continue
                if self.block_count(act_ast, next_ast) == 0:
                    vis_dict[act_ast] += 1
                    vis_dict[next_ast] += 1
        return vis_dict

    def base_asteroid_shots_list(self, p_position: Position2D) -> list[Position2D]:
        rv_ast_list = list()
        for next_pos in self.position_dict:
            if next_pos != p_position:
                turn_rank = self.block_count(p_position, next_pos)
                if next_pos.x >= p_position.x and next_pos.y < p_position.y:
                    quarter_rank = 0
                elif next_pos.x > p_position.x and next_pos.y >= p_position.y:
                    quarter_rank = 1
                elif next_pos.x <= p_position.x and next_pos.y > p_position.y:
                    quarter_rank = 2
                else:
                    quarter_rank = 3
                if next_pos.x == p_position.x:
                    angle_rank = -10000000
                else:
                    angle_rank = (next_pos.y - p_position.y) / (next_pos.x - p_position.x)
                rv_ast_list.append([turn_rank, quarter_rank, angle_rank, next_pos])
        return [shot[3] for shot in sorted(rv_ast_list)]


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    g = CGridx()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        g.add_row(inp_row, p_chars_to_skip='.')

    answer1 = g.base_visible_count
    shot200 = g.base_asteroid_shots_list(g.base)[199]
    answer2 = shot200.x * 100 + shot200.y

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 10, solve_puzzle)


if __name__ == '__main__':
    main()
