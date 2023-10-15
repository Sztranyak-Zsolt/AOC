from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CClaim:
    def __init__(self, p_id: int, p_left_gap: int, p_top_gap: int, p_width: int, p_height: int):
        self.id = p_id
        self.left_gap = p_left_gap
        self.top_gap = p_top_gap
        self.width = p_width
        self.height = p_height

    def positions(self) -> set[(int, int)]:
        rs = set()
        for x in range(self.width):
            for y in range(self.height):
                rs.add((self.left_gap + x, self.top_gap + y))
        return rs


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer2 = None
    claim_list = []
    act_positions = set()
    double_pos = set()

    for claim_id, left_gap, top_gap, width, height in yield_input_data(p_input_file_path, p_chars_to_space='#@x,:'):
        new_claim = CClaim(claim_id, left_gap, top_gap, width, height)
        new_pos_set = new_claim.positions()
        double_pos |= act_positions & new_pos_set
        act_positions |= new_pos_set
        claim_list.append(new_claim)
    for act_claim in claim_list:
        if double_pos & act_claim.positions() == set():
            answer2 = act_claim.id
            break
    answer1 = len(double_pos)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 3, solve_puzzle)


if __name__ == '__main__':
    main()
