from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D
from collections import defaultdict


class Grid(CGridBase):
    def calc_heat(self, p_min_step: int, p_max_step: int) -> int:
        start_pos = Position2D(0, self.max_y)
        heat_dict = defaultdict(lambda: [])
        heat_dict[0] = [(start_pos, Position2D(0, 0))]
        visited = dict()
        target_pos = Position2D(self.max_x, 0)
        while heat_dict:
            act_heat = min(heat_dict)
            act_steps = heat_dict.pop(act_heat)
            for act_pos, act_dir in act_steps:
                if act_pos == target_pos:
                    return act_heat
                next_dirs = []
                if act_dir.x == 0:
                    next_dirs.extend([Position2D(1, 0), Position2D(-1, 0)])
                if act_dir.y == 0:
                    next_dirs.extend([Position2D(0, 1), Position2D(0, -1)])
                for next_dir in next_dirs:
                    new_heat_loss = 0
                    for next_step in range(1, p_max_step + 1):
                        next_pos = Position2D(act_pos.x + next_dir.x * next_step, act_pos.y + next_dir.y * next_step)
                        if not self.is_position_on_grid(next_pos):
                            continue
                        new_heat_loss += self.position_dict[next_pos]
                        if next_step < p_min_step or (next_pos, 1 if next_dir.x else 0) in visited and visited[
                           (next_pos, 1 if next_dir.x else 0)] <= act_heat + new_heat_loss:
                            continue
                        visited[(next_pos, 1 if next_dir.x else 0)] = act_heat + new_heat_loss
                        heat_dict[act_heat + new_heat_loss].append((next_pos, next_dir))
        return -1


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    g = Grid()
    for y, inp_row in enumerate(yield_input_data(p_input_file_path, p_whole_row=True, p_chars_to_space='',
                                                 p_reversed=True, p_convert_to_num=False)):
        for x, act_val in enumerate(inp_row):
            g.add_item(Position2D(x, y), int(act_val))

    answer1 = g.calc_heat(1, 3)
    answer2 = g.calc_heat(4, 10)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 17, solve_puzzle)


if __name__ == '__main__':
    main()
