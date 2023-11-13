from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, Position2D, neighbor_positions


class CCave(CGridBase):

    @property
    def route_length_with_lowest_risk(self) -> int:
        risk_dict = {0: [Position2D(0, 0)]}
        checked_positions = set()
        act_risk = 0
        while True:
            for act_risk_positions in risk_dict[act_risk]:
                if act_risk_positions in checked_positions:
                    continue
                checked_positions.add(act_risk_positions)
                if act_risk_positions == Position2D(self.max_x, self.max_y):
                    return act_risk
                for next_pos in neighbor_positions(act_risk_positions):
                    if next_pos not in self.position_dict or next_pos in checked_positions:
                        continue
                    if (next_risk_level := act_risk + self.position_dict[next_pos]) not in risk_dict:
                        risk_dict[next_risk_level] = []
                    risk_dict[next_risk_level].append(next_pos)
            del risk_dict[act_risk]
            act_risk += 1
            while act_risk not in risk_dict:
                act_risk += 1

    def enlarge_cave(self):
        nex_pos_dict = self.position_dict.copy()
        for gx in range(5):
            for gy in range(5):
                if gx == gy == 0:
                    continue
                for p, v in self.position_dict.items():
                    nex_pos_dict[Position2D(p.x + gx * (self.max_x + 1), p.y + gy * (self.max_y + 1))] = \
                        (v + gx + gy - 1) % 9 + 1
        self.position_dict = nex_pos_dict
        self.max_x = (self.max_x + 1) * 5 - 1
        self.max_y = (self.max_y + 1) * 5 - 1


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    cc = CCave()
    for y, inp_row in enumerate(yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False)):
        for x, h in enumerate(inp_row):
            cc.add_item(Position2D(x, y), int(h))
    answer1 = cc.route_length_with_lowest_risk
    cc.enlarge_cave()
    answer2 = cc.route_length_with_lowest_risk
    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 15, solve_puzzle)


if __name__ == '__main__':
    main()
