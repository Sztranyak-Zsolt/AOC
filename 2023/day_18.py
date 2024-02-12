from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_vector import Position2D, add_positions, neighbor_positions
from collections import deque, namedtuple
from functools import cache

TEdge = namedtuple('TEdge', ('pos1', 'pos2', 'prev_dir', 'next_dir'))


class CDigger:
    def __init__(self):
        super().__init__()
        self.digger_pos = Position2D(0, 0)
        self.instruction: list[tuple[Position2D, int]] = []
        self.advanced_instruction: list[tuple[Position2D, int]] = []

    def add_instructions(self, p_direction: str, p_step: int, p_color: str):
        dig_map = {'R': Position2D(1, 0), 'D': Position2D(0, -1), 'L': Position2D(-1, 0), 'U': Position2D(0, 1),
                   '0': Position2D(1, 0), '1': Position2D(0, -1), '2': Position2D(-1, 0), '3': Position2D(0, 1)}
        self.instruction.append((dig_map[p_direction], p_step))
        self.advanced_instruction.append((dig_map[p_color[-1]], int(p_color[1:-1], 16)))

    @cache
    def edges(self, p_advanced: bool = False) -> list[TEdge]:
        rl = []
        act_position = self.digger_pos
        act_instruction = self.instruction if not p_advanced else self.advanced_instruction
        for i, (act_dir, act_step) in enumerate(act_instruction):
            next_pos = add_positions(act_position, Position2D(act_dir.x * act_step, act_dir.y * act_step))
            prev_dir = act_instruction[i - 1][0]
            if i == len(act_instruction) - 1:
                next_dir = act_instruction[0][0]
            else:
                next_dir = act_instruction[i + 1][0]
            if act_dir in [Position2D(-1, 0), Position2D(0, -1)]:
                rl.append(TEdge(next_pos, act_position, next_dir, Position2D(-prev_dir.x, -prev_dir.y)))
            elif act_dir in [Position2D(1, 0), Position2D(0, 1)]:
                rl.append(TEdge(act_position, next_pos, Position2D(-prev_dir.x, -prev_dir.y), next_dir))
            act_position = next_pos
        return rl

    def calc_all_dig_periods(self, p_advanced: bool = False):
        rv = 0
        act_periods = []
        prev_y = 0
        act_edge = self.edges(p_advanced)
        for y in sorted({e.pos1.y for e in act_edge}):
            rv += sum((period[1] - period[0] + 1) * (y - prev_y) for period in act_periods)
            for p1, p2, d1, d2 in sorted([e for e in act_edge
                                          if e.pos1.y <= y <= e.pos2.y and
                                          e.prev_dir in [Position2D(0, 1), Position2D(0, -1)]]):
                if d1 == d2 == Position2D(0, 1):
                    periods_to_split = [p for p in act_periods if p[0] < p1.x < p[1]]
                    if periods_to_split:
                        act_periods.remove(periods_to_split[0])
                        act_periods.append((periods_to_split[0][0], p1.x))
                        act_periods.append((p2.x, periods_to_split[0][1]))
                        rv += p2.x - p1.x - 1
                        continue
                    act_periods.append((p1.x, p2.x))
                    continue
                if d1 == d2 == Position2D(0, -1):
                    if (p1.x, p2.x) in act_periods:
                        act_periods.remove((p1.x, p2.x))
                        rv += p2.x - p1.x + 1
                        continue
                    pp1 = [(x1, x2) for x1, x2 in act_periods if x2 == p1.x][0]
                    pp2 = [(x1, x2) for x1, x2 in act_periods if x1 == p2.x][0]
                    act_periods.remove(pp1)
                    act_periods.remove(pp2)
                    act_periods.append((pp1[0], pp2[1]))
                    continue
                pp = [(x1, x2) for x1, x2 in act_periods if {x1, x2} & {p1.x, p2.x}][0]
                act_periods.remove(pp)
                if d1 == Position2D(0, 1) and pp[1] == p2.x:
                    rv += p2.x - p1.x
                    act_periods.append((pp[0], p1.x))
                elif d1 == Position2D(0, 1) and pp[0] == p2.x:
                    act_periods.append((p1.x, pp[1]))
                elif d1 == Position2D(0, -1) and pp[0] == p1.x:
                    act_periods.append((p2.x, pp[1]))
                    rv += p2.x - p1.x
                else:
                    act_periods.append((pp[0], p2.x))
            prev_y = y
        return rv

    def dig_area_with_flooding(self) -> int:
        rv = sum(s for p, s in self.instruction)
        dq = deque()
        visited = set()
        dq.append(add_positions(self.digger_pos, Position2D(1, 1)))
        min_x = min(p.x for p, p2, d, d2 in self.edges())
        while dq:
            act_pos = dq.popleft()
            if act_pos.x < min_x:
                return -1
            for np in neighbor_positions(act_pos):
                if np in visited:
                    continue
                visited.add(np)
                for point1, point2 in [(p1, p2) for p1, p2, d1, d2 in self.edges() if p1.x == np.x or p1.y == np.y]:
                    if point1.x <= np.x <= point2.x and point2.y <= np.y <= point1.y:
                        break
                else:
                    rv += 1
                    dq.append(np)
        return rv


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    g = CDigger()
    for d_dir, d_step, d_color in yield_input_data(p_input_file_path, p_chars_to_space='()'):
        g.add_instructions(d_dir, d_step, d_color)

    # answer1 = g.dig_area_with_flooding()
    answer1 = g.calc_all_dig_periods()
    answer2 = g.calc_all_dig_periods(True)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 18, solve_puzzle)


if __name__ == '__main__':
    main()
