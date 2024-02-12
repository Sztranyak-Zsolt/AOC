from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, add_positions
from collections import deque


class CGrid(CGridBase):

    def energized_tiles_count(self, p_starting_pos: Position2D, p_starting_dir: Position2D) -> int:
        dir_change = {(Position2D(1, 0), '-'): [Position2D(1, 0)],
                      (Position2D(1, 0), '|'): [Position2D(0, 1), Position2D(0, -1)],
                      (Position2D(1, 0), '\\'): [Position2D(0, -1)],
                      (Position2D(1, 0), '/'): [Position2D(0, 1)],
                      (Position2D(-1, 0), '-'): [Position2D(-1, 0)],
                      (Position2D(-1, 0), '|'): [Position2D(0, 1), Position2D(0, -1)],
                      (Position2D(-1, 0), '\\'): [Position2D(0, 1)],
                      (Position2D(-1, 0), '/'): [Position2D(0, -1)],
                      (Position2D(0, 1), '-'): [Position2D(1, 0), Position2D(-1, 0)],
                      (Position2D(0, 1), '|'): [Position2D(0, 1)],
                      (Position2D(0, 1), '\\'): [Position2D(-1, 0)],
                      (Position2D(0, 1), '/'): [Position2D(1, 0)],
                      (Position2D(0, -1), '-'): [Position2D(1, 0), Position2D(-1, 0)],
                      (Position2D(0, -1), '|'): [Position2D(0, -1)],
                      (Position2D(0, -1), '\\'): [Position2D(1, 0)],
                      (Position2D(0, -1), '/'): [Position2D(-1, 0)]
                      }
        visited_state_set = set()
        dq = deque([[p_starting_pos, p_starting_dir]])
        while dq:
            act_pos, act_dir = dq.popleft()
            next_pos = add_positions(act_pos, act_dir)
            if not self.is_position_on_grid(next_pos):
                continue
            if next_pos not in self.position_dict:
                if (next_pos, act_dir) in visited_state_set:
                    continue
                visited_state_set.add((next_pos, act_dir))
                dq.append([next_pos, act_dir])
                continue
            for next_dir in dir_change[(act_dir, self.position_dict[next_pos])]:
                if (next_pos, next_dir) in visited_state_set:
                    continue
                visited_state_set.add((next_pos, next_dir))
                dq.append([next_pos, next_dir])
        return len(set([p for p, c in visited_state_set]))

    def max_beam(self):
        rv = 0
        for x in range(self.min_x, self.max_x + 1):
            rv = max(rv, self.energized_tiles_count(Position2D(x, -1), Position2D(0, 1)))
            rv = max(rv, self.energized_tiles_count(Position2D(x, self.max_y + 1), Position2D(0, -1)))
        for y in range(self.min_y, self.max_y + 1):
            rv = max(rv, self.energized_tiles_count(Position2D(-1, y), Position2D(1, 0)))
            rv = max(rv, self.energized_tiles_count(Position2D(self.max_x + 1, y), Position2D(-1, 0)))
        return rv


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    g = CGrid()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True):
        g.add_row(inp_row, p_chars_to_skip='.')
    answer1 = g.energized_tiles_count(Position2D(-1, g.max_y), Position2D(1, 0))
    answer2 = g.max_beam()
    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 16, solve_puzzle)


if __name__ == '__main__':
    main()
